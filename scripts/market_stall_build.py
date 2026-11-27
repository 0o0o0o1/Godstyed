# 마을 컨테이너 시장 골목 — 노점 컨테이너 5종 (Blender, exec(open(...).read()) 로 실행)
# 1 BU = 1 stud. 원점 = 바닥 중앙. 긴 쪽 = X, 문 달린 끝 = +X, 노점 열린 옆면 = -Y.
# Studio 로 들어가면 Blender (x, y, z) -> 모델 로컬 (-x, z, y)  → 열린 옆면은 Roblox -Z.
# 부품 이름: <에셋접두사>_<부품>__<팔레트키>[__NoCollide][__TEX]
#   몸체(__TEX) = StallSteel 타일 텍스처(UV u = 길이/24, v = 높이/12), 셔터 = WhSiding(ShutterOrange) 재사용.
import bpy, bmesh, math
from mathutils import Vector, Matrix, noise

TU, TV = 24.0, 12.0
H = 12.0

PREVIEW = {
    "RustRed": (120, 55, 40), "FadedBlue": (55, 80, 100), "Olive": (85, 90, 60), "DirtyWhite": (170, 165, 150),
    "DarkSteel": (60, 60, 62), "SteelOxide": (104, 52, 38), "Wood": (110, 85, 60), "Canvas": (90, 85, 65),
    "ShutterOrange": (158, 98, 50),
}


def _lin(c):
    c = c / 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def pmat(key):
    name = "M_" + key
    m = bpy.data.materials.get(name)
    if m is None:
        m = bpy.data.materials.new(name); m.use_nodes = True
    rgb = PREVIEW[key]
    col = tuple(_lin(v) for v in rgb) + (1.0,)
    b = next((n for n in m.node_tree.nodes if n.type == "BSDF_PRINCIPLED"), None)
    if b:
        b.inputs["Base Color"].default_value = col
        b.inputs["Roughness"].default_value = 0.8
    m.diffuse_color = col
    return m


def collection(name):
    col = bpy.data.collections.get(name)
    if col is None:
        col = bpy.data.collections.new(name); bpy.context.scene.collection.children.link(col)
    for o in list(col.objects):
        bpy.data.objects.remove(o, do_unlink=True)
    return col


class Part:
    """bmesh 하나 = Blender 오브젝트 하나 (머티리얼 하나)."""
    def __init__(self, name, key):
        self.name, self.key = name, key
        self.bm = bmesh.new()
        self.uv = self.bm.loops.layers.uv.new("UVMap")

    def face(self, vs, uvs):
        f = self.bm.faces.new(vs)
        for lp, t in zip(f.loops, uvs):
            lp[self.uv].uv = t
        return f

    def finish(self, col, closed=True):
        bm = self.bm
        if closed:
            bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
        me = bpy.data.meshes.new(self.name)
        bm.to_mesh(me); bm.free()
        ob = bpy.data.objects.new(self.name, me)
        col.objects.link(ob)
        ob.data.materials.append(pmat(self.key))
        return ob


def box_uv(p, n, uoff):
    ax = max(range(3), key=lambda i: abs(n[i]))
    if ax == 0:
        return (p.y / TU + uoff, p.z / TV)
    if ax == 1:
        return (p.x / TU + uoff, p.z / TV)
    return (p.x / TU + uoff, 0.62 + p.y / 40.0)


def box(P, x0, x1, y0, y1, z0, z1, uoff=0.0):
    bm = P.bm
    c = [Vector((x, y, z)) for z in (z0, z1) for y in (y0, y1) for x in (x0, x1)]
    v = [bm.verts.new(q) for q in c]
    quads = [((0, 2, 3, 1), (0, 0, -1)), ((4, 5, 7, 6), (0, 0, 1)), ((0, 1, 5, 4), (0, -1, 0)),
             ((2, 6, 7, 3), (0, 1, 0)), ((0, 4, 6, 2), (-1, 0, 0)), ((1, 3, 7, 5), (1, 0, 0))]
    for idx, n in quads:
        vs = [v[i] for i in idx]
        P.face(vs, [box_uv(q.co, n, uoff) for q in vs])


def tube(P, a, b, r, seg=8, uoff=0.0):
    bm = P.bm
    a, b = Vector(a), Vector(b)
    d = (b - a).normalized()
    t = d.cross(Vector((0, 0, 1)))
    if t.length < 1e-3:
        t = d.cross(Vector((1, 0, 0)))
    t.normalize(); s = d.cross(t)
    ra, rb = [], []
    for i in range(seg):
        ang = 2 * math.pi * i / seg
        o = (t * math.cos(ang) + s * math.sin(ang)) * r
        ra.append(bm.verts.new(a + o)); rb.append(bm.verts.new(b + o))
    L = (b - a).length
    for i in range(seg):
        j = (i + 1) % seg
        P.face([ra[i], ra[j], rb[j], rb[i]], [(i / seg, 0), ((i + 1) / seg, 0), ((i + 1) / seg, L / TV), (i / seg, L / TV)])
    P.face(list(reversed(ra)), [(0.5, 0.5)] * seg)
    P.face(rb, [(0.5, 0.5)] * seg)


def profile(a0, a1, pitch, depth):
    """골판 단면: (a, o) 점 목록. o = 0 마루, -depth 골."""
    pat = [(0.0, 0.0), (0.33, 0.0), (0.5, -depth), (0.83, -depth)]
    pts = []
    k = math.floor(a0 / pitch) - 1
    while True:
        for f, o in pat:
            pts.append((k * pitch + f * pitch, o))
        k += 1
        if k * pitch > a1 + pitch:
            break
    def o_at(a):
        for i in range(len(pts) - 1):
            if pts[i][0] <= a <= pts[i + 1][0]:
                t = (a - pts[i][0]) / max(1e-9, pts[i + 1][0] - pts[i][0])
                return pts[i][1] + (pts[i + 1][1] - pts[i][1]) * t
        return 0.0
    out = [(a0, o_at(a0))] + [p for p in pts if a0 + 1e-4 < p[0] < a1 - 1e-4] + [(a1, o_at(a1))]
    return out


def sheet(P, a0, a1, h0, h1, mapf, depth=0.25, thick=0.08, pitch=2.0, dent=0.0, seed=0.0, uvf=None, nh=8, xf=None,
          caps=(True, True, True, True)):
    """골판 철판(두께 있는 닫힌 판). mapf(a, h, o) -> Vector. o 는 바깥(+)쪽 오프셋."""
    prof = profile(a0, a1, pitch, depth)
    hs = [h0 + (h1 - h0) * i / nh for i in range(nh + 1)]
    bm = P.bm

    def dz(a, h):
        if dent == 0.0:
            return 0.0
        w = math.sin(math.pi * (a - a0) / (a1 - a0)) * math.sin(math.pi * (h - h0) / (h1 - h0))
        n = noise.noise(Vector((a * 0.18 + seed, h * 0.22, seed * 0.7)))
        n2 = noise.noise(Vector((a * 0.6 + seed * 3, h * 0.5, 4.0)))
        return dent * w * (0.75 * n + 0.25 * n2)

    def mk(a, h, o):
        q = mapf(a, h, o + dz(a, h))
        return xf @ q if xf is not None else q

    outer = [[bm.verts.new(mk(a, h, o)) for (a, o) in prof] for h in hs]
    inner = [[bm.verts.new(mk(a, h, o - thick)) for (a, o) in prof] for h in hs]
    uvf = uvf or (lambda a, h: (a / TU, h / TV))
    na = len(prof)
    for j in range(nh):
        for i in range(na - 1):
            a_, b_ = prof[i][0], prof[i + 1][0]
            uv = [uvf(a_, hs[j]), uvf(b_, hs[j]), uvf(b_, hs[j + 1]), uvf(a_, hs[j + 1])]
            P.face([outer[j][i], outer[j][i + 1], outer[j + 1][i + 1], outer[j + 1][i]], uv)
            P.face([inner[j + 1][i], inner[j + 1][i + 1], inner[j][i + 1], inner[j][i]], [uv[3], uv[2], uv[1], uv[0]])
    # caps: 0 = h0 (bottom), 1 = h1 (top), 2 = a0, 3 = a1
    for ci, j in ((0, 0), (1, nh)):
        if caps[ci]:
            for i in range(na - 1):
                a_, b_ = prof[i][0], prof[i + 1][0]
                P.face([outer[j][i], inner[j][i], inner[j][i + 1], outer[j][i + 1]],
                       [uvf(a_, hs[j]), uvf(a_, hs[j] + 0.1), uvf(b_, hs[j] + 0.1), uvf(b_, hs[j])])
    for ci, i in ((2, 0), (3, na - 1)):
        if caps[ci]:
            for j in range(nh):
                a_ = prof[i][0]
                P.face([outer[j][i], outer[j + 1][i], inner[j + 1][i], inner[j][i]],
                       [uvf(a_, hs[j]), uvf(a_, hs[j + 1]), uvf(a_ + 0.1, hs[j + 1]), uvf(a_ + 0.1, hs[j])])


def build_stall(prefix, L, O, kind, gap=0.0, color="RustRed", uoff=0.0, seed=1.0):
    """kind: flap / canvas / shutter / shutter_bent.  O = 옆면 개구부 반길이."""
    col = collection(prefix)
    L2, W2 = L / 2.0, 6.0
    TEX = "__" + color + "__TEX"
    obs = []
    uvw = (lambda a, h: (a / TU + uoff, h / TV))

    # ---- 프레임 (모서리 기둥·주물·레일) ----
    F = Part(prefix + "_Frame" + "__" + color + "__NoCollide__TEX", color)
    for sx in (-1, 1):
        for sy in (-1, 1):
            xa, xb = sorted((sx * (L2 - 0.9), sx * L2)); ya, yb = sorted((sy * (W2 - 0.9), sy * W2))
            box(F, xa, xb, ya, yb, 0.0, 0.9, uoff); box(F, xa, xb, ya, yb, H - 0.9, H, uoff)
            xa, xb = sorted((sx * (L2 - 0.7), sx * L2)); ya, yb = sorted((sy * (W2 - 0.7), sy * W2))
            box(F, xa, xb, ya, yb, 0.9, H - 0.9, uoff)
    for sy in (-1, 1):
        ya, yb = sorted((sy * (W2 - 0.5), sy * W2))
        box(F, -L2 + 0.9, L2 - 0.9, ya, yb, 0.1, 0.9, uoff)
        box(F, -L2 + 0.9, L2 - 0.9, ya, yb, H - 0.9, H, uoff)
    for sx in (-1, 1):
        xa, xb = sorted((sx * (L2 - 0.5), sx * L2))
        box(F, xa, xb, -W2 + 0.9, W2 - 0.9, 0.1, 0.9, uoff)
        xa, xb = sorted((sx * (L2 - 0.9), sx * L2))
        box(F, xa, xb, -W2 + 0.9, W2 - 0.9, H - 0.9, H, uoff)
    obs.append(F.finish(col))

    # ---- 뒷벽 (+Y), 양 끝벽 ----
    B = Part(prefix + "_Back" + TEX, color)
    sheet(B, -L2 + 0.7, L2 - 0.7, 0.9, H - 0.9, lambda a, h, o: Vector((a, W2 - 0.1 + o, h)), dent=0.22, seed=seed, uvf=uvw, nh=3)
    obs.append(B.finish(col))
    for sx, nm in ((-1, "EndW"), (1, "EndDoor")):
        E = Part(prefix + "_" + nm + TEX, color)
        sheet(E, -W2 + 0.7, W2 - 0.7, 0.9, H - 0.9, (lambda s: (lambda a, h, o: Vector((s * (L2 - 0.1 + o), a, h))))(sx),
              dent=(0.15 if sx < 0 else 0.0), seed=seed + 5 * sx, uvf=(lambda a, h: (a / TU + uoff + 0.3, h / TV)), pitch=2.0, nh=3)
        obs.append(E.finish(col))

    # 문 쪽 철물 (잠금 막대 4개, 받침, 손잡이, 문 틈)
    HW = Part(prefix + "_DoorHW__DarkSteel__NoCollide", "DarkSteel")
    xr = L2 + 0.05
    for yy in (-4.2, -1.5, 1.5, 4.2):
        tube(HW, (xr, yy, 1.2), (xr, yy, H - 1.2), 0.13, 8)
        for zz in (1.6, 6.0, H - 1.6):
            box(HW, L2 - 0.1, xr, yy - 0.25, yy + 0.25, zz - 0.2, zz + 0.2)
        box(HW, xr, xr + 0.12, yy - 0.08, yy + (0.9 if yy < 0 else -0.9), 4.4, 4.7)
    box(HW, L2 - 0.1, L2 + 0.02, -0.06, 0.06, 0.9, H - 0.9)
    obs.append(HW.finish(col))

    # ---- 바닥 판자 ----
    FL = Part(prefix + "_Floor__Wood", "Wood")
    y = -W2 + 0.5; i = 0
    while y < W2 - 0.5 - 1e-3:
        y1 = min(W2 - 0.5, y + 0.95)
        edge = (y < -W2 + 0.7) or (y1 > W2 - 0.7)
        xl = L2 - (0.7 if edge else 0.45)
        zt = 1.15 - (0.04 if i % 3 == 1 else 0.0)
        box(FL, -xl, xl, y, y1 - 0.04, 0.9, zt)
        y = y1; i += 1
    obs.append(FL.finish(col))

    # ---- 지붕 ----
    R = Part(prefix + "_Roof" + TEX, color)
    sheet(R, -L2 + 0.9, L2 - 0.9, -W2 + 0.5, W2 - 0.5, lambda a, h, o: Vector((a, h, 11.8 + o)), depth=0.06, thick=0.2,
          pitch=4.0, dent=0.12, seed=seed + 9, uvf=(lambda a, h: (a / TU + uoff, 0.62 + h / 40.0)), nh=3)
    obs.append(R.finish(col))

    # ---- 열린 옆면 (-Y) ----
    side = lambda a, h, o: Vector((a, -(W2 - 0.1 + o), h))
    for nm, a0, a1 in (("SideW", -L2 + 0.7, -O - 0.4), ("SideE", O + 0.4, L2 - 0.7)):
        S = Part(prefix + "_" + nm + TEX, color)
        sheet(S, a0, a1, 0.9, H - 0.9, side, dent=0.12, seed=seed + a0, uvf=uvw, nh=3)
        obs.append(S.finish(col))
    J = Part(prefix + "_Jambs" + "__" + color + "__NoCollide__TEX", color)
    for s in (-1, 1):
        xa, xb = sorted((s * O, s * (O + 0.4)))
        box(J, xa, xb, -W2 + 0.05, -W2 + 0.5, 0.9, H - 0.9, uoff)
    obs.append(J.finish(col))

    if kind == "flap":
        zc = 3.8
        C = Part(prefix + "_Counter" + TEX, color)
        sheet(C, -O + gap, O, 0.9, zc, side, dent=0.08, seed=seed + 2, uvf=uvw, nh=1)
        box(C, -O + gap, O, -W2 - 0.3, -W2 + 0.8, zc, zc + 0.2, uoff)
        obs.append(C.finish(col))
        # 위로 들어 올린 옆판 (윗 레일 아래 경첩, -110° 회전)
        piv_y, piv_z = -(W2 - 0.1) - 0.15, H - 0.95
        ang = math.radians(-110)
        xf = Matrix.Translation((0, piv_y, piv_z)) @ Matrix.Rotation(ang, 4, 'X') @ Matrix.Translation((0, -piv_y, -piv_z))
        FP = Part(prefix + "_Flap" + "__" + color + "__NoCollide__TEX", color)
        sheet(FP, -O + 0.05, O - 0.05, zc + 0.2, H - 1.05, side, dent=0.10, seed=seed + 7, uvf=uvw, nh=3, xf=xf)
        obs.append(FP.finish(col))
        # 받침대 2개: 카운터 위 → 옆판 아랫면(골 안쪽 면) 가까이
        ST = Part(prefix + "_Struts__SteelOxide__NoCollide", "SteelOxide")
        tip = xf @ Vector((0, -(W2 - 0.1 - 0.25 - 0.08) + 0.28, zc + 0.2 + 1.4))
        for xx in (-O + gap + 3.0, O - 3.0):
            tube(ST, (xx, -W2 + 0.25, zc + 0.32), (xx, tip.y, tip.z), 0.17, 8)
        obs.append(ST.finish(col))
    elif kind == "canvas":
        # 찢긴 방수포 차양: 윗 레일 바깥 → 골목 쪽 기둥 2개
        CV = Part(prefix + "_Canvas__Canvas__NoCollide", "Canvas")
        bm = CV.bm
        nx, ns = 28, 9
        xa, xb = -O - 0.6, O + 0.6
        ys, zs, ye, ze = -W2 - 0.06, H - 0.95, -W2 - 5.6, 8.9
        grid = {}
        for i in range(nx + 1):
            x = xa + (xb - xa) * i / nx
            xn = i / nx
            tear = 0.80 + 0.2 * (0.5 + 0.5 * noise.noise(Vector((x * 0.35, 3.1, seed))))
            for j in range(ns + 1):
                s = j / ns
                if s > tear + 0.06:
                    continue
                s2 = min(s, tear)
                yy = ys + (ye - ys) * s2
                zz = zs + (ze - zs) * s2 - 0.9 * math.sin(math.pi * xn) * math.sin(math.pi * 0.5 * s2) \
                    + 0.18 * noise.noise(Vector((x * 0.5, s2 * 3, seed + 2)))
                grid[(i, j)] = Vector((x, yy, zz))
        holes = set()
        for i in range(nx):
            for j in range(ns):
                if noise.noise(Vector((i * 0.45 + seed, j * 0.55, 7.0))) > 0.42:
                    holes.add((i, j))
        top, bot = {}, {}
        for k, p in grid.items():
            top[k] = bm.verts.new(p)
            bot[k] = bm.verts.new(p - Vector((0, 0, 0.035)))
        for i in range(nx):
            for j in range(ns):
                ks = [(i, j), (i + 1, j), (i + 1, j + 1), (i, j + 1)]
                if any(k not in grid for k in ks) or (i, j) in holes:
                    continue
                uvs = [(k[0] / nx * 3, k[1] / ns) for k in ks]
                CV.face([top[k] for k in ks][::-1], uvs[::-1])
                CV.face([bot[k] for k in ks], uvs)
        ob = CV.finish(col, closed=False)
        obs.append(ob)
        for nm, xx in (("PoleW", -O + 1.0), ("PoleE", O - 1.0)):
            ip = round((xx - xa) / (xb - xa) * nx)
            jl = max(j for (i_, j) in grid if i_ == ip)
            pz = grid[(ip, jl)]
            PL = Part(prefix + "_" + nm + "__SteelOxide", "SteelOxide")
            tube(PL, (xx, pz.y, 0.0), (xx, pz.y, pz.z - 0.06), 0.22, 8)
            obs.append(PL.finish(col))
    else:
        # 말림 셔터: 위 셔터 상자 + 양옆 가이드 + 가로 골 셔터판 (WhSiding ShutterOrange 텍스처)
        SB = Part(prefix + "_ShutterBox__DarkSteel__NoCollide", "DarkSteel")
        box(SB, -O, O, -W2 - 0.45, -W2 + 0.55, H - 2.1, H - 0.9)
        for s in (-1, 1):
            xa, xb = sorted((s * (O - 0.45), s * O))
            box(SB, xa, xb, -W2 - 0.25, -W2 + 0.5, 0.9, H - 2.1)
        obs.append(SB.finish(col))
        ush = (lambda a, h: (a / 9.6, (h + 15.0) / 30.0))
        sh_map = lambda a, h, o: Vector((h, -(W2 - 0.25 + o), a))
        bent = (kind == "shutter_bent")

        def bulge_map(a, h, o):
            q = sh_map(a, h, o)
            if bent:
                t = min(1.0, max(0.0, (a - 1.3) / 1.3)) if a < 2.6 else max(0.0, 1.0 - (a - 2.6) / 2.4)
                w = max(0.0, 1.0 - abs(h + 3.5) / 5.0)
                q.y += 1.6 * (t * t) * w * (0.8 + 0.2 * math.sin(h * 2.3))
            return q
        if bent:
            for nm, h0, h1, a0 in (("ShutterA", -O + 0.45, -2.2, 2.6), ("ShutterB", -2.2, O - 0.45, 0.9)):
                SH = Part("WhSiding_" + prefix + nm + "__ShutterOrange__TEX", "ShutterOrange")
                sheet(SH, a0, H - 2.1, h0, h1, bulge_map, depth=0.14, thick=0.05, pitch=0.6, uvf=ush, nh=5)
                obs.append(SH.finish(col))
        else:
            SH = Part("WhSiding_" + prefix + "Shutter__ShutterOrange__TEX", "ShutterOrange")
            sheet(SH, 0.9, H - 2.1, -O + 0.45, O - 0.45, sh_map, depth=0.14, thick=0.05, pitch=0.6, uvf=ush, nh=1)
            obs.append(SH.finish(col))
        LK = Part(prefix + "_Lock__DarkSteel__NoCollide", "DarkSteel")
        box(LK, (-2.2 if bent else -O + 0.45), O - 0.45, -W2 - 0.12, -W2 + 0.1, 0.9, 1.4)  # 아래 막대 (찌그러진 쪽은 끊김)
        box(LK, 2.0, 2.6, -W2 - 0.4, -W2 - 0.12, 0.95, 1.6)           # 자물쇠 고리 받침
        box(LK, 1.95, 2.65, -W2 - 0.55, -W2 - 0.4, 0.55, 1.15)          # 자물쇠
        obs.append(LK.finish(col))
    return obs


STALLS = [
    ("Stall40F", 48, 18.0, "flap", 8.0, "RustRed", 0.00, 1.0),
    ("Stall40C", 48, 18.0, "canvas", 0.0, "FadedBlue", 0.37, 2.0),
    ("Stall20F", 24, 8.0, "flap", 6.0, "Olive", 0.61, 3.0),
    ("Stall20S", 24, 8.0, "shutter", 0.0, "DirtyWhite", 0.18, 4.0),
    ("Stall20B", 24, 8.0, "shutter_bent", 0.0, "RustRed", 0.83, 5.0),
]


def build_all(offset=30.0):
    out = []
    for k, (pre, L, O, kind, gap, colr, uoff, seed) in enumerate(STALLS):
        obs = build_stall(pre, L, O, kind, gap, colr, uoff, seed)
        # 미리보기용으로 Y 방향으로 띄워 놓음 (오브젝트 위치는 0 에 두고 컬렉션 인스턴스 대신 location 만 옮겼다가 내보낼 때 되돌림)
        out.append("%s: %d objects" % (pre, len(obs)))
    return "\n".join(out)
