# 그림자 발걸음(단검) 찌르기 칼날 궤적 메시 — Vfx.ShadowStep 의 BladeMesh (+ 자식 Core)
# 실행: exec(open(r"D:\god\scripts\shadow_step_blade.py", encoding="utf-8").read())
# 축: Blender +X = 찌르는 방향(끝), 꼬리 = X 0, 폭 = Y, 두께 = Z. 1 BU = 1 스터드
# 단면은 마름모(가운데 능선이 두껍고 양 날은 0) → 어느 각도에서 봐도 칼날 모양
# Outer: 길이 6.5, 최대 폭 0.8(꼬리에서 72%), 두께 0.12 / Core: 안쪽 흰 심 (폭 35%, 두께 60%, 0.6 ~ 6.25)
import bpy, bmesh, math

COL = "ShadowStepBlade"
EXPORT = r"D:\god\exports\ShadowStepBlade.fbx"
L, W, T, PEAK = 6.5, 0.8, 0.12, 0.72
STATIONS = 18


def width_at(u):
    # u: 0(꼬리) ~ 1(끝). 꼬리는 가늘게 길게 끌리고, 끝은 오목하게 날카로움
    if u <= PEAK:
        k = u / PEAK
        return 0.03 + (1 - 0.03) * (k ** 0.55)
    k = (1 - u) / (1 - PEAK)
    return k ** 1.35


def blade(name, x0, x1, wscale, tscale):
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    rings = []
    for i in range(STATIONS + 1):
        u = i / STATIONS
        # 끝 쪽에 점을 더 촘촘히 (곡선이 매끈하게)
        u = 1 - (1 - u) ** 1.25
        x = x0 + (x1 - x0) * u
        w = W * wscale * width_at(u) / 2
        t = T * tscale * max(width_at(u), 0.15) / 2
        if i == STATIONS:
            rings.append([bm.verts.new((x, 0, 0))])
            continue
        rings.append([
            bm.verts.new((x, -w, 0)),
            bm.verts.new((x, 0, t)),
            bm.verts.new((x, w, 0)),
            bm.verts.new((x, 0, -t)),
        ])
    # 꼬리 뚜껑
    bm.faces.new(list(reversed(rings[0])))
    for a, b in zip(rings[:-1], rings[1:]):
        if len(b) == 1:
            for j in range(4):
                bm.faces.new((a[j], a[(j + 1) % 4], b[0]))
        else:
            for j in range(4):
                bm.faces.new((a[j], a[(j + 1) % 4], b[(j + 1) % 4], b[j]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new(name, me)
    return ob


def build():
    col = bpy.data.collections.get(COL)
    if col:
        for o in list(col.objects):
            bpy.data.objects.remove(o, do_unlink=True)
    else:
        col = bpy.data.collections.new(COL)
        bpy.context.scene.collection.children.link(col)
    outer = blade("BladeMesh", 0.0, L, 1.0, 1.0)
    core = blade("Core", 0.6, L - 0.25, 0.35, 0.6)
    for ob, rgb in ((outer, (0.15, 0.0, 0.8)), (core, (1, 1, 1))):
        col.objects.link(ob)
        mat = bpy.data.materials.get("M_" + ob.name) or bpy.data.materials.new("M_" + ob.name)
        mat.diffuse_color = (*rgb, 1)
        ob.data.materials.clear()
        ob.data.materials.append(mat)
    tris = sum(len(p.vertices) - 2 for o in (outer, core) for p in o.data.polygons)
    return outer, core, tris


def export():
    col = bpy.data.collections[COL]
    bpy.ops.object.select_all(action="DESELECT")
    meshes = [o for o in col.objects if o.type == "MESH"]
    for o in meshes:
        o.select_set(True)
    bpy.context.view_layer.objects.active = meshes[0]
    bpy.ops.export_scene.fbx(
        filepath=EXPORT, use_selection=True, object_types={"MESH"},
        apply_unit_scale=True, apply_scale_options="FBX_SCALE_ALL",
        axis_forward="-Z", axis_up="Y", use_mesh_modifiers=True,
        use_triangles=True, mesh_smooth_type="FACE", add_leaf_bones=False, bake_anim=False,
    )
    return EXPORT


_outer, _core, _tris = build()
print("ShadowStepBlade tris", _tris, "outer dims", tuple(round(v, 3) for v in _outer.dimensions),
      "core dims", tuple(round(v, 3) for v in _core.dimensions))
print("exported", export())
