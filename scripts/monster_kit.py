# 몬스터 메쉬 공용 키트 (Blender, 안전 모드 끔 → exec(open(...).read()) 로 불러 씀)
# 좌표: Blender (x, y, z) = Roblox HRP 기준 (-X, Z, Y). 캐릭터 앞 = -y, 캐릭터 오른쪽 = -x.
# 오브젝트 이름 = <R15 부위>__<재질키>
# 2026-11-20: Slag Walker(slag_walker_build.py)에서 분리. loft 아래 방향 경로의 면 뒤집힘 수정 +
#             finalize 에서 덩어리별 부호 부피로 면 방향 자동 교정(뒤집힌 메쉬 재발 방지).
import bpy, bmesh, math
from mathutils import Vector, Matrix, noise

PIECES = {}

RIG = {  # Roblox HRP 기준 중심, 크기 (AshenHusk R15)
    "Head": ((0, 1.674, 0), (1.16, 1.18, 1.16)), "UpperTorso": ((0, 0.25, 0), (1.94, 1.70, 1.0)),
    "LowerTorso": ((0, -0.8, 0), (1.99, 0.40, 1.0)),
    "LeftUpperArm": ((-1.472, 0.428, 0), (1, 1.24, 1)), "RightUpperArm": ((1.472, 0.428, 0), (1, 1.24, 1)),
    "LeftLowerArm": ((-1.472, -0.202, 0), (1, 1.12, 1)), "RightLowerArm": ((1.472, -0.202, 0), (1, 1.12, 1)),
    "LeftHand": ((-1.472, -0.865, 0), (0.98, 0.32, 1.03)), "RightHand": ((1.472, -0.865, 0), (0.98, 0.32, 1.03)),
    "LeftUpperLeg": ((-0.498, -1.471, 0), (0.99, 1.36, 0.97)), "RightUpperLeg": ((0.498, -1.471, 0), (0.99, 1.36, 0.97)),
    "LeftLowerLeg": ((-0.498, -2.334, 0), (0.99, 1.30, 0.97)), "RightLowerLeg": ((0.498, -2.334, 0), (0.99, 1.30, 0.97)),
    "LeftFoot": ((-0.498, -3.036, 0), (1.01, 0.31, 1.0)), "RightFoot": ((0.498, -3.036, 0), (1.01, 0.31, 1.0)),
}


def get_col(name):
    c = bpy.data.collections.get(name)
    if c is None:
        c = bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(c)
    return c


def reset(colname):
    PIECES.clear()
    col = get_col(colname)
    for o in list(col.objects):
        bpy.data.objects.remove(o, do_unlink=True)
    return col


def bm_for(name):
    if name not in PIECES:
        PIECES[name] = bmesh.new()
    return PIECES[name]


def fbm(p, octaves, seed):
    s = 0.0; a = 1.0; f = 1.0; tot = 0.0
    for i in range(octaves):
        s += a * noise.noise(p * f + Vector((seed * 7.13 + i * 3.1, seed * 3.7, seed * 1.9)))
        tot += a; a *= 0.5; f *= 2.03
    return s / tot


def rock(p, seed):
    r = 1.0 - abs(fbm(p, 4, seed)) * 2.0
    c = noise.cell(p * 0.8 + Vector((seed * 1.7, 0, 0)))
    return 0.72 * r + 0.28 * (c * 2.0 - 1.0)


def cr(p0, p1, p2, p3, t):
    t2 = t * t; t3 = t2 * t
    return 0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t2 + (-p0 + 3 * p1 - 3 * p2 + p3) * t3)


def loft(name, keys, segs=16, sub=3, expo=1.0, cap0=0.0, cap1=0.0, amp=0.0, freq=4.0, seed=0, up=None):
    """keys = [(x, y, z, rx, ry), ...] 경로를 따라 초타원 단면. up = 단면 x축 기준 방향(기본 월드 X)."""
    bm = bm_for(name)
    K = [Vector(k) for k in keys]
    Kx = [K[0]] + K + [K[-1]]
    pts = []
    for i in range(1, len(Kx) - 2):
        n = sub if i < len(Kx) - 3 else sub + 1
        for s in range(n):
            pts.append(cr(Kx[i - 1], Kx[i], Kx[i + 1], Kx[i + 2], s / sub))
    ref = Vector(up) if up is not None else Vector((1, 0, 0))
    rows = []
    for j, P in enumerate(pts):
        c = Vector((P[0], P[1], P[2]))
        a = Vector(pts[max(0, j - 1)][0:3]); b = Vector(pts[min(len(pts) - 1, j + 1)][0:3])
        t = (b - a).normalized()
        xa = (ref - t * ref.dot(t))
        if xa.length < 1e-4:
            xa = Vector((0, 1, 0)) - t * t.y
        xa.normalize()
        ya = t.cross(xa)  # 오른손 좌표계 유지 (xa × ya = t)
        row = []
        for i in range(segs):
            ang = 2 * math.pi * i / segs
            ca = math.cos(ang); sa = math.sin(ang)
            ux = math.copysign(abs(ca) ** expo, ca); uy = math.copysign(abs(sa) ** expo, sa)
            p = c + xa * (ux * P[3]) + ya * (uy * P[4])
            if amp > 0:
                p = p + (xa * ux + ya * uy).normalized() * amp * fbm(p * freq, 3, seed)
            row.append(bm.verts.new(p))
        rows.append((row, c, t))
    for j in range(len(rows) - 1):
        r0 = rows[j][0]; r1 = rows[j + 1][0]
        for i in range(segs):
            i2 = (i + 1) % segs
            bm.faces.new((r0[i], r0[i2], r1[i2], r1[i]))
    for which, capl in ((0, cap0), (1, cap1)):
        row, c, t = rows[0] if which == 0 else rows[-1]
        sgn = -1.0 if which == 0 else 1.0
        inner = [bm.verts.new(c + (v.co - c) * 0.6 + t * sgn * capl * 0.75) for v in row]
        pole = bm.verts.new(c + t * sgn * capl)
        for i in range(segs):
            i2 = (i + 1) % segs
            if which == 0:
                bm.faces.new((row[i2], row[i], inner[i], inner[i2])); bm.faces.new((inner[i2], inner[i], pole))
            else:
                bm.faces.new((row[i], row[i2], inner[i2], inner[i])); bm.faces.new((inner[i], inner[i2], pole))
    return bm


def blob(name, c, r, segs=12, rings=8, amp=0.0, freq=3.0, seed=0, square=1.0, kind="smooth", rot=None):
    bm = bm_for(name)
    res = bmesh.ops.create_uvsphere(bm, u_segments=segs, v_segments=rings, radius=1.0)
    c = Vector(c)
    R = rot if rot is not None else Matrix.Identity(3)
    for v in res["verts"]:
        d = v.co.copy()
        if square != 1.0:
            d = Vector((math.copysign(abs(d.x) ** square, d.x), math.copysign(abs(d.y) ** square, d.y), math.copysign(abs(d.z) ** square, d.z)))
        n = d.normalized() if d.length > 1e-6 else Vector((0, 0, 1))
        p = Vector((d.x * r[0], d.y * r[1], d.z * r[2]))
        if amp > 0:
            w = p + c
            nz = rock(w * freq, seed) if kind == "rock" else fbm(w * freq, 3, seed)
            p = p + Vector((n.x * r[0], n.y * r[1], n.z * r[2])).normalized() * (amp * nz)
        v.co = R @ p + c
    return res["verts"]


def box(name, c, size, rot=None, bevel=0.0):
    bm = bm_for(name)
    res = bmesh.ops.create_cube(bm, size=1.0)
    R = rot if rot is not None else Matrix.Identity(3)
    for v in res["verts"]:
        v.co = R @ Vector((v.co.x * size[0], v.co.y * size[1], v.co.z * size[2])) + Vector(c)
    return res["verts"]


def tube(name, a, b, r0, r1, segs=8, rings=2):
    bm = bm_for(name)
    a = Vector(a); b = Vector(b)
    zd = (b - a).normalized(); L = (b - a).length
    M = Vector((0, 0, 1)).rotation_difference(zd).to_matrix()
    rows = []
    for j in range(rings + 1):
        t = j / rings
        rad = r0 + (r1 - r0) * t
        rows.append([bm.verts.new(M @ Vector((math.cos(2 * math.pi * i / segs) * rad, math.sin(2 * math.pi * i / segs) * rad, t * L)) + a) for i in range(segs)])
    for j in range(rings):
        for i in range(segs):
            i2 = (i + 1) % segs
            bm.faces.new((rows[j][i], rows[j][i2], rows[j + 1][i2], rows[j + 1][i]))
    bm.faces.new(list(reversed(rows[0])))
    tip = bm.verts.new(b + zd * r1)
    for i in range(segs):
        bm.faces.new((rows[-1][i], rows[-1][(i + 1) % segs], tip))


def finger(name, pts, r0, r1, segs=6):
    n = len(pts) - 1
    for i in range(n):
        tube(name, pts[i], pts[i + 1], r0 + (r1 - r0) * i / n, r0 + (r1 - r0) * (i + 1) / n, segs, 1)


def torus(name, c, R0, R1, r, frame, useg=8, vseg=4):
    """타원 고리(사슬 고리). frame = 3x3 (열: 고리 평면 x, 고리 평면 y(긴 축), 법선). R0/R1 = x/y 반지름, r = 굵기."""
    bm = bm_for(name)
    c = Vector(c)
    rows = []
    for i in range(useg):
        u = 2 * math.pi * i / useg
        cu, su = math.cos(u), math.sin(u)
        ring_c = Vector((cu * R0, su * R1, 0))
        radial = Vector((cu * R1, su * R0, 0)).normalized()
        row = []
        for j in range(vseg):
            v = 2 * math.pi * j / vseg
            p = ring_c + radial * (math.cos(v) * r) + Vector((0, 0, math.sin(v) * r))
            row.append(bm.verts.new(frame @ p + c))
        rows.append(row)
    for i in range(useg):
        i2 = (i + 1) % useg
        for j in range(vseg):
            j2 = (j + 1) % vseg
            bm.faces.new((rows[i][j], rows[i2][j], rows[i2][j2], rows[i][j2]))


def chain(name, path, link_len=0.30, link_w=0.18, thick=0.035, useg=10, vseg=4, twist0=0.0):
    """경로(점 목록)를 따라 서로 90° 엇갈린 사슬 고리."""
    P = [Vector(p) for p in path]
    Px = [P[0]] + P + [P[-1]]
    dense = []
    for i in range(1, len(Px) - 2):
        for s in range(12):
            dense.append(cr(Px[i - 1], Px[i], Px[i + 1], Px[i + 2], s / 12))
    dense.append(P[-1])
    pitch = link_len - 2.2 * thick  # 고리 안쪽 길이만큼 (서로 맞물림)
    acc = 0.0
    k = 0
    last = dense[0]
    placed = [dense[0]]
    for q in dense[1:]:
        acc += (q - last).length
        last = q
        if acc >= pitch:
            placed.append(q)
            acc = 0.0
    for i in range(len(placed) - 1):
        a, b = placed[i], placed[i + 1]
        t = (b - a).normalized()
        c = (a + b) * 0.5
        ref = Vector((0, 0, 1)) if abs(t.z) < 0.9 else Vector((1, 0, 0))
        n0 = (ref - t * ref.dot(t)).normalized()
        ang = twist0 + (math.pi / 2 if i % 2 else 0.0)
        n = (n0 * math.cos(ang) + t.cross(n0) * math.sin(ang)).normalized()
        xa = n.cross(t)
        frame = Matrix((xa, t, n)).transposed()
        torus(name, c, link_w * 0.5 - thick, link_len * 0.5 - thick, thick, frame, useg, vseg)
        k += 1
    return k


def hook(name, M, scale=1.0, shank=0.6, R=0.38, thick=0.13, segs=10):
    """크레인 갈고리 (로컬: 축=+z 위, 갈고리 고리는 y-z 평면, 끝이 +y 쪽). M = 4x4 배치 행렬."""
    tmp = "__hooktmp"
    PIECES.pop(tmp, None)
    s = scale
    keys = [(0, 0, (shank + 0.0) * s, thick * 0.8 * s, thick * 0.8 * s), (0, 0, 0.0, thick * s, thick * 1.1 * s)]
    # 고리: 축 아래 끝(0,0,0)에서 시작해 원 중심 (0, R, 0) 주위로 약 290°
    for k in range(1, 12):
        a = math.pi + (k / 11) * math.radians(290)  # 시작각 180°(=축 위치) → 반시계
        y = R * s + math.cos(a) * R * s
        z = math.sin(a) * R * s
        taper = 1.0 - 0.75 * (k / 11) ** 1.5
        keys.append((0, y, z, thick * s * taper, thick * 1.25 * s * taper))
    loft(tmp, keys, segs=segs, sub=2, cap0=0.02 * s, cap1=0.06 * s, up=(1, 0, 0))
    # 위쪽 회전 너트 + 고리 눈
    loft(tmp, [(0, 0, shank * s, 0.17 * s, 0.17 * s), (0, 0, (shank + 0.16) * s, 0.17 * s, 0.17 * s)], segs=segs, sub=1, cap0=0.0, cap1=0.0)
    torus(tmp, (0, 0, (shank + 0.36) * s), 0.12 * s, 0.17 * s, 0.05 * s, Matrix.Identity(3) @ Matrix(((1, 0, 0), (0, 0, 1), (0, 1, 0))).transposed(), 10, 5)
    src = PIECES.pop(tmp)
    for v in src.verts:
        v.co = M @ v.co
    me = bpy.data.meshes.new("_tmp")
    src.to_mesh(me); src.free()
    bm_for(name).from_mesh(me)
    bpy.data.meshes.remove(me)


def push(name, c, rad, amount):
    bm = PIECES[name]
    bm.normal_update()
    c = Vector(c)
    for v in bm.verts:
        d = (v.co - c).length
        if d < rad:
            f = 1 - d / rad
            v.co += v.normal * amount * f * f * (3 - 2 * f)


def shell(dst, src, seed, bias_dir, bias_k, bias_c, offset, thick, mfreq=2.2, holes=0.55, amp=0.0, rfreq=5.0, zmin=None, zmax=None, cut=None):
    """src 표면을 offset 만큼 띄운 얇은 껍질(옷 조각·조끼·껍질). 마스크 음수면 구멍. amp>0 이면 울퉁불퉁(rock)."""
    sb = PIECES[src].copy()
    sb.normal_update()
    bias_dir = Vector(bias_dir)
    mask = {}
    for v in sb.verts:
        m = holes * fbm(v.co * mfreq, 3, seed) + bias_k * bias_dir.dot(v.co) + bias_c
        if zmin is not None and v.co.z < zmin:
            m = -1
        if zmax is not None and v.co.z > zmax:
            m = -1
        if cut is not None and cut(v.co):
            m = -1
        mask[v.index] = m
    kill = [f for f in sb.faces if sum(mask[v.index] for v in f.verts) / len(f.verts) < 0.0]
    bmesh.ops.delete(sb, geom=kill, context='FACES')
    bmesh.ops.delete(sb, geom=[v for v in sb.verts if not v.link_faces], context='VERTS')
    sb.normal_update()
    edge = set(v for e in sb.edges if e.is_boundary for v in e.verts)
    for v in sb.verts:
        m = 0.5 if v in edge else 1.0
        h = offset * m + (amp * m * rock(v.co * rfreq, seed) if amp > 0 else 0.0)
        v.co += v.normal.copy() * max(0.008, h)
    bmesh.ops.solidify(sb, geom=sb.faces[:], thickness=thick)
    me = bpy.data.meshes.new("_tmp")
    sb.to_mesh(me); sb.free()
    bm_for(dst).from_mesh(me)
    bpy.data.meshes.remove(me)


def fix_components(bm):
    """연결된 덩어리마다 부호 부피를 계산해 음수(안쪽을 향함)면 면 방향을 뒤집는다."""
    bm.faces.index_update()
    bm.faces.ensure_lookup_table()
    seen = set()
    flipped = 0
    for f0 in bm.faces:
        if f0.index in seen:
            continue
        comp = []
        stack = [f0]
        seen.add(f0.index)
        while stack:
            f = stack.pop()
            comp.append(f)
            for e in f.edges:
                for g in e.link_faces:
                    if g.index not in seen:
                        seen.add(g.index)
                        stack.append(g)
        vol = 0.0
        for f in comp:
            vs = [v.co for v in f.verts]
            for i in range(1, len(vs) - 1):
                vol += vs[0].dot(vs[i].cross(vs[i + 1]))
        if vol < 0:
            bmesh.ops.reverse_faces(bm, faces=comp)
            flipped += 1
    return flipped


def finalize(col, matcol, decimate=None, sharp_keys=("Rust", "Slag")):
    for key, c in matcol.items():
        m = bpy.data.materials.get("MK_" + key) or bpy.data.materials.new("MK_" + key)
        m.use_nodes = True
        bsdf = next(n for n in m.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
        bsdf.inputs["Base Color"].default_value = (c[0], c[1], c[2], 1)
        m.diffuse_color = (c[0], c[1], c[2], 1)
    tris = 0
    flips = 0
    for name, bm in list(PIECES.items()):
        if name.startswith("__"):
            bm.free(); continue
        bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.0005)
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
        flips += fix_components(bm)
        me = bpy.data.meshes.new(name)
        bm.to_mesh(me)
        bm.free()
        o = bpy.data.objects.new(name, me)
        col.objects.link(o)
        key = name.split("__")[1]
        me.materials.append(bpy.data.materials["MK_" + key])
        for p in me.polygons:
            p.use_smooth = True
        if key in sharp_keys:
            bm2 = bmesh.new(); bm2.from_mesh(me)
            for e in bm2.edges:
                if len(e.link_faces) == 2 and e.calc_face_angle(0) > math.radians(38):
                    e.smooth = False
            bm2.to_mesh(me); bm2.free()
        tris += sum(len(p.vertices) - 2 for p in me.polygons)
        if decimate:
            ratio = decimate.get(key, 1.0)
            if ratio >= 1.0 and len(me.polygons) > 500:
                ratio = decimate.get("_big", 1.0)
            if ratio < 1.0:
                md = o.modifiers.new("Decimate", 'DECIMATE'); md.ratio = ratio; md.use_collapse_triangulate = True
    PIECES.clear()
    dg = bpy.context.evaluated_depsgraph_get()
    tris2 = sum(sum(len(p.vertices) - 2 for p in o.evaluated_get(dg).data.polygons) for o in col.objects)
    return "pieces %d tris %d -> %d (flipped comps %d)" % (len(col.objects), tris, tris2, flips)


def rig_ref():
    ref = get_col("MK_RigRef")
    if ref.objects:
        return
    for n, (c, s) in RIG.items():
        me = bpy.data.meshes.new("REF_" + n)
        bm = bmesh.new(); bmesh.ops.create_cube(bm, size=1.0)
        for v in bm.verts:
            v.co = Vector((-(c[0] + v.co.x * s[0]), c[2] + v.co.z * s[2], c[1] + v.co.y * s[1]))
        bm.to_mesh(me); bm.free()
        o = bpy.data.objects.new("REF_" + n, me)
        ref.objects.link(o); o.display_type = 'WIRE'; o.hide_render = True


def render_setup():
    sc = bpy.context.scene
    try:
        sc.render.engine = 'CYCLES'
    except TypeError:
        pass
    sc.cycles.device = 'CPU'; sc.cycles.samples = 24; sc.cycles.use_denoising = True
    sc.render.resolution_x = 560; sc.render.resolution_y = 700; sc.render.resolution_percentage = 100
    w = bpy.data.worlds.get("World") or bpy.data.worlds.new("World")
    sc.world = w; w.use_nodes = True
    bg = next(n for n in w.node_tree.nodes if n.type == "BACKGROUND")
    bg.inputs[0].default_value = (0.35, 0.37, 0.40, 1); bg.inputs[1].default_value = 0.6
    for n, loc, e, s in (("MKP_Key", (3, -6, 3), 900, 4), ("MKP_Rim", (-4, 5, 4), 600, 3)):
        if not bpy.data.objects.get(n):
            ld = bpy.data.lights.new(n, 'AREA'); ld.energy = e; ld.size = s
            o = bpy.data.objects.new(n, ld); sc.collection.objects.link(o); o.location = loc
            o.rotation_euler = (Vector((0, 0, -0.5)) - Vector(loc)).to_track_quat('-Z', 'Y').to_euler()
    cam = bpy.data.objects.get("MKP_Cam")
    if cam is None:
        cam = bpy.data.objects.new("MKP_Cam", bpy.data.cameras.new("MKP_Cam")); sc.collection.objects.link(cam)
    cam.data.lens = 50
    sc.camera = cam
    return cam


def shot(fname, dirv, tgt=(-0.1, 0, -0.45), dist=11.5):
    sc = bpy.context.scene
    cam = render_setup()
    tgt = Vector(tgt)
    cam.location = tgt + Vector(dirv).normalized() * dist
    cam.rotation_euler = (tgt - cam.location).to_track_quat('-Z', 'Y').to_euler()
    sc.render.filepath = "D:\\god\\exports\\_preview\\" + fname + ".png"
    bpy.ops.render.render(write_still=True)


def uv_box(col, tiles):
    for o in col.objects:
        t = tiles.get(o.name.split("__")[1], 1.0)
        bm = bmesh.new(); bm.from_mesh(o.data)
        uv = bm.loops.layers.uv.verify()
        for f in bm.faces:
            n = f.normal
            if abs(n.x) >= abs(n.y) and abs(n.x) >= abs(n.z):
                ax = 0
            elif abs(n.y) >= abs(n.z):
                ax = 1
            else:
                ax = 2
            for l in f.loops:
                c = l.vert.co
                if ax == 0:
                    u = c.y * (1 if n.x > 0 else -1); v = c.z
                elif ax == 1:
                    u = c.x * (-1 if n.y > 0 else 1); v = c.z
                else:
                    u = c.x; v = c.y * (1 if n.z > 0 else -1)
                l[uv].uv = (u / t + 0.37 * ax, v / t + 0.21 * ax)
        bm.to_mesh(o.data); bm.free()


def export_fbx(col, path):
    for o in bpy.context.view_layer.objects:
        o.select_set(False)
    meshes = [o for o in col.objects if o.type == 'MESH']
    for o in meshes:
        o.hide_set(False); o.select_set(True)
    bpy.context.view_layer.objects.active = meshes[0]
    bpy.ops.export_scene.fbx(filepath=path, use_selection=True, object_types={"MESH"}, apply_unit_scale=True,
                             apply_scale_options="FBX_SCALE_ALL", axis_forward="-Z", axis_up="Y", bake_space_transform=False,
                             use_mesh_modifiers=True, use_triangles=True, mesh_smooth_type="FACE", add_leaf_bones=False, bake_anim=False)


def bbox_table(col):
    """Studio 배치용: 각 메쉬 바운딩 중심을 Roblox HRP 기준 (-x, z, y) 로."""
    dg = bpy.context.evaluated_depsgraph_get()
    out = []
    for o in col.objects:
        me = o.evaluated_get(dg).data
        xs = [v.co.x for v in me.vertices]; ys = [v.co.y for v in me.vertices]; zs = [v.co.z for v in me.vertices]
        c = ((min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2, (min(zs) + max(zs)) / 2)
        out.append('["%s"]={%.4f,%.4f,%.4f}' % (o.name, -c[0], c[2], c[1]))
    return ",\n".join(out)


def overlaps(col, pairs_skip=()):
    from mathutils.bvhtree import BVHTree
    dg = bpy.context.evaluated_depsgraph_get()
    objs = list(col.objects)
    T = {o.name: BVHTree.FromObject(o, dg) for o in objs}
    res = []
    for i in range(len(objs)):
        for j in range(i + 1, len(objs)):
            n = len(T[objs[i].name].overlap(T[objs[j].name]))
            if n:
                res.append((n, objs[i].name, objs[j].name))
    res.sort(reverse=True)
    return res
