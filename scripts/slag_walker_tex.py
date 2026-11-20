# Slag Walker 타일 텍스처 셰이더 (굽기용) — Blender MCP 안전 모드용
# 굽기 판 SW_BakePlane(UV 0..1) + 머티리얼 BAKE_SWSlag / BAKE_SWCloth / BAKE_SWSkin.
# 출력 소켓은 "OUT_<채널>" 이름의 Emission 노드 입력으로 모아 두고, 굽기 때 Material Output 에 연결을 바꿔 끼움.
# 4D 노이즈 링 좌표 (R cos2πu, R sin2πu, R cos2πv, R sin2πv) 로 양방향 이음매 없이 반복.
import bpy, math

TAU = 2 * math.pi

def N(nt, kind, x, y):
    n = nt.nodes.new(kind)
    n.location = (x, y)
    return n

def L(nt, a, ai, b, bi):
    nt.links.new(a.outputs[ai], b.inputs[bi])

def math_node(nt, op, x, y, a=None, b=None):
    n = N(nt, "ShaderNodeMath", x, y)
    n.operation = op
    if a is not None and not hasattr(a, "is_linked"):
        n.inputs[0].default_value = a
    if b is not None and not hasattr(b, "is_linked"):
        n.inputs[1].default_value = b
    return n

def periodic(nt, uvsep, R, off, x, y):
    """uvsep: Separate XYZ(UV). 반환 (vector 노드, w 노드)."""
    cu = math_node(nt, "COSINE", x, y); su = math_node(nt, "SINE", x, y - 40)
    cv = math_node(nt, "COSINE", x, y - 80); sv = math_node(nt, "SINE", x, y - 120)
    mu = math_node(nt, "MULTIPLY", x - 150, y, None, TAU); mv = math_node(nt, "MULTIPLY", x - 150, y - 80, None, TAU)
    L(nt, uvsep, 0, mu, 0); L(nt, uvsep, 1, mv, 0)
    L(nt, mu, 0, cu, 0); L(nt, mu, 0, su, 0); L(nt, mv, 0, cv, 0); L(nt, mv, 0, sv, 0)
    comb = N(nt, "ShaderNodeCombineXYZ", x + 300, y)
    outs = []
    for k, src in enumerate((cu, su, cv)):
        m = math_node(nt, "MULTIPLY", x + 150, y - 40 * k, None, R)
        L(nt, src, 0, m, 0)
        L(nt, m, 0, comb, k)
    w = math_node(nt, "MULTIPLY_ADD", x + 150, y - 160)
    L(nt, sv, 0, w, 0)
    w.inputs[1].default_value = R
    w.inputs[2].default_value = off
    return comb, w

def noise4(nt, vec, w, scale, detail, rough, x, y):
    n = N(nt, "ShaderNodeTexNoise", x, y)
    n.noise_dimensions = '4D'
    L(nt, vec, 0, n, "Vector"); L(nt, w, 0, n, "W")
    n.inputs["Scale"].default_value = scale
    n.inputs["Detail"].default_value = detail
    n.inputs["Roughness"].default_value = rough
    return n

def voronoi4(nt, vec, w, scale, feature, x, y, vec_out=0):
    n = N(nt, "ShaderNodeTexVoronoi", x, y)
    n.voronoi_dimensions = '4D'
    n.feature = feature
    nt.links.new(vec.outputs[vec_out], n.inputs["Vector"])
    L(nt, w, 0, n, "W")
    n.inputs["Scale"].default_value = scale
    return n

def maprange(nt, sock_node, sock, a, b, c, d, x, y, smooth=True):
    n = N(nt, "ShaderNodeMapRange", x, y)
    if smooth:
        n.interpolation_type = 'SMOOTHSTEP'
    n.clamp = True
    nt.links.new(sock_node.outputs[sock], n.inputs[0])
    n.inputs[1].default_value = a; n.inputs[2].default_value = b
    n.inputs[3].default_value = c; n.inputs[4].default_value = d
    return n

def rgb(nt, col, x, y):
    n = N(nt, "ShaderNodeRGB", x, y)
    n.outputs[0].default_value = (col[0], col[1], col[2], 1)
    return n

def mix(nt, fac_node, fac_out, a_node, b_node, x, y, blend='MIX'):
    n = N(nt, "ShaderNodeMix", x, y)
    n.data_type = 'RGBA'
    n.blend_type = blend
    n.clamp_result = True
    if fac_node is None:
        n.inputs[0].default_value = fac_out
    else:
        nt.links.new(fac_node.outputs[fac_out], n.inputs[0])
    nt.links.new(a_node.outputs[2] if a_node.bl_idname == "ShaderNodeMix" else a_node.outputs[0], n.inputs[6])
    nt.links.new(b_node.outputs[2] if b_node.bl_idname == "ShaderNodeMix" else b_node.outputs[0], n.inputs[7])
    return n

def out_emit(nt, name, src_node, src_out, x, y):
    e = N(nt, "ShaderNodeEmission", x, y)
    e.name = "OUT_" + name
    e.label = "OUT_" + name
    nt.links.new(src_node.outputs[src_out], e.inputs[0])
    return e

def out_normal(nt, height_node, height_out, strength, dist, x, y):
    b = N(nt, "ShaderNodeBump", x, y)
    b.inputs["Strength"].default_value = strength
    b.inputs["Distance"].default_value = dist
    nt.links.new(height_node.outputs[height_out], b.inputs["Height"])
    p = N(nt, "ShaderNodeBsdfPrincipled", x + 200, y)
    p.name = "OUT_Normal"
    nt.links.new(b.outputs[0], p.inputs["Normal"])
    return p

def new_mat(name):
    m = bpy.data.materials.get(name)
    if m:
        bpy.data.materials.remove(m)
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    for n in list(nt.nodes):
        if n.type != "OUTPUT_MATERIAL":
            nt.nodes.remove(n)
    tc = N(nt, "ShaderNodeTexCoord", -2400, 0)
    sep = N(nt, "ShaderNodeSeparateXYZ", -2200, 0)
    L(nt, tc, "UV", sep, 0)
    img = N(nt, "ShaderNodeTexImage", 1400, 600)
    img.name = "BAKE_TARGET"
    return m, nt, sep

# ---------------- 슬래그 ----------------
m, nt, sep = new_mat("BAKE_SWSlag")
P, W = periodic(nt, sep, 1.0, 0.0, -2000, 0)
warp = noise4(nt, P, W, 1.6, 3, 0.5, -1500, 300)
wsub = N(nt, "ShaderNodeVectorMath", -1300, 300); wsub.operation = 'SUBTRACT'
L(nt, warp, "Color", wsub, 0); wsub.inputs[1].default_value = (0.5, 0.5, 0.5)
wsc = N(nt, "ShaderNodeVectorMath", -1150, 300); wsc.operation = 'SCALE'
L(nt, wsub, 0, wsc, 0); wsc.inputs["Scale"].default_value = 0.45
wadd = N(nt, "ShaderNodeVectorMath", -1000, 300); wadd.operation = 'ADD'
L(nt, P, 0, wadd, 0); L(nt, wsc, 0, wadd, 1)
edge = voronoi4(nt, wadd, W, 1.35, 'DISTANCE_TO_EDGE', -800, 300)
cell = voronoi4(nt, wadd, W, 1.35, 'F1', -800, 60)
# 큰 판 사이 굵은 균열 + 판 안의 가는 균열(2단)
edge2 = voronoi4(nt, wadd, W, 3.4, 'DISTANCE_TO_EDGE', -800, -180)
crackA = maprange(nt, edge, "Distance", 0.0, 0.045, 1.0, 0.0, -550, 400)
crackA2 = maprange(nt, edge2, "Distance", 0.0, 0.018, 0.55, 0.0, -550, 200)
cA = math_node(nt, "MAXIMUM", -350, 350); L(nt, crackA, 0, cA, 0); L(nt, crackA2, 0, cA, 1)
crackB = maprange(nt, edge, "Distance", 0.0, 0.10, 1.0, 0.0, -550, 0)
crackB2 = maprange(nt, edge2, "Distance", 0.0, 0.04, 0.85, 0.0, -550, -200)
cB = math_node(nt, "MAXIMUM", -350, 0); L(nt, crackB, 0, cB, 0); L(nt, crackB2, 0, cB, 1)
rim = maprange(nt, edge, "Distance", 0.0, 0.26, 1.0, 0.0, -550, -400)
det = noise4(nt, P, W, 5.0, 10, 0.6, -800, -500)
ash = noise4(nt, P, W, 1.2, 4, 0.55, -800, -750)
pitsv = voronoi4(nt, P, W, 7.5, 'F1', -800, -1000)
pits = maprange(nt, pitsv, "Distance", 0.0, 0.16, 1.0, 0.0, -550, -1000)
cellr = N(nt, "ShaderNodeSeparateColor", -550, 60); L(nt, cell, "Color", cellr, 0)
# 색 A (식은 형)
c_dark = rgb(nt, (0.030, 0.027, 0.026), -300, -1300)
c_grey = rgb(nt, (0.150, 0.140, 0.130), -300, -1400)
c_rust = rgb(nt, (0.130, 0.060, 0.030), -300, -1500)
c_heat = rgb(nt, (0.200, 0.030, 0.008), -300, -1600)
c_orng = rgb(nt, (1.000, 0.300, 0.040), -300, -1700)
ashm = maprange(nt, ash, "Fac", 0.45, 0.68, 0.0, 0.85, -300, -800)
m1 = mix(nt, ashm, 0, c_dark, c_grey, 0, -1300)
rustm = maprange(nt, cellr, 0, 0.72, 0.95, 0.0, 0.7, -300, -900)
m2 = mix(nt, rustm, 0, m1, c_rust, 200, -1300)
detm = maprange(nt, det, "Fac", 0.35, 0.65, 0.65, 1.15, -300, -1000, smooth=False)
m3 = N(nt, "ShaderNodeMix", 400, -1300); m3.data_type = 'RGBA'; m3.blend_type = 'MULTIPLY'; m3.inputs[0].default_value = 1.0
nt.links.new(m2.outputs[2], m3.inputs[6]); nt.links.new(detm.outputs[0], m3.inputs[7])
pitd = math_node(nt, "MULTIPLY", 400, -1000, None, 0.8); L(nt, pits, 0, pitd, 0)
m4 = mix(nt, pitd, 0, m3, c_dark, 600, -1300)
rimA = math_node(nt, "MULTIPLY", 600, -1000, None, 0.45); L(nt, rim, 0, rimA, 0)
m5 = mix(nt, rimA, 0, m4, c_heat, 800, -1300)
colA = mix(nt, cA, 0, m5, c_orng, 1000, -1300)
out_emit(nt, "ColorA", colA, 2, 1200, -1300)
# 색 B (갓 굳은 형): 판이 더 어둡고 붉게 달아오름, 균열 넓고 밝음
c_hotp = rgb(nt, (0.090, 0.025, 0.012), -300, -1900)
c_hot2 = rgb(nt, (0.550, 0.090, 0.010), -300, -2000)
c_yel = rgb(nt, (1.000, 0.520, 0.120), -300, -2100)
b1 = mix(nt, None, 0.55, m4, c_hotp, 600, -1900)
rimB = math_node(nt, "MULTIPLY", 600, -1700, None, 0.85); L(nt, rim, 0, rimB, 0)
b2 = mix(nt, rimB, 0, b1, c_hot2, 800, -1900)
colB = mix(nt, cB, 0, b2, c_yel, 1000, -1900)
out_emit(nt, "ColorB", colB, 2, 1200, -1900)
# 발광 마스크
eA = math_node(nt, "MULTIPLY_ADD", 900, 500); L(nt, rim, 0, eA, 0); eA.inputs[1].default_value = 0.08; L(nt, cA, 0, eA, 2)
eAc = math_node(nt, "MINIMUM", 1050, 500, None, 1.0); L(nt, eA, 0, eAc, 0)
out_emit(nt, "EmitA", eAc, 0, 1200, 500)
eB = math_node(nt, "MULTIPLY_ADD", 900, 300); L(nt, rim, 0, eB, 0); eB.inputs[1].default_value = 0.35; L(nt, cB, 0, eB, 2)
eBc = math_node(nt, "MINIMUM", 1050, 300, None, 1.0); L(nt, eB, 0, eBc, 0)
out_emit(nt, "EmitB", eBc, 0, 1200, 300)
# 높이 → 노멀
hplate = math_node(nt, "MULTIPLY_ADD", 300, 100); L(nt, cellr, 0, hplate, 0); hplate.inputs[1].default_value = 0.35; L(nt, det, "Fac", hplate, 2)
inv = math_node(nt, "SUBTRACT", 300, -50, 1.0); L(nt, cB, 0, inv, 1)
h1 = math_node(nt, "MULTIPLY", 500, 100); L(nt, hplate, 0, h1, 0); L(nt, inv, 0, h1, 1)
h2 = math_node(nt, "MULTIPLY_ADD", 700, 100); L(nt, pits, 0, h2, 0); h2.inputs[1].default_value = -0.25; L(nt, h1, 0, h2, 2)
out_normal(nt, h2, 0, 1.0, 0.06, 900, 100)
# 거칠기
rg = maprange(nt, det, "Fac", 0.3, 0.7, 0.97, 0.80, 700, -200, smooth=False)
rgc = mix(nt, cB, 0, rg, rgb(nt, (0.45, 0.45, 0.45), 600, -350), 900, -200)
out_emit(nt, "Rough", rgc, 2, 1200, -200)

# ---------------- 작업복 ----------------
m, nt, sep = new_mat("BAKE_SWCloth")
P, W = periodic(nt, sep, 1.0, 3.0, -2000, 0)
# 능직(twill) 결: sin(2πN(u+v)) 와 sin(2πN(u-v)), N = 56 (정수라 이음매 없음)
uv_plus = math_node(nt, "ADD", -1500, 600); L(nt, sep, 0, uv_plus, 0); L(nt, sep, 1, uv_plus, 1)
w1 = math_node(nt, "MULTIPLY", -1350, 600, None, TAU * 56); L(nt, uv_plus, 0, w1, 0)
w1s = math_node(nt, "SINE", -1200, 600); L(nt, w1, 0, w1s, 0)
vv = math_node(nt, "MULTIPLY", -1350, 450, None, TAU * 112); L(nt, sep, 1, vv, 0)
vvs = math_node(nt, "SINE", -1200, 450); L(nt, vv, 0, vvs, 0)
weave = math_node(nt, "MULTIPLY_ADD", -1050, 550); L(nt, w1s, 0, weave, 0); weave.inputs[1].default_value = 0.5; L(nt, vvs, 0, weave, 2)
dust = noise4(nt, P, W, 1.3, 5, 0.55, -800, 200)
soot = noise4(nt, P, W, 2.4, 6, 0.6, -800, -50)
burnv = voronoi4(nt, P, W, 1.6, 'F1', -800, -300)
bnoise = noise4(nt, P, W, 6.0, 4, 0.5, -800, -550)
bsum = math_node(nt, "MULTIPLY_ADD", -550, -300); L(nt, bnoise, "Fac", bsum, 0); bsum.inputs[1].default_value = 0.18; L(nt, burnv, "Distance", bsum, 2)
burn = maprange(nt, bsum, 0, 0.18, 0.24, 1.0, 0.0, -350, -300)
burnring = maprange(nt, bsum, 0, 0.20, 0.33, 1.0, 0.0, -350, -450)
splv = voronoi4(nt, P, W, 7.0, 'F1', -800, -800)
splc = N(nt, "ShaderNodeSeparateColor", -550, -800); L(nt, splv, "Color", splc, 0)
spl0 = maprange(nt, splv, "Distance", 0.05, 0.09, 1.0, 0.0, -350, -750)
splsel = maprange(nt, splc, 0, 0.62, 0.66, 0.0, 1.0, -350, -900)
spl = math_node(nt, "MULTIPLY", -150, -800); L(nt, spl0, 0, spl, 0); L(nt, splsel, 0, spl, 1)
c_navy = rgb(nt, (0.060, 0.072, 0.092), -300, -1300)
c_dust = rgb(nt, (0.200, 0.190, 0.175), -300, -1400)
c_soot = rgb(nt, (0.015, 0.014, 0.014), -300, -1500)
c_brn = rgb(nt, (0.130, 0.075, 0.035), -300, -1600)
c_slg = rgb(nt, (0.050, 0.046, 0.045), -300, -1700)
dm = maprange(nt, dust, "Fac", 0.48, 0.72, 0.0, 0.75, -100, 200)
k1 = mix(nt, dm, 0, c_navy, c_dust, 0, -1300)
wm = maprange(nt, weave, 0, -1.5, 1.5, 0.85, 1.12, -100, 550, smooth=False)
k2 = N(nt, "ShaderNodeMix", 200, -1300); k2.data_type = 'RGBA'; k2.blend_type = 'MULTIPLY'; k2.inputs[0].default_value = 1.0
nt.links.new(k1.outputs[2], k2.inputs[6]); nt.links.new(wm.outputs[0], k2.inputs[7])
sm = maprange(nt, soot, "Fac", 0.55, 0.75, 0.0, 0.8, -100, -50)
k3 = mix(nt, sm, 0, k2, c_soot, 400, -1300)
k4 = mix(nt, burnring, 0, k3, c_brn, 600, -1300)
k5 = mix(nt, burn, 0, k4, c_soot, 800, -1300)
k6 = mix(nt, spl, 0, k5, c_slg, 1000, -1300)
out_emit(nt, "Color", k6, 2, 1200, -1300)
hc = math_node(nt, "MULTIPLY", 300, 400, None, 0.25); L(nt, weave, 0, hc, 0)
hw = noise4(nt, P, W, 3.0, 3, 0.5, -800, 450)
hc2 = math_node(nt, "MULTIPLY_ADD", 500, 400); L(nt, hw, "Fac", hc2, 0); hc2.inputs[1].default_value = 1.2; L(nt, hc, 0, hc2, 2)
hc3 = math_node(nt, "MULTIPLY_ADD", 700, 400); L(nt, spl, 0, hc3, 0); hc3.inputs[1].default_value = 0.6; L(nt, hc2, 0, hc3, 2)
hc4 = math_node(nt, "MULTIPLY_ADD", 850, 400); L(nt, burn, 0, hc4, 0); hc4.inputs[1].default_value = -0.4; L(nt, hc3, 0, hc4, 2)
out_normal(nt, hc4, 0, 0.6, 0.03, 1000, 400)
cr = maprange(nt, spl, 0, 0.0, 1.0, 0.93, 0.70, 900, 0, smooth=False)
out_emit(nt, "Rough", cr, 0, 1200, 0)

# ---------------- 피부 ----------------
m, nt, sep = new_mat("BAKE_SWSkin")
P, W = periodic(nt, sep, 1.0, 7.0, -2000, 0)
blot = noise4(nt, P, W, 1.8, 5, 0.6, -800, 300)
soot = noise4(nt, P, W, 2.6, 6, 0.65, -800, 50)
ashn = noise4(nt, P, W, 1.1, 4, 0.5, -800, -200)
crk = voronoi4(nt, P, W, 3.0, 'DISTANCE_TO_EDGE', -800, -450)
crkm = maprange(nt, crk, "Distance", 0.0, 0.03, 1.0, 0.0, -550, -450)
por = voronoi4(nt, P, W, 22.0, 'F1', -800, -700)
porm = maprange(nt, por, "Distance", 0.0, 0.18, 1.0, 0.0, -550, -700)
c_sk = rgb(nt, (0.200, 0.090, 0.065), -300, -1300)
c_sk2 = rgb(nt, (0.090, 0.040, 0.030), -300, -1400)
c_st = rgb(nt, (0.020, 0.017, 0.016), -300, -1500)
c_as = rgb(nt, (0.300, 0.280, 0.260), -300, -1600)
c_rw = rgb(nt, (0.350, 0.040, 0.020), -300, -1700)
bm1 = maprange(nt, blot, "Fac", 0.4, 0.65, 0.0, 1.0, -100, 300)
s1 = mix(nt, bm1, 0, c_sk, c_sk2, 0, -1300)
sm2 = maprange(nt, soot, "Fac", 0.55, 0.72, 0.0, 0.85, -100, 50)
s2 = mix(nt, sm2, 0, s1, c_st, 200, -1300)
am = maprange(nt, ashn, "Fac", 0.6, 0.75, 0.0, 0.6, -100, -200)
s3 = mix(nt, am, 0, s2, c_as, 400, -1300)
s4 = mix(nt, crkm, 0, s3, c_rw, 600, -1300)
out_emit(nt, "Color", s4, 2, 1200, -1300)
hs = math_node(nt, "MULTIPLY_ADD", 300, 300); L(nt, crkm, 0, hs, 0); hs.inputs[1].default_value = -0.5; L(nt, blot, "Fac", hs, 2)
hs2 = math_node(nt, "MULTIPLY_ADD", 500, 300); L(nt, porm, 0, hs2, 0); hs2.inputs[1].default_value = -0.12; L(nt, hs, 0, hs2, 2)
out_normal(nt, hs2, 0, 0.5, 0.02, 700, 300)
sr = maprange(nt, soot, "Fac", 0.4, 0.7, 0.55, 0.85, 900, 0, smooth=False)
out_emit(nt, "Rough", sr, 0, 1200, 0)

# ---------------- 굽기 판 ----------------
bc = bpy.data.collections.get("SW_TexBake")
if bc is None:
    bc = bpy.data.collections.new("SW_TexBake")
    bpy.context.scene.collection.children.link(bc)
pl = bpy.data.objects.get("SW_BakePlane")
if pl is None:
    me = bpy.data.meshes.new("SW_BakePlane")
    me.from_pydata([(0, 0, -10), (1, 0, -10), (1, 1, -10), (0, 1, -10)], [], [(0, 1, 2, 3)])
    uvl = me.uv_layers.new(name="UVMap")
    for i, c in enumerate(((0, 0), (1, 0), (1, 1), (0, 1))):
        uvl.data[i].uv = c
    pl = bpy.data.objects.new("SW_BakePlane", me)
    bc.objects.link(pl)
pl.hide_render = False
print("materials ok")
