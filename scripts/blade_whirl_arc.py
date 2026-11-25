# 칼날 회오리(단검) 회전 칼날 궤적 메시 — Vfx.BladeWhirl 의 WhirlBlade (+ 자식 Core)
# 실행: exec(open(r"D:\god\scripts\blade_whirl_arc.py", encoding="utf-8").read())
# 수평(XY) 초승달 칼날 2장이 180° 마주 봄 → 바운딩 중심 = 회전 중심 = 원점 (Roblox 에서 CFrame 회전만 하면 캐릭터를 감싸며 돎)
# 각 칼날: 바깥 날 반지름 R, 110° 호, 꼬리(뒤)는 가늘게 끌리고 앞(반시계 = Roblox 에서 +Y 축 양의 회전 = 왼쪽으로 도는 방향) 끝이 날카로움
# 단면 마름모: 바깥 날·안쪽 끝은 두께 0, 가운데 능선 두께 T. Core = 안쪽 흰 심 (폭 40%, 두께 60%, 호 조금 짧게)
import bpy, bmesh, math

COL = "BladeWhirl"
EXPORT = r"D:\god\exports\BladeWhirl.fbx"
R, W, T = 4.6, 0.55, 0.07
SPAN = math.radians(110)
PEAK = 0.82  # 가장 넓은 곳 (꼬리 0 ~ 끝 1)
STATIONS = 26


def width_at(u):
    if u <= PEAK:
        k = u / PEAK
        return 0.02 + 0.98 * (k ** 1.4)  # 꼬리에서 천천히 굵어짐 (끌리는 잔상)
    k = (1 - u) / (1 - PEAK)
    return k ** 0.8  # 끝은 짧고 날카롭게


def crescent(bm, start_angle, r_out, wscale, tscale, u0, u1):
    rings = []
    for i in range(STATIONS + 1):
        s = i / STATIONS
        u = u0 + (u1 - u0) * s
        a = start_angle + SPAN * u
        w = W * wscale * width_at(u)
        t = T * tscale * max(width_at(u), 0.2) / 2
        c, sn = math.cos(a), math.sin(a)
        if i == STATIONS:
            rings.append([bm.verts.new((r_out * c, r_out * sn, 0))])
            continue
        rm = r_out - w / 2
        ri = r_out - w
        rings.append([
            bm.verts.new((r_out * c, r_out * sn, 0)),
            bm.verts.new((rm * c, rm * sn, t)),
            bm.verts.new((ri * c, ri * sn, 0)),
            bm.verts.new((rm * c, rm * sn, -t)),
        ])
    bm.faces.new(list(reversed(rings[0])))
    for a, b in zip(rings[:-1], rings[1:]):
        if len(b) == 1:
            for j in range(4):
                bm.faces.new((a[j], a[(j + 1) % 4], b[0]))
        else:
            for j in range(4):
                bm.faces.new((a[j], a[(j + 1) % 4], b[(j + 1) % 4], b[j]))


def make(name, r_out, wscale, tscale, u0, u1):
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    for k in range(2):
        crescent(bm, -SPAN / 2 + math.pi * k, r_out, wscale, tscale, u0, u1)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(me)
    bm.free()
    return bpy.data.objects.new(name, me)


def build():
    col = bpy.data.collections.get(COL)
    if col:
        for o in list(col.objects):
            bpy.data.objects.remove(o, do_unlink=True)
    else:
        col = bpy.data.collections.new(COL)
        bpy.context.scene.collection.children.link(col)
    outer = make("WhirlBlade", R, 1.0, 1.0, 0.0, 1.0)
    core = make("Core", R - 0.06, 0.4, 0.6, 0.18, 0.97)
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


# 그림자 발걸음 칼날(ShadowStepBlade) 이 보이면 겹쳐 보이지 않게 숨김
_prev = bpy.data.collections.get("ShadowStepBlade")
if _prev:
    _prev.hide_viewport = True
_outer, _core, _tris = build()
print("BladeWhirl tris", _tris, "outer dims", tuple(round(v, 3) for v in _outer.dimensions),
      "core dims", tuple(round(v, 3) for v in _core.dimensions))
print("exported", export())
