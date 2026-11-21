# 월드 지도 Steelworks 구역용 공장 아이콘 v2 (2026-11-21, 사용자: "너무 조잡해, 상가·빌딩 그림과 비슷하게")
# Cycles(CPU) + Freestyle 잉크 선(검은 외곽선·모서리 선) + 평면 색 3단 음영, 2배로 렌더 → 합성 때 절반으로 줄여 선을 매끈하게
# exec(open(r"D:\god\scripts\steelworks_icons.py", encoding="utf-8").read()); render_all()
import bpy, bmesh, math, os
from mathutils import Vector, Matrix

ICON_DIR = r"D:\god\exports\steelworks_zone\icons"
os.makedirs(ICON_DIR, exist_ok=True)
PAL = {  # 표시색 (상가·빌딩 그림 톤)
    "wall": (0.90, 0.83, 0.68), "wall2": (0.80, 0.71, 0.55), "conc": (0.72, 0.70, 0.66),
    "roof": (0.80, 0.45, 0.28), "roof2": (0.66, 0.35, 0.22), "teal": (0.42, 0.56, 0.58), "slate": (0.48, 0.50, 0.55),
    "metal": (0.66, 0.66, 0.64), "rust": (0.62, 0.34, 0.20), "rust2": (0.45, 0.24, 0.15), "dark": (0.16, 0.14, 0.13),
    "window": (0.30, 0.38, 0.45), "coal": (0.22, 0.21, 0.21), "yellow": (0.90, 0.68, 0.25), "brick": (0.70, 0.36, 0.25),
    "blue": (0.36, 0.50, 0.66), "olive": (0.50, 0.56, 0.34), "green": (0.42, 0.55, 0.32),
}
SHADE = (1.0, 0.84, 0.66)       # 위 / 빛 받는 면 / 그늘 면
LIGHT = Vector((-0.55, -0.35, 0.76)).normalized()
INK = (0.05, 0.04, 0.035)


def srgb_to_lin(c):
    return tuple(((x + 0.055) / 1.055) ** 2.4 if x > 0.04045 else x / 12.92 for x in c)


def scene():
    sc = bpy.data.scenes.get("ZoneIcons") or bpy.data.scenes.new("ZoneIcons")
    bpy.context.window.scene = sc
    for o in list(sc.collection.objects):
        if o.name != "ZI_Cam":
            bpy.data.objects.remove(o, do_unlink=True)
    try:
        sc.render.engine = 'CYCLES'          # 이 PC 는 EEVEE(GPU)가 몇 장 뒤부터 검게 나옴 → Cycles CPU
        sc.cycles.device = 'CPU'; sc.cycles.samples = 12; sc.cycles.use_denoising = False
        sc.cycles.max_bounces = 0
    except (TypeError, AttributeError):
        sc.render.engine = 'BLENDER_EEVEE'
    sc.render.film_transparent = True
    try:
        sc.view_settings.view_transform = 'Standard'
    except TypeError:
        pass
    sc.view_settings.look = 'None'; sc.view_settings.exposure = 0; sc.view_settings.gamma = 1
    sc.render.image_settings.file_format = 'PNG'; sc.render.image_settings.color_mode = 'RGBA'
    sc.render.resolution_percentage = 100
    sc.render.use_freestyle = True
    sc.render.line_thickness_mode = 'ABSOLUTE'; sc.render.line_thickness = 2.0
    vl = sc.view_layers[0]; vl.use_freestyle = True
    fs = vl.freestyle_settings; fs.crease_angle = math.radians(140)
    ls = fs.linesets[0] if fs.linesets else fs.linesets.new("Ink")
    ls.select_by_visibility = True; ls.visibility = 'VISIBLE'
    ls.select_by_edge_types = True
    ls.select_silhouette = True; ls.select_border = True; ls.select_crease = True; ls.select_external_contour = True
    ls.linestyle.color = srgb_to_lin(INK); ls.linestyle.thickness = 2.0
    # 창문·문 같은 작은 디테일은 선 없이 색만 (선이 너무 빽빽해지지 않게)
    noink = bpy.data.collections.get("ZI_NoInk") or bpy.data.collections.new("ZI_NoInk")
    if noink.name not in [c.name for c in sc.collection.children]:
        sc.collection.children.link(noink)
    for o in list(noink.objects):
        bpy.data.objects.remove(o, do_unlink=True)
    ls.select_by_collection = True; ls.collection = noink; ls.collection_negation = 'EXCLUSIVE'
    cam = bpy.data.objects.get("ZI_Cam")
    if cam is None:
        cam = bpy.data.objects.new("ZI_Cam", bpy.data.cameras.new("ZI_Cam"))
    if cam.name not in sc.collection.objects:
        sc.collection.objects.link(cam)
    cam.data.type = 'ORTHO'
    sc.camera = cam
    if sc.world is None:
        sc.world = bpy.data.worlds.new("ZI_World")
    return sc, cam


def mat(key, level=0):
    name = "ZI2_%s_%d" % (key, level)
    m = bpy.data.materials.get(name)
    if m is None:
        m = bpy.data.materials.new(name); m.use_nodes = True
        nt = m.node_tree
        for n in list(nt.nodes):
            nt.nodes.remove(n)
        em = nt.nodes.new("ShaderNodeEmission"); out = nt.nodes.new("ShaderNodeOutputMaterial")
        nt.links.new(em.outputs[0], out.inputs[0])
        c = srgb_to_lin(tuple(min(1.0, x * SHADE[level]) for x in PAL[key]))
        em.inputs[0].default_value = (c[0], c[1], c[2], 1); em.inputs[1].default_value = 1.0
    return m


def add(sc, bm, key, name="p"):
    bm.normal_update()
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(name, me)
    if key in ("window", "dark"):
        bpy.data.collections["ZI_NoInk"].objects.link(o)
    else:
        sc.collection.objects.link(o)
    for lv in range(3):
        me.materials.append(mat(key, lv))
    for p in me.polygons:
        n = p.normal
        p.material_index = 0 if n.z > 0.55 else (1 if n.dot(LIGHT) > 0.05 else 2)
    return o


def box(sc, c, s, key, rot=0.0):
    bm = bmesh.new(); bmesh.ops.create_cube(bm, size=1.0)
    R = Matrix.Rotation(rot, 3, 'Z')
    for v in bm.verts:
        v.co = R @ Vector((v.co.x * s[0], v.co.y * s[1], v.co.z * s[2])) + Vector(c)
    return add(sc, bm, key)


def cyl(sc, c, r, h, key, r2=None, seg=20):
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=seg, radius1=r, radius2=r if r2 is None else r2, depth=h)
    for v in bm.verts:
        v.co += Vector((c[0], c[1], c[2] + h / 2))
    return add(sc, bm, key)


def dome(sc, c, r, key, seg=16):
    bm = bmesh.new(); bmesh.ops.create_uvsphere(bm, u_segments=seg, v_segments=8, radius=r)
    bmesh.ops.delete(bm, geom=[v for v in bm.verts if v.co.z < -1e-4], context='VERTS')
    for v in bm.verts:
        v.co += Vector(c)
    return add(sc, bm, key)


def rodv(sc, a, b, r, key, seg=10):
    a, b = Vector(a), Vector(b); d = b - a; L = d.length
    bm = bmesh.new(); bmesh.ops.create_cone(bm, cap_ends=True, segments=seg, radius1=r, radius2=r, depth=L)
    R = d.to_track_quat('Z', 'Y').to_matrix()
    for v in bm.verts:
        v.co = R @ v.co + (a + b) / 2
    return add(sc, bm, key)


def windows_front(sc, x0, x1, y, z0, z1, n, rows=1, w=0.5, h=0.6):
    """앞면(-y)에 창문 n개 × rows 줄"""
    for r in range(rows):
        z = z0 + (z1 - z0) * (r + 0.5) / rows
        for i in range(n):
            x = x0 + (x1 - x0) * (i + 0.5) / n
            box(sc, (x, y - 0.03, z), (w, 0.06, h), "window")


def gable(sc, c, w, d, h, rh, wall, roof):
    box(sc, (c[0], c[1], c[2] + h / 2), (w, d, h), wall)
    bm = bmesh.new()
    o = 0.2
    pts = [(-w / 2 - o, -d / 2 - o, h), (w / 2 + o, -d / 2 - o, h), (w / 2 + o, 0, h + rh), (-w / 2 - o, 0, h + rh),
           (-w / 2 - o, d / 2 + o, h), (w / 2 + o, d / 2 + o, h)]
    vs = [bm.verts.new(Vector(p) + Vector(c)) for p in pts]
    bm.faces.new((vs[0], vs[1], vs[2], vs[3])); bm.faces.new((vs[3], vs[2], vs[5], vs[4]))
    bm.faces.new((vs[0], vs[3], vs[4])); bm.faces.new((vs[1], vs[5], vs[2])); bm.faces.new((vs[0], vs[4], vs[5], vs[1]))
    add(sc, bm, roof)
    # 박공 벽 삼각형 (양 끝)
    for sx in (-1, 1):
        bm = bmesh.new()
        tri = [bm.verts.new(Vector((sx * w / 2, -d / 2, h)) + Vector(c)), bm.verts.new(Vector((sx * w / 2, d / 2, h)) + Vector(c)),
               bm.verts.new(Vector((sx * w / 2, 0, h + rh - 0.05)) + Vector(c))]
        bm.faces.new(tri); add(sc, bm, wall)


# ---------------- 아이콘 ----------------
def furnace(sc):
    cyl(sc, (0, 0, 0), 2.8, 1.2, "conc")
    cyl(sc, (0, 0, 1.2), 2.2, 6.2, "rust", r2=1.7)
    for z in (2.8, 4.6, 6.4):
        cyl(sc, (0, 0, z), 2.35 - (z - 1.2) * 0.08, 0.3, "rust2")
    cyl(sc, (0, 0, 7.4), 1.7, 1.6, "rust", r2=0.9)
    box(sc, (0, 0, 9.4), (1.2, 1.2, 2.4), "rust2")
    for x in (-0.5, 0.5):
        rodv(sc, (x, 0, 10.6), (x, 0, 12.0), 0.22, "rust2")
    rodv(sc, (-0.5, 0, 11.9), (0.5, 0, 11.9), 0.22, "rust2")
    for i, x in enumerate((-6.6, -4.4)):          # 열풍로 2기 (돔 지붕)
        cyl(sc, (x, 2.2, 0), 1.15, 7.0, "metal")
        dome(sc, (x, 2.2, 7.0), 1.15, "metal")
        for z in (2.3, 4.6):
            cyl(sc, (x, 2.2, z), 1.2, 0.22, "slate")
    rodv(sc, (-6.6, 2.2, 5.2), (-1.8, 0.8, 5.2), 0.4, "rust")     # 열풍관
    rodv(sc, (1.2, 0, 10.2), (4.4, 1.2, 6.2), 0.45, "rust")      # 하강관
    cyl(sc, (4.6, 1.4, 0), 0.9, 6.2, "rust2", r2=0.9)            # 집진기
    cyl(sc, (4.6, 1.4, 6.2), 0.9, 0.9, "rust2", r2=0.2)
    gable(sc, (0, -3.6, 0), 6.4, 3.0, 2.8, 1.0, "wall", "roof")   # 주상
    windows_front(sc, -2.6, 2.6, -5.1, 1.0, 2.2, 4)
    box(sc, (1.9, -5.12, 0.85), (0.9, 0.06, 1.6), "dark")
    # 스킵 경사 다리 (노랑 트러스)
    rodv(sc, (8.6, -1.2, 0.2), (1.4, -0.4, 8.6), 0.3, "yellow")
    rodv(sc, (8.6, -0.2, 0.2), (1.4, 0.4, 8.6), 0.3, "yellow")
    for t in (0.2, 0.45, 0.7):
        a = Vector((8.6, -1.2, 0.2)).lerp(Vector((1.4, -0.4, 8.6)), t); b = Vector((8.6, -0.2, 0.2)).lerp(Vector((1.4, 0.4, 8.6)), t)
        rodv(sc, a, b, 0.14, "yellow")


def chimneys(sc):
    box(sc, (0, 0, 1.1), (5.6, 2.6, 2.2), "wall2")
    windows_front(sc, -2.2, 2.2, -1.3, 0.6, 1.6, 4)
    for x, h in ((-1.5, 12.5), (1.4, 10.5)):
        cyl(sc, (x, 0.3, 2.2), 0.8, h - 2.2, "brick", r2=0.55)
        for z in (h - 1.0, h - 3.0):
            cyl(sc, (x, 0.3, z), 0.62, 0.35, "dark")
        cyl(sc, (x, 0.3, h), 0.6, 0.25, "dark")


def cooling(sc):
    for x, y in ((-2.5, 0.8), (2.5, -0.8)):
        bm = bmesh.new(); seg, rings = 24, 8; rows = []
        for i in range(rings + 1):
            t = i / rings; z = 8.0 * t
            r = 2.5 - 2.2 * t + 1.5 * t * t
            rows.append([bm.verts.new((x + math.cos(2 * math.pi * k / seg) * r, y + math.sin(2 * math.pi * k / seg) * r, z)) for k in range(seg)])
        for i in range(rings):
            for k in range(seg):
                k2 = (k + 1) % seg
                bm.faces.new((rows[i][k], rows[i][k2], rows[i + 1][k2], rows[i + 1][k]))
        bm.faces.new(list(reversed(rows[0])))
        add(sc, bm, "wall")
        cyl(sc, (x, y, 7.95), 1.75, 0.12, "dark")
        for k in range(8):                       # 아래 기둥 줄무늬
            a = 2 * math.pi * k / 8
            box(sc, (x + math.cos(a) * 2.45, y + math.sin(a) * 2.45, 0.4), (0.25, 0.25, 0.8), "slate")


def gasholder(sc):
    cyl(sc, (0, 0, 0), 3.0, 5.6, "metal", seg=24)
    dome(sc, (0, 0, 5.6), 3.0, "metal", seg=24)
    for k in range(6):
        a = 2 * math.pi * (k + 0.5) / 6
        box(sc, (math.cos(a) * 3.3, math.sin(a) * 3.3, 3.9), (0.4, 0.4, 7.8), "rust")
    cyl(sc, (0, 0, 7.6), 3.38, 0.3, "rust", seg=24)


def shed_factory(roof, w=9.0, d=4.0):
    def f(sc):
        gable(sc, (0, 0, 0), w, d, 2.6, 1.2, "wall", roof)
        windows_front(sc, -w / 2 + 0.8, w / 2 - 2.0, -d / 2, 1.0, 2.0, int(w / 1.6))
        box(sc, (w / 2 - 1.0, -d / 2 - 0.03, 1.0), (1.2, 0.06, 2.0), "dark")
    return f


def sawshed(sc, w=11.0):
    box(sc, (0, 0, 1.4), (w, 5.0, 2.8), "wall")
    n = 5
    for i in range(n):
        x0 = -w / 2 + i * w / n
        bm = bmesh.new()
        pts = [(x0, -2.6, 2.8), (x0 + w / n, -2.6, 2.8), (x0 + w / n, -2.6, 4.1), (x0, 2.6, 2.8), (x0 + w / n, 2.6, 2.8), (x0 + w / n, 2.6, 4.1)]
        vs = [bm.verts.new(p) for p in pts]
        bm.faces.new((vs[0], vs[1], vs[2])); bm.faces.new((vs[3], vs[5], vs[4]))
        bm.faces.new((vs[0], vs[2], vs[5], vs[3])); bm.faces.new((vs[1], vs[4], vs[5], vs[2])); bm.faces.new((vs[0], vs[3], vs[4], vs[1]))
        add(sc, bm, "teal")
        box(sc, (x0 + w / n - 0.05, 0, 3.45), (0.08, 4.6, 1.0), "window")
    windows_front(sc, -w / 2 + 0.6, w / 2 - 2.2, -2.5, 0.9, 2.0, 6)
    box(sc, (w / 2 - 1.2, -2.53, 1.1), (1.5, 0.06, 2.2), "dark")


def house(roof):
    def f(sc):
        gable(sc, (0, 0, 0), 3.6, 2.8, 2.0, 1.2, "wall", roof)
        box(sc, (0.8, -1.43, 0.75), (0.65, 0.06, 1.3), "dark")
        box(sc, (-0.7, -1.43, 1.25), (0.7, 0.06, 0.6), "window")
        box(sc, (-1.0, 0.6, 3.0), (0.4, 0.4, 1.2), "brick")
    return f


def office(sc):
    box(sc, (0, 0, 2.6), (6.0, 3.6, 5.2), "wall2")
    box(sc, (0, 0, 5.3), (6.3, 3.9, 0.25), "slate")
    windows_front(sc, -2.6, 2.6, -1.8, 0.6, 4.6, 5, rows=3)
    box(sc, (1.6, 1.0, 6.0), (1.2, 1.2, 1.2), "metal")       # 옥상 물탱크


def crane(sc):
    for x in (-1.8, 1.8):
        for y in (-1.3, 1.3):
            box(sc, (x, y, 3.4), (0.7, 0.7, 6.8), "yellow")
    box(sc, (0, 0, 7.1), (4.4, 3.4, 0.8), "yellow")
    box(sc, (0.6, 0, 8.2), (2.0, 1.8, 1.5), "wall")
    box(sc, (-4.4, 0, 8.0), (11.0, 0.9, 0.8), "yellow")
    box(sc, (-8.8, 0, 5.9), (0.25, 0.25, 3.4), "dark")
    box(sc, (-8.8, 0, 4.0), (0.9, 0.9, 0.6), "dark")


def coal(sc):
    bm = bmesh.new(); bmesh.ops.create_uvsphere(bm, u_segments=18, v_segments=8, radius=1.0)
    for v in bm.verts:
        v.co = Vector((v.co.x * 4.2, v.co.y * 2.4, max(0.0, v.co.z) * 1.9))
    add(sc, bm, "coal")


def tanks(sc):
    for x, y in ((-1.7, 0.7), (1.7, 0.7), (0, -1.3)):
        cyl(sc, (x, y, 0), 1.3, 2.4, "metal")
        dome(sc, (x, y, 2.4), 1.3, "metal")
        cyl(sc, (x, y, 1.2), 1.34, 0.18, "slate")


def containers(sc):
    for (x, y, z, key) in ((-1.5, 0, 0, "rust"), (1.5, 0, 0, "blue"), (0, 0.1, 1.3, "olive"), (-1.5, 2.2, 0, "blue"), (1.5, 2.2, 0, "rust2")):
        box(sc, (x, y, z + 0.65), (2.8, 1.3, 1.3), key)


def silo(sc):
    for x in (-1.2, 1.2):
        cyl(sc, (x, 0, 0), 1.1, 6.0, "conc")
        cyl(sc, (x, 0, 6.0), 1.1, 1.0, "conc", r2=0.3)
    box(sc, (0, 0, 6.8), (1.4, 1.0, 1.0), "rust")


def tree(sc):
    cyl(sc, (0, 0, 0), 0.18, 1.0, "rust2")
    bm = bmesh.new(); bmesh.ops.create_uvsphere(bm, u_segments=10, v_segments=6, radius=1.0)
    for v in bm.verts:
        v.co = Vector((v.co.x, v.co.y, v.co.z * 0.9)) + Vector((0, 0, 1.6))
    add(sc, bm, "green")


ICONS = {"furnace": furnace, "chimneys": chimneys, "cooling": cooling, "gasholder": gasholder,
         "shed_o": shed_factory("roof"), "shed_r": shed_factory("roof2"), "shed_t": shed_factory("teal", 8.0, 3.6),
         "shed_s": shed_factory("slate", 7.0, 3.4), "sawshed": sawshed, "house_o": house("roof"), "house_r": house("roof2"),
         "house_t": house("teal"), "office": office, "crane": crane, "coal": coal, "tanks": tanks, "containers": containers,
         "silo": silo, "tree": tree}
PPU = 4.0      # 최종 지도 픽셀 / 단위 (렌더는 2배)
ELEV = math.radians(36); YAW = math.radians(-20)


def render_icon(name):
    sc, cam = scene()
    ICONS[name](sc)
    d = Vector((math.sin(YAW) * math.cos(ELEV), -math.cos(YAW) * math.cos(ELEV), math.sin(ELEV)))
    q = (-d).to_track_quat('-Z', 'Y')
    right = q @ Vector((1, 0, 0)); up = q @ Vector((0, 1, 0))
    us = []; vs = []
    for o in sc.collection.all_objects:
        if o.type == 'MESH':
            for v in o.data.vertices:
                us.append(v.co.dot(right)); vs.append(v.co.dot(up))
    m = 0.8
    u0, u1, v0, v1 = min(us) - m, max(us) + m, min(vs) - m, max(vs) + m
    k = PPU * 2
    wpx = max(8, int(round((u1 - u0) * k))); hpx = max(8, int(round((v1 - v0) * k)))
    wpx += wpx % 2; hpx += hpx % 2
    u1 = u0 + wpx / k; v1 = v0 + hpx / k
    cam.location = right * ((u0 + u1) / 2) + up * ((v0 + v1) / 2) + d * 80
    cam.rotation_euler = q.to_euler()
    cam.data.ortho_scale = max(wpx, hpx) / k
    sc.render.resolution_x, sc.render.resolution_y = wpx, hpx
    sc.render.filepath = os.path.join(ICON_DIR, name + ".png")
    bpy.ops.render.render(write_still=True, scene=sc.name)
    return name, wpx // 2, hpx // 2


def render_all(names=None):
    prev = bpy.context.window.scene
    out = [render_icon(n) for n in (names or ICONS.keys())]
    bpy.context.window.scene = prev
    return out
