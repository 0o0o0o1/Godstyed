# 창 스킬 아이콘 (흰 실루엣 기호, 투명 배경) — 기존 스킬 아이콘(흰 단색 기호: 교차 칼·해·초승달·창 화살표)과 같은 스타일
# 사슬 갈고리 / 도약 찌르기 / 창 휘두르기 / 신의 창 → exports/icons/Skill_<id>.png (512x512)
# (관통 돌격은 기존 아이콘 88017100002295 그대로)
# 모양을 2D 다각형으로 만들어 위에서 정사영 렌더 (발광 흰색, 그림자 없음).
# 실행: D:\blender.exe -b --factory-startup --python D:\god\scripts\spear_skill_icons.py
import bpy, bmesh, math, os
from mathutils import Vector

OUT = r"D:\god\exports\icons"
SIZE = 512
os.makedirs(OUT, exist_ok=True)


def reset():
    for o in list(bpy.data.objects):
        if o.type != "CAMERA":
            bpy.data.objects.remove(o, do_unlink=True)
    for m in list(bpy.data.meshes):
        bpy.data.meshes.remove(m)


def scene():
    sc = bpy.context.scene
    try:
        sc.render.engine = "CYCLES"
    except TypeError:
        pass
    sc.cycles.samples = 16
    sc.cycles.use_denoising = False
    sc.render.film_transparent = True
    sc.render.resolution_x = sc.render.resolution_y = SIZE
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGBA"
    sc.view_settings.view_transform = "Standard"
    cam_data = bpy.data.cameras.new("IconCam")
    cam_data.type = "ORTHO"
    cam_data.ortho_scale = 2.0  # -1..1
    cam = bpy.data.objects.new("IconCam", cam_data)
    cam.location = (0, 0, 5)
    sc.collection.objects.link(cam)
    sc.camera = cam
    w = bpy.data.worlds.new("IconWorld")
    w.use_nodes = True
    bg = next(n for n in w.node_tree.nodes if n.type == "BACKGROUND")
    bg.inputs[1].default_value = 0.0
    sc.world = w
    return sc


def white_mat():
    m = bpy.data.materials.get("IconWhite")
    if m:
        return m
    m = bpy.data.materials.new("IconWhite")
    m.use_nodes = True
    nt = m.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    e = nt.nodes.new("ShaderNodeEmission")
    e.inputs["Color"].default_value = (1, 1, 1, 1)
    e.inputs["Strength"].default_value = 1.0
    o = nt.nodes.new("ShaderNodeOutputMaterial")
    nt.links.new(e.outputs[0], o.inputs["Surface"])
    return m


def poly(points, name="Poly", z=0.0):
    """닫힌 2D 다각형 (볼록·오목 모두, 삼각분할은 bmesh)"""
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    verts = [bm.verts.new((p[0], p[1], z)) for p in points]
    face = bm.faces.new(verts)
    bmesh.ops.triangulate(bm, faces=[face])
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(ob)
    ob.data.materials.append(white_mat())
    return ob


def rot(p, a):
    c, s = math.cos(a), math.sin(a)
    return (p[0] * c - p[1] * s, p[0] * s + p[1] * c)


def place(points, at, angle):
    return [(at[0] + rot(p, angle)[0], at[1] + rot(p, angle)[1]) for p in points]


def spear(tip, angle, length, shaft=0.05, blade_len=0.38, blade_w=0.12, z=0.0):  # 1차보다 굵게 (기존 아이콘처럼 굵은 기호)
    """창: 창끝 tip 에서 angle(라디안, 창끝이 가리키는 방향) 반대로 length 만큼. 잎 모양 날 + 날밑 + 자루"""
    # 로컬: 창끝 (0,0), 자루는 -x 쪽
    b = blade_len
    blade = [(0, 0), (-b * 0.35, blade_w), (-b * 0.85, blade_w * 0.75), (-b, shaft * 0.9), (-b, -shaft * 0.9), (-b * 0.85, -blade_w * 0.75), (-b * 0.35, -blade_w)]
    guard = [(-b - 0.0, 0.10), (-b - 0.06, 0.10), (-b - 0.06, -0.10), (-b - 0.0, -0.10)]
    shaft_pts = [(-b - 0.06, shaft), (-length, shaft), (-length, -shaft), (-b - 0.06, -shaft)]
    out = []
    for pts in (blade, guard, shaft_pts):
        out.append(poly(place(pts, tip, angle), z=z))
    return out


def arc_band(cx, cy, r, a0, a1, w0, w1, steps=64, z=0.0, taper_pow=1.0):
    """원호 띠: 각 a0→a1, 두께 w0→w1 (끝이 뾰족하게 하려면 w1=0).
    한 장의 오목 다각형으로 만들면 삼각분할이 안쪽을 채워 버려서(1차 휘두르기 아이콘) 사각형 띠로 만듦"""
    me = bpy.data.meshes.new("Arc")
    bm = bmesh.new()
    outer, inner = [], []
    for i in range(steps + 1):
        k = i / steps
        a = a0 + (a1 - a0) * k
        w = max(w0 + (w1 - w0) * (k ** taper_pow), 1e-4)
        outer.append(bm.verts.new((cx + math.cos(a) * (r + w / 2), cy + math.sin(a) * (r + w / 2), z)))
        inner.append(bm.verts.new((cx + math.cos(a) * (r - w / 2), cy + math.sin(a) * (r - w / 2), z)))
    for i in range(steps):
        bm.faces.new((outer[i], outer[i + 1], inner[i + 1], inner[i]))
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new("Arc", me)
    bpy.context.scene.collection.objects.link(ob)
    ob.data.materials.append(white_mat())
    return ob


def ring(cx, cy, rx, ry, w, angle=0.0, z=0.0, steps=40):
    """타원 고리 (사슬 고리): 바깥·안쪽 두 개를 하나의 면으로 (구멍 있는 면은 bmesh 로 직접)"""
    me = bpy.data.meshes.new("Ring")
    bm = bmesh.new()
    o, i_ = [], []
    for s in range(steps):
        a = 2 * math.pi * s / steps
        po = rot((math.cos(a) * rx, math.sin(a) * ry), angle)
        pi = rot((math.cos(a) * (rx - w), math.sin(a) * (ry - w)), angle)
        o.append(bm.verts.new((cx + po[0], cy + po[1], z)))
        i_.append(bm.verts.new((cx + pi[0], cy + pi[1], z)))
    for s in range(steps):
        t = (s + 1) % steps
        bm.faces.new((o[s], o[t], i_[t], i_[s]))
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new("Ring", me)
    bpy.context.scene.collection.objects.link(ob)
    ob.data.materials.append(white_mat())
    return ob


def star4(cx, cy, r, thin=0.28, z=0.0):
    pts = []
    for i in range(8):
        a = math.pi / 2 + i * math.pi / 4
        rr = r if i % 2 == 0 else r * thin
        pts.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr))
    return poly(pts, z=z)


def streak(p0, p1, w0, w1=0.0):
    """끝이 뾰족해지는 선 (속도선·빛줄기)"""
    d = Vector((p1[0] - p0[0], p1[1] - p0[1]))
    n = Vector((-d.y, d.x)).normalized()
    return poly([(p0[0] + n.x * w0 / 2, p0[1] + n.y * w0 / 2), (p1[0] + n.x * w1 / 2, p1[1] + n.y * w1 / 2),
                 (p1[0] - n.x * w1 / 2, p1[1] - n.y * w1 / 2), (p0[0] - n.x * w0 / 2, p0[1] - n.y * w0 / 2)])


def render(name):
    sc = bpy.context.scene
    path = os.path.join(OUT, name + ".png")
    sc.render.filepath = path
    bpy.ops.render.render(write_still=True)
    print("icon:", path)


# ── 사슬 갈고리: 오른쪽 위로 날아가는 창 + 꼬리에 이어진 사슬이 왼쪽 아래로 휘어짐
def icon_chain_hook():
    reset()
    a = math.radians(38)
    tip = (0.82, 0.62)
    spear(tip, a, 0.9)
    butt = (tip[0] - math.cos(a) * 0.9, tip[1] - math.sin(a) * 0.9)
    # 사슬: 꼬리에서 왼쪽 아래로 늘어지는 곡선(2차 베지어) 위에 고리를 같은 간격으로 — 그림 밖으로 안 나가게
    p0 = Vector(butt)
    p2 = Vector((-0.78, -0.62))
    p1 = Vector((-0.55, 0.25))
    def bez(t):
        return p0 * (1 - t) ** 2 + p1 * 2 * (1 - t) * t + p2 * t * t
    samples = [bez(i / 200) for i in range(201)]
    lengths = [0.0]
    for i in range(1, len(samples)):
        lengths.append(lengths[-1] + (samples[i] - samples[i - 1]).length)
    total = lengths[-1]
    n = 7
    for i in range(n):
        target = total * (i + 0.5) / n
        j = next(k for k in range(len(lengths)) if lengths[k] >= target)
        pt = samples[j]
        nxt = samples[min(j + 3, len(samples) - 1)]
        ang = math.atan2(nxt.y - pt.y, nxt.x - pt.x)
        if i % 2 == 0:
            ring(pt.x, pt.y, 0.12, 0.075, 0.042, ang)
        else:
            poly(place([(-0.12, 0.024), (0.12, 0.024), (0.12, -0.024), (-0.12, -0.024)], (pt.x, pt.y), ang))
    # 날아가는 속도선
    for off, ln in ((0.10, 0.28), (-0.10, 0.22), (0.0, 0.34)):
        p0 = (tip[0] - math.cos(a) * 0.35 + math.cos(a + math.pi / 2) * off, tip[1] - math.sin(a) * 0.35 + math.sin(a + math.pi / 2) * off)
        p1 = (p0[0] - math.cos(a) * ln, p0[1] - math.sin(a) * ln)
        streak(p0, p1, 0.04, 0.0)
    render("Skill_chain_hook")


# ── 도약 찌르기: 왼쪽 아래에서 솟아 오른쪽으로 떨어지는 점선 궤적 + 아래로 내리꽂는 창 + 땅 충격
def icon_leap_strike():
    reset()
    # 궤적 (점선 원호)
    cx, cy, r = -0.05, -0.45, 0.78
    for i in range(7):
        a0 = math.radians(170 - i * 17)
        arc_band(cx, cy, r, a0, a0 - math.radians(9), 0.06, 0.06, steps=8)
    # 창: 오른쪽 위에서 아래로 (끝이 땅에 박힘)
    tip = (0.55, -0.62)
    spear(tip, math.radians(-75), 0.95, shaft=0.055, blade_len=0.4, blade_w=0.13)
    # 땅 선 + 충격
    poly([(-0.92, -0.70), (0.95, -0.70), (0.95, -0.76), (-0.92, -0.76)])
    for ang, ln in ((150, 0.32), (120, 0.25), (60, 0.25), (30, 0.32)):
        a = math.radians(ang)
        p0 = (tip[0] + math.cos(a) * 0.1, -0.66 + math.sin(a) * 0.06)
        p1 = (p0[0] + math.cos(a) * ln, p0[1] + math.sin(a) * ln * 0.7)
        streak(p0, p1, 0.04, 0.0)
    render("Skill_leap_strike")


# ── 창 휘두르기: 가운데 비스듬한 창 + 둘레를 감는 굵은 회전 원호 (앞머리 굵고 꼬리 뾰족) + 반짝
def icon_spear_sweep():
    reset()
    spear((0.62, 0.18), math.radians(12), 1.25)
    arc_band(0, 0, 0.8, math.radians(20), math.radians(20 + 290), 0.2, 0.0, steps=96, taper_pow=1.4)
    arc_band(0, 0, 0.56, math.radians(110), math.radians(110 + 130), 0.07, 0.0, steps=48, taper_pow=1.2)  # 안쪽 작은 원호 (1차는 바깥 원호와 겹쳐 뭉침)
    star4(-0.62, 0.62, 0.12)
    star4(0.72, -0.58, 0.08)
    render("Skill_spear_sweep")


# ── 신의 창: 위에서 내리꽂히는 큰 창 + 뒤로 퍼지는 빛줄기 + 땅의 표적 고리
def icon_god_spear():
    reset()
    spear((0.0, -0.55), math.radians(-90), 1.4, shaft=0.07, blade_len=0.55, blade_w=0.2)
    for ang in (60, 75, 105, 120, 40, 140):
        a = math.radians(ang)
        p0 = (math.cos(a) * 0.22, 0.55 + math.sin(a) * 0.05)
        p1 = (math.cos(a) * 0.95, 0.55 + math.sin(a) * 0.40)
        streak(p0, p1, 0.05, 0.0)
    ring(0.0, -0.62, 0.66, 0.18, 0.06)
    ring(0.0, -0.62, 0.38, 0.1, 0.045)
    render("Skill_god_spear")


scene()
icon_chain_hook()
icon_leap_strike()
icon_spear_sweep()
icon_god_spear()
print("done")
