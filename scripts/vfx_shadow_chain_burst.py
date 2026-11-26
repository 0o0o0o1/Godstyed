# 그림자 연쇄 처형 — 대상 몸에서 원형으로 터지는 그림자 구슬 (2026-11-26 사용자 참고 그림: 가운데 흰·라일락 빛 구슬을
# 어두운 남보라 리본들이 공처럼 감싸 돌다가 찢어지며 터짐). 그림을 베끼지 않고 느낌만 참고해 Python(numpy + Pillow)으로 새로 그림.
# 실행: python scripts/vfx_shadow_chain_burst.py → exports/vfx/shadow_chain/burst_*.png (+ _burst_preview.png)
#
#   burst_body  1024x1024 4x4(칸 256) 리본 몸통 16칸: 바깥에서 말려 들며 공을 감쌈(0~4) → 돌며 머묾(5~7) → 바깥으로 터져
#               찢어지며 사라짐(8~15). 흰색 + 알파 → 어두운 남보라로 칠함
#   burst_rim   같은 칸·같은 리본의 바깥 가장자리 빛 (라일락으로, 빛나게)
#   burst_glow  512x512 가운데 빛 구슬 (흰 심 + 부드러운 번짐)
# 리본 하나 = 기울어진 타원(공 둘레를 감는 고리를 비스듬히 본 모습) 위의 호. 가운데 굵고 양 끝 뾰족, 끝은 바깥으로 살짝 말림,
#   가장자리는 노이즈로 찢긴 결

import math
import os
import numpy as np
from PIL import Image, ImageFilter

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "exports", "vfx", "shadow_chain")
os.makedirs(OUT, exist_ok=True)
RNG = np.random.default_rng(20261128)
N = 256


def smoothstep(e0, e1, x):
    d = np.asarray(e1 - e0, dtype=np.float64)
    d = np.where(np.abs(d) < 1e-6, 1e-6, d)
    t = np.clip((x - e0) / d, 0.0, 1.0)
    return t * t * (3 - 2 * t)


def noise1d_periodic(n, cells, rng):
    """주기 2π 로 이어지는 1D 노이즈 (각도용)"""
    pts = rng.random(cells)
    pts = np.append(pts, pts[0])
    x = np.linspace(0, 1, n)
    return np.interp(x, np.linspace(0, 1, cells + 1), pts)


def ang_noise(theta, table):
    """각도 theta(라디안 배열)에서 주기 노이즈 값"""
    k = ((theta % (2 * math.pi)) / (2 * math.pi)) * (len(table) - 1)
    return np.interp(k, np.arange(len(table)), table)


yy, xx = np.mgrid[0:N, 0:N].astype(np.float64)
X = (xx - N / 2) / (N / 2)
Y = -(yy - N / 2) / (N / 2)  # 위 = +

# 리본 정의 (같은 리본을 16칸 내내 씀)
# 2차 (첫 결과 확인 뒤): 가늘고 톱니 가장자리라 가시 발톱 같았음 → 굵고 매끈한 잉크 리본, 공 둘레에 고르게(각도 나눠 배치),
#   빛은 안쪽(구슬 쪽) 가장자리만, 터질 때 점선 대신 큰 조각 2~3개로 찢어짐 + 바깥으로 튀는 물방울
RIBBONS = []
COUNT = 9
for i in range(COUNT):
    RIBBONS.append({
        "phi": (i + RNG.uniform(-0.3, 0.3)) / COUNT * 2 * math.pi,
        "len": math.radians(RNG.uniform(120, 230)),
        "tilt": (i * 0.618 % 1) * math.pi,
        "squash": RNG.uniform(0.3, 1.0),
        "r": RNG.uniform(0.52, 0.66),
        "w": RNG.uniform(0.08, 0.16),
        "spin": RNG.uniform(0.6, 1.3) * (1 if RNG.random() < 0.8 else -1),
        "hook": RNG.uniform(0.1, 0.25),
        "tear": noise1d_periodic(512, 10, RNG),  # 낮은 주파수 (매끈한 굵기 변화)
        "tear2": noise1d_periodic(512, 4, RNG),
        "split": noise1d_periodic(512, 5, RNG),  # 터질 때 큰 조각으로 끊기는 곳
        "delay": RNG.uniform(0, 0.12),
    })
DROPS = [(RNG.uniform(0, 2 * math.pi), RNG.uniform(0.55, 0.8), RNG.uniform(0.02, 0.045)) for _ in range(14)]


def frame(k):
    t = k / 15.0
    body = np.zeros((N, N))
    rim = np.zeros((N, N))
    for rb in RIBBONS:
        tt = np.clip(t - rb["delay"] * (1 - t), 0, 1)
        form = smoothstep(0.0, 0.3, tt)
        burst = smoothstep(0.5, 1.0, tt)
        radius = rb["r"] * (1.4 - 0.4 * form) + 0.4 * burst ** 0.7
        arc = rb["len"] * (0.3 + 0.7 * form)
        width = rb["w"] * (0.45 + 0.55 * form) * (1 - 0.6 * burst)
        rot = rb["phi"] + rb["spin"] * (1.5 * tt + 0.7 * burst)
        c, s_ = math.cos(rb["tilt"]), math.sin(rb["tilt"])
        u = X * c + Y * s_
        v = (-X * s_ + Y * c) / rb["squash"]
        re = np.sqrt(u * u + v * v)
        th = np.arctan2(v, u)
        rel = ((th - rot + math.pi) % (2 * math.pi)) - math.pi
        sfrac = rel / (arc / 2)
        on = np.abs(sfrac) <= 1
        # 앞머리(+1) 쪽이 굵고 꼬리(-1) 쪽으로 길게 가늘어짐 (흐르는 잉크)
        head = np.clip((1 - sfrac) / 0.35, 0, 1) ** 0.7
        tail = np.clip((sfrac + 1) / 1.65, 0, 1) ** 1.4
        prof = head * tail
        target = radius * (1 + rb["hook"] * np.clip(sfrac, 0, 1) ** 4)
        swell = 0.75 + 0.5 * ang_noise(th * 2, rb["tear"]) * (0.7 + 0.3 * ang_noise(th, rb["tear2"]))
        half = width * prof * swell
        d = re - target
        thick_enough = smoothstep(0.004, 0.012, half)  # 꼬리 끝 머리카락 같은 점선·직선 찌꺼기 제거
        band = smoothstep(half + 0.008, half * 0.82, np.abs(d)) * on * thick_enough
        rimband = smoothstep(-half * 0.95, -half * 0.55, d) * smoothstep(-half * 0.15, -half * 0.5, d) * on * thick_enough  # 안쪽 가장자리
        if burst > 0:
            keep = smoothstep(burst * 0.9 - 0.06, burst * 0.9 + 0.06, ang_noise(th * 1.5 + rb["phi"], rb["split"]))
            band *= keep
            rimband *= keep
        body = np.maximum(body, band)
        rim = np.maximum(rim, rimband * 0.9)
    # 터질 때 바깥으로 튀는 물방울 (눈물 모양, 바깥으로 길쭉)
    pb = smoothstep(0.5, 0.75, t) * (1 - smoothstep(0.85, 1.0, t))
    if pb > 0:
        for ang, r0, size in DROPS:
            rr = r0 + 0.35 * smoothstep(0.5, 1.0, t)
            cx, cy = math.cos(ang) * rr, math.sin(ang) * rr
            ox, oy = math.cos(ang), math.sin(ang)
            px, py = X - cx, Y - cy
            along = px * ox + py * oy
            side = -px * oy + py * ox
            drop = smoothstep(1.0, 0.7, np.sqrt((along / (size * 2.2)) ** 2 + (side / size) ** 2))
            body = np.maximum(body, drop * pb)
            rim = np.maximum(rim, drop * pb * smoothstep(0.0, -size * 0.6, along) * 0.8)
    fade = 1 - smoothstep(0.75, 1.0, t)
    edge = smoothstep(1.0, 0.9, np.sqrt(X * X + Y * Y))
    return np.clip(body * fade * edge, 0, 1), np.clip(rim * fade * edge, 0, 1)


def sheet(which):
    out = np.zeros((N * 4, N * 4))
    for k in range(16):
        b, r = frame(k)
        a = b if which == "body" else r
        row, col = divmod(k, 4)
        out[row * N:(row + 1) * N, col * N:(col + 1) * N] = a
    return out


def glow(n=512):
    yy2, xx2 = np.mgrid[0:n, 0:n].astype(np.float64)
    r = np.sqrt(((xx2 - n / 2) / (n / 2)) ** 2 + ((yy2 - n / 2) / (n / 2)) ** 2)
    core = smoothstep(0.34, 0.26, r)
    halo = np.exp(-((r / 0.42) ** 2) * 2.2) * 0.85
    a = np.clip(np.maximum(core, halo) * smoothstep(1.0, 0.85, r), 0, 1)
    return a


def save(name, alpha):
    a = np.clip(alpha, 0, 1)
    w = np.full_like(a, 255, dtype=np.uint8)
    Image.fromarray(np.dstack([w, w, w, (a * 255).astype(np.uint8)]), "RGBA").save(os.path.join(OUT, name + ".png"))
    return os.path.join(OUT, name + ".png")


def preview():
    """확인용: 회색 바탕에 몸통(남보라) + 가장자리(라일락) + 빛 구슬을 겹쳐 칸별로"""
    body = np.asarray(Image.open(os.path.join(OUT, "burst_body.png")), dtype=np.float64)[..., 3] / 255
    rim = np.asarray(Image.open(os.path.join(OUT, "burst_rim.png")), dtype=np.float64)[..., 3] / 255
    g = np.asarray(Image.open(os.path.join(OUT, "burst_glow.png")).resize((N, N)), dtype=np.float64)[..., 3] / 255
    bg = np.array([70, 70, 78], dtype=np.float64)
    img = np.ones((N * 4, N * 4, 3)) * bg
    glow_full = np.tile(g, (4, 4))
    # 빛 구슬: 감싸는 동안 밝고 터지며 사라짐 (칸별 세기)
    gk = np.zeros((N * 4, N * 4))
    for k in range(16):
        row, col = divmod(k, 4)
        t = k / 15
        gk[row * N:(row + 1) * N, col * N:(col + 1) * N] = (0.4 + 0.6 * smoothstep(0, 0.3, t)) * (1 - smoothstep(0.55, 0.85, t))
    lil = np.array([190, 130, 255]) / 255
    a = glow_full * gk
    img = img * (1 - a[..., None]) + (np.array([255, 255, 255]) * (0.6 + 0.4 * lil))[None, None, :] * a[..., None]
    dark = np.array([28, 14, 70], dtype=np.float64)
    img = img * (1 - body[..., None]) + dark * body[..., None]
    img = img * (1 - rim[..., None]) + np.array([190, 140, 255]) * rim[..., None]
    p = os.path.join(OUT, "_burst_preview.png")
    Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)).resize((768, 768), Image.LANCZOS).save(p)
    return p


if __name__ == "__main__":
    save("burst_body", sheet("body"))
    save("burst_rim", sheet("rim"))
    save("burst_glow", glow())
    print(preview())
