# 마을 place 병원 앞 구급차 (Blender, exec → build_ambulances())
# Blender 좌표: 앞 = +X, 왼쪽 = +Y, 위 = +Z, 원점 = 바닥 중앙. 1 BU = 1 stud.
# Studio: 모델 로컬 (-x, z, y) → 앞이 Roblox -X.
# 부품 이름은 맵 차량 키트(ShopRoadKit.Car_Truck)와 같은 방식: <에셋>_<부품> (Paint/Stripe/Trim/Glass/Light/TailLight/
#   LightRed/LightBlue/Tire/Hub/Interior). 텍스처 없음, Studio 에서 색·재질을 이름으로 붙임.
# 변형: Ambulance_Open (뒷문·옆문 열림), Ambulance_Crashed (앞이 찌그러짐, 앞유리 깨짐, 왼쪽 앞바퀴 펑크, 문 닫힘)
import bpy, bmesh, math
from mathutils import Vector, Matrix, noise

COLS = {
    "Paint": (0.60, 0.59, 0.55), "Stripe": (0.45, 0.10, 0.08), "Trim": (0.03, 0.03, 0.035), "Glass": (0.03, 0.04, 0.045),
    "Light": (0.55, 0.55, 0.5), "TailLight": (0.25, 0.02, 0.02), "LightRed": (0.5, 0.03, 0.03), "LightBlue": (0.03, 0.08, 0.5),
    "Tire": (0.05, 0.05, 0.05), "Hub": (0.1, 0.1, 0.09), "Interior": (0.02, 0.02, 0.02),
}


class Kit:
    def __init__(self, asset):
        self.asset = asset
        self.bms = {}

    def bm(self, key):
        if key not in self.bms:
            self.bms[key] = bmesh.new()
        return self.bms[key]

    def box(self, key, x0, x1, y0, y1, z0, z1, M=None):
        bm = self.bm(key)
        cs = [Vector((x, y, z)) for z in (z0, z1) for y in (y0, y1) for x in (x0, x1)]
        if M is not None:
            cs = [M @ c for c in cs]
        v = [bm.verts.new(c) for c in cs]
        for q in ((0, 2, 3, 1), (4, 5, 7, 6), (0, 1, 5, 4), (2, 6, 7, 3), (0, 4, 6, 2), (1, 3, 7, 5)):
            bm.faces.new([v[i] for i in q])

    def prism(self, key, pts, y0, y1, M=None):
        """XZ 다각형(반시계) 을 Y 로 밀어냄."""
        bm = self.bm(key)
        a = [bm.verts.new(Vector((x, y0, z)) if M is None else M @ Vector((x, y0, z))) for x, z in pts]
        b = [bm.verts.new(Vector((x, y1, z)) if M is None else M @ Vector((x, y1, z))) for x, z in pts]
        bm.faces.new(a); bm.faces.new(list(reversed(b)))
        n = len(pts)
        for i in range(n):
            j = (i + 1) % n
            bm.faces.new([a[i], b[i], b[j], a[j]])

    def wheel(self, cx, cy, cz, r, w, seg=16, flat=0.0):
        """타이어(옆으로 누운 원통) + 허브."""
        for key, rr, ww, ofs in (("Tire", r, w, 0.0), ("Hub", r * 0.55, 0.12, w / 2 + 0.06)):
            bm = self.bm(key)
            s = 1 if cy > 0 else -1
            y0 = cy - w / 2 if key == "Tire" else cy + s * (w / 2)
            y1 = cy + w / 2 if key == "Tire" else cy + s * (w / 2 + 0.12)
            ra, rb = [], []
            for i in range(seg):
                ang = 2 * math.pi * i / seg
                x = cx + rr * math.cos(ang); z = cz + rr * math.sin(ang)
                if key == "Tire" and flat > 0:
                    z = max(z, cz - rr + flat)
                ra.append(bm.verts.new((x, y0, z))); rb.append(bm.verts.new((x, y1, z)))
            for i in range(seg):
                j = (i + 1) % seg
                bm.faces.new([ra[i], ra[j], rb[j], rb[i]])
            bm.faces.new(list(reversed(ra))); bm.faces.new(rb)

    def finish(self, col, deform=None):
        obs = []
        for key, bm in self.bms.items():
            if deform is not None:
                for v in bm.verts:
                    v.co = deform(v.co, key)
            bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
            name = self.asset + "_" + key
            me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
            ob = bpy.data.objects.new(name, me); col.objects.link(ob)
            m = bpy.data.materials.get("M_Amb_" + key) or bpy.data.materials.new("M_Amb_" + key)
            c = COLS[key]; m.diffuse_color = (c[0], c[1], c[2], 1)
            ob.data.materials.append(m)
            obs.append(ob)
        return obs


def rotz(deg, px, py):
    return Matrix.Translation((px, py, 0)) @ Matrix.Rotation(math.radians(deg), 4, 'Z') @ Matrix.Translation((-px, -py, 0))


def build(asset, open_doors=False, crashed=False):
    col = bpy.data.collections.get(asset)
    if col is None:
        col = bpy.data.collections.new(asset); bpy.context.scene.collection.children.link(col)
    for o in list(col.objects):
        bpy.data.objects.remove(o, do_unlink=True)
    K = Kit(asset)
    W2 = 4.8
    BX0, BX1, BZ0, BZ1 = -12.5, 4.3, 3.6, 11.6     # 환자칸 상자
    T = 0.25
    # ---- 환자칸 (속 빈 상자) ----
    K.box("Paint", BX0, BX1, -W2, W2, BZ0, BZ0 + T)                       # 바닥
    K.box("Paint", BX0, BX1, -W2, W2, BZ1 - T, BZ1)                       # 지붕
    K.box("Paint", BX0, BX1, W2 - T, W2, BZ0 + T, BZ1 - T)                # 왼쪽 벽
    DX0, DX1, DZ0, DZ1 = -1.0, 3.0, 4.0, 11.0                             # 오른쪽 옆문 구멍
    K.box("Paint", BX0, DX0, -W2, -W2 + T, BZ0 + T, BZ1 - T)
    K.box("Paint", DX1, BX1, -W2, -W2 + T, BZ0 + T, BZ1 - T)
    K.box("Paint", DX0, DX1, -W2, -W2 + T, BZ0 + T, DZ0)
    K.box("Paint", DX0, DX1, -W2, -W2 + T, DZ1, BZ1 - T)
    K.box("Paint", BX1 - T, BX1, -W2 + T, W2 - T, BZ0 + T, BZ1 - T)       # 앞 칸막이
    RY, RZ0, RZ1 = 4.3, 4.0, 11.0                                          # 뒷문 구멍
    K.box("Paint", BX0, BX0 + T, -W2 + T, W2 - T, RZ1, BZ1 - T)
    K.box("Paint", BX0, BX0 + T, -W2 + T, W2 - T, BZ0 + T, RZ0)
    K.box("Paint", BX0, BX0 + T, RY, W2 - T, RZ0, RZ1)
    K.box("Paint", BX0, BX0 + T, -W2 + T, -RY, RZ0, RZ1)
    # 줄무늬 (벽 바깥 0.04, 문 자리는 문에 따로)
    SZ0, SZ1 = 6.6, 7.6
    K.box("Stripe", BX0 + T, BX1, W2, W2 + 0.04, SZ0, SZ1)
    K.box("Stripe", BX0 + T, DX0, -W2 - 0.04, -W2, SZ0, SZ1)
    K.box("Stripe", DX1, BX1, -W2 - 0.04, -W2, SZ0, SZ1)
    K.box("Stripe", BX0 - 0.04, BX0, RY, W2, SZ0, SZ1)
    K.box("Stripe", BX0 - 0.04, BX0, -W2, -RY, SZ0, SZ1)
    # 상자 모서리 경광등 (앞·뒤 위 구석)
    for (x0, x1) in ((BX1 - 0.9, BX1 - 0.2), (BX0 + 0.2, BX0 + 0.9)):
        for s in (-1, 1):
            K.box("LightRed", x0, x1, s * (W2 - 0.9), s * (W2 - 0.2), BZ1, BZ1 + 0.4) if s > 0 else \
                K.box("LightRed", x0, x1, -(W2 - 0.2), -(W2 - 0.9), BZ1, BZ1 + 0.4)
    # 뒤 미등·번호판 자리
    for s in (-1, 1):
        a, b = sorted((s * 4.0, s * 4.6))
        K.box("TailLight", BX0 - 0.15, BX0, a, b, 4.2, 5.6)
    # 실내: 바닥 깔판, 왼쪽 수납장, 들것
    K.box("Interior", BX0 + T, BX1 - T, -W2 + T, W2 - T, BZ0 + T, BZ0 + T + 0.08)
    K.box("Interior", -10.5, 3.6, W2 - T - 1.3, W2 - T, 6.0, 10.8)
    K.box("Trim", -10.0, -2.0, -1.6, 1.0, BZ0 + T + 0.08, BZ0 + 1.6)       # 들것 틀
    K.box("Paint", -10.0, -2.0, -1.5, 0.9, BZ0 + 1.6, BZ0 + 2.0)          # 매트
    # ---- 운전석 (아치 깎인 옆 모양을 Y 로 밀어냄) ----
    arch = []
    cxw, czw, rr = 8.5, 1.7, 2.0
    for i in range(9):
        ang = math.pi - math.pi * i / 8.0
        x = cxw + rr * math.cos(ang); z = czw + rr * math.sin(ang)
        if z >= 2.2:
            arch.append((x, z))
    prof = [(4.5, 2.2), (6.56, 2.2)] + arch + [(10.44, 2.2), (13.0, 2.2), (13.2, 4.9), (12.7, 5.7), (9.9, 6.1),
                                               (8.7, 9.2), (4.5, 9.2)]
    K.prism("Paint", prof, -4.4, 4.4)
    # 앞유리·옆창 (면에서 0.03 띄움)
    a, b = Vector((9.85, 0, 6.25)), Vector((8.8, 0, 9.0))
    n = Vector((3.1, 0, 1.2)).normalized() * 0.04
    K.prism("Glass", [(a.x + n.x, a.z + n.z), (a.x + n.x + 0.05, a.z + n.z - 0.05), (b.x + n.x + 0.05, b.z + n.z - 0.05), (b.x + n.x, b.z + n.z)], -3.9, 3.9)
    for s in (-1, 1):
        y0, y1 = sorted((s * 4.4, s * 4.44))
        K.prism("Glass", [(5.2, 6.4), (9.3, 6.4), (8.45, 8.7), (5.2, 8.7)], y0, y1)
        y0, y1 = sorted((s * 4.4, s * 4.45))
        K.box("Trim", 4.5, 4.62, y0, y1, 2.4, 9.0)                        # 문 틈
        K.box("Trim", 7.35, 7.45, y0, y1, 2.4, 6.3)
        K.box("Trim", 5.3, 6.1, y0 + s * 0.05, y1 + s * 0.05, 5.6, 5.8)  # 손잡이
        a2, b2 = sorted((s * 4.45, s * 5.3))
        K.box("Trim", 9.0, 9.25, a2, b2, 7.0, 7.2)                        # 거울 팔
        a3, b3 = sorted((s * 5.3, s * 5.45))
        K.box("Trim", 8.8, 9.45, a3, b3, 6.3, 7.8)                        # 거울
    # 범퍼·그릴·전조등
    K.box("Trim", 13.0, 13.8, -4.5, 4.5, 2.0, 3.2)
    K.box("Trim", 13.15, 13.35, -2.6, 2.6, 3.4, 4.8)
    for s in (-1, 1):
        a, b = sorted((s * 3.0, s * 4.1))
        K.box("Light", 13.12, 13.4, a, b, 3.6, 4.6)
    # 지붕 경광등 바
    K.box("Trim", 5.4, 8.0, -3.6, 3.6, 9.2, 9.5)
    K.box("LightRed", 6.0, 7.4, 0.2, 3.4, 9.5, 10.0)
    K.box("LightBlue", 6.0, 7.4, -3.4, -0.2, 9.5, 10.0)
    # 차대·옆 스커트·뒤 발판
    K.box("Trim", -11.0, 4.5, -2.6, 2.6, 2.0, BZ0)
    for s in (-1, 1):
        a, b = sorted((s * 4.2, s * 4.6))
        K.box("Trim", -4.4, 4.2, a, b, 2.6, BZ0)
    K.box("Trim", BX0 - 0.9, BX0, -4.2, 4.2, 2.7, 3.4)
    # ---- 바퀴 ----
    for (x, y, flat) in ((8.5, 4.1, 0.0), (8.5, -4.1, 0.0), (-6.5, 4.1, 0.0), (-6.5, -4.1, 0.0)):
        if crashed and x > 0 and y > 0:
            flat = 0.55
        K.wheel(x, y, 1.7, 1.7, 1.2, flat=flat)
    # ---- 문 ----
    def rear_leaf(sign, M):
        y0, y1 = (0.03, RY) if sign > 0 else (-RY, -0.03)
        K.box("Paint", BX0 - 0.25, BX0, y0, y1, RZ0, RZ1, M)
        ys0, ys1 = (y0 + 0.9, y1 - 0.6) if sign > 0 else (y0 + 0.6, y1 - 0.9)
        K.box("Glass", BX0 - 0.29, BX0 - 0.25, ys0, ys1, 8.0, 10.2, M)
        K.box("Stripe", BX0 - 0.29, BX0 - 0.25, y0, y1, SZ0, SZ1, M)
        hy0, hy1 = (0.5, 1.4) if sign > 0 else (-1.4, -0.5)
        K.box("Trim", BX0 - 0.4, BX0 - 0.25, hy0, hy1, 6.0, 6.25, M)
    def side_door(M):
        K.box("Paint", DX0, DX1, -W2 - 0.25, -W2, DZ0, DZ1, M)
        K.box("Glass", DX0 + 0.6, DX1 - 0.6, -W2 - 0.29, -W2 - 0.25, 8.2, 10.2, M)
        K.box("Stripe", DX0, DX1, -W2 - 0.29, -W2 - 0.25, SZ0, SZ1, M)
        K.box("Trim", DX0 + 0.3, DX0 + 1.2, -W2 - 0.4, -W2 - 0.29, 6.0, 6.25, M)
    if open_doors:
        rear_leaf(1, rotz(-100, BX0 - 0.25, RY + 0.25))
        rear_leaf(-1, rotz(100, BX0 - 0.25, -RY - 0.25))
        side_door(rotz(80, DX1 + 0.05, -W2 - 0.3))
    else:
        rear_leaf(1, None); rear_leaf(-1, None); side_door(None)

    deform = None
    if crashed:
        def deform(c, key):
            if c.x > 9.0:
                k = (c.x - 9.0)
                side = 1.0 + 0.7 * (c.y / 4.5)
                n1 = noise.noise(Vector((c.x * 0.7, c.y * 0.7, c.z * 0.7)))
                return Vector((c.x - k * 0.33 * side + 0.15 * n1 * k, c.y + 0.05 * n1 * k, c.z - k * 0.07 * side + 0.12 * n1))
            return c
    obs = K.finish(col, deform)
    tris = sum(sum(len(p.vertices) - 2 for p in o.data.polygons) for o in obs)
    return "%s: %d objects, %d tris" % (asset, len(obs), tris)


def build_ambulances():
    return build("Ambulance_Open", open_doors=True) + "\n" + build("Ambulance_Crashed", crashed=True)
