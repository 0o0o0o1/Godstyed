# 도약 찌르기: 땅에 박히는 '빛의 창' (고품질 모델)
# 창날(잎 모양, 가운데 능선 + 날 경사 + 홈), 날개 돌기, 소켓 고리, 자루(마디 고리 + 나선 감김), 끝으로 갈수록 빛으로 사라짐.
# 창끝이 원점(z=0)에서 위로 선다. 1 단위 = 1 스터드. 오브젝트 하나 "LightLance" (UV 펼침 포함).
# 실행: exec(open(r"D:\god\scripts\vfx_leap_lance.py", encoding="utf-8").read())
import bpy, bmesh, math
from mathutils import Vector, Matrix

SCENE = "VFX_LeapLance"
if SCENE in bpy.data.scenes:
    bpy.data.scenes.remove(bpy.data.scenes[SCENE])
# 예전 실행이 남긴 같은 이름 오브젝트·메시 정리 (이름이 .001 로 밀리지 않게)
for o in [o for o in bpy.data.objects if o.name.startswith("LightLance")]:
    bpy.data.objects.remove(o)
for me_ in [m_ for m_ in bpy.data.meshes if m_.name.startswith("LightLance") and m_.users == 0]:
    bpy.data.meshes.remove(me_)
sc = bpy.data.scenes.new(SCENE)
bpy.context.window.scene = sc

bm = bmesh.new()


def loft(rings, cap_bottom=True, cap_top=True):
    """rings: 같은 점 개수의 고리 목록 (아래→위). 옆면 + 뚜껑."""
    vs = [[bm.verts.new(p) for p in r] for r in rings]
    n = len(rings[0])
    for a, b in zip(vs, vs[1:]):
        for k in range(n):
            bm.faces.new((a[k], a[(k + 1) % n], b[(k + 1) % n], b[k]))
    if cap_bottom:
        bm.faces.new(list(reversed(vs[0])))
    if cap_top:
        bm.faces.new(vs[-1])
    return vs


# ---- 창날 ----
# 단면 8점: 날 끝(좌우) → 날 경사 → 능선(앞뒤). w=반폭, t=능선 반두께, e=날 경사 시작 비율
def blade_ring(z, w, t, e=0.55):
    """단면 12점: 날 끝 바로 안쪽(0.86w)에 점을 하나 더 둬서 날 끝 발광이 얇은 선으로만 남게"""
    q = 0.86
    pts = [
        (w, 0), (w * q, t * 0.16), (w * e, t * 0.55), (0, t), (-w * e, t * 0.55), (-w * q, t * 0.16),
        (-w, 0), (-w * q, -t * 0.16), (-w * e, -t * 0.55), (0, -t), (w * e, -t * 0.55), (w * q, -t * 0.16),
    ]
    return [Vector((x, y, z)) for x, y in pts]


BLADE = [  # (z, 반폭, 능선 반두께)
    (0.0, 0.0, 0.0),
    (0.35, 0.16, 0.07),
    (1.0, 0.42, 0.14),
    (2.0, 0.72, 0.2),
    (3.1, 0.92, 0.24),
    (4.1, 0.96, 0.25),  # 가장 넓은 곳
    (5.0, 0.82, 0.23),
    (5.8, 0.55, 0.2),
    (6.4, 0.34, 0.18),  # 날 목
]
rings = []
for z, w, t in BLADE[1:]:
    rings.append(blade_ring(z, w, t))
tip = bm.verts.new((0, 0, 0))
bv = loft(rings, cap_bottom=False, cap_top=False)
NB = len(bv[0])
for k in range(NB):
    bm.faces.new((tip, bv[0][(k + 1) % NB], bv[0][k]))

# ---- 날개 돌기 (날 목 양옆, 아래로 휜 갈고리) ----
def wing(side):
    pts = []
    base_z = 6.5
    path = [(0.3, base_z), (0.75, base_z - 0.05), (1.15, base_z - 0.35), (1.35, base_z - 0.85)]
    secs = []
    for i, (x, z) in enumerate(path):
        r = 0.16 * (1 - i / (len(path) - 0.2))
        r = max(r, 0.03)
        secs.append([Vector((side * x + side * dx * r, dy * r * 0.7, z + dz * r)) for dx, dy, dz in [(0, 1, 0), (1, 0, 0), (0, -1, 0), (-1, 0, 0)]])
    loft(secs)


wing(1)
wing(-1)

# ---- 소켓 (날 목 → 자루), 고리 3개 ----
def tube(z0, z1, r0, r1, n=16, z_steps=1):
    rs = []
    for s in range(z_steps + 1):
        u = s / z_steps
        z = z0 + (z1 - z0) * u
        r = r0 + (r1 - r0) * u
        rs.append([Vector((math.cos(a) * r, math.sin(a) * r, z)) for a in [k / n * math.tau for k in range(n)]])
    return loft(rs)


tube(6.3, 6.9, 0.36, 0.3)
tube(6.9, 8.2, 0.3, 0.24, z_steps=2)
for zc, rr in [(7.05, 0.34), (7.6, 0.31), (8.15, 0.3)]:
    tube(zc - 0.07, zc + 0.07, rr, rr)

# ---- 자루: z 8.2 → 19, 마디 고리 + 나선 감김 ----
tube(8.2, 19.0, 0.2, 0.17, n=12, z_steps=6)
for zc in (11.0, 14.5, 18.0):
    tube(zc - 0.1, zc + 0.1, 0.27, 0.27, n=12)
# 나선 감김: 가는 띠 (z 8.4 → 10.6)
turns, seg = 3.5, 70
strip = []
for i in range(seg + 1):
    u = i / seg
    a = u * turns * math.tau
    z = 8.4 + u * 2.2
    c, s = math.cos(a), math.sin(a)
    strip.append([Vector((c * 0.235, s * 0.235, z - 0.05)), Vector((c * 0.235, s * 0.235, z + 0.05)), Vector((c * 0.205, s * 0.205, z + 0.05)), Vector((c * 0.205, s * 0.205, z - 0.05))])
loft(strip)

me = bpy.data.meshes.new("LightLance")
bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-5)
bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
bm.to_mesh(me)
bm.free()
obj = bpy.data.objects.new("LightLance", me)
sc.collection.objects.link(obj)
bpy.context.view_layer.objects.active = obj
obj.select_set(True)
# 날카로운 모서리는 각지게, 나머지는 부드럽게
for p in me.polygons:
    p.use_smooth = True
try:
    me.set_sharp_from_angle(angle=math.radians(35))
except Exception:
    pass
# UV: smart project
bpy.ops.object.mode_set(mode="EDIT")
bpy.ops.mesh.select_all(action="SELECT")
bpy.ops.uv.smart_project(angle_limit=math.radians(50), island_margin=0.02)
bpy.ops.object.mode_set(mode="OBJECT")
tris = sum(len(p.vertices) - 2 for p in me.polygons)
print("lance built, tris", tris, "dims", tuple(round(d, 2) for d in obj.dimensions))
