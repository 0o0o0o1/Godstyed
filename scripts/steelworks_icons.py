# 월드 지도 Steelworks 구역용 공장 아이콘 (Blender Workbench 렌더, 투명 배경 PNG)
# exec(open(r"D:\god\scripts\steelworks_icons.py", encoding="utf-8").read()); render_all()
import bpy, bmesh, math, os
from mathutils import Vector, Matrix

ICON_DIR = r"D:\god\exports\steelworks_zone\icons"
os.makedirs(ICON_DIR, exist_ok=True)
PAL = {  # 상가 구역 그림에서 뽑은 색 (선형 아님, 표시색) → Workbench 재질색
    "wall": (0.86, 0.79, 0.64), "wall2": (0.76, 0.67, 0.50), "roof": (0.75, 0.48, 0.33), "roof2": (0.61, 0.39, 0.26),
    "metal": (0.60, 0.57, 0.52), "rust": (0.58, 0.36, 0.24), "dark": (0.27, 0.21, 0.16), "smoke": (0.88, 0.86, 0.82),
    "coal": (0.30, 0.27, 0.25), "yellow": (0.80, 0.62, 0.30), "brick": (0.62, 0.36, 0.27),
    "blue": (0.42, 0.52, 0.58), "olive": (0.52, 0.55, 0.38),
}


def srgb_to_lin(c):
    return tuple(((x + 0.055) / 1.055) ** 2.4 if x > 0.04045 else x / 12.92 for x in c)


def scene():
    sc = bpy.data.scenes.get("ZoneIcons") or bpy.data.scenes.new("ZoneIcons")
    bpy.context.window.scene = sc
    for o in list(sc.collection.objects):
        bpy.data.objects.remove(o, do_unlink=True)
    sc.render.engine = 'BLENDER_WORKBENCH'
    d = sc.display.shading
    d.light = 'FLAT'; d.color_type = 'MATERIAL'
    d.show_object_outline = True; d.object_outline_color = srgb_to_lin((0.24, 0.17, 0.11))
    d.show_cavity = False
    d.show_shadows = False; d.show_specular_highlight = False
    sc.render.film_transparent = True
    sc.display_settings.display_device = 'sRGB'
    try:
        sc.view_settings.view_transform = 'Standard'
    except TypeError:
        pass
    sc.render.image_settings.file_format = 'PNG'; sc.render.image_settings.color_mode = 'RGBA'
    sc.render.resolution_percentage = 100
    cam = bpy.data.objects.get("ZI_Cam")
    if cam is None:
        cam = bpy.data.objects.new("ZI_Cam", bpy.data.cameras.new("ZI_Cam"))
    if cam.name not in sc.collection.objects:
        sc.collection.objects.link(cam)
    cam.data.type = 'ORTHO'
    sc.camera = cam
    return sc, cam


SHADE = (1.0, 0.86, 0.70)     # 툰 3단: 위·빛 받는 면·그늘 면
LIGHT = Vector((-0.55, -0.35, 0.76)).normalized()


def mat(key, level=0):
    m = bpy.data.materials.get("ZI_%s_%d" % (key, level)) or bpy.data.materials.new("ZI_%s_%d" % (key, level))
    c = srgb_to_lin(tuple(min(1.0, x * SHADE[level]) for x in PAL[key]))
    m.diffuse_color = (c[0], c[1], c[2], 1)
    return m


def add(sc, bm, key, name="p"):
    bm.normal_update()
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(name, me); sc.collection.objects.link(o)
    for lv in range(3):
        me.materials.append(mat(key, lv))
    for p in me.polygons:
        n = p.normal
        if n.z > 0.55: p.material_index = 0
        elif n.dot(LIGHT) > 0.05: p.material_index = 1
        else: p.material_index = 2
    return o


def box(sc, c, s, key, rot=0.0):
    bm = bmesh.new(); bmesh.ops.create_cube(bm, size=1.0)
    for v in bm.verts:
        v.co = Matrix.Rotation(rot, 3, 'Z') @ Vector((v.co.x * s[0], v.co.y * s[1], v.co.z * s[2])) + Vector(c)
    return add(sc, bm, key)


def cyl(sc, c, r, h, key, r2=None, seg=20):
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=seg, radius1=r, radius2=r if r2 is None else r2, depth=h)
    for v in bm.verts:
        v.co += Vector((c[0], c[1], c[2] + h / 2))
    return add(sc, bm, key)


def hyper(sc, c, r0, rm, r1, h, key, seg=24, rings=8):
    """냉각탑 (쌍곡선 단면)"""
    bm = bmesh.new(); rows = []
    for i in range(rings + 1):
        t = i / rings; z = h * t
        r = (1 - t) ** 2 * r0 + 2 * (1 - t) * t * (rm * 2 - (r0 + r1) / 2) + t * t * r1
        rows.append([bm.verts.new((c[0] + math.cos(2 * math.pi * k / seg) * r, c[1] + math.sin(2 * math.pi * k / seg) * r, c[2] + z)) for k in range(seg)])
    for i in range(rings):
        for k in range(seg):
            k2 = (k + 1) % seg
            bm.faces.new((rows[i][k], rows[i][k2], rows[i + 1][k2], rows[i + 1][k]))
    bm.faces.new(list(reversed(rows[0])))
    return add(sc, bm, key)


def gable(sc, c, w, d, h, rh, wall, roof, rot=0.0):
    """박공 지붕 창고 (x 폭 w, y 깊이 d)"""
    box(sc, (c[0], c[1], c[2] + h / 2), (w, d, h), wall, rot)
    bm = bmesh.new()
    pts = [(-w / 2 - 0.15, -d / 2 - 0.15, h), (w / 2 + 0.15, -d / 2 - 0.15, h), (w / 2 + 0.15, 0, h + rh), (-w / 2 - 0.15, 0, h + rh),
           (-w / 2 - 0.15, d / 2 + 0.15, h), (w / 2 + 0.15, d / 2 + 0.15, h)]
    R = Matrix.Rotation(rot, 3, 'Z')
    vs = [bm.verts.new(R @ Vector(p) + Vector(c)) for p in pts]
    bm.faces.new((vs[0], vs[1], vs[2], vs[3])); bm.faces.new((vs[3], vs[2], vs[5], vs[4]))
    bm.faces.new((vs[0], vs[3], vs[4])); bm.faces.new((vs[1], vs[5], vs[2]))
    bm.faces.new((vs[0], vs[4], vs[5], vs[1]))
    add(sc, bm, roof)


def smoke(sc, c, n=3, r=0.55):
    for i in range(n):
        bm = bmesh.new(); bmesh.ops.create_uvsphere(bm, u_segments=12, v_segments=7, radius=r * (1 + 0.3 * i))
        for v in bm.verts:
            v.co += Vector((c[0] + i * 0.75, c[1] - i * 0.25, c[2] + i * 0.8))
        add(sc, bm, "smoke")


# ---------------- 아이콘 정의 (단위: 아이콘 하나 = 대략 10~14 단위 폭) ----------------
def furnace(sc):
    cyl(sc, (0, 0, 0), 2.4, 1.0, "wall2")
    cyl(sc, (0, 0, 1.0), 1.9, 6.5, "rust", r2=1.6)
    cyl(sc, (0, 0, 7.5), 1.6, 1.4, "rust", r2=0.9)
    cyl(sc, (0, 0, 8.9), 0.45, 2.2, "dark")
    for x in (-4.6, -3.0, 3.4):      # 열풍로
        cyl(sc, (x, 1.6, 0), 1.0, 6.8, "metal")
        cyl(sc, (x, 1.6, 6.8), 1.0, 0.6, "metal", r2=0.4)
    box(sc, (0, -2.6, 1.4), (5.0, 2.4, 2.8), "wall")
    gable(sc, (0, -2.6, 0), 5.2, 2.6, 2.8, 1.0, "wall", "roof")
    for a, b in ((Vector((0.9, 0, 9.5)), Vector((2.9, 0.6, 7.2))), (Vector((-0.9, 0, 9.5)), Vector((-3.0, 1.6, 7.0)))):  # 가스관
        d = b - a; L = d.length
        bm = bmesh.new(); bmesh.ops.create_cone(bm, cap_ends=True, segments=10, radius1=0.32, radius2=0.32, depth=L)
        R = d.to_track_quat('Z', 'Y').to_matrix()
        for v in bm.verts:
            v.co = R @ v.co + (a + b) / 2
        add(sc, bm, "rust")
    # 경사 컨베이어 (스킵): 땅 → 노정
    a, b = Vector((7.5, -0.6, 0.3)), Vector((1.6, -0.3, 7.6))
    d = b - a; L = d.length
    bm = bmesh.new(); bmesh.ops.create_cube(bm, size=1.0)
    R = d.to_track_quat('Z', 'Y').to_matrix()
    for v in bm.verts:
        v.co = R @ Vector((v.co.x * 0.9, v.co.y * 0.6, v.co.z * L)) + (a + b) / 2
    add(sc, bm, "yellow")
    smoke(sc, (0.3, 0, 11.6), 3, 0.7)


def chimneys(sc):
    for x, h in ((-1.3, 11.0), (1.3, 9.0)):
        cyl(sc, (x, 0, 0), 0.75, h, "brick", r2=0.55)
        cyl(sc, (x, 0, h - 1.2), 0.62, 0.35, "dark")
        smoke(sc, (x + 0.4, 0, h + 0.8), 3, 0.6)
    box(sc, (0, 0, 0.6), (4.6, 2.0, 1.2), "wall2")


def cooling(sc):
    for x, y in ((-2.2, 0.6), (2.2, -0.6)):
        hyper(sc, (x, y, 0), 2.2, 1.4, 1.6, 7.0, "wall")
        cyl(sc, (x, y, 6.95), 1.62, 0.1, "dark")
        smoke(sc, (x, y, 7.8), 3, 1.0)


def gasholder(sc):
    cyl(sc, (0, 0, 0), 2.8, 5.5, "metal", seg=24)
    cyl(sc, (0, 0, 5.5), 2.8, 0.8, "metal", r2=2.2, seg=24)
    for k in range(10):
        a = 2 * math.pi * k / 10
        box(sc, (math.cos(a) * 3.0, math.sin(a) * 3.0, 3.6), (0.25, 0.25, 7.2), "rust")
    for z in (2.4, 4.8, 7.0):
        cyl(sc, (0, 0, z), 3.08, 0.18, "rust", seg=24)


def shed(sc, w=9.0):
    gable(sc, (0, 0, 0), w, 3.6, 2.4, 1.1, "wall", "roof")
    box(sc, (w / 2 - 0.9, -1.9, 1.0), (1.2, 0.1, 1.8), "dark")
    for x in (-w / 2 + 1.5, -w / 2 + 3.2, -w / 2 + 4.9):
        box(sc, (x, -1.82, 1.5), (0.8, 0.05, 0.5), "dark")


def sawshed(sc, w=10.0):
    box(sc, (0, 0, 1.3), (w, 4.4, 2.6), "wall")
    n = 5
    for i in range(n):
        x0 = -w / 2 + i * w / n
        bm = bmesh.new()
        pts = [(x0, -2.3, 2.6), (x0 + w / n, -2.3, 2.6), (x0 + w / n, -2.3, 3.8), (x0, 2.3, 2.6), (x0 + w / n, 2.3, 2.6), (x0 + w / n, 2.3, 3.8)]
        vs = [bm.verts.new(p) for p in pts]
        bm.faces.new((vs[0], vs[1], vs[2])); bm.faces.new((vs[3], vs[5], vs[4]))
        bm.faces.new((vs[0], vs[2], vs[5], vs[3])); bm.faces.new((vs[1], vs[4], vs[5], vs[2])); bm.faces.new((vs[0], vs[3], vs[4], vs[1]))
        add(sc, bm, "roof2" if i % 2 else "roof")
    box(sc, (-w / 2 + 1.2, -2.25, 1.0), (1.4, 0.1, 1.9), "dark")


def crane(sc):
    for x in (-1.2, 1.2):
        for y in (-1.0, 1.0):
            box(sc, (x, y, 3.0), (0.3, 0.3, 6.0), "yellow")
    box(sc, (0, 0, 6.2), (3.0, 2.6, 0.5), "yellow")
    box(sc, (0, 0, 7.0), (1.6, 1.4, 1.2), "wall")
    box(sc, (-3.0, 0, 6.9), (9.0, 0.5, 0.45), "yellow")
    box(sc, (-6.8, 0, 4.6), (0.08, 0.08, 4.5), "dark")
    box(sc, (-6.8, 0, 2.3), (0.6, 0.6, 0.4), "dark")


def coal(sc):
    bm = bmesh.new(); bmesh.ops.create_uvsphere(bm, u_segments=16, v_segments=8, radius=1.0)
    for v in bm.verts:
        v.co = Vector((v.co.x * 3.6, v.co.y * 2.2, max(0.0, v.co.z) * 1.6))
    add(sc, bm, "coal")


def tanks(sc):
    for x, y in ((-1.5, 0.6), (1.5, 0.6), (0, -1.2)):
        cyl(sc, (x, y, 0), 1.2, 2.2, "metal")
        cyl(sc, (x, y, 2.2), 1.2, 0.4, "metal", r2=0.6)


def house(sc):
    gable(sc, (0, 0, 0), 3.4, 2.6, 1.8, 1.0, "wall", "roof")
    box(sc, (0.7, -1.32, 0.7), (0.6, 0.05, 1.2), "dark")
    box(sc, (-0.6, -1.32, 1.1), (0.6, 0.05, 0.5), "dark")


def containers(sc):
    for (x, y, z, key) in ((-1.4, 0, 0, "rust"), (1.4, 0, 0, "blue"), (0, 0.2, 1.3, "olive"), (-1.4, 2.0, 0, "blue")):
        box(sc, (x, y, z + 0.65), (2.6, 1.2, 1.3), key)


ICONS = {"house": house, "containers": containers, "furnace": furnace, "chimneys": chimneys, "cooling": cooling, "gasholder": gasholder, "shed": shed,
         "shed2": sawshed, "crane": crane, "coal": coal, "tanks": tanks}
PPU = 3.0   # 지도 1024×746 에서 아이콘 1 단위 = 3 px (상가 집 아이콘 ≈ 14 px 와 맞춤)
ELEV = math.radians(34); YAW = math.radians(-22)


def render_icon(name):
    sc, cam = scene()
    ICONS[name](sc)
    d = Vector((math.sin(YAW) * math.cos(ELEV), -math.cos(YAW) * math.cos(ELEV), math.sin(ELEV)))
    q = (-d).to_track_quat('-Z', 'Y')
    right = q @ Vector((1, 0, 0)); up = q @ Vector((0, 1, 0))
    us = []; vs = []
    for o in sc.collection.objects:
        if o.type == 'MESH':
            for v in o.data.vertices:
                us.append(v.co.dot(right)); vs.append(v.co.dot(up))
    m = 0.6
    u0, u1, v0, v1 = min(us) - m, max(us) + m, min(vs) - m, max(vs) + m
    wpx = max(4, int(round((u1 - u0) * PPU))); hpx = max(4, int(round((v1 - v0) * PPU)))
    u1 = u0 + wpx / PPU; v1 = v0 + hpx / PPU
    ctr = right * ((u0 + u1) / 2) + up * ((v0 + v1) / 2)
    cam.location = ctr + d * 80
    cam.rotation_euler = q.to_euler()
    cam.data.ortho_scale = max(wpx, hpx) / PPU
    sc.render.resolution_x, sc.render.resolution_y = wpx, hpx
    sc.render.filepath = os.path.join(ICON_DIR, name + ".png")
    bpy.ops.render.render(write_still=True, scene=sc.name)
    return sc.render.filepath


def render_all(names=None):
    prev = bpy.context.window.scene
    out = [render_icon(n) for n in (names or ICONS.keys())]
    bpy.context.window.scene = prev
    return out
