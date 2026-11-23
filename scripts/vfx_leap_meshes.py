# 도약 찌르기 메시: 빛의 결정 창날(7조각 + 심 + 밑동 결정), 들린 돌판 8, 돌 파편 4
# 1 Blender 단위 = 1 스터드, Z 위. 창날은 끝이 아래(z=0 이 땅에 닿는 끝), 조각은 실제 자리에 겹쳐 놓여 한 창날을 이룸.
# 실행: exec(open(r"D:\god\scripts\vfx_leap_meshes.py", encoding="utf-8").read())  → D:\god\exports\vfx\LeapMeshes.fbx
import bpy, bmesh, math, random, os
from mathutils import Vector

random.seed(7)
SCENE = "VFX_LeapMeshes"
if SCENE in bpy.data.scenes:
    bpy.data.scenes.remove(bpy.data.scenes[SCENE])
sc = bpy.data.scenes.new(SCENE)
bpy.context.window.scene = sc


def new_obj(name, bm, loc=(0, 0, 0)):
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    for p in me.polygons:
        p.use_smooth = False
    o = bpy.data.objects.new(name, me)
    o.location = loc
    sc.collection.objects.link(o)
    return o


# ---- 결정 창날 ----
# 단면 = 마름모(폭 w, 두께 t). 높이별 (z, w, t). 끝(z=0)은 점.
PROFILE = [
    (0.0, 0.0, 0.0),
    (1.2, 0.9, 0.42),
    (2.6, 1.6, 0.66),
    (4.2, 2.3, 0.86),
    (5.8, 2.5, 0.92),   # 가장 넓은 곳
    (7.4, 2.1, 0.82),
    (8.8, 1.3, 0.62),
    (9.9, 0.75, 0.5),   # 날 밑 목
    (10.6, 2.9, 0.55),  # 날개(코등이): 양옆으로 뾰족
    (11.3, 0.55, 0.45),
    (14.5, 0.42, 0.38), # 자루 쪽 결정 (위로 사라짐)
]
JIT = 0.06


def ring(z, w, t, twist=0.0):
    pts = []
    for k, (x, y) in enumerate([(w / 2, 0), (0, t / 2), (-w / 2, 0), (0, -t / 2)]):
        jx = (random.random() - 0.5) * JIT * w
        jy = (random.random() - 0.5) * JIT * t
        a = twist
        px = (x + jx) * math.cos(a) - (y + jy) * math.sin(a)
        py = (x + jx) * math.sin(a) + (y + jy) * math.cos(a)
        pts.append(Vector((px, py, z)))
    return pts


rings = [ring(z, w, t, twist=0.03 * i) for i, (z, w, t) in enumerate(PROFILE)]
# 조각: 연속한 두 고리 사이 (첫 조각은 끝점 → 고리)
SEGMENTS = [(0, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 8), (8, 10)]  # 고리 번호 범위 → 7조각
for si, (a, b) in enumerate(SEGMENTS):
    bm = bmesh.new()
    layers = []
    for ri in range(a, b + 1):
        if PROFILE[ri][1] == 0:
            layers.append([bm.verts.new((0, 0, PROFILE[ri][0]))])
        else:
            layers.append([bm.verts.new(p) for p in rings[ri]])
    for l0, l1 in zip(layers, layers[1:]):
        if len(l0) == 1:
            for k in range(4):
                bm.faces.new((l0[0], l1[(k + 1) % 4], l1[k]))
        else:
            for k in range(4):
                bm.faces.new((l0[k], l0[(k + 1) % 4], l1[(k + 1) % 4], l1[k]))
    # 위·아래 뚜껑
    if len(layers[0]) == 4:
        bm.faces.new(list(reversed(layers[0])))
    bm.faces.new(layers[-1])
    # 날 옆면에서 비스듬히 위·바깥으로 자란 작은 결정 (가운데 조각들)
    if si in (1, 2, 3, 4):
        z0, z1 = PROFILE[a][0], PROFILE[b][0]
        for side in (1, -1):
            if random.random() < 0.25:
                continue
            zc = random.uniform(z0 + 0.2, z1 - 0.2)
            # 그 높이의 반폭 (선형 보간)
            wa, wb = PROFILE[a][1], PROFILE[b][1]
            half = (wa + (wb - wa) * (zc - z0) / max(z1 - z0, 1e-3)) / 2
            base = Vector((side * half * 0.8, random.uniform(-0.1, 0.1), zc))
            dirv = Vector((side * random.uniform(0.8, 1.0), random.uniform(-0.25, 0.25), random.uniform(0.5, 0.9))).normalized()
            ln = random.uniform(0.9, 1.6)
            r0 = random.uniform(0.14, 0.22)
            up = Vector((0, 1, 0)) if abs(dirv.y) < 0.9 else Vector((1, 0, 0))
            u = dirv.cross(up).normalized()
            v2 = dirv.cross(u).normalized()
            vs = [bm.verts.new(base + (u * math.cos(k * math.pi / 2) + v2 * math.sin(k * math.pi / 2)) * r0) for k in range(4)]
            tip = bm.verts.new(base + dirv * ln)
            for k in range(4):
                bm.faces.new((vs[k], vs[(k + 1) % 4], tip))
            bm.faces.new(list(reversed(vs)))
    new_obj("Shard%d" % (si + 1), bm)

# 심: 창날 안쪽의 가는 빛 (폭·두께 40%)
bm = bmesh.new()
core_layers = []
for (z, w, t) in PROFILE[:10]:
    if w == 0:
        core_layers.append([bm.verts.new((0, 0, z + 0.25))])
    else:
        s = 0.4
        core_layers.append([bm.verts.new((x, y, z)) for (x, y) in [(w * s / 2, 0), (0, t * s / 2), (-w * s / 2, 0), (0, -t * s / 2)]])
for l0, l1 in zip(core_layers, core_layers[1:]):
    if len(l0) == 1:
        for k in range(4):
            bm.faces.new((l0[0], l1[(k + 1) % 4], l1[k]))
    else:
        for k in range(4):
            bm.faces.new((l0[k], l0[(k + 1) % 4], l1[(k + 1) % 4], l1[k]))
bm.faces.new(core_layers[-1])
new_obj("Core", bm)

# 밑동 결정: 땅에서 바깥으로 기운 가시 6개 (한 메시)
bm = bmesh.new()
for k in range(6):
    ang = k / 6 * math.tau + random.uniform(-0.3, 0.3)
    h = random.uniform(1.2, 2.6)
    r0 = random.uniform(0.25, 0.4)
    base = Vector((math.cos(ang) * 0.9, math.sin(ang) * 0.9, -0.3))
    tilt = Vector((math.cos(ang), math.sin(ang), 0)) * random.uniform(0.5, 0.9)
    tip = base + Vector((0, 0, h)) + tilt * h * 0.6
    vs = []
    for j in range(4):
        a2 = ang + j * math.pi / 2 + 0.4
        vs.append(bm.verts.new(base + Vector((math.cos(a2) * r0, math.sin(a2) * r0, 0))))
    t = bm.verts.new(tip)
    for j in range(4):
        bm.faces.new((vs[j], vs[(j + 1) % 4], t))
    bm.faces.new(list(reversed(vs)))
new_obj("BaseShards", bm)


# ---- 들린 돌판 8 ----
def slab(name, cx, cy, ang):
    bm = bmesh.new()
    n = random.choice([5, 6])
    rx, ry = random.uniform(1.4, 1.9), random.uniform(1.0, 1.4)
    top = []
    for k in range(n):
        a = k / n * math.tau + random.uniform(-0.25, 0.25)
        r = random.uniform(0.75, 1.05)
        x, y = math.cos(a) * rx * r, math.sin(a) * ry * r
        # 바깥으로 가로로 긴 판 (ang 방향이 바깥)
        px = x * math.cos(ang) - y * math.sin(ang)
        py = x * math.sin(ang) + y * math.cos(ang)
        top.append(bm.verts.new((px, py, random.uniform(-0.06, 0.06))))
    f = bm.faces.new(top)
    ext = bmesh.ops.extrude_face_region(bm, geom=[f])
    vs = [e for e in ext["geom"] if isinstance(e, bmesh.types.BMVert)]
    thick = random.uniform(0.7, 1.0)
    for v in vs:
        v.co.z -= thick
        v.co.x *= 0.88
        v.co.y *= 0.88  # 아래가 좁은 쐐기
    # 윗면을 조금 깨뜨림: 가운데 점으로 부채꼴 분할 후 살짝 올림
    topf = [fc for fc in bm.faces if all(v.co.z > -0.1 for v in fc.verts)][0]
    res = bmesh.ops.poke(bm, faces=[topf])
    for v in res["verts"]:
        v.co.z += random.uniform(0.05, 0.18)
    bmesh.ops.translate(bm, verts=bm.verts, vec=Vector((cx, cy, 0)))
    new_obj(name, bm)


for k in range(8):
    ang = k / 8 * math.tau + random.uniform(-0.15, 0.15)
    r = random.uniform(3.6, 4.4)
    slab("Slab%d" % (k + 1), math.cos(ang) * r, math.sin(ang) * r, ang)


# ---- 돌 파편 4 ----
for k in range(4):
    bm = bmesh.new()
    bmesh.ops.create_icosphere(bm, subdivisions=1, radius=1.0)
    for v in bm.verts:
        v.co *= random.uniform(0.75, 1.15)
    sx, sy, sz = random.uniform(0.35, 0.6), random.uniform(0.3, 0.5), random.uniform(0.25, 0.4)
    for v in bm.verts:
        v.co.x *= sx; v.co.y *= sy; v.co.z *= sz
    bmesh.ops.translate(bm, verts=bm.verts, vec=Vector((12 + k * 2, 0, 0)))
    new_obj("Rock%d" % (k + 1), bm)

# ---- FBX ----
os.makedirs(r"D:\god\exports\vfx", exist_ok=True)
bpy.ops.object.select_all(action="DESELECT")
for o in sc.objects:
    o.select_set(True)
bpy.context.view_layer.objects.active = sc.objects[0]
path = r"D:\god\exports\vfx\LeapMeshes.fbx"
wanted = dict(filepath=path, use_selection=True, object_types={"MESH"}, apply_unit_scale=True,
              apply_scale_options="FBX_SCALE_ALL", axis_forward="-Z", axis_up="Y", bake_space_transform=False,
              use_mesh_modifiers=True, use_triangles=True, mesh_smooth_type="FACE", add_leaf_bones=False, bake_anim=False)
valid = {p.identifier for p in bpy.ops.export_scene.fbx.get_rna_type().properties}
bpy.ops.export_scene.fbx(**{k: v for k, v in wanted.items() if k in valid})
tris = sum(sum(len(p.vertices) - 2 for p in o.data.polygons) for o in sc.objects)
print("exported", path, "objects", len(sc.objects), "tris", tris)
