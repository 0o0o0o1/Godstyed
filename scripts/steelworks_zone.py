# 월드 지도(마을 지도 창) "Steelworks" 구역 그림 3장(zone·outline·glow) 만들기 — Blender 안 numpy 로 합성
# 기준: 바탕 지도 rbxassetid://90493874819845 (1024×746). 땅/바다/상가 구역 마스크는 Studio EditableImage 로 읽어
# RLE(창 X0=40, Y0=160, 300×420; L=검은 땅, S=상가 구역, W=그 밖)로 여기 붙여 넣음.
# 실행 1단계: exec(open(r"D:\god\scripts\steelworks_zone.py", encoding="utf-8").read()); preview()
import numpy as np, bpy, math, re, os

OUT = r"D:\god\exports\steelworks_zone"
os.makedirs(OUT, exist_ok=True)
W, H = 1024, 746
X0, Y0, MW, MH = 40, 160, 300, 420
RLE = open(r"D:\god\scripts\steelworks_zone_rle.txt", encoding="utf-8").read().strip()


def decode():
    land = np.zeros((H, W), bool); shop = np.zeros((H, W), bool)
    for y, row in enumerate(RLE.split("/")):
        x = 0
        for c, n in re.findall(r"([LSW])(\d+)", row):
            n = int(n)
            if c == "L": land[Y0 + y, X0 + x:X0 + x + n] = True
            elif c == "S": shop[Y0 + y, X0 + x:X0 + x + n] = True
            x += n
    return land, shop


def poly_mask(pts):
    """짝홀 규칙 다각형 채우기 (이미지 좌표, y 아래로)"""
    m = np.zeros((H, W), bool)
    ys = np.arange(H) + 0.5
    n = len(pts)
    for y in range(H):
        yy = y + 0.5; xs = []
        for i in range(n):
            x1, y1 = pts[i]; x2, y2 = pts[(i + 1) % n]
            if (y1 <= yy < y2) or (y2 <= yy < y1):
                xs.append(x1 + (yy - y1) * (x2 - x1) / (y2 - y1))
        xs.sort()
        for k in range(0, len(xs) - 1, 2):
            a = int(math.ceil(xs[k] - 0.5)); b = int(math.floor(xs[k + 1] - 0.5))
            if b >= a: m[y, max(0, a):min(W, b + 1)] = True
    return m


def save_png(name, rgba):
    """rgba: (H, W, 4) float 0..1, 위가 0행 → Blender 이미지는 아래가 0행"""
    img = bpy.data.images.get(name) or bpy.data.images.new(name, rgba.shape[1], rgba.shape[0], alpha=True)
    if img.size[0] != rgba.shape[1] or img.size[1] != rgba.shape[0]:
        img.scale(rgba.shape[1], rgba.shape[0])
    img.pixels.foreach_set(np.ascontiguousarray(rgba[::-1]).ravel().astype(np.float32))
    img.filepath_raw = os.path.join(OUT, name + ".png"); img.file_format = 'PNG'
    img.save()
    return img.filepath_raw


# 구역 다각형 (이미지 좌표). 땅 ∧ ¬상가 ∧ 다각형 = 공장 구역
ZONE = [(60, 335), (95, 322), (130, 327), (160, 316), (190, 323), (222, 313), (255, 321), (285, 315), (310, 328),
        (328, 350), (336, 382), (332, 410), (323, 428), (300, 470), (255, 520), (200, 528), (150, 528), (110, 507),
        (95, 490), (90, 460), (60, 420)]


def region():
    land, shop = decode()
    return land & ~shop & poly_mask(ZONE), land, shop


def preview():
    reg, land, shop = region()
    rgba = np.zeros((H, W, 4), np.float32); rgba[..., 3] = 1
    rgba[...] = (0.45, 0.55, 0.58, 1)
    rgba[land] = (0.05, 0.05, 0.05, 1)
    rgba[shop] = (0.85, 0.75, 0.6, 1)
    rgba[reg] = (0.9, 0.55, 0.25, 1)
    crop = rgba[280:600, 30:400]
    big = np.repeat(np.repeat(crop, 2, 0), 2, 1)
    print(save_png("sw_preview", big), int(reg.sum()))


# ===================== 2단계: 합성 =====================
# exec(open(r"D:\god\scripts\steelworks_icons.py", encoding="utf-8").read()); render_all()   # 아이콘 (PPU 3)
# exec(open(r"D:\god\scripts\steelworks_zone.py", encoding="utf-8").read()); build()
ICON_DIR = os.path.join(OUT, "icons")
# 아이콘 배치: (이름, 바닥 가운데 x, y) — 뒤(위)부터 그림
# v2 (2026-11-21): 잉크 선 아이콘(2배 렌더 → 절반), 상가처럼 길 따라 빽빽하게
PLACE = [("house_o", 122, 352), ("house_r", 138, 346), ("house_t", 129, 368), ("house_o", 146, 365),
         ("gasholder", 178, 368), ("office", 205, 356), ("house_t", 240, 343), ("house_o", 254, 336), ("chimneys", 272, 366),
         ("tanks", 302, 352), ("silo", 318, 384), ("shed_t", 160, 398), ("shed_s", 186, 412), ("furnace", 228, 420),
         ("cooling", 296, 410), ("crane", 136, 428), ("containers", 124, 452), ("sawshed", 272, 458), ("coal", 160, 458),
         ("coal", 186, 468), ("shed_o", 230, 478), ("shed_r", 200, 446), ("house_r", 108, 466),
         ("tree", 250, 392), ("tree", 258, 398)]
TREES = [(110, 336), (304, 338), (325, 362), (252, 392), (140, 492), (118, 476), (252, 486), (196, 330), (318, 400)]
ROADS = [[(326, 432), (290, 425), (250, 428), (200, 424), (160, 428), (118, 437)],      # 동서 큰길 (상가 쪽 → 부두)
         [(212, 324), (214, 360), (222, 392), (226, 428), (226, 460), (220, 500)],      # 남북 길
         [(250, 428), (268, 404), (290, 380), (318, 368)]]                              # 냉각탑 쪽 갈림길
CONVEYOR = []                                          # 석탄 → 용광로
RAIL = []
PAPER = np.array([217, 193, 152]) / 255.0


def load_png(path):
    img = bpy.data.images.load(path, check_existing=False)
    w, h = img.size
    a = np.array(img.pixels[:], np.float32).reshape(h, w, 4)[::-1].copy()
    bpy.data.images.remove(img)
    return a


def blur(a, n=1):
    for _ in range(n):
        a = (a + np.roll(a, 1, 0) + np.roll(a, -1, 0) + np.roll(a, 1, 1) + np.roll(a, -1, 1)) / 5.0
    return a


def dist(mask, maxd):
    """mask 바깥 픽셀까지의 대략 거리 (8방향 팽창 횟수). mask 안 = 0"""
    d = np.full(mask.shape, maxd + 1, np.float32); d[mask] = 0
    cur = mask.copy()
    for k in range(1, maxd + 1):
        nxt = cur.copy()
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)):
            nxt |= np.roll(np.roll(cur, dy, 0), dx, 1)
        d[nxt & ~cur] = k
        cur = nxt
    return d


def draw_line(canvas, pts, width, col, alpha=1.0):
    """두께 있는 폴리라인 (거리 기반 안티앨리어싱)"""
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32) + 0.5
    acc = np.zeros((H, W), np.float32)
    for (x1, y1), (x2, y2) in zip(pts[:-1], pts[1:]):
        x0, x9 = int(min(x1, x2) - width - 2), int(max(x1, x2) + width + 2)
        y0, y9 = int(min(y1, y2) - width - 2), int(max(y1, y2) + width + 2)
        sx, sy = xx[y0:y9, x0:x9], yy[y0:y9, x0:x9]
        dx, dy = x2 - x1, y2 - y1; L2 = dx * dx + dy * dy
        t = np.clip(((sx - x1) * dx + (sy - y1) * dy) / L2, 0, 1)
        dd = np.hypot(sx - (x1 + t * dx), sy - (y1 + t * dy))
        cov = np.clip(width / 2 + 0.5 - dd, 0, 1)
        acc[y0:y9, x0:x9] = np.maximum(acc[y0:y9, x0:x9], cov)
    a = acc[..., None] * alpha
    canvas[..., :3] = canvas[..., :3] * (1 - a) + np.array(col) * a
    return acc


def build():
    reg, land, shop = region()
    regf = blur(reg.astype(np.float32), 1) * reg + (blur(reg.astype(np.float32), 1) * ~reg) * 0.5
    rng = np.random.default_rng(7)
    # 종이: 큰 얼룩 + 고운 결
    low = blur(rng.normal(0, 1, (H // 8 + 1, W // 8 + 1)).astype(np.float32), 2)
    low = np.repeat(np.repeat(low, 8, 0), 8, 1)[:H, :W]
    low = blur(low, 4)
    grain = rng.normal(0, 1, (H, W)).astype(np.float32)
    lum = 1.0 + 0.035 * low / (np.abs(low).max() + 1e-6) + 0.012 * grain
    zone = np.zeros((H, W, 4), np.float32)
    zone[..., :3] = PAPER[None, None, :] * lum[..., None]
    # 해안 쪽 살짝 진하게 (가장자리 4px)
    edge = dist(~reg, 6)
    zone[..., :3] *= (1 - 0.06 * np.clip(1 - (edge - 1) / 5, 0, 1))[..., None]
    # 길·철길
    for r in ROADS:
        draw_line(zone, r, 5.2, (0.55, 0.47, 0.36))
        draw_line(zone, r, 3.4, (0.80, 0.76, 0.68))
    if CONVEYOR:
        draw_line(zone, CONVEYOR, 3.2, (0.42, 0.30, 0.18)); draw_line(zone, CONVEYOR, 1.6, (0.80, 0.62, 0.30))
    if RAIL:
        draw_line(zone, RAIL, 1.6, (0.33, 0.25, 0.18))
    for (x1, y1), (x2, y2) in zip(RAIL[:-1], RAIL[1:]):
        L = math.hypot(x2 - x1, y2 - y1); n = int(L / 4)
        for k in range(n + 1):
            t = k / max(1, n); cx, cy = x1 + (x2 - x1) * t, y1 + (y2 - y1) * t
            nx, ny = -(y2 - y1) / L, (x2 - x1) / L
            draw_line(zone, [(cx - nx * 2.2, cy - ny * 2.2), (cx + nx * 2.2, cy + ny * 2.2)], 1.0, (0.33, 0.25, 0.18))
    # 나무 점
    for (x, y) in TREES:
        yy, xx = np.mgrid[y - 5:y + 5, x - 5:x + 5].astype(np.float32) + 0.5
        cov = np.clip(2.6 - np.hypot(xx - x, yy - y), 0, 1)[..., None]
        zone[y - 5:y + 5, x - 5:x + 5, :3] = zone[y - 5:y + 5, x - 5:x + 5, :3] * (1 - cov) + np.array((0.47, 0.53, 0.36)) * cov
        rim = np.clip(3.3 - np.hypot(xx - x, yy - y), 0, 1)[..., None] - cov
        zone[y - 5:y + 5, x - 5:x + 5, :3] = zone[y - 5:y + 5, x - 5:x + 5, :3] * (1 - rim * 0.8) + np.array((0.3, 0.26, 0.18)) * rim * 0.8
    # 아이콘 (그림자 살짝 + 알파 합성)
    report = []
    for name, cx, by in sorted(PLACE, key=lambda p: p[2]):
        ic = load_png(os.path.join(ICON_DIR, name + ".png"))
        ic = ic.reshape(ic.shape[0] // 2, 2, ic.shape[1] // 2, 2, 4).mean(axis=(1, 3))   # 2배 렌더 → 실제 크기
        ic[..., :3] = np.where(ic[..., 3:4] > 1e-4, ic[..., :3], 0)
        h, w = ic.shape[:2]
        x0 = int(round(cx - w / 2)); y0 = int(round(by - h))
        a = ic[..., 3:4]
        # 바닥 그림자 (아이콘 아래쪽 가로 타원)
        sh = np.zeros((H, W), np.float32)
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        sh = np.clip(1 - np.hypot((xx - cx - 2) / (w * 0.45), (yy - by + 1) / (h * 0.12 + 2)), 0, 1) * 0.25
        zone[..., :3] *= (1 - sh)[..., None]
        sub = zone[y0:y0 + h, x0:x0 + w]
        sub[..., :3] = sub[..., :3] * (1 - a) + ic[..., :3] * a
        inside = (reg[y0:y0 + h, x0:x0 + w] * a[..., 0]).sum() / max(1e-6, a.sum())
        report.append("%s %.0f%%" % (name, inside * 100))
    zone[..., 3] = np.clip(regf, 0, 1)
    # 테두리(흰 5px)·빛(흰, 바깥 강하게 14px / 안 약하게 26px)
    d_out = dist(reg, 16)          # 바깥 거리
    d_in = dist(~reg, 28)          # 안 거리
    outline = np.zeros((H, W, 4), np.float32); outline[..., :3] = 1
    b = np.where(reg, d_in, d_out)
    outline[..., 3] = np.clip(3.0 - b, 0, 1)
    glow = np.zeros((H, W, 4), np.float32); glow[..., :3] = 1
    glow[..., 3] = np.where(reg, 0.36 * np.exp(-(d_in - 1) / 9.0) * (d_in <= 28), 0.78 * np.clip(1 - (d_out - 1) / 14.0, 0, 1))
    print(save_png("SteelworksZone", zone), save_png("SteelworksOutline", outline), save_png("SteelworksGlow", glow))
    # 확인용: 바탕(대략) + 구역 + 테두리
    pv = np.zeros((H, W, 4), np.float32); pv[...] = (0.45, 0.55, 0.58, 1)
    pv[land] = (0.05, 0.05, 0.05, 1); pv[shop] = (0.85, 0.76, 0.6, 1)
    a = zone[..., 3:4]; pv[..., :3] = pv[..., :3] * (1 - a) + zone[..., :3] * a
    oa = outline[..., 3:4]; pv[..., :3] = pv[..., :3] * (1 - oa) + np.array((0.95, 0.55, 0.2)) * oa
    crop = pv[290:530, 40:360]
    save_png("sw_compose_preview", np.repeat(np.repeat(crop, 3, 0), 3, 1))
    # 마우스 판정용 경계 점 48개 (중심에서 방사선, 가장 먼 구역 픽셀)
    ys, xs = np.nonzero(reg); cy, cx = ys.mean(), xs.mean()
    pts = []
    for k in range(48):
        ang = 2 * math.pi * k / 48; dx, dy = math.cos(ang), math.sin(ang); last = (cx, cy)
        for r in range(1, 400):
            x, y = int(cx + dx * r), int(cy + dy * r)
            if not (0 <= x < W and 0 <= y < H): break
            if reg[y, x]: last = (x, y)
        pts.append((int(last[0]), int(last[1])))
    print("inside", report)
    print("center", round(cx), round(cy))
    print("POINTS", ", ".join("{ %d, %d }" % p for p in pts))
