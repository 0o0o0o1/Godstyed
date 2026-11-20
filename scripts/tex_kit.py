# 타일 텍스처 굽기 공용 키트 (Blender, exec(open(...).read()) 로 불러 씀)
# 4D 노이즈 링 좌표 (R cos2πu, R sin2πu, R cos2πv, R sin2πv) 로 양방향 이음매 없이 반복.
# 머티리얼 출력: "OUT_<채널>" Emission(값) / "OUT_Normal" Principled(Bump) → bake_jobs 로 1024 PNG 굽기.
import bpy, math

TAU = 2 * math.pi
TEX_DIR = "D:\\god\\exports\\textures\\"


def N(nt, kind, x=0, y=0):
    n = nt.nodes.new(kind); n.location = (x, y); return n


def L(nt, a, ai, b, bi):
    nt.links.new(a.outputs[ai], b.inputs[bi])


def mathn(nt, op, a=None, b=None):
    n = N(nt, "ShaderNodeMath"); n.operation = op
    if a is not None:
        n.inputs[0].default_value = a
    if b is not None:
        n.inputs[1].default_value = b
    return n


def mul(nt, a, ao, b, bo):
    n = mathn(nt, "MULTIPLY"); L(nt, a, ao, n, 0); L(nt, b, bo, n, 1); return n


def madd(nt, a, ao, k, b, bo):
    """a*k + b"""
    n = mathn(nt, "MULTIPLY_ADD"); L(nt, a, ao, n, 0); n.inputs[1].default_value = k; L(nt, b, bo, n, 2); return n


def periodic(nt, uvsep, R, off):
    cu = mathn(nt, "COSINE"); su = mathn(nt, "SINE"); cv = mathn(nt, "COSINE"); sv = mathn(nt, "SINE")
    mu = mathn(nt, "MULTIPLY", None, TAU); mv = mathn(nt, "MULTIPLY", None, TAU)
    L(nt, uvsep, 0, mu, 0); L(nt, uvsep, 1, mv, 0)
    L(nt, mu, 0, cu, 0); L(nt, mu, 0, su, 0); L(nt, mv, 0, cv, 0); L(nt, mv, 0, sv, 0)
    comb = N(nt, "ShaderNodeCombineXYZ")
    for k, src in enumerate((cu, su, cv)):
        m = mathn(nt, "MULTIPLY", None, R); L(nt, src, 0, m, 0); L(nt, m, 0, comb, k)
    w = mathn(nt, "MULTIPLY_ADD"); L(nt, sv, 0, w, 0); w.inputs[1].default_value = R; w.inputs[2].default_value = off
    return comb, w


def noise4(nt, vec, w, scale, detail, rough):
    n = N(nt, "ShaderNodeTexNoise"); n.noise_dimensions = '4D'
    L(nt, vec, 0, n, "Vector"); L(nt, w, 0, n, "W")
    n.inputs["Scale"].default_value = scale; n.inputs["Detail"].default_value = detail; n.inputs["Roughness"].default_value = rough
    return n


def voronoi4(nt, vec, w, scale, feature):
    n = N(nt, "ShaderNodeTexVoronoi"); n.voronoi_dimensions = '4D'; n.feature = feature
    nt.links.new(vec.outputs[0], n.inputs["Vector"]); L(nt, w, 0, n, "W"); n.inputs["Scale"].default_value = scale
    return n


def mrange(nt, sn, so, a, b, c, d, smooth=True):
    n = N(nt, "ShaderNodeMapRange")
    if smooth:
        n.interpolation_type = 'SMOOTHSTEP'
    n.clamp = True
    nt.links.new(sn.outputs[so], n.inputs[0])
    n.inputs[1].default_value = a; n.inputs[2].default_value = b; n.inputs[3].default_value = c; n.inputs[4].default_value = d
    return n


def rgb(nt, col):
    n = N(nt, "ShaderNodeRGB"); n.outputs[0].default_value = (col[0], col[1], col[2], 1); return n


def _out(node):
    return node.outputs[2] if node.bl_idname == "ShaderNodeMix" else node.outputs[0]


def mix(nt, fac, fo, a, b, blend='MIX'):
    n = N(nt, "ShaderNodeMix"); n.data_type = 'RGBA'; n.blend_type = blend; n.clamp_result = True
    if fac is None:
        n.inputs[0].default_value = fo
    else:
        nt.links.new(fac.outputs[fo], n.inputs[0])
    nt.links.new(_out(a), n.inputs[6]); nt.links.new(_out(b), n.inputs[7])
    return n


def out_emit(nt, name, src, so):
    e = N(nt, "ShaderNodeEmission"); e.name = "OUT_" + name; nt.links.new(src.outputs[so], e.inputs[0]); return e


def out_normal(nt, hn, ho, strength, dist):
    b = N(nt, "ShaderNodeBump"); b.inputs["Strength"].default_value = strength; b.inputs["Distance"].default_value = dist
    nt.links.new(hn.outputs[ho], b.inputs["Height"])
    p = N(nt, "ShaderNodeBsdfPrincipled"); p.name = "OUT_Normal"; nt.links.new(b.outputs[0], p.inputs["Normal"])
    return p


def new_mat(name):
    m = bpy.data.materials.get(name)
    if m:
        bpy.data.materials.remove(m)
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree
    for n in list(nt.nodes):
        if n.type != "OUTPUT_MATERIAL":
            nt.nodes.remove(n)
    tc = N(nt, "ShaderNodeTexCoord"); sep = N(nt, "ShaderNodeSeparateXYZ"); L(nt, tc, "UV", sep, 0)
    img = N(nt, "ShaderNodeTexImage"); img.name = "BAKE_TARGET"
    return m, nt, sep


def cloth_mat(name, base, dust=(0.20, 0.19, 0.175), seed=3.0, dust_amt=0.75, soot_amt=0.8):
    """작업복 천(능직 결 + 먼지 + 그을음 + 탄 구멍 + 슬래그 튐). Slag Walker 작업복과 같은 레시피."""
    m, nt, sep = new_mat(name)
    P, W = periodic(nt, sep, 1.0, seed)
    uvp = mathn(nt, "ADD"); L(nt, sep, 0, uvp, 0); L(nt, sep, 1, uvp, 1)
    w1 = mathn(nt, "MULTIPLY", None, TAU * 56); L(nt, uvp, 0, w1, 0); w1s = mathn(nt, "SINE"); L(nt, w1, 0, w1s, 0)
    vv = mathn(nt, "MULTIPLY", None, TAU * 112); L(nt, sep, 1, vv, 0); vvs = mathn(nt, "SINE"); L(nt, vv, 0, vvs, 0)
    weave = madd(nt, w1s, 0, 0.5, vvs, 0)
    dust_n = noise4(nt, P, W, 1.3, 5, 0.55); soot = noise4(nt, P, W, 2.4, 6, 0.6)
    burnv = voronoi4(nt, P, W, 1.6, 'F1'); bnoise = noise4(nt, P, W, 6.0, 4, 0.5)
    bsum = madd(nt, bnoise, "Fac", 0.18, burnv, "Distance")
    burn = mrange(nt, bsum, 0, 0.18, 0.24, 1.0, 0.0); ring = mrange(nt, bsum, 0, 0.20, 0.33, 1.0, 0.0)
    splv = voronoi4(nt, P, W, 7.0, 'F1'); splc = N(nt, "ShaderNodeSeparateColor"); L(nt, splv, "Color", splc, 0)
    spl0 = mrange(nt, splv, "Distance", 0.05, 0.09, 1.0, 0.0); sel = mrange(nt, splc, 0, 0.62, 0.66, 0.0, 1.0)
    spl = mul(nt, spl0, 0, sel, 0)
    oil = noise4(nt, P, W, 0.9, 3, 0.5); oilm = mrange(nt, oil, "Fac", 0.58, 0.72, 0.0, 0.7)
    k1 = mix(nt, mrange(nt, dust_n, "Fac", 0.48, 0.72, 0.0, dust_amt), 0, rgb(nt, base), rgb(nt, dust))
    wm = mrange(nt, weave, 0, -1.5, 1.5, 0.85, 1.12, smooth=False)
    k2 = N(nt, "ShaderNodeMix"); k2.data_type = 'RGBA'; k2.blend_type = 'MULTIPLY'; k2.inputs[0].default_value = 1.0
    nt.links.new(k1.outputs[2], k2.inputs[6]); nt.links.new(wm.outputs[0], k2.inputs[7])
    k2b = mix(nt, oilm, 0, k2, rgb(nt, (0.03, 0.028, 0.025)))           # 기름 얼룩
    k3 = mix(nt, mrange(nt, soot, "Fac", 0.55, 0.75, 0.0, soot_amt), 0, k2b, rgb(nt, (0.015, 0.014, 0.014)))
    k4 = mix(nt, ring, 0, k3, rgb(nt, (0.13, 0.075, 0.035)))
    k5 = mix(nt, burn, 0, k4, rgb(nt, (0.015, 0.014, 0.014)))
    k6 = mix(nt, spl, 0, k5, rgb(nt, (0.05, 0.046, 0.045)))
    out_emit(nt, "Color", k6, 2)
    return m


def rust_mat(name, paint=None, seed=11.0):
    """녹슨 쇠. paint=(r,g,b) 이면 그 위에 벗겨진 도장(크레인 노랑 등)."""
    m, nt, sep = new_mat(name)
    P, W = periodic(nt, sep, 1.0, seed)
    big = noise4(nt, P, W, 1.4, 6, 0.6)
    fine = noise4(nt, P, W, 7.0, 10, 0.65)
    pitv = voronoi4(nt, P, W, 9.0, 'F1')
    pits = mrange(nt, pitv, "Distance", 0.0, 0.14, 1.0, 0.0)
    flake = voronoi4(nt, P, W, 7.0, 'F1'); flc = N(nt, "ShaderNodeSeparateColor"); L(nt, flake, "Color", flc, 0)
    rustm = mrange(nt, big, "Fac", 0.38, 0.62, 0.15, 1.0)
    c_iron = rgb(nt, (0.055, 0.050, 0.046)); c_rust = rgb(nt, (0.30, 0.12, 0.045)); c_deep = rgb(nt, (0.12, 0.05, 0.025))
    c_flk = rgb(nt, (0.27, 0.11, 0.045))
    r1 = mix(nt, rustm, 0, c_iron, c_rust)
    fm = mrange(nt, fine, "Fac", 0.35, 0.65, 0.0, 1.0)
    r2 = mix(nt, mul(nt, fm, 0, rustm, 0), 0, r1, c_deep)
    r3 = mix(nt, mul(nt, mrange(nt, flc, 0, 0.86, 0.9, 0.0, 0.5), 0, rustm, 0), 0, r2, c_flk)
    r4 = mix(nt, mul(nt, pits, 0, rustm, 0), 0, r3, rgb(nt, (0.03, 0.02, 0.015)))
    col = r4
    metal = mrange(nt, rustm, 0, 0.3, 0.8, 0.75, 0.12, smooth=False)
    rough = mrange(nt, rustm, 0, 0.3, 0.8, 0.45, 0.92, smooth=False)
    height = madd(nt, fine, "Fac", 0.5, mul(nt, rustm, 0, big, "Fac"), 0)
    height = madd(nt, pits, 0, -0.35, height, 0)
    if paint is not None:
        chip_n = noise4(nt, P, W, 3.2, 8, 0.7)
        edge = madd(nt, fine, "Fac", 0.25, chip_n, "Fac")
        paintm = mrange(nt, edge, 0, 0.64, 0.68, 1.0, 0.0)      # 1 = 도장 남음
        grime = noise4(nt, P, W, 1.1, 4, 0.5)
        pc = mix(nt, mrange(nt, grime, "Fac", 0.45, 0.75, 0.0, 0.55), 0, rgb(nt, paint), rgb(nt, (0.10, 0.08, 0.04)))
        pc2 = mix(nt, mrange(nt, fine, "Fac", 0.3, 0.7, 0.0, 0.25), 0, pc, rgb(nt, (0.0, 0.0, 0.0)))
        col = mix(nt, paintm, 0, r4, pc2)
        metal = mix(nt, paintm, 0, metal, rgb(nt, (0.0, 0.0, 0.0)))
        rough = mix(nt, paintm, 0, rough, rgb(nt, (0.62, 0.62, 0.62)))
        height = madd(nt, paintm, 0, 0.35, height, 0)
        out_emit(nt, "Metal", metal, 2); out_emit(nt, "Rough", rough, 2)
    else:
        out_emit(nt, "Metal", metal, 0); out_emit(nt, "Rough", rough, 0)
    out_emit(nt, "Color", col, 2)
    out_normal(nt, height, 0, 0.8, 0.03)
    return m


def bake_plane():
    pl = bpy.data.objects.get("TK_BakePlane")
    if pl is None:
        me = bpy.data.meshes.new("TK_BakePlane")
        me.from_pydata([(0, 0, -10), (1, 0, -10), (1, 1, -10), (0, 1, -10)], [], [(0, 1, 2, 3)])
        uvl = me.uv_layers.new(name="UVMap")
        for i, c in enumerate(((0, 0), (1, 0), (1, 1), (0, 1))):
            uvl.data[i].uv = c
        pl = bpy.data.objects.new("TK_BakePlane", me)
        bpy.context.scene.collection.objects.link(pl)
    pl.hide_render = False
    return pl


def bake_jobs(jobs, subdir, size=1024):
    """jobs = [(머티리얼, 채널, 파일이름), ...]  채널 Normal 은 NORMAL, 나머지 EMIT. 호출당 2~3장 권장."""
    sc = bpy.context.scene
    try:
        sc.render.engine = 'CYCLES'
    except TypeError:
        pass
    sc.cycles.device = 'CPU'; sc.cycles.samples = 4; sc.render.bake.margin = 8; sc.render.bake.normal_space = 'TANGENT'
    pl = bake_plane()
    for o in bpy.context.view_layer.objects:
        o.select_set(False)
    pl.select_set(True); bpy.context.view_layer.objects.active = pl
    done = []
    for matname, ch, fname in jobs:
        m = bpy.data.materials[matname]; nt = m.node_tree
        pl.data.materials.clear(); pl.data.materials.append(m)
        out = next(n for n in nt.nodes if n.type == "OUTPUT_MATERIAL")
        nt.links.new(nt.nodes["OUT_" + ch].outputs[0], out.inputs["Surface"])
        im = bpy.data.images.get("TK_" + fname)
        if im:
            bpy.data.images.remove(im)
        im = bpy.data.images.new("TK_" + fname, size, size, alpha=False)
        im.colorspace_settings.name = "sRGB" if ch == "Color" else "Non-Color"
        t = nt.nodes["BAKE_TARGET"]; t.image = im; nt.nodes.active = t
        bpy.ops.object.bake(type='NORMAL' if ch == "Normal" else 'EMIT')
        im.filepath_raw = TEX_DIR + subdir + "\\" + fname + ".png"; im.file_format = 'PNG'; im.save()
        done.append(fname)
    return done


def foil_mat(name, seed=21.0):
    """알루미늄 코팅 내열복: 구김 + 누빔 선 + 그을음 + 열 변색 + 찢겨 드러난 속감(금속 아님)."""
    m, nt, sep = new_mat(name)
    P, W = periodic(nt, sep, 1.0, seed)
    crk = noise4(nt, P, W, 6.0, 8, 0.7)                     # 구김 (고주파)
    crkb = noise4(nt, P, W, 2.2, 4, 0.6)                    # 큰 주름
    # 누빔 선: u 방향 6줄, v 방향 4줄 (정수라 이음매 없음)
    qu = mathn(nt, "MULTIPLY", None, TAU * 3); L(nt, sep, 0, qu, 0); qus = mathn(nt, "COSINE"); L(nt, qu, 0, qus, 0)
    qv = mathn(nt, "MULTIPLY", None, TAU * 2); L(nt, sep, 1, qv, 0); qvs = mathn(nt, "COSINE"); L(nt, qv, 0, qvs, 0)
    lu = mrange(nt, qus, 0, 0.975, 0.995, 0.0, 1.0); lv = mrange(nt, qvs, 0, 0.985, 0.998, 0.0, 0.5)
    seam = mathn(nt, "MAXIMUM"); L(nt, lu, 0, seam, 0); L(nt, lv, 0, seam, 1)
    soot = noise4(nt, P, W, 0.7, 5, 0.55); sootm = mrange(nt, soot, "Fac", 0.50, 0.78, 0.0, 0.75)
    heat = noise4(nt, P, W, 0.55, 3, 0.5); heatm = mrange(nt, heat, "Fac", 0.50, 0.70, 0.0, 0.6)
    tearv = voronoi4(nt, P, W, 2.4, 'F1'); tn = noise4(nt, P, W, 7.0, 4, 0.6)
    tsum = madd(nt, tn, "Fac", 0.12, tearv, "Distance")
    tear = mrange(nt, tsum, 0, 0.13, 0.16, 1.0, 0.0)
    c_foil = rgb(nt, (0.62, 0.62, 0.60)); c_dull = rgb(nt, (0.50, 0.50, 0.49))
    f1 = mix(nt, mrange(nt, crk, "Fac", 0.35, 0.65, 0.0, 1.0), 0, c_foil, c_dull)
    f2 = mix(nt, mul(nt, seam, 0, mathn(nt, "MULTIPLY", 1.0, 0.35), 0), 0, f1, rgb(nt, (0.25, 0.25, 0.25)))
    f3 = mix(nt, heatm, 0, f2, rgb(nt, (0.40, 0.26, 0.12)))           # 열 변색(갈색)
    f4 = mix(nt, sootm, 0, f3, rgb(nt, (0.035, 0.032, 0.03)))         # 그을음
    f5 = mix(nt, tear, 0, f4, rgb(nt, (0.30, 0.26, 0.19)))             # 찢긴 속감(유리섬유)
    out_emit(nt, "Color", f5, 2)
    metal = mix(nt, tear, 0, mix(nt, sootm, 0, rgb(nt, (0.85, 0.85, 0.85)), rgb(nt, (0.1, 0.1, 0.1))), rgb(nt, (0.0, 0.0, 0.0)))
    out_emit(nt, "Metal", metal, 2)
    r0 = mrange(nt, crk, "Fac", 0.3, 0.7, 0.22, 0.42, smooth=False)
    rough = mix(nt, tear, 0, mix(nt, sootm, 0, r0, rgb(nt, (0.85, 0.85, 0.85))), rgb(nt, (0.95, 0.95, 0.95)))
    out_emit(nt, "Rough", rough, 2)
    h = madd(nt, crk, "Fac", 0.6, crkb, "Fac")
    h = madd(nt, seam, 0, -0.35, h, 0)
    h = madd(nt, tear, 0, -0.3, h, 0)
    out_normal(nt, h, 0, 0.9, 0.025)
    return m
