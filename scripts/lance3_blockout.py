# 빛의 창 v3 — 1단계 블록아웃 (reference-modeling). 참고 이미지를 세운 것(references/lance_ref_straight.png) 기준.
# 좌표: x = 이미지 가로(스터드, 가운데 0), z = 머리 끝 0 → 꼬리 30, y = 두께(앞뒤).
# 각 덩어리 = (이름, 중심 x, 중심 z, 폭, 높이, 두께, y축 기울기(도, + = 위쪽이 +x 로)), 납작 상자.
# 실행: exec(open(r"D:\god\scripts\lance3_blockout.py", encoding="utf-8").read())
import bpy, bmesh, math
from mathutils import Matrix, Vector

SCENE = "VFX_Lance3"
if SCENE in bpy.data.scenes:
    bpy.data.scenes.remove(bpy.data.scenes[SCENE])
for o in [o for o in bpy.data.objects if o.name.startswith("L3_")]:
    bpy.data.objects.remove(o)
if bpy.context.window is not None:
    sc = bpy.data.scenes.new(SCENE)
    bpy.context.window.scene = sc
else:  # 명령줄(-b): 창이 없으니 기본 장면을 비워서 씀
    sc = bpy.context.scene
    sc.name = SCENE
    for o in list(sc.objects):
        bpy.data.objects.remove(o)

PARTS = [
    # 머리
    ("L3_CrystalR", 0.98, 4.85, 0.74, 9.8, 0.34, 7.6),
    ("L3_CrystalL", -0.85, 4.5, 0.5, 5.0, 0.26, -3.5),
    ("L3_FinL1", -1.55, 8.4, 0.32, 3.8, 0.12, -6.0),
    ("L3_FinL2", -1.2, 8.2, 0.26, 3.0, 0.12, -4.0),
    ("L3_Spike", -0.02, 3.2, 0.27, 5.6, 0.18, 0.0),
    ("L3_HeadHub", 0.12, 6.75, 1.0, 2.5, 0.45, 0.0),
    ("L3_Spine", 0.02, 9.5, 0.8, 3.0, 0.38, 0.0),
    ("L3_Ribbon", -0.75, 11.15, 1.18, 0.2, 0.04, 46.0),
    ("L3_Cable", 0.3, 11.75, 0.4, 1.5, 0.14, 0.0),
    ("L3_NeckHub", -0.1, 12.6, 1.0, 0.6, 0.4, 0.0),
    ("L3_FrameL", -0.17, 13.85, 0.26, 1.9, 0.14, 0.0),
    ("L3_FrameR1", 0.47, 13.25, 0.2, 1.1, 0.14, 50.0),
    ("L3_FrameR2", 0.52, 14.2, 0.2, 1.42, 0.14, -32.0),
    # 자루·꼬리
    ("L3_Shaft", -0.1, 19.1, 0.2, 8.6, 0.2, 0.0),
    ("L3_Capsule", -0.17, 24.2, 0.72, 1.6, 0.4, 0.0),
    ("L3_ButtHub", -0.08, 25.5, 0.8, 1.0, 0.35, 0.0),
    ("L3_ButtSpike", -0.13, 27.8, 0.36, 4.4, 0.12, 0.0),
]


def slab(name, cx, cz, w, h, d, tilt):
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=Vector((w, d, h)), verts=bm.verts)
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(name, me)
    o.location = (cx, 0, cz)
    o.rotation_euler = (0, math.radians(tilt), 0)
    sc.collection.objects.link(o)
    return o


for p in PARTS:
    slab(*p)

# 꼬리 지느러미: 삼각형 (위 꼭짓점 = 창끝 근처, 아래 = 오른쪽 바깥)
bm = bmesh.new()
tri = [(-0.12, 29.7), (0.05, 29.4), (1.18, 25.35), (0.85, 25.3), (-0.02, 27.0)]
for y in (-0.05, 0.05):
    pass
vs0 = [bm.verts.new((x, -0.05, z)) for x, z in tri]
vs1 = [bm.verts.new((x, 0.05, z)) for x, z in tri]
bm.faces.new(vs0); bm.faces.new(list(reversed(vs1)))
n = len(tri)
for k in range(n):
    bm.faces.new((vs0[k], vs0[(k + 1) % n], vs1[(k + 1) % n], vs1[k]))
bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
me = bpy.data.meshes.new("L3_ButtFin"); bm.to_mesh(me); bm.free()
sc.collection.objects.link(bpy.data.objects.new("L3_ButtFin", me))
print("blockout parts", len(sc.objects))
