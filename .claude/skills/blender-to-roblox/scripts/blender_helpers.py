# Blender -> Roblox helpers.
# The Blender MCP runs in SAFE MODE (no exec/open/os), so do NOT try to load this file from Blender.
# Instead: Read this file, paste its full contents at the top of the execute_blender_code script,
# then append the calls you need. The export folder must already exist (create it from the shell).
# Functions: setup_scene(), make_palette_materials(), make_calibration_cube(),
#            check_asset(name), export_asset(name)

import bpy
import bmesh
from mathutils import Vector

EXPORT_DIR = r"C:\Users\CafeAlle\Desktop\god\exports"

PALETTE = {
    "RustRed": (120, 55, 40), "FadedBlue": (55, 80, 100), "Olive": (85, 90, 60),
    "DirtyWhite": (170, 165, 150), "CraneYellow": (175, 110, 40), "DarkSteel": (60, 60, 62),
    "Rust": (105, 60, 40), "Concrete": (95, 95, 90), "DiamondPlate": (80, 80, 80),
    "Rubber": (30, 30, 30), "Glass": (90, 105, 110), "Canvas": (90, 85, 65),
    "Wood": (110, 85, 60), "Hazard": (190, 150, 40),
    # texture-set variants (Warehouse_Main): visuals from SurfaceAppearance
    "SidingTeal": (95, 115, 108), "RoofZinc": (122, 124, 120),
    "ShutterOrange": (158, 98, 50), "SteelBlue": (60, 68, 78),
}
OPTIONS = {"NoCollide", "Hull", "Box", "Precise", "TEX"}
TRI_LIMIT_PART = 20000


def _srgb_to_linear(c):
    c = c / 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def setup_scene():
    """1 Blender unit = 1 stud."""
    s = bpy.context.scene
    s.unit_settings.system = 'METRIC'
    s.unit_settings.scale_length = 1.0
    return "scene ready: 1 BU = 1 stud, export dir = " + EXPORT_DIR


def make_palette_materials():
    """Create M_<key> preview materials matching the palette (preview only)."""
    for key, rgb in PALETTE.items():
        name = "M_" + key
        mat = bpy.data.materials.get(name) or bpy.data.materials.new(name)
        mat.use_nodes = True
        bsdf = next((n for n in mat.node_tree.nodes if n.type == "BSDF_PRINCIPLED"), None)
        col = tuple(_srgb_to_linear(v) for v in rgb) + (1.0,)
        if bsdf:
            bsdf.inputs["Base Color"].default_value = col
            bsdf.inputs["Roughness"].default_value = 0.8
        mat.diffuse_color = col
    return "palette materials: " + ", ".join("M_" + k for k in PALETTE)


def get_collection(name):
    col = bpy.data.collections.get(name)
    if col is None:
        col = bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(col)
    return col


def parse_name(obj_name):
    """'Asset_Part__Palette__Opt' -> (base, palette, options)"""
    parts = obj_name.split("__")
    base = parts[0]
    palette = parts[1] if len(parts) > 1 else None
    opts = set(parts[2:])
    return base, palette, opts


def make_calibration_cube():
    """48 x 12 x 12 box, bottom-center origin, arrow on +X, in collection 'Calib_Cube'."""
    setup_scene()
    make_palette_materials()
    col = get_collection("Calib_Cube")
    for o in list(col.objects):
        bpy.data.objects.remove(o, do_unlink=True)

    def box(name, size, center, mat):
        me = bpy.data.meshes.new(name)
        bm = bmesh.new()
        bmesh.ops.create_cube(bm, size=1.0)
        for v in bm.verts:
            v.co = Vector((v.co.x * size[0] + center[0], v.co.y * size[1] + center[1], v.co.z * size[2] + center[2]))
        bm.to_mesh(me); bm.free()
        ob = bpy.data.objects.new(name, me)
        ob.data.materials.append(bpy.data.materials["M_" + mat])
        col.objects.link(ob)
        return ob

    box("Calib_Body__FadedBlue", (48, 12, 12), (0, 0, 6), "FadedBlue")
    # arrow marker on +X end (sticks out 4 studs) and on top (+Z) near +X
    box("Calib_ArrowX__Hazard", (4, 4, 4), (26, 0, 6), "Hazard")
    box("Calib_TopMark__RustRed", (8, 2, 1), (18, 0, 12.5), "RustRed")
    return "calibration cube created in collection 'Calib_Cube' (body 48x12x12, +X marker)"


def _tri_count(ob):
    deps = bpy.context.evaluated_depsgraph_get()
    me = ob.evaluated_get(deps).to_mesh()
    n = sum(len(p.vertices) - 2 for p in me.polygons)
    ngons = sum(1 for p in me.polygons if len(p.vertices) > 4)
    ob.evaluated_get(deps).to_mesh_clear()
    return n, ngons


def check_asset(name):
    col = bpy.data.collections.get(name)
    if col is None:
        return "ERROR: no collection named " + name
    meshes = [o for o in col.all_objects if o.type == "MESH"]
    if not meshes:
        return "ERROR: collection has no meshes"
    issues, lines = [], []
    total = 0
    mn = Vector((1e9, 1e9, 1e9)); mx = Vector((-1e9, -1e9, -1e9))
    for ob in meshes:
        base, pal, opts = parse_name(ob.name)
        if pal is None:
            issues.append(f"{ob.name}: missing __<palette> suffix")
        elif pal not in PALETTE:
            issues.append(f"{ob.name}: unknown palette key '{pal}'")
        bad = opts - OPTIONS
        if bad:
            issues.append(f"{ob.name}: unknown option(s) {sorted(bad)}")
        if any(abs(r) > 1e-4 for r in ob.rotation_euler) or any(abs(s - 1) > 1e-4 for s in ob.scale):
            issues.append(f"{ob.name}: unapplied rotation/scale (Ctrl+A)")
        nmat = len([m for m in ob.data.materials if m])
        if nmat > 1:
            issues.append(f"{ob.name}: {nmat} materials (split into one object per material)")
        tris, ngons = _tri_count(ob)
        total += tris
        if tris > TRI_LIMIT_PART:
            issues.append(f"{ob.name}: {tris} tris > {TRI_LIMIT_PART}")
        if ngons:
            lines.append(f"  note {ob.name}: {ngons} n-gons (triangulated on export)")
        for c in ob.bound_box:
            w = ob.matrix_world @ Vector(c)
            mn = Vector((min(mn.x, w.x), min(mn.y, w.y), min(mn.z, w.z)))
            mx = Vector((max(mx.x, w.x), max(mx.y, w.y), max(mx.z, w.z)))
    size = mx - mn
    center = (mn + mx) / 2
    if abs(mn.z) > 0.05:
        issues.append(f"bottom is at Z={mn.z:.2f}, should be 0")
    if abs(center.x) > 0.05 or abs(center.y) > 0.05:
        issues.append(f"XY center is ({center.x:.2f}, {center.y:.2f}), should be (0, 0)")
    head = (f"{name}: {len(meshes)} meshes, {total} tris, "
            f"size L(X)={size.x:.2f} W(Y)={size.y:.2f} H(Z)={size.z:.2f}")
    body = "\n".join(lines)
    status = "OK" if not issues else "ISSUES:\n  - " + "\n  - ".join(issues)
    return head + ("\n" + body if body else "") + "\n" + status


def export_asset(name, force=False):
    report = check_asset(name)
    if "ISSUES" in report and not force:
        return "NOT EXPORTED (fix issues or pass force=True)\n" + report
    col = bpy.data.collections[name]
    meshes = [o for o in col.all_objects if o.type == "MESH"]
    has_tex = any("TEX" in parse_name(o.name)[2] for o in meshes)
    bpy.ops.object.select_all(action="DESELECT")
    for o in meshes:
        o.hide_set(False)
        o.select_set(True)
    bpy.context.view_layer.objects.active = meshes[0]
    path = EXPORT_DIR + "\\" + name + ".fbx"
    wanted = dict(
        filepath=path, use_selection=True, object_types={"MESH"},
        apply_unit_scale=True, apply_scale_options="FBX_SCALE_ALL",
        axis_forward="-Z", axis_up="Y", bake_space_transform=False,
        use_mesh_modifiers=True, use_triangles=True, mesh_smooth_type="FACE",
        add_leaf_bones=False, bake_anim=False,
        path_mode="COPY" if has_tex else "AUTO", embed_textures=has_tex,
    )
    valid = {p.identifier for p in bpy.ops.export_scene.fbx.get_rna_type().properties}
    kwargs = {k: v for k, v in wanted.items() if k in valid}
    skipped = sorted(set(wanted) - valid)
    bpy.ops.export_scene.fbx(**kwargs)
    return (f"exported {path}"
            + (f"\n(skipped unsupported options: {skipped})" if skipped else "")
            + "\n" + report)
