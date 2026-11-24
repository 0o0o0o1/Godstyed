# 신의 창 박힐 때 연출용 메시 (2026-11-24, 사용자 참고 그림: 번개가 꽂힌 자리에서 꽃잎처럼 날개가 솟고, 옆으로 번개 날이 튀고, 빛 돔)
# 결정(사용자): 꽃잎 날개(어두운 색 말고 밝은 빛) / 옆으로 튀는 번개 날 / 바닥 빛 돔 / 타격감 / 돌은 범위만큼 넓게 + 바깥에서 솟구치는 돌 효과 하나 더
# 메시 (1 unit = 1 stud, Z = 위):
#   GSI_Petal   꽃잎 날개 하나: 길이 6(바닥 뿌리 → 끝), 폭 최대 2.2, 안쪽으로 오목하게 휘고 끝이 뾰족 + 살짝 비틀림. 피벗 = 뿌리(바닥 중심)
#               Roblox 에서 고리로 8~12장을 바깥으로 기울여 세우고, 솟으며 펼쳐졌다 사라짐 (Neon 반투명, 밝은 빛)
#   GSI_Ring    얇은 고리(토러스) 반지름 1, 굵기 0.06 — 돔 테두리 빛 고리 (크기는 Roblox 에서)
#   GSI_Dome    위가 둥근 반구(밑면 열림) 반지름 1 — 바닥 빛 돔 (Neon/ForceField)
#   GSI_Shard1..4  바깥에서 땅을 뚫고 솟구치는 뾰족한 돌 조각 (길이 2.5~4, 각진 면). 피벗 = 밑동
# 실행: exec(open(r"D:\god\scripts\vfx_god_spear_impact.py", encoding="utf-8").read())  (Blender MCP 또는 명령줄)
import bpy, bmesh, math, random
from mathutils import Vector

RNG = random.Random(21)
COLL = "GodSpearImpact"


def clear():
    if COLL in bpy.data.collections:
        c = bpy.data.collections[COLL]
        for o in list(c.objects):
            bpy.data.objects.remove(o, do_unlink=True)
    else:
        c = bpy.data.collections.new(COLL)
        bpy.context.scene.collection.children.link(c)
    return c


def finish(bm, name, coll, smooth=False):
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    for p in me.polygons:
        p.use_smooth = smooth
    ob = bpy.data.objects.new(name, me)
    coll.objects.link(ob)
    return ob


def petal(coll):
    """꽃잎: 길이 방향 u(0 뿌리 → 1 끝), 폭 방향 v(-1..1). 넓고 끝이 둥글게 좁아지는 잎 모양,
    단면은 안쪽(-Y) 오목한 얕은 호, 위로 갈수록 바깥(+Y)으로 휘어 넘어감, 두께 0.08 (v1 은 가늘고 비틀려 가시처럼 보였음)"""
    L, W = 8.5, 1.25  # 사용자: 더 길고 날카롭게 (6, 1.6 → 8.5, 1.25)
    nu, nv = 16, 10
    bm = bmesh.new()
    rows_f, rows_b = [], []
    for i in range(nu + 1):
        u = i / nu
        # 뿌리 쪽이 넓고 끝으로 갈수록 곧게 좁아져 뾰족 (칼날·불꽃 느낌)
        half = W * (math.sin(math.pi * min(0.1 + 1.6 * u, 0.5)) ** 0.6) * (1 - u) ** 1.15 + 0.015
        bend = 1.9 * u * u
        twist = 0.12 * u
        rf, rb = [], []
        for j in range(nv + 1):
            v = -1 + 2 * j / nv
            x = v * half
            cup = 0.32 * half * (1 - v * v)
            for side, rows in ((0.04, rf), (-0.04, rb)):
                y = bend - cup + side
                z = u * L * (1 - 0.12 * u)
                rows.append(bm.verts.new((x * math.cos(twist), y + x * math.sin(twist) * 0.2, z)))
        rows_f.append(rf)
        rows_b.append(rb)
    for rows, flip in ((rows_f, False), (rows_b, True)):
        for i in range(nu):
            for j in range(nv):
                q = (rows[i][j], rows[i][j + 1], rows[i + 1][j + 1], rows[i + 1][j])
                bm.faces.new(q[::-1] if flip else q)
    for i in range(nu):
        for j in (0, nv):
            bm.faces.new((rows_f[i][j], rows_f[i + 1][j], rows_b[i + 1][j], rows_b[i][j]))
    for j in range(nv):
        bm.faces.new((rows_f[0][j], rows_b[0][j], rows_b[0][j + 1], rows_f[0][j + 1]))
        bm.faces.new((rows_f[nu][j], rows_f[nu][j + 1], rows_b[nu][j + 1], rows_b[nu][j]))
    return finish(bm, "GSI_Petal", coll, smooth=True)


def ring(coll):
    bm = bmesh.new()
    seg, sides, R, r = 48, 6, 1.0, 0.06
    rings = []
    for i in range(seg):
        a = 2 * math.pi * i / seg
        c = Vector((math.cos(a), math.sin(a), 0))
        ring_v = []
        for k in range(sides):
            b = 2 * math.pi * k / sides
            p = c * (R + r * math.cos(b)) + Vector((0, 0, r * math.sin(b)))
            ring_v.append(bm.verts.new(p))
        rings.append(ring_v)
    for i in range(seg):
        a, b = rings[i], rings[(i + 1) % seg]
        for k in range(sides):
            bm.faces.new((a[k], a[(k + 1) % sides], b[(k + 1) % sides], b[k]))
    return finish(bm, "GSI_Ring", coll, smooth=True)


def dome(coll):
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=32, v_segments=16, radius=1.0)
    for v in [v for v in bm.verts if v.co.z < -0.01]:
        bm.verts.remove(v)
    return finish(bm, "GSI_Dome", coll, smooth=True)


def shard(coll, idx):
    """뾰족한 돌 조각: 불규칙한 5~6각 기둥이 위로 좁아져 끝이 뾰족, 면마다 각짐"""
    bm = bmesh.new()
    n = RNG.choice((5, 6))
    h = RNG.uniform(2.5, 4.0)
    base_r = RNG.uniform(0.6, 0.95)
    lean = Vector((RNG.uniform(-0.25, 0.25), RNG.uniform(-0.25, 0.25), 0))
    levels = [(0.0, 1.0), (0.35, RNG.uniform(0.75, 0.95)), (0.7, RNG.uniform(0.4, 0.6))]
    rings = []
    for t, s in levels:
        rv = []
        for k in range(n):
            a = 2 * math.pi * k / n + RNG.uniform(-0.25, 0.25)
            r = base_r * s * RNG.uniform(0.8, 1.15)
            rv.append(bm.verts.new(Vector((math.cos(a) * r, math.sin(a) * r, t * h)) + lean * t))
        rings.append(rv)
    tip = bm.verts.new(Vector((RNG.uniform(-0.15, 0.15), RNG.uniform(-0.15, 0.15), h)) + lean)
    for a, b in zip(rings, rings[1:]):
        for k in range(n):
            bm.faces.new((a[k], a[(k + 1) % n], b[(k + 1) % n], b[k]))
    for k in range(n):
        bm.faces.new((rings[-1][k], rings[-1][(k + 1) % n], tip))
    bm.faces.new(list(reversed(rings[0])))
    return finish(bm, "GSI_Shard%d" % idx, coll)


def build():
    coll = clear()
    p = petal(coll)
    r = ring(coll)
    r.location = (8, 0, 0)
    d = dome(coll)
    d.location = (12, 0, 0)
    for i in range(1, 5):
        s = shard(coll, i)
        s.location = (16 + i * 3, 0, 0)
    tris = sum(sum(len(f.vertices) - 2 for f in o.data.polygons) for o in coll.objects)
    print("impact parts", [o.name for o in coll.objects], "tris", tris)


def export():
    import os
    coll = bpy.data.collections[COLL]
    bpy.ops.object.select_all(action="DESELECT")
    for o in coll.objects:
        o.select_set(True)
    bpy.context.view_layer.objects.active = coll.objects[0]
    path = r"D:\god\exports\vfx\GodSpearImpact.fbx"
    wanted = dict(filepath=path, use_selection=True, object_types={"MESH"}, apply_unit_scale=True,
                  apply_scale_options="FBX_SCALE_ALL", axis_forward="-Z", axis_up="Y", bake_space_transform=False,
                  use_mesh_modifiers=True, use_triangles=True, mesh_smooth_type="FACE", add_leaf_bones=False, bake_anim=False)
    valid = {p.identifier for p in bpy.ops.export_scene.fbx.get_rna_type().properties}
    bpy.ops.export_scene.fbx(**{k: v for k, v in wanted.items() if k in valid})
    print("exported", path)


build()
