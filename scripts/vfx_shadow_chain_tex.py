# 그림자 연쇄(단검 5번 스킬) 텍스처 — Python(numpy + Pillow)만 씀, Blender 안 씀.
# 실행: python scripts/vfx_shadow_chain_tex.py  → exports/vfx/shadow_chain/*.png (+ _preview.png 확인용)
# 모든 그림은 색 없는 흰색 + 알파 (색은 ParticleEmitter/Beam.Color, ImageColor3 로 칠함)
#
#   ink_puff     1024x1024 8x8(칸 128) 잉크 연기 64칸: 2D 유체 계산(회전하는 흐름장 + 처음 바깥으로 터짐)으로 덩어리가
#                말려 퍼지며 옅어짐. 검게 칠해 사라짐·도착·처형에 씀 (ParticleEmitter Grid8x8 OneShot)
#   streak_body  1024x256 그림자 궤적 몸통 (Beam Stretch, 가로 0 = 출발 → 1 = 도착): 도착 쪽이 굵고, 출발 쪽은 마른 붓 가닥으로 갈라짐
#   streak_edge  1024x256 같은 궤적의 빛나는 테두리 선 (몸통 위에 겹쳐 라일락으로)
#   slash        1024x1024 4x4(칸 256) 칼자국 16칸: 가로 바늘 칼자국이 그어지고(앞 3칸) → 머물다 → 결로 갈라지며 사라짐
#                (ParticleEmitter FacingCamera, Rotation 으로 방향, 두 개 엇갈리면 X)
#   mark         512x512 그림자 표식: 끊긴 고리 + 네 갈래 가시 + 가운데 마름모 (BillboardGui, 벤 적 몸에)

import math
import os
import numpy as np
from PIL import Image, ImageFilter

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "exports", "vfx", "shadow_chain")
os.makedirs(OUT, exist_ok=True)
RNG = np.random.default_rng(20261127)


def smoothstep(e0, e1, x):
    d = np.asarray(e1 - e0, dtype=np.float64)
    d = np.where(np.abs(d) < 1e-6, 1e-6, d)
    t = np.clip((x - e0) / d, 0.0, 1.0)
    return t * t * (3 - 2 * t)


def noise2d(h, w, cy, cx, rng, octaves=3):
    out = np.zeros((h, w))
    amp = total = 0.0
    amp = 1.0
    for o in range(octaves):
        gy, gx = cy * (2 ** o) + 1, cx * (2 ** o) + 1
        small = Image.fromarray((rng.random((gy, gx)) * 255).astype(np.uint8))
        out += amp * np.asarray(small.resize((w, h), Image.BICUBIC), dtype=np.float64) / 255.0
        total += amp
        amp *= 0.5
    return out / total


def noise1d(n, cells, rng, octaves=3):
    x = np.linspace(0, 1, n)
    out = np.zeros(n)
    amp, total = 1.0, 0.0
    for o in range(octaves):
        c = cells * (2 ** o)
        out += amp * np.interp(x, np.linspace(0, 1, c + 1), rng.random(c + 1))
        total += amp
        amp *= 0.5
    return out / total


def blur(a, r):
    im = Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8))
    return np.asarray(im.filter(ImageFilter.GaussianBlur(r)), dtype=np.float64) / 255.0


def save(name, alpha, value=None):
    a = np.clip(alpha, 0, 1)
    v = np.ones_like(a) if value is None else np.clip(value, 0, 1)
    rgb = (v * 255).astype(np.uint8)
    Image.fromarray(np.dstack([rgb, rgb, rgb, (a * 255).astype(np.uint8)]), "RGBA").save(os.path.join(OUT, name + ".png"))
    return os.path.join(OUT, name + ".png")


def sample(f, x, y):
    """f 를 (x, y) 픽셀 좌표에서 이중선형으로 (가장자리는 붙잡음)"""
    h, w = f.shape
    x = np.clip(x, 0, w - 1.001)
    y = np.clip(y, 0, h - 1.001)
    x0, y0 = np.floor(x).astype(int), np.floor(y).astype(int)
    fx, fy = x - x0, y - y0
    return (f[y0, x0] * (1 - fx) * (1 - fy) + f[y0, x0 + 1] * fx * (1 - fy)
            + f[y0 + 1, x0] * (1 - fx) * fy + f[y0 + 1, x0 + 1] * fx * fy)


# ---------------- 잉크 연기 (2D 유체 비슷한 계산) ----------------
def ink_puff(rng, frames=64, n=128):
    yy, xx = np.mgrid[0:n, 0:n].astype(np.float64)
    cx = cy = (n - 1) / 2
    dx, dy = xx - cx, yy - cy
    r = np.sqrt(dx * dx + dy * dy) + 1e-6
    # 처음 덩어리: 가운데 뭉친 잉크 + 노이즈로 울퉁불퉁 + 작은 덩이 몇 개
    d = smoothstep(n * 0.2, n * 0.05, r) * (0.6 + 0.6 * noise2d(n, n, 4, 4, rng, 3))
    for _ in range(5):
        a = rng.uniform(0, 2 * math.pi)
        rr = rng.uniform(0.05, 0.14) * n
        bx, by = cx + math.cos(a) * rr, cy + math.sin(a) * rr
        d += smoothstep(n * 0.07, 0, np.sqrt((xx - bx) ** 2 + (yy - by) ** 2)) * rng.uniform(0.4, 0.8)
    d = np.clip(d, 0, 1.4)
    # 흐름장: 두 흐름 함수(노이즈) 사이를 시간에 따라 섞은 회전 흐름(발산 없음) + 처음 바깥으로 터지는 흐름
    psi_a = noise2d(n, n, 3, 3, rng, 3)
    psi_b = noise2d(n, n, 3, 3, rng, 3)
    cells = []
    for f in range(frames):
        t = f / (frames - 1)
        for _ in range(2):  # 프레임당 두 번
            psi = psi_a * (1 - t) + psi_b * t
            gy, gx = np.gradient(psi)
            swirl = 26.0 * (0.6 + 0.4 * (1 - t))
            vx, vy = gy * swirl * n / 8, -gx * swirl * n / 8
            burst = 3.2 * (1 - t) ** 2.2  # 2차: 칸을 더 채우게 (1차 1.6 은 칸의 40%만)
            vx += dx / r * burst * smoothstep(0, n * 0.3, r) * 1.0
            vy += dy / r * burst * smoothstep(0, n * 0.3, r) * 1.0
            vy -= 0.25 * t  # 아주 살짝 위로 (그림 위 = 위)
            d = sample(d, xx - vx * 0.5, yy - vy * 0.5)
            d *= 0.993
        if f % 6 == 5:
            d = d * 0.7 + blur(d / 1.4, 0.8) * 1.4 * 0.3  # 조금씩 번짐
        # 알파: 잉크 농도 → 부드럽게, 가장자리는 결이 남게
        alpha = 1 - np.exp(-2.2 * d)
        alpha *= smoothstep(n * 0.5, n * 0.42, r)  # 칸 가장자리 투명
        alpha *= 1 - t ** 1.8  # 끝으로 갈수록 옅어짐 (2차: 늦게)
        cells.append(alpha)
    sheet = np.zeros((n * 8, n * 8))
    for i, c in enumerate(cells):
        row, col = divmod(i, 8)
        sheet[row * n:(row + 1) * n, col * n:(col + 1) * n] = c
    return sheet


# ---------------- 그림자 궤적 띠 ----------------
W, H = 1024, 256
U = np.linspace(0, 1, W)[None, :].repeat(H, 0)  # 0 출발 → 1 도착
V = np.linspace(-1, 1, H)[:, None].repeat(W, 1)


def wavy(amount, rng, cells=5):
    return V + (noise2d(H, W, 3, cells, rng, 2) - 0.5) * 2 * amount


def fibers(v01, rows, rng, sharp=1.6):
    f = noise1d(rows, 60, rng, 4)
    f = np.interp(v01, np.linspace(0, 1, rows), f)
    return np.clip((f - 0.25) / 0.6, 0, 1) ** sharp


def streak_half():
    # 도착 쪽(u=1)이 굵고 끝은 둥글게 빠짐, 출발 쪽으로 가늘어짐
    return 0.85 * np.clip(U / 0.82, 0, 1) ** 1.3 * np.clip((0.97 - U) / 0.14, 0, 1) ** 0.55  # 2차: 끝이 그림 안에서 닫힘


def streak_body(rng):
    half = np.maximum(streak_half() * (0.85 + 0.3 * noise2d(H, W, 1, 12, rng, 2)), 1e-3)
    vv = wavy(0.1, rng)
    inside = smoothstep(half, half * 0.75, np.abs(vv))
    fib = blur(fibers(np.clip((vv + 1) / 2, 0, 1), 2000, rng), 1.0)
    breaks = noise2d(H, W, 10, 16, rng, 3)
    erosion = smoothstep(0.1 + 0.6 * (1 - U), 0.25 + 0.6 * (1 - U), breaks)  # 출발 쪽일수록 많이 갈라짐
    a = inside * (0.35 + 0.65 * fib) * (0.15 + 0.85 * erosion)
    a *= smoothstep(0.0, 0.15, U) * (streak_half() > 0.004)  # 끝 찌꺼기 선 제거
    a *= smoothstep(1.0, 0.9, np.abs(V))
    return a


def streak_edge(rng):
    # 2차: 1차는 2D 노이즈로 끊어 덩어리져 보였음 → 길이 방향(1D)으로만 길게 끊기는 가는 선 두 줄 + 가운데 심
    half = np.maximum(streak_half(), 1e-3)
    vv = wavy(0.05, rng, 4)
    rel = np.abs(vv) / half
    edge = smoothstep(0.7, 0.86, rel) * smoothstep(0.98, 0.88, rel)
    core = smoothstep(0.07, 0.0, np.abs(wavy(0.03, rng, 3))) * smoothstep(0.45, 0.95, U)
    up = (vv < 0)
    keep_top = smoothstep(0.35, 0.5, noise1d(W, 9, rng, 2))[None, :]
    keep_bot = smoothstep(0.35, 0.5, noise1d(W, 9, rng, 2))[None, :]
    keep = np.where(up, keep_top, keep_bot)
    a = np.maximum(edge * keep * 0.9, core)
    a *= smoothstep(0.2, 0.6, U) * (half > 0.01)
    a *= smoothstep(1.0, 0.9, np.abs(V))
    return a


# ---------------- 칼자국 플립북 ----------------
def slash_sheet(rng, n=256):
    yy, xx = np.mgrid[0:n, 0:n].astype(np.float64)
    x = (xx - n / 2) / (n / 2)  # -1..1, 가로 = 칼자국 길이
    y = (yy - n / 2) / (n / 2)
    bend = 0.08
    yc = y - bend * (1 - x * x)  # 살짝 휜 칼자국
    fib = np.clip((noise1d(800, 140, rng, 3) - 0.3) / 0.5, 0, 1) ** 1.6
    sheet = np.zeros((n * 4, n * 4))
    for k in range(16):
        draw = min(1.0, (k + 1) / 3.0)  # 앞 3칸 그어짐
        fade = max(0.0, (k - 4) / 11.0)  # 5칸째부터 사라짐
        head = -0.95 + 1.9 * draw
        s = (x + 0.95) / 1.9  # 0 꼬리 → 1 머리
        on = (x >= -0.95) & (x <= head)
        # 굵기: 머리 쪽 70% 에서 가장 굵고 양 끝 바늘
        prof = np.clip(s / 0.7, 0, 1) ** 0.9 * np.clip((1 - s) / 0.3, 0, 1) ** 0.6
        thick = 0.15 * prof * (1 - 0.65 * fade)
        band = smoothstep(thick + 0.012, thick * 0.55, np.abs(yc)) * on
        f = np.interp(yc, np.linspace(-0.25, 0.25, fib.size), fib)
        core = smoothstep(thick * 0.45, 0, np.abs(yc)) * on
        a = np.maximum(band * (0.55 + 0.45 * f), core)
        # 그어지는 앞머리 밝은 점
        if draw < 1:
            a += smoothstep(0.08, 0.0, np.sqrt(((x - head) / 1.6) ** 2 + yc ** 2)) * 0.8
        # 사라짐: 결 방향(가로)으로 길쭉하게 갈라지며 (꼬리부터)
        brk = noise2d(n, n, 18, 3, rng, 2)
        thr = fade * 1.1 + (1 - s) * 0.3 * fade
        a *= smoothstep(thr - 0.06, thr + 0.06, brk)
        a *= (1 - fade) ** 0.6
        # 옆에 가는 머리카락 선 하나 (조금 늦게)
        hair = smoothstep(0.008, 0.0, np.abs(yc + 0.06 - 0.02 * x)) * ((x > -0.6) & (x < head * 0.9)) * 0.7 * (1 - fade)
        a = np.clip(np.maximum(a, hair), 0, 1)
        r, c = divmod(k, 4)
        sheet[r * n:(r + 1) * n, c * n:(c + 1) * n] = a
    return sheet


# ---------------- 표식 ----------------
def mark(rng, n=512):
    yy, xx = np.mgrid[0:n, 0:n].astype(np.float64)
    x, y = (xx - n / 2) / (n / 2), (yy - n / 2) / (n / 2)
    r = np.sqrt(x * x + y * y)
    th = np.arctan2(y, x)
    # 끊긴 고리: 네 조각 (가시 사이)
    ring = smoothstep(0.035, 0.0, np.abs(r - 0.72)) * smoothstep(0.08, 0.2, np.abs(np.sin(2 * (th - math.pi / 4))))
    ring *= 0.75 + 0.25 * noise2d(n, n, 2, 40, rng, 2)
    # 네 갈래 가시 (위·아래 길게, 좌우 짧게): 가늘고 끝이 뾰족한 마름모
    spikes = np.zeros_like(r)
    for ang, length in ((0, 0.62), (math.pi / 2, 0.92), (math.pi, 0.62), (-math.pi / 2, 0.92)):
        ax, ay = math.cos(ang), math.sin(ang)
        along = x * ax + y * ay
        side = np.abs(-x * ay + y * ax)
        w = 0.07 * np.clip(1 - along / length, 0, 1) * (along > 0.05)
        spikes = np.maximum(spikes, smoothstep(w + 0.006, w * 0.4, side) * (along < length) * (along > 0.05))
    # 가운데 마름모 (속은 비움)
    dia = np.abs(x) + np.abs(y)
    diamond = smoothstep(0.03, 0.0, np.abs(dia - 0.16)) + smoothstep(0.1, 0.07, dia)  # 테두리 + 작은 꽉 찬 심
    a = np.clip(np.maximum(np.maximum(ring, spikes), diamond), 0, 1)
    glow = blur(a, 6) * 0.45
    return np.clip(np.maximum(a, glow), 0, 1)


def preview(paths):
    ims = [Image.open(p) for p in paths]
    width = 1100
    placed, y = [], 10
    for im in ims:
        s = min(1.0, (width - 20) / im.width, 520 / im.height)
        im2 = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)
        placed.append((im2, y))
        y += im2.height + 10
    canvas = Image.new("RGBA", (width, y), (110, 100, 120, 255))
    for im2, yy in placed:
        canvas.alpha_composite(im2, (10, yy))
    p = os.path.join(OUT, "_preview.png")
    canvas.convert("RGB").save(p)
    return p


if __name__ == "__main__":
    paths = [
        save("ink_puff", ink_puff(RNG)),
        save("streak_body", streak_body(RNG)),
        save("streak_edge", streak_edge(RNG)),
        save("slash", slash_sheet(RNG)),
        save("mark", mark(RNG)),
    ]
    print(preview(paths))
