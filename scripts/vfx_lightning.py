# 신의 창 번개 줄기 그림 (2026-11-24, 사용자: Neon 막대 번개가 "퀄리티가 떨어지고 너무 가늘다" → Blender 번개 그림 + 굵게)
# 그림 4장 (각 1024x256, 가로 = 번개 길이 방향: 왼쪽 = 하늘, 오른쪽 = 창). Roblox 에서 하늘→창을 잇는 넓은 Beam(FaceCamera)에
# Stretch 로 씌우고 0.05초마다 4장을 바꿔 깜빡임.
# 모양: 가운데 밀어내기로 꺾인 주 줄기 + 잔가지 몇 개. 흰 심(가늘고 아주 밝음) + 청록 빛무리 + 바깥 엷은 보라 빛무리(층마다 굵기·투명도 다름)
# 명령줄: blender -b --factory-startup --python-expr "exec(open(r'D:\god\scripts\vfx_lightning.py', encoding='utf-8').read())"
import bpy, random, os, math

OUT = r"D:\god\exports\vfx"
W, H = 1024, 128  # v2 (2026-11-24): 8:1 — 번개 길이 140 · 폭 16 에 그대로 맞춰 늘어나지 않게 (4:1 을 늘리니 바람 줄기처럼 보였음, 마디로 나누니 이음매가 끊겨 보였음)
ASPECT = H / W  # 화면 세로 반높이 = ASPECT (가로 -1..1)


def scene():
    name = "VFX_Lightning"
    if name in bpy.data.scenes:
        bpy.data.scenes.remove(bpy.data.scenes[name])
    sc = bpy.data.scenes.new(name)
    if bpy.context.window:
        bpy.context.window.scene = sc
    sc.render.engine = "CYCLES"
    sc.cycles.samples = 24
    sc.cycles.use_denoising = False
    sc.render.film_transparent = True
    sc.render.resolution_x, sc.render.resolution_y = W, H
    sc.render.resolution_percentage = 100
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGBA"
    sc.view_settings.view_transform = "Standard"
    sc.world = bpy.data.worlds.new(name + "W")
    cam = bpy.data.cameras.new(name + "Cam")
    cam.type = "ORTHO"
    cam.ortho_scale = 2.0
    co = bpy.data.objects.new(name + "Cam", cam)
    co.location = (0, 0, 5)
    sc.collection.objects.link(co)
    sc.camera = co
    return sc


def glow_mat(name, color, strength, alpha):
    """발광 + 투명: alpha 만큼만 보임 (빛무리 층)"""
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    emit = nt.nodes.new("ShaderNodeEmission")
    emit.inputs["Color"].default_value = (*color, 1)
    emit.inputs["Strength"].default_value = strength
    tr = nt.nodes.new("ShaderNodeBsdfTransparent")
    mix = nt.nodes.new("ShaderNodeMixShader")
    mix.inputs["Fac"].default_value = alpha
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    nt.links.new(tr.outputs[0], mix.inputs[1])
    nt.links.new(emit.outputs[0], mix.inputs[2])
    nt.links.new(mix.outputs[0], out.inputs["Surface"])
    m.blend_method = "BLEND" if hasattr(m, "blend_method") else None
    return m


def jag(a, b, depth, rough, rng):
    pts = [a, b]
    for d in range(depth):
        nxt = [pts[0]]
        amp = rough * (DECAY ** d)
        for i in range(len(pts) - 1):
            (x0, y0), (x1, y1) = pts[i], pts[i + 1]
            mx, my = (x0 + x1) / 2, (y0 + y1) / 2
            seg = math.hypot(x1 - x0, y1 - y0)
            nx, ny = -(y1 - y0) / max(seg, 1e-6), (x1 - x0) / max(seg, 1e-6)
            off = rng.uniform(-1, 1) * amp * seg
            nxt.append((mx + nx * off, my + ny * off))
            nxt.append((x1, y1))
        pts = nxt
    return pts


def curve(sc, name, pts, radius, mat, taper_end=1.0):
    cu = bpy.data.curves.new(name, "CURVE")
    cu.dimensions = "3D"
    cu.bevel_depth = radius
    cu.bevel_resolution = 2
    sp = cu.splines.new("POLY")
    sp.points.add(len(pts) - 1)
    n = len(pts)
    for i, (x, y) in enumerate(pts):
        sp.points[i].co = (x, y, 0, 1)
        sp.points[i].radius = 1.0 - (1.0 - taper_end) * (i / (n - 1))
    ob = bpy.data.objects.new(name, cu)
    ob.data.materials.append(mat)
    sc.collection.objects.link(ob)
    return ob


DECAY = 0.82  # 단계마다 꺾임 세기 감소 (0.55 는 잔 꺾임이 거의 없어 매끈했음)
WHITE = (1.0, 1.0, 1.0)
MINT = (0.75, 1.0, 0.85)
TEAL = (0.25, 1.0, 0.85)
VIOLET = (0.65, 0.5, 1.0)


def blur(img, sigma):
    """가우스 흐림 (FFT, 가로·세로 모두). img: (h, w, c)"""
    import numpy as np
    h, w = img.shape[:2]
    fy = np.fft.fftfreq(h)[:, None]
    fx = np.fft.fftfreq(w)[None, :]
    k = np.exp(-2 * (math.pi ** 2) * (sigma ** 2) * (fx ** 2 + fy ** 2))
    out = np.empty_like(img)
    for c in range(img.shape[2]):
        out[:, :, c] = np.real(np.fft.ifft2(np.fft.fft2(img[:, :, c]) * k))
    return np.clip(out, 0, None)


def bolt(index, seed):
    """흰 심·연초록 안쪽만 렌더 → numpy 로 빛무리(청록 좁게 + 보라빛 넓게)를 더하고 밝기를 알파로"""
    import numpy as np
    sc = scene()
    rng = random.Random(seed)
    m_core = glow_mat("Core%d" % index, WHITE, 6.0, 1.0)
    m_in = glow_mat("In%d" % index, MINT, 3.0, 0.8)
    ymax = ASPECT * 0.55
    main = jag((-1.02, 0.0), (1.0, 0.0), 6, 0.5, rng)
    # 세로로 화면을 넘지 않게 비율로 줄임 (잘라내면 평평한 구간이 생겼음)
    peak = max(abs(y) for _, y in main) or 1.0
    scale = min(1.0, ymax / peak)
    main = [(x, y * scale) for x, y in main]
    curve(sc, "MainIn", main, 0.0075, m_in)
    curve(sc, "MainCore", main, 0.0032, m_core)
    for _ in range(rng.randint(4, 6)):
        i = rng.randint(len(main) // 8, len(main) * 7 // 8)
        x0, y0 = main[i]
        length = rng.uniform(0.08, 0.22)
        ang = rng.uniform(0.3, 0.85) * (1 if rng.random() < 0.5 else -1)
        br = jag((x0, y0), (x0 + math.cos(ang) * length, y0 + math.sin(ang) * length * 0.5), 5, 0.45, rng)
        peak_b = max(abs(y) for _, y in br) or 1.0
        if peak_b > ASPECT * 0.9:
            br = [(x, y * ASPECT * 0.9 / peak_b) for x, y in br]
        curve(sc, "BranchIn", br, 0.007, m_in, taper_end=0.1)
        curve(sc, "BranchCore", br, 0.0028, m_core, taper_end=0.1)
    tmp = os.path.join(OUT, "_lightning_tmp.png")
    sc.render.filepath = tmp
    bpy.ops.render.render(write_still=True, scene=sc.name)
    img = bpy.data.images.load(tmp, check_existing=False)
    px = np.array(img.pixels[:], np.float32).reshape(H, W, 4)
    bpy.data.images.remove(img)
    os.remove(tmp)
    base = px[:, :, :3] * px[:, :, 3:4]  # 검은 바탕 위 빛
    lum = base.max(axis=2, keepdims=True)
    g1 = blur(lum, 2.0) * np.array(TEAL)
    g2 = blur(lum, 6.0) * np.array((0.3, 1.0, 0.65))  # 초록·청록 (파랑으로 치우치지 않게)
    g3 = blur(lum, 14.0) * np.array((0.55, 0.6, 1.0))  # 바깥 엷은 보랏빛
    rgb = base + g1 * 2.2 + g2 * 2.6 + g3 * 2.0
    a = np.clip(rgb.max(axis=2, keepdims=True), 0, 1)
    col = np.clip(rgb / np.maximum(a, 1e-4), 0, 1)
    out = np.concatenate([col, a], axis=2)
    o = bpy.data.images.new("Lightning%d" % index, W, H, alpha=True)
    o.pixels[:] = out.ravel()
    path = os.path.join(OUT, "Lightning%d.png" % index)
    o.filepath_raw = path
    o.file_format = "PNG"
    o.save()
    bpy.data.images.remove(o)
    print("rendered", path)


for i, seed in enumerate((11, 29, 47, 83), start=1):
    bolt(i, seed)
