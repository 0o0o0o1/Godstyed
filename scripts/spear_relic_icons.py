# 창 성유물 아이콘 5개 — 기존 성유물 아이콘(빛나는 룬이 새겨진 회색 돌판 + 가장자리 빛 + 주변 반짝이, 무기마다 룬 색)과 같은 스타일,
# 창 색 = 초록. 스킬마다 돌 모양·룬이 다름. → exports/icons/Relic_<id>.png (512x512, 투명 배경)
#   관통 돌격: 끝이 뾰족한 오벨리스크 + 위로 꿰뚫는 창 룬     사슬 갈고리: 둥근 돌판 + 갈고리·고리 룬
#   도약 찌르기: 비스듬히 깨진 조각 + 포물선·내리꽂는 룬       창 휘두르기: 둥근 원반 + 회오리 룬
#   신의 창: 마름모(연) 모양 + 빛살 속 내리꽂는 창 룬
# 실행: D:\blender.exe -b --factory-startup --python D:\god\scripts\spear_relic_icons.py
import bpy, bmesh, math, os, random
from mathutils import Vector

OUT = r"D:\god\exports\icons"
SIZE = 512
os.makedirs(OUT, exist_ok=True)
GREEN = (0.2, 1.0, 0.38, 1)
GREEN_SOFT = (0.62, 1.0, 0.7, 1)
RIM = (0.45, 1.0, 0.55, 1)  # 테두리 빛도 초록 (1차 흰색은 밋밋)


def clear():
    for o in list(bpy.data.objects):
        if o.type not in ("CAMERA", "LIGHT"):
            bpy.data.objects.remove(o, do_unlink=True)
    for m in list(bpy.data.meshes):
        if m.users == 0:
            bpy.data.meshes.remove(m)


def setup():
    for o in list(bpy.data.objects):
        bpy.data.objects.remove(o, do_unlink=True)
    sc = bpy.context.scene
    try:
        sc.render.engine = "CYCLES"
    except TypeError:
        pass
    sc.cycles.samples = 64
    sc.cycles.use_denoising = True
    sc.render.film_transparent = True
    sc.render.resolution_x = sc.render.resolution_y = SIZE
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGBA"
    sc.view_settings.view_transform = "Standard"
    cam_data = bpy.data.cameras.new("Cam")
    cam_data.type = "ORTHO"
    cam_data.ortho_scale = 2.2
    cam = bpy.data.objects.new("Cam", cam_data)
    cam.location = (0, 0, 6)
    sc.collection.objects.link(cam)
    sc.camera = cam
    # 왼쪽 위에서 비추는 빛 + 약한 주변광 (돌의 굴곡·가장자리 밝기)
    sun = bpy.data.lights.new("Key", "SUN")
    sun.energy = 2.4
    sun.angle = math.radians(8)
    so = bpy.data.objects.new("Key", sun)
    so.rotation_euler = (math.radians(35), math.radians(-30), math.radians(-20))
    sc.collection.objects.link(so)
    w = bpy.data.worlds.new("W")
    w.use_nodes = True
    bg = next(n for n in w.node_tree.nodes if n.type == "BACKGROUND")
    bg.inputs[0].default_value = (0.6, 0.65, 0.7, 1)
    bg.inputs[1].default_value = 0.22  # 1차는 돌이 하얗게 떠서 어둡게
    sc.world = w


def mat_stone(seed):
    m = bpy.data.materials.new("Stone%d" % seed)
    m.use_nodes = True
    nt = m.node_tree
    bsdf = next(n for n in nt.nodes if n.type == "BSDF_PRINCIPLED")
    tc = nt.nodes.new("ShaderNodeTexCoord")
    nz = nt.nodes.new("ShaderNodeTexNoise")
    nz.inputs["Scale"].default_value = 6.0
    nz.inputs["Detail"].default_value = 8.0
    nz.inputs["Roughness"].default_value = 0.6
    try:
        nz.noise_dimensions = "4D"
        nz.inputs["W"].default_value = seed * 1.7
    except Exception:
        pass
    nt.links.new(tc.outputs["Object"], nz.inputs["Vector"])
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    ramp.color_ramp.elements[0].position = 0.3
    ramp.color_ramp.elements[0].color = (0.07, 0.075, 0.08, 1)
    ramp.color_ramp.elements[1].position = 0.75
    ramp.color_ramp.elements[1].color = (0.34, 0.35, 0.37, 1)
    nt.links.new(nz.outputs["Fac"], ramp.inputs["Fac"])
    nt.links.new(ramp.outputs["Color"], bsdf.inputs["Base Color"])
    bsdf.inputs["Roughness"].default_value = 0.85
    bump = nt.nodes.new("ShaderNodeBump")
    bump.inputs["Strength"].default_value = 0.9
    nt.links.new(nz.outputs["Fac"], bump.inputs["Height"])
    nt.links.new(bump.outputs["Normal"], bsdf.inputs["Normal"])
    return m


def mat_glow(color, strength, alpha):
    m = bpy.data.materials.new("Glow")
    m.use_nodes = True
    nt = m.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    e = nt.nodes.new("ShaderNodeEmission")
    e.inputs["Color"].default_value = color
    e.inputs["Strength"].default_value = strength
    t = nt.nodes.new("ShaderNodeBsdfTransparent")
    mx = nt.nodes.new("ShaderNodeMixShader")
    mx.inputs["Fac"].default_value = alpha
    nt.links.new(t.outputs[0], mx.inputs[1])
    nt.links.new(e.outputs[0], mx.inputs[2])
    o = nt.nodes.new("ShaderNodeOutputMaterial")
    nt.links.new(mx.outputs[0], o.inputs["Surface"])
    return m


def link(me, name, mat):
    ob = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(ob)
    ob.data.materials.append(mat)
    return ob


def jitter_outline(points, amount, seed):
    """윤곽을 잘게 나누고 흔들어 깎인 돌처럼"""
    rnd = random.Random(seed)
    out = []
    for i in range(len(points)):
        a = Vector(points[i])
        b = Vector(points[(i + 1) % len(points)])
        for k in range(4):
            p = a.lerp(b, k / 4)
            out.append((p.x + rnd.uniform(-amount, amount), p.y + rnd.uniform(-amount, amount)))
    return out


def stone(outline, seed, depth=0.22):
    """돌판: 윤곽 → 두께 → 모서리 깎기, 앞면 z = 0"""
    pts = jitter_outline(outline, 0.018, seed)
    me = bpy.data.meshes.new("Stone")
    bm = bmesh.new()
    vs = [bm.verts.new((p[0], p[1], 0)) for p in pts]
    f = bm.faces.new(vs)
    ext = bmesh.ops.extrude_face_region(bm, geom=[f])
    moved = [e for e in ext["geom"] if isinstance(e, bmesh.types.BMVert)]
    bmesh.ops.translate(bm, verts=moved, vec=(0, 0, -depth))
    bmesh.ops.triangulate(bm, faces=bm.faces[:])
    bm.to_mesh(me)
    bm.free()
    ob = link(me, "Stone", mat_stone(seed))
    bev = ob.modifiers.new("Bevel", "BEVEL")
    bev.width = 0.05
    bev.segments = 3
    bev.limit_method = "ANGLE"
    # 앞면을 울퉁불퉁하게 (빛 방향에 따라 굴곡이 보이게)
    sub = ob.modifiers.new("Sub", "SUBSURF")
    sub.subdivision_type = "SIMPLE"
    sub.levels = sub.render_levels = 4
    tex = bpy.data.textures.new("StoneLumps%d" % seed, "CLOUDS")
    tex.noise_scale = 0.35
    disp = ob.modifiers.new("Disp", "DISPLACE")
    disp.texture = tex
    disp.strength = 0.07
    disp.direction = "Z"
    # 테두리 빛: 돌보다 조금 크게 뒤에 깔린 판 (가장자리로 빛이 새어 나오는 느낌)
    cx = sum(p[0] for p in pts) / len(pts)
    cy = sum(p[1] for p in pts) / len(pts)
    for scale, alpha, z in ((1.04, 0.75, -0.3), (1.09, 0.35, -0.32), (1.16, 0.16, -0.34), (1.25, 0.07, -0.36)):
        me2 = bpy.data.meshes.new("Rim")
        bm2 = bmesh.new()
        vs2 = [bm2.verts.new((cx + (p[0] - cx) * scale, cy + (p[1] - cy) * scale, z)) for p in pts]
        f2 = bm2.faces.new(vs2)
        bmesh.ops.triangulate(bm2, faces=[f2])
        bm2.to_mesh(me2)
        bm2.free()
        link(me2, "Rim", mat_glow(RIM, 0.9, alpha))  # 세면 흰색으로 날아가 초록이 안 보임
    return ob


def strip(points, width, z, mat):
    """폴리라인을 두께 있는 띠로"""
    me = bpy.data.meshes.new("Strip")
    bm = bmesh.new()
    left, right = [], []
    n = len(points)
    for i in range(n):
        p = Vector(points[i])
        if i == 0:
            d = Vector(points[1]) - p
        elif i == n - 1:
            d = p - Vector(points[i - 1])
        else:
            d = Vector(points[i + 1]) - Vector(points[i - 1])
        d.normalize()
        nrm = Vector((-d.y, d.x))
        left.append(bm.verts.new((p.x + nrm.x * width / 2, p.y + nrm.y * width / 2, z)))
        right.append(bm.verts.new((p.x - nrm.x * width / 2, p.y - nrm.y * width / 2, z)))
    for i in range(n - 1):
        bm.faces.new((left[i], left[i + 1], right[i + 1], right[i]))
    bm.to_mesh(me)
    bm.free()
    return link(me, "Rune", mat)


def rune(strokes, scale=1.0):
    """룬 선들: 밝은 심 + 넓게 번지는 빛 두 겹"""
    core = mat_glow((0.85, 1.0, 0.88, 1), 5.0, 1.0)
    mid = mat_glow(GREEN, 4.0, 0.85)
    halo = mat_glow(GREEN, 2.5, 0.35)
    for s in strokes:
        s = [(p[0] * scale, p[1] * scale) for p in s]
        strip(s, 0.2, 0.09, mat_glow(GREEN, 2.0, 0.12))
        strip(s, 0.11, 0.095, halo)
        strip(s, 0.055, 0.1, mid)
        strip(s, 0.022, 0.105, core)


def arc_pts(cx, cy, r, a0, a1, steps=24):
    return [(cx + math.cos(a0 + (a1 - a0) * i / steps) * r, cy + math.sin(a0 + (a1 - a0) * i / steps) * r) for i in range(steps + 1)]


def diamonds(positions, seed):
    rnd = random.Random(seed)
    mat = mat_glow(GREEN_SOFT, 1.3, 0.95)
    halo = mat_glow(GREEN, 1.2, 0.35)
    for (x, y, r) in positions:
        for rr, m, z in ((r * 1.9, halo, 0.12), (r, mat, 0.13)):
            me = bpy.data.meshes.new("Dia")
            bm = bmesh.new()
            vs = [bm.verts.new((x, y + rr * 1.4, z)), bm.verts.new((x + rr * 0.7, y, z)), bm.verts.new((x, y - rr * 1.4, z)), bm.verts.new((x - rr * 0.7, y, z))]
            bm.faces.new(vs)
            bm.to_mesh(me)
            bm.free()
            link(me, "Dia", m)


def render(name):
    sc = bpy.context.scene
    path = os.path.join(OUT, name + ".png")
    sc.render.filepath = path
    bpy.ops.render.render(write_still=True)
    print("relic icon:", path)


SPARKS = [(-0.8, 0.55, 0.07), (0.82, 0.35, 0.055), (-0.74, -0.5, 0.05), (0.78, -0.62, 0.07), (0.58, 0.84, 0.045), (-0.42, -0.88, 0.045)]

# 관통 돌격: 오벨리스크 + 위로 꿰뚫는 창(화살) + 가로지르는 꺾쇠
def relic_piercing_lunge():
    clear()
    stone([(0.0, 0.92), (0.24, 0.55), (0.3, -0.78), (0.1, -0.9), (-0.12, -0.88), (-0.3, -0.76), (-0.25, 0.55)], 1)
    rune([[(0, -0.62), (0, 0.55)], [(-0.12, 0.38), (0, 0.58), (0.12, 0.38)], [(-0.16, -0.05), (0, 0.08), (0.16, -0.05)], [(-0.16, -0.25), (0, -0.12), (0.16, -0.25)]])
    diamonds(SPARKS, 1)
    render("Relic_piercing_lunge")


# 사슬 갈고리: 둥근 돌판 + 갈고리(J) + 고리 세 개
def relic_chain_hook():
    clear()
    stone([(-0.62, 0.55), (-0.2, 0.78), (0.35, 0.74), (0.7, 0.4), (0.72, -0.35), (0.4, -0.75), (-0.25, -0.8), (-0.68, -0.45)], 2)
    hook = [(0.12, 0.5), (0.12, -0.2)] + arc_pts(-0.08, -0.2, 0.2, 0, -math.pi, 16)[1:] + [(-0.28, 0.0)]
    rings = []
    for i, (x, y) in enumerate(((0.12, 0.62), (0.12, 0.62))):
        pass
    r1 = arc_pts(-0.35, 0.42, 0.09, 0, 2 * math.pi, 20)
    r2 = arc_pts(-0.45, 0.22, 0.09, 0, 2 * math.pi, 20)
    r3 = arc_pts(-0.5, 0.0, 0.07, 0, 2 * math.pi, 20)
    rune([hook, [(0.0, 0.5), (0.24, 0.5)], r1, r2, r3])
    diamonds(SPARKS, 2)
    render("Relic_chain_hook")


# 도약 찌르기: 비스듬히 깨진 조각 + 포물선 + 내리꽂는 화살 + 땅 선
def relic_leap_strike():
    clear()
    stone([(-0.55, 0.62), (0.05, 0.85), (0.62, 0.5), (0.5, -0.1), (0.66, -0.7), (-0.1, -0.82), (-0.62, -0.55), (-0.45, 0.0)], 3)
    rune([arc_pts(0.0, -0.2, 0.42, math.radians(170), math.radians(20), 20), [(0.4, -0.06), (0.4, -0.58)], [(0.28, -0.44), (0.4, -0.6), (0.52, -0.44)], [(-0.4, -0.62), (0.3, -0.62)]])
    diamonds(SPARKS, 3)
    render("Relic_leap_strike")


# 창 휘두르기: 원반 + 회오리(나선) + 가로지르는 창
def relic_spear_sweep():
    clear()
    disc = [(math.cos(a) * (0.74 + 0.05 * math.sin(a * 3)), math.sin(a) * (0.74 + 0.05 * math.sin(a * 3))) for a in [i * 2 * math.pi / 14 for i in range(14)]]
    stone(disc, 4)
    spiral = [(math.cos(t) * (0.08 + t * 0.055), math.sin(t) * (0.08 + t * 0.055)) for t in [i * 0.2 for i in range(46)]]
    rune([spiral, [(-0.5, -0.12), (0.52, 0.16)], [(0.38, 0.2), (0.55, 0.17), (0.43, 0.04)]])
    diamonds(SPARKS, 4)
    render("Relic_spear_sweep")


# 신의 창: 마름모(연) 돌 + 위에서 내리꽂는 창 + 빛살 + 땅 고리
def relic_god_spear():
    clear()
    stone([(0.0, 0.95), (0.5, 0.25), (0.38, -0.55), (0.0, -0.92), (-0.38, -0.55), (-0.5, 0.25)], 5)
    rays = []
    for ang in (35, 60, 120, 145):
        a = math.radians(ang)
        rays.append([(math.cos(a) * 0.12, 0.45 + math.sin(a) * 0.05), (math.cos(a) * 0.36, 0.45 + math.sin(a) * 0.28)])
    rune([[(0, 0.6), (0, -0.4)], [(-0.12, -0.24), (0, -0.44), (0.12, -0.24)]] + rays + [arc_pts(0, -0.55, 0.2, 0, 2 * math.pi, 24)])
    diamonds(SPARKS, 5)
    render("Relic_god_spear")


setup()
relic_piercing_lunge()
relic_chain_hook()
relic_leap_strike()
relic_spear_sweep()
relic_god_spear()
print("done")
