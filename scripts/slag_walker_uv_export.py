# Slag Walker: 박스 투영 UV(재질별 타일 크기) + FBX 내보내기 — slag_walker_build.py 다음에 실행
# 굽기 셰이더는 slag_walker_tex.py (굽기 절차: OUT_<채널> 노드를 Material Output 에 연결 → EMIT / NORMAL 굽기, 1024, 호출당 2~3장)
import bpy, bmesh
col = bpy.data.collections["SlagWalker"]
TILE = {"Slag": 1.5, "Cloth": 1.2, "Skin": 1.0, "Helmet": 1.0, "Boot": 1.0, "Dark": 1.0, "Glow": 1.0}
for o in col.objects:
    t = TILE[o.name.split("__")[1]]
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

for o in bpy.context.view_layer.objects:
    o.select_set(False)
meshes = [o for o in col.objects if o.type == 'MESH']
for o in meshes:
    o.hide_set(False); o.select_set(True)
bpy.context.view_layer.objects.active = meshes[0]
bpy.ops.export_scene.fbx(filepath="D:\\god\\exports\\SlagWalker.fbx", use_selection=True, object_types={"MESH"},
    apply_unit_scale=True, apply_scale_options="FBX_SCALE_ALL", axis_forward="-Z", axis_up="Y", bake_space_transform=False,
    use_mesh_modifiers=True, use_triangles=True, mesh_smooth_type="FACE", add_leaf_bones=False, bake_anim=False)
# Studio: 각 MeshPart 를 HRP.CFrame * CFrame.new(-cx, cz, cy) 에 두고 (c = Blender 바운딩 중심) 이름의 부위에 Weld("Attach")
