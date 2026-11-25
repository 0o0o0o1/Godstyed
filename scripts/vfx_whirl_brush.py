# 칼날 회오리 v5 키트(Slash VFX System) 텍스처를 대신할 붓질 그림 — Python(numpy + Pillow)만 씀, Blender 안 씀.
# 실행: python scripts/vfx_whirl_brush.py  → exports/vfx/whirl_brush/*.png (+ _preview.png 확인용)
# 모든 그림은 색 없는 흰색 + 알파 (색은 Beam.Color / ParticleEmitter.Color 로 칠함, VfxConfig 규칙)
#
# 빔 텍스처 (1024x256, Beam TextureMode Stretch: 가로 = 빔 길이, 세로 = 폭, 가로 1 쪽 = 칼날 머리)
#   beam_body  두툼한 몸통: 머리 쪽이 굵고 날카롭게 끝남, 길이 방향 붓 섬유, 꼬리는 가닥으로 갈라져 사라짐
#   beam_core  날카로운 심: 가늘고 밝은 렌즈, 양 끝 바늘처럼
#   beam_wisp  끊긴 가닥: 몸통 둘레에 흩날리는 길고 가는 붓 획들
# 플립북 (1024x1024, 4x4 칸 256, ParticleEmitter Grid4x4 OneShot, 칸 가운데 = 초승달 원 중심)
#   flip_thick 굵은 초승달이 그어지고(앞 4칸) → 가늘어지며 섬유로 흩어짐
#   flip_thin  가는 초승달 선
#   flip_trail 중간 굵기, 오래 남으며 옅어짐

import os
import numpy as np
from PIL import Image, ImageFilter

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "exports", "vfx", "whirl_brush")
os.makedirs(OUT, exist_ok=True)
RNG = np.random.default_rng(20261126)


def smoothstep(e0, e1, x):
    d = np.asarray(e1 - e0, dtype=np.float64)
    d = np.where(np.abs(d) < 1e-6, 1e-6, d)
    t = np.clip((x - e0) / d, 0.0, 1.0)
    return t * t * (3 - 2 * t)


def noise1d(n, cells, rng, octaves=3):
    """길이 n, 부드러운 1D 노이즈 0..1"""
    out = np.zeros(n)
    amp, total = 1.0, 0.0
    x = np.linspace(0, 1, n)
    for o in range(octaves):
        c = cells * (2 ** o)
        pts = rng.random(c + 1)
        xs = np.linspace(0, 1, c + 1)
        out += amp * np.interp(x, xs, pts)
        total += amp
        amp *= 0.5
    return out / total


def noise2d(h, w, cells_y, cells_x, rng, octaves=3):
    """부드러운 2D 노이즈 0..1 (작은 격자를 bicubic 으로 키움)"""
    out = np.zeros((h, w))
    amp, total = 1.0, 0.0
    for o in range(octaves):
        cy, cx = cells_y * (2 ** o) + 1, cells_x * (2 ** o) + 1
        small = Image.fromarray((rng.random((cy, cx)) * 255).astype(np.uint8))
        big = np.asarray(small.resize((w, h), Image.BICUBIC), dtype=np.float64) / 255.0
        out += amp * big
        total += amp
        amp *= 0.5
    return out / total


def fibers(v, n_rows, rng, sharp=2.2):
    """세로 좌표 v(0..1 배열)에 대한 붓 섬유 세기: 가는 줄이 촘촘히, 굵기·세기 제각각 (길이 방향으로 이어지는 결)"""
    f = noise1d(n_rows, 60, rng, octaves=4)
    f = np.interp(v, np.linspace(0, 1, n_rows), f)
    return np.clip((f - 0.25) / 0.6, 0, 1) ** sharp


def save(name, alpha, value=None):
    a = np.clip(alpha, 0, 1)
    v = np.ones_like(a) if value is None else np.clip(value, 0, 1)
    rgb = (v * 255).astype(np.uint8)
    img = np.dstack([rgb, rgb, rgb, (a * 255).astype(np.uint8)])
    path = os.path.join(OUT, name + ".png")
    Image.fromarray(img, "RGBA").save(path)
    return path


# ---------------- 빔 텍스처 ----------------
W, H = 1024, 256
u = np.linspace(0, 1, W)[None, :].repeat(H, 0)  # 0 꼬리 → 1 머리
v = np.linspace(-1, 1, H)[:, None].repeat(W, 1)  # 폭 방향 -1..1


def lens(u, peak, tail_pow, tip):
    """칼날 반폭 (0..1): 꼬리에서 천천히 커져 peak 에서 가장 굵고 머리 tip 구간에서 날카롭게 0"""
    rise = np.clip(u / peak, 0, 1) ** tail_pow
    head = np.clip((1 - u) / tip, 0, 1) ** 0.55
    return rise * head


def blur(a, radius):
    im = Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8))
    return np.asarray(im.filter(ImageFilter.GaussianBlur(radius)), dtype=np.float64) / 255.0


def wavy_v(amount, rng, cells=5):
    """결이 길이 방향으로 물결치게: v 를 u 에 따라 조금씩 밀어 줌 (줄마다 다르게)"""
    shift = (noise2d(H, W, 3, cells, rng, 2) - 0.5) * 2 * amount
    return v + shift


def beam_body(rng):
    half = 0.92 * lens(u, 0.7, 1.6, 0.3) ** 1.25  # 머리 끝을 더 뾰족하게
    edge = np.maximum(half * (0.85 + 0.3 * noise2d(H, W, 1, 10, rng, 2)), 1e-3)
    inside = smoothstep(edge, edge * 0.8, np.abs(v))
    # 결: 물결치는 섬유, 대비는 낮게 (자로 그은 줄 느낌 빼기), 세로로 살짝 번짐
    vv = wavy_v(0.12, rng)
    fib = fibers(np.clip((vv + 1) / 2, 0, 1), 2400, rng, sharp=1.6)
    fib = blur(fib, 1.2)
    breaks = noise2d(H, W, 14, 8, rng, 3)
    erosion = smoothstep(0.12 + 0.5 * (1 - u), 0.3 + 0.5 * (1 - u), breaks)
    a = inside * (0.2 + 0.8 * fib) * (0.25 + 0.75 * erosion)
    a *= 0.3 + 0.7 * smoothstep(0.05, 0.75, u)
    # 2차 (v5 와 비교 후): 또렷한 앞 날 — 한쪽 가장자리를 가늘고 진하게
    lead = inside * smoothstep(0.62, 0.9, -v / edge) * smoothstep(0.15, 0.6, u) * (0.6 + 0.4 * erosion)
    a = np.maximum(a, lead)
    # 번짐은 아주 조금만 (1차 0.45 는 연기처럼 뭉개졌음)
    glow = blur(inside * smoothstep(0.2, 0.85, u), 6) * 0.12
    a = np.maximum(a, glow)
    a *= smoothstep(1.0, 0.9, np.abs(v))
    a *= smoothstep(0.0, 0.03, u) * smoothstep(1.0, 0.985, u)
    rim = smoothstep(-0.1, 0.9, -v / edge) * 0.3
    value = np.clip(0.75 + 0.25 * smoothstep(0.4, 0.95, u) + rim, 0, 1)
    return a, value


def beam_core(rng):
    # 2차 (v5 와 비교 후): 빔 5겹 중 3겹이 이 그림을 씀 → 번짐 없이 또렷하게, 띠 가운데 구간(u 0.22~0.82)만 차지하는 칼날
    #   (1차는 길이 전체 + 번짐 0.5 라 화면에서 흐릿한 라일락 얼룩으로 보였음)
    k = np.clip((u - 0.22) / 0.6, 0, 1)  # 칼날 안 0 꼬리 → 1 머리
    half = 0.7 * np.clip(k / 0.62, 0, 1) ** 0.8 * np.clip((1 - k) / 0.38, 0, 1) ** 0.75
    half *= (k > 0) & (k < 1)
    edge = np.maximum(half * (0.93 + 0.14 * noise2d(H, W, 1, 12, rng, 2)), 1e-3)
    a = smoothstep(edge, edge * 0.88, np.abs(wavy_v(0.03, rng)))
    fib = fibers(np.clip((wavy_v(0.05, rng) + 1) / 2, 0, 1), 1600, rng, sharp=1.2)
    a *= 0.7 + 0.3 * fib
    a *= half > 0.004  # 가운데 줄 찌꺼기 (반폭 0 인 곳)
    return a, None


def beam_wisp(rng):
    a = np.zeros((H, W))
    yy = np.arange(H)[:, None]
    xx = np.arange(W)[None, :]
    for _ in range(46):
        x0 = rng.uniform(-0.1, 0.75) * W
        length = rng.uniform(0.15, 0.55) * W
        x1 = x0 + length
        y0 = rng.normal(0, 0.38) * H / 2 + H / 2
        bend = rng.uniform(-18, 18)
        thick = rng.uniform(1.2, 5.5)
        strength = rng.uniform(0.25, 0.9)
        t = (xx - x0) / max(x1 - x0, 1)
        inside_t = (t >= 0) & (t <= 1)
        yc = y0 + bend * np.sin(np.clip(t, 0, 1) * np.pi)
        # 획: 가운데 굵고 양 끝 가늘게 (앞쪽 끝이 더 뾰족)
        prof = np.clip(t, 0, 1) ** 0.6 * np.clip(1 - t, 0, 1) ** 0.9 * 2.4
        w = thick * np.clip(prof, 0, 1)
        d = np.abs(yy - yc)
        stroke = smoothstep(w + 1.2, w * 0.4, d) * inside_t * strength
        # 마른 붓: 획 안에서 길이 방향으로 끊김
        dry = smoothstep(0.35, 0.6, noise1d(W, 30, rng, 3))[None, :]
        a = np.maximum(a, stroke * (0.4 + 0.6 * dry))
    a *= smoothstep(0.0, 0.25, u) * smoothstep(1.0, 0.8, u)
    return a, None


# ---------------- 플립북 ----------------
C = 256  # 칸 크기
cy, cx = np.mgrid[0:C, 0:C].astype(np.float64)
dx, dy = (cx - C / 2) / (C / 2), (cy - C / 2) / (C / 2)
R = np.sqrt(dx * dx + dy * dy)
TH = np.arctan2(dx, dy)  # 0 = 칸 아래쪽, 반시계 +
ARC_C = np.pi * 0.15  # 초승달 가운데 방향 (아래에서 조금 돌림, 원본처럼 왼쪽 아래에 무게)


def crescent_frame(rng, k, style, fib_r, breaks):
    """k = 0..15 칸 번호. 반환 알파 (C x C)"""
    outer = 0.9
    grow = min(1.0, (k + 1) / 4.0)  # 앞 4칸: 호가 그어짐
    fade = max(0.0, (k - 3) / 12.0)  # 그 뒤: 가늘어지며 사라짐
    span = np.radians(style["span"]) * (0.35 + 0.65 * grow)
    start = ARC_C - np.radians(style["span"]) / 2
    rel = (TH - start) % (2 * np.pi)
    s = rel / max(span, 1e-3)  # 0 꼬리 → 1 머리 (그어지는 방향)
    on = (s >= 0) & (s <= 1)
    thick = style["thick"] * (1 - 0.75 * fade)
    # 두께: 머리 쪽 굵고 양 끝 바늘
    prof = np.clip(s, 0, 1) ** 0.8 * np.clip(1 - s, 0, 1) ** 0.35 * 2.0
    t = thick * np.clip(prof, 0, 1)
    inner = outer - t
    band = smoothstep(inner - 0.012, inner + 0.01, R) * smoothstep(outer + 0.012, outer - 0.006, R) * on
    # 섬유 (반지름 방향으로 촘촘한 결 → 호를 따라 이어지는 줄)
    fib = np.interp(R, np.linspace(0, 1.2, fib_r.size), fib_r)
    # 2차: 바깥 날만 밝고 안쪽으로 투명하게 빠짐 (1차는 면 전체가 칠해져 넓은 보라 덩어리로 보였음)
    toward_edge = smoothstep(inner, outer, R) ** 2.2
    a = band * (0.08 + 0.92 * toward_edge) * (0.5 + 0.5 * fib)
    # 바깥 날 테두리 밝게
    a = np.maximum(a, band * smoothstep(outer - 0.05, outer - 0.005, R) * 0.95)
    # 사라짐: 낮은 주파수 노이즈로 갈라지며 (꼬리부터)
    thr = fade * 1.15 + (1 - np.clip(s, 0, 1)) * 0.35 * fade
    a *= smoothstep(thr - 0.08, thr + 0.08, breaks)
    a *= (1 - fade) ** 0.7 * style["alpha"]
    return a


def flipbook(rng, style):
    sheet = np.zeros((C * 4, C * 4))
    fib_r = np.clip((noise1d(900, 120, rng, 3) - 0.3) / 0.5, 0, 1) ** 1.8
    for k in range(16):
        breaks = noise2d(C, C, 6, 6, rng, 3)
        a = crescent_frame(rng, k, style, fib_r, breaks)
        r, c = divmod(k, 4)
        sheet[r * C:(r + 1) * C, c * C:(c + 1) * C] = a
    return sheet


def preview(paths):
    """확인용: 어두운 회색 바탕에 모두 붙여 한 장으로"""
    ims = [Image.open(p) for p in paths]
    width = 1100
    rows = []
    y = 10
    canvas = Image.new("RGBA", (width, 10), (55, 55, 65, 255))
    placed = []
    for im in ims:
        scale = min(1.0, (width - 20) / im.width, 512 / im.height)
        im2 = im.resize((int(im.width * scale), int(im.height * scale)), Image.LANCZOS)
        placed.append((im2, y))
        y += im2.height + 10
    canvas = Image.new("RGBA", (width, y), (55, 55, 65, 255))
    for im2, yy in placed:
        canvas.alpha_composite(im2, (10, yy))
    p = os.path.join(OUT, "_preview.png")
    canvas.convert("RGB").save(p)
    return p


if __name__ == "__main__":
    paths = []
    a, val = beam_body(RNG)
    paths.append(save("beam_body", a, val))
    a, _ = beam_core(RNG)
    paths.append(save("beam_core", a))
    a, _ = beam_wisp(RNG)
    paths.append(save("beam_wisp", a))
    paths.append(save("flip_thick", flipbook(RNG, {"span": 165, "thick": 0.17, "alpha": 1.0})))
    paths.append(save("flip_thin", flipbook(RNG, {"span": 150, "thick": 0.09, "alpha": 1.0})))
    paths.append(save("flip_trail", flipbook(RNG, {"span": 175, "thick": 0.12, "alpha": 0.85})))
    print(preview(paths))
    for p in paths:
        print(p)
