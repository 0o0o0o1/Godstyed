# 도약 찌르기: 빛의 창 v2 (사용자 참고 이미지 느낌: 기계식 검은 창 + 빛나는 결정 날 3개)
# 창날 쪽이 아래(z=0 이 가운데 결정 날 끝), 위로 갈수록 기계 척추 → 열린 틀 → 가는 검은 자루 → 꼬리(캡슐 틀 + 검은 화살촉).
# 오브젝트 두 개: LanceMetal (검은 금속, 꼭짓점 값 Glow = 빛나는 줄·코어) / LanceCrystal (결정 날).
# 1 단위 = 1 스터드. 실행: exec(open(r"D:\god\scripts\vfx_leap_lance2.py", encoding="utf-8").read())
import bpy, bmesh, math, random
from mathutils import Vector, Matrix

random.seed(5)
SCENE = "VFX_LeapLance2"
if SCENE in bpy.data.scenes:
    bpy.data.scenes.remove(bpy.data.scenes[SCENE])
for o in [o for o in bpy.data.objects if o.name.startswith(("LanceMetal", "LanceCrystal"))]:
    bpy.data.objects.remove(o)
sc = bpy.data.scenes.new(SCENE)
bpy.context.window.scene = sc

parts = {"metal": [], "crystal": []}  # (bmesh 조각, 발광값)


class Piece:
    def __init__(self, kind, glow=0.0):
        self.bm = bmesh.new()
        self.glow = glow
        parts[kind].append(self)

    def loft(self, rings, cap0=True, cap1=True):
        vs = [[self.bm.verts.new(p) for p in r] for r in rings]
        n = len(rings[0])
        for a, b in zip(vs, vs[1:]):
            for k in range(n):
                self.bm.faces.new((a[k], a[(k + 1) % n], b[(k + 1) % n], b[k]))
        if cap0:
            self.bm.faces.new(list(reversed(vs[0])))
        if cap1:
            self.bm.faces.new(vs[-1])
        return vs

    def cone_tip(self, ring, tip):
        t = self.bm.verts.new(tip)
        vs = [self.bm.verts.new(p) for p in ring]
        n = len(vs)
        for k in range(n):
            self.bm.faces.new((t, vs[(k + 1) % n], vs[k]))
        return vs, t

    def transform(self, mat):
        bmesh.ops.transform(self.bm, matrix=mat, verts=self.bm.verts)


def ring_circle(z, r, n=12, cx=0.0, cy=0.0, rot=0.0, sx=1.0, sy=1.0):
    return [Vector((cx + math.cos(rot + k / n * math.tau) * r * sx, cy + math.sin(rot + k / n * math.tau) * r * sy, z)) for k in range(n)]


def tube_path(piece, pts, r, n=8, r_end=None):
    """점 목록을 따라 가는 관 (끝 뚜껑 포함)"""
    rings = []
    for i, p in enumerate(pts):
        d = (pts[min(i + 1, len(pts) - 1)] - pts[max(i - 1, 0)]).normalized()
        up = Vector((0, 0, 1)) if abs(d.z) < 0.95 else Vector((1, 0, 0))
        u = d.cross(up).normalized()
        v = d.cross(u).normalized()
        rr = r if r_end is None else r + (r_end - r) * i / (len(pts) - 1)
        rings.append([p + (u * math.cos(k / n * math.tau) + v * math.sin(k / n * math.tau)) * rr for k in range(n)])
    piece.loft(rings)


# ---------- 결정 날 3개 ----------
def crystal_blade(length, width, thick, lean_deg, x_off, z_base, twist=0.0):
    pc = Piece("crystal")
    # 단면 6점 (한쪽 날이 더 날카로운 납작한 결정)
    def sec(z, w, t):
        pts = [(w, 0), (0.35 * w, t), (-0.55 * w, t * 0.85), (-0.95 * w, 0), (-0.55 * w, -t * 0.85), (0.35 * w, -t)]
        return [Vector((x, y, z)) for x, y in pts]
    # 참고 이미지: 긴 결정 조각 — 끝 가까이(25%)에서 가장 넓고 뿌리 쪽으로 천천히 좁아짐, 끝은 한쪽 날로 비스듬히 깎임(끌 모양)
    prof = [(0.06, 0.45, 0.35), (0.25, 1.0, 0.8), (0.5, 0.92, 1.0), (0.75, 0.76, 0.9), (1.0, 0.55, 0.7)]
    rings = [sec(f * length, w * width, t * thick) for f, w, t in prof]
    tipv = pc.bm.verts.new((0.85 * width, 0, -0.02 * length))
    vs = pc.loft(rings, cap0=False, cap1=True)
    for k in range(6):
        pc.bm.faces.new((tipv, vs[0][(k + 1) % 6], vs[0][k]))
    m = Matrix.Translation((x_off, 0, z_base)) @ Matrix.Rotation(math.radians(lean_deg), 4, "Y") @ Matrix.Rotation(twist, 4, "Z")
    pc.transform(m)
    return pc


# 뿌리에서 날을 놓는 함수: 날 끝 = 뿌리에서 아래(-z)로 length, lean 만큼 옆으로
def fan_blade(length, width, thick, lean_deg, root_x, root_z, twist=0.0):
    a = math.radians(lean_deg)
    tip_x = root_x - math.sin(a) * length
    tip_z = root_z - math.cos(a) * length
    return crystal_blade(length, width, thick, lean_deg, tip_x, tip_z, twist)


# ---- 참고 이미지 그대로: 긴 왼쪽 결정 / 짧은 오른쪽 결정 / 가운데 검은 금속 창끝 (거의 평행, 살짝만 벌어짐) ----
fan_blade(10.0, 0.72, 0.28, 7.0, -0.42, 9.6, 0.15)   # 왼쪽 큰 결정 (가장 김, 맨 앞까지)
fan_blade(7.2, 0.55, 0.24, -4.0, 0.5, 9.2, -0.15)    # 오른쪽 결정 (짧음)
# 가운데 검은 금속 창끝: 가늘고 긴 마름모, 가운데 빛나는 줄
pc = Piece("metal")
spike = [(0.0, 0.0, 0.0), (0.6, 0.12, 0.07), (2.0, 0.2, 0.1), (5.0, 0.22, 0.12), (8.6, 0.25, 0.14)]
rings = [[Vector((x * w + 0.05, y * t, z)) for x, y in [(1, 0), (0, 1), (-1, 0), (0, -1)]] for z, w, t in spike[1:]]
tipv = pc.bm.verts.new((0.05, 0, 0.35))
vs = pc.loft(rings, cap0=False, cap1=True)
for k in range(4):
    pc.bm.faces.new((tipv, vs[0][(k + 1) % 4], vs[0][k]))
gl = Piece("metal", glow=1.0)  # 창끝 앞면 빛나는 줄
gl.loft([[Vector((0.04, -0.105, 1.2)), Vector((0.06, -0.105, 1.2)), Vector((0.06, -0.125, 1.2)), Vector((0.04, -0.125, 1.2))],
         [Vector((0.03, -0.13, 8.0)), Vector((0.07, -0.13, 8.0)), Vector((0.07, -0.15, 8.0)), Vector((0.03, -0.15, 8.0))]])
# 오른쪽 뒤로 향한 검은 갈고리 2개 (뿌리에서 자루 쪽으로 뾰족, 참고 이미지 오른쪽 아래 이빨)
for zb, ln, out in ((8.0, 3.2, 0.75), (8.7, 2.4, 0.55)):
    pc = Piece("metal")
    base = Vector((0.78, 0, zb))
    tip = Vector((0.78 + out, 0, zb + ln))
    ring = [base + Vector((math.cos(a) * 0.1, math.sin(a) * 0.06, math.sin(a) * 0.0)) for a in [k / 5 * math.tau for k in range(5)]]
    vs, t = pc.cone_tip(ring, tip)
    pc.bm.faces.new(list(reversed(vs)))
# 척추에서 늘어진 빛나는 띠 (참고 이미지의 파란 리본 → 초록)
gl = Piece("metal", glow=1.0)
rib = [Vector((-0.35 - 0.12 * u, -0.05, 11.2 + u * 2.4)) for u in [i / 6 for i in range(7)]]
gl.loft([[p + Vector((-0.09, 0, 0)), p + Vector((0.09, 0, 0)), p + Vector((0.09, 0.025, 0)), p + Vector((-0.09, 0.025, 0))] for p in rib])

# 결정 뿌리를 감싸는 검은 하우징: 아래가 넓고 위로 좁아지는 각진 발톱 모양 (z 8.2 → 10.4)
pc = Piece("metal")
def claw(z, w, d):
    return [Vector((x * w, y * d, z)) for x, y in [(1, 0), (0.55, 0.8), (-0.55, 0.8), (-1, 0), (-0.55, -0.8), (0.55, -0.8)]]
pc.loft([claw(8.3, 0.72, 0.3), claw(8.75, 0.86, 0.34), claw(9.6, 0.58, 0.29), claw(10.4, 0.34, 0.22)])
# 하우징 앞 삼각 장식 + 빛나는 눈
pc = Piece("metal")
pc.loft([[Vector((-0.24, -0.33, 8.85)), Vector((0.24, -0.33, 8.85)), Vector((0, -0.33, 9.35))], [Vector((-0.24, -0.4, 8.85)), Vector((0.24, -0.4, 8.85)), Vector((0, -0.4, 9.35))]])
gl = Piece("metal", glow=1.0)
gl.loft([[Vector((-0.1, -0.405, 8.93)), Vector((0.1, -0.405, 8.93)), Vector((0, -0.405, 9.15))], [Vector((-0.1, -0.425, 8.93)), Vector((0.1, -0.425, 8.93)), Vector((0, -0.425, 9.15))]])

# ---------- 기계 척추 (z 10.4 → 14): 길쭉한 각진 마디가 좌우로 어긋나며 쌓이고, 양쪽 아래로 휜 톱니 ----------
z = 10.4
k = 0
while z < 13.9:
    h = random.uniform(0.55, 0.75)
    w = 0.42 - (z - 10.4) * 0.035
    off = 0.07 if k % 2 else -0.07
    pc = Piece("metal")
    def dia(zz, ww, dd):
        return [Vector((off + x * ww, y * dd, zz)) for x, y in [(1, 0), (0.3, 1), (-0.3, 1), (-1, 0), (-0.3, -1), (0.3, -1)]]
    pc.loft([dia(z, w * 0.7, 0.2), dia(z + h * 0.3, w, 0.27), dia(z + h * 0.85, w * 0.8, 0.24), dia(z + h, w * 0.6, 0.18)])
    for side in (-1, 1):
        if random.random() < 0.45:
            sp = Piece("metal")
            b = Vector((off + side * w * 0.85, 0, z + h * 0.4))
            ring = [b + Vector((0, math.cos(a) * 0.035, math.sin(a) * 0.09)) for a in [j / 4 * math.tau for j in range(4)]]
            tip = b + Vector((side * random.uniform(0.15, 0.3), 0, -random.uniform(0.25, 0.4)))
            vs, t = sp.cone_tip(ring, tip)
            sp.bm.faces.new(list(reversed(vs)))
    if k % 2 == 1:  # 앞면 빛나는 가는 줄
        gl = Piece("metal", glow=1.0)
        y = -0.255
        gl.loft([[Vector((off - w * 0.35, y, z + h * 0.35)), Vector((off + w * 0.35, y, z + h * 0.35)), Vector((off + w * 0.35, y - 0.025, z + h * 0.35)), Vector((off - w * 0.35, y - 0.025, z + h * 0.35))],
                 [Vector((off - w * 0.2, y, z + h * 0.7)), Vector((off + w * 0.2, y, z + h * 0.7)), Vector((off + w * 0.2, y - 0.025, z + h * 0.7)), Vector((off - w * 0.2, y - 0.025, z + h * 0.7))]])
    z += h - 0.04
    k += 1

# 척추의 빛나는 코어 2개 (작은 구)
for zc, yc in ((11.6, -0.27), (13.0, -0.24)):
    gl = Piece("metal", glow=1.0)
    bmesh.ops.create_uvsphere(gl.bm, u_segments=10, v_segments=6, radius=0.11)
    gl.transform(Matrix.Translation((0, yc, zc)))
# ---------- 열린 틀 (z 14 → 16.8): 가는 기둥 두 갈래가 벌어졌다 모임 ----------
Z_UP = 3.0
for side in (-1, 1):
    pts = [Vector((side * 0.18, 0, 11.0 + Z_UP))]
    for i in range(1, 9):
        u = i / 8
        pts.append(Vector((side * (0.18 + math.sin(u * math.pi) * (0.55 if side < 0 else 0.35)), 0.05 * side, 11.0 + Z_UP + u * 2.8)))
    tube_path(Piece("metal"), pts, 0.075 if side < 0 else 0.06, n=6)
# 틀 가운데 마디 고리 + 코어
pc = Piece("metal")
pc.loft([ring_circle(15.1, 0.16, 10), ring_circle(15.35, 0.2, 10), ring_circle(15.6, 0.16, 10)])
gl = Piece("metal", glow=1.0)
bmesh.ops.create_uvsphere(gl.bm, u_segments=10, v_segments=6, radius=0.12)
gl.transform(Matrix.Translation((0, -0.18, 15.35)))
# 틀 위 조인트
pc = Piece("metal")
pc.loft([ring_circle(16.7, 0.13, 8), ring_circle(16.95, 0.17, 8), ring_circle(17.25, 0.12, 8)])

# ---------- 가는 검은 자루 (z 14.2 → 25.5) ----------
pc = Piece("metal")
pc.loft([ring_circle(17.2, 0.09, 10), ring_circle(28.5, 0.09, 10)])

# ---------- 꼬리: 캡슐 틀 + 빛나는 캡슐 + 검은 화살촉 ----------
pc = Piece("metal")
pc.loft([ring_circle(28.4, 0.12, 10), ring_circle(28.6, 0.17, 10), ring_circle(28.8, 0.12, 10)])
for side in (-1, 1):
    pts = [Vector((side * 0.1, 0, 28.8 + u * 1.6)) + Vector((side * math.sin(u * math.pi) * 0.22, 0, 0)) for u in [i / 6 for i in range(7)]]
    tube_path(Piece("metal"), pts, 0.045, n=6)
gl = Piece("metal", glow=1.0)
gl.loft([ring_circle(29.0, 0.07, 10), ring_circle(29.15, 0.11, 10), ring_circle(30.05, 0.11, 10), ring_circle(30.2, 0.07, 10)])
pc = Piece("metal")
pc.loft([ring_circle(30.35, 0.12, 10), ring_circle(30.55, 0.16, 10), ring_circle(30.75, 0.11, 10)])
# 화살촉: 납작한 삼각 날 (위로 뾰족), 한쪽 날끝은 빛나는 줄
pc = Piece("metal")
tri = lambda y: [Vector((-0.5, y, 30.75)), Vector((0.5, y, 30.75)), Vector((0.06, y, 34.0))]
pc.loft([tri(0.05), tri(-0.05)])
gl = Piece("metal", glow=1.0)
gl.loft([[Vector((0.43, 0.055, 30.85)), Vector((0.47, 0.055, 30.85)), Vector((0.08, 0.055, 33.7))],
         [Vector((0.43, 0.075, 30.85)), Vector((0.47, 0.075, 30.85)), Vector((0.08, 0.075, 33.7))]])


# ---------- 합쳐서 오브젝트 두 개 ----------
def build(name, kind):
    bm = bmesh.new()
    glow_vals = []
    for pc in parts[kind]:
        me_tmp = bpy.data.meshes.new("_tmp")
        bmesh.ops.recalc_face_normals(pc.bm, faces=pc.bm.faces)
        pc.bm.to_mesh(me_tmp)
        n0 = len(bm.verts)
        bm.from_mesh(me_tmp)
        bpy.data.meshes.remove(me_tmp)
        glow_vals += [pc.glow] * (len(bm.verts) - n0)
        pc.bm.free()
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    attr = me.color_attributes.new("Glow", "FLOAT_COLOR", "POINT")
    for i, g in enumerate(glow_vals):
        attr.data[i].color = (g, g, g, 1)
    for p in me.polygons:
        p.use_smooth = False
    o = bpy.data.objects.new(name, me)
    sc.collection.objects.link(o)
    bpy.context.view_layer.objects.active = o
    for x in sc.objects:
        x.select_set(x == o)
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.uv.smart_project(angle_limit=math.radians(55), island_margin=0.015)
    bpy.ops.object.mode_set(mode="OBJECT")
    return o


metal = build("LanceMetal", "metal")
crystal = build("LanceCrystal", "crystal")
tris = lambda o: sum(len(p.vertices) - 2 for p in o.data.polygons)
print("built metal tris", tris(metal), "crystal tris", tris(crystal), "metal dims", tuple(round(d, 2) for d in metal.dimensions))
