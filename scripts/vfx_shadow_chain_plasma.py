# 그림자 연쇄 처형 — 플라즈마 구슬 + 안쪽 핵 폭발 (2026-11-26 사용자 참고 그림: 검은 바탕에 남보라 소용돌이 구름 구슬,
# 흰·라일락 번개 줄기, 가운데 밝은 핵). 앞서 만든 리본 소용돌이(vfx_shadow_chain_burst.py)를 대신함.
# 그림을 베끼지 않고 느낌만 참고해 Python(numpy + Pillow)으로 새로 그림.
# 실행: python scripts/vfx_shadow_chain_plasma.py → exports/vfx/shadow_chain/plasma_*.png (+ _plasma_preview.png)
#
#   plasma_orb  1024x1024 4x4(칸 256) 모임: 크게 퍼진 구름이 바깥→안으로 빠르게 압축돼 구슬이 되고 (ORB_SIZE_KEYS), 번개가 핵으로 빨려 들며 핵이 작고 밝아짐.
#               색이 들어간 RGBA (Roblox 에서 Color 흰색, LightEmission 1). 캐릭터보다 작게 (약 4스터드)
#   plasma_pop  1024x1024 4x4 폭발: 핵 섬광 → 충격파 고리 → 껍질이 찢겨 바깥으로 흩어짐 → 보라 잔광. 약 9스터드
#               구슬 껍질 반지름은 pop 칸 기준 ORB_IN_POP 에서 시작 (orb 크기 / pop 크기)

import math
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "exports", "vfx", "shadow_chain")
os.makedirs(OUT, exist_ok=True)
N = 256
ORB_STUDS, POP_STUDS = 4.2, 9.0
ORB_R = 0.82  # orb 칸 안에서 구슬 반지름 (칸 반폭 = 1)
ORB_IN_POP = ORB_R * ORB_STUDS / POP_STUDS

RNG = np.random.default_rng(20261126)
TBL = [RNG.random((256, 256)) for _ in range(4)]


def smoothstep(e0, e1, x):
    d = e1 - e0
    if abs(d) < 1e-9:
        d = 1e-9
    t = np.clip((x - e0) / d, 0.0, 1.0)
    return t * t * (3 - 2 * t)


def vnoise(x, y, k=0):
    tb = TBL[k]
    xi = np.floor(x).astype(np.int64)
    yi = np.floor(y).astype(np.int64)
    fx, fy = x - xi, y - yi
    fx = fx * fx * (3 - 2 * fx)
    fy = fy * fy * (3 - 2 * fy)
    x0, y0 = xi % 256, yi % 256
    x1, y1 = (x0 + 1) % 256, (y0 + 1) % 256
    a = tb[y0, x0] * (1 - fx) + tb[y0, x1] * fx
    b = tb[y1, x0] * (1 - fx) + tb[y1, x1] * fx
    return a * (1 - fy) + b * fy


def fbm(x, y, k=0, octaves=5):
    s, amp, tot = 0.0, 0.5, 0.0
    for o in range(octaves):
        s = s + vnoise(x * 2 ** o + 13.1 * o, y * 2 ** o - 7.7 * o, k) * amp
        tot += amp
        amp *= 0.5
    return s / tot


def ridged(x, y, k=0, octaves=4, sharp=5.0):
    """가는 실(필라멘트): 노이즈가 0.5 를 지나는 곳이 밝은 선"""
    n = fbm(x, y, k, octaves)
    return (1 - np.abs(n * 2 - 1)) ** sharp


yy, xx = np.mgrid[0:N, 0:N].astype(np.float64)
X = (xx - N / 2 + 0.5) / (N / 2)
Y = -(yy - N / 2 + 0.5) / (N / 2)
R = np.sqrt(X * X + Y * Y)
TH = np.arctan2(Y, X)

# 색: 세기 → 남보라 → 보라 → 라일락 → 흰색
STOPS = [(0.0, (10, 2, 30)), (0.22, (55, 18, 140)), (0.45, (118, 52, 230)), (0.7, (190, 140, 255)), (0.88, (235, 215, 255)), (1.0, (255, 255, 255))]


def colorize(I):
    I = np.clip(I, 0, 1)
    rgb = np.zeros(I.shape + (3,))
    for (p0, c0), (p1, c1) in zip(STOPS[:-1], STOPS[1:]):
        m = (I >= p0) & (I <= p1)
        f = ((I - p0) / (p1 - p0))[m][:, None]
        rgb[m] = np.array(c0) * (1 - f) + np.array(c1) * f
    a = np.clip(I * 1.5, 0, 1) ** 0.85
    return rgb, a


def plasma_shell(radius, rot, seed_shift, tear=0.0, stretch=0.0):
    """소용돌이 구름 구슬. radius: 칸 기준 반지름, rot: 회전, tear: 0~1 찢어짐, stretch: 바깥으로 늘어남"""
    rn = R / radius
    # 소용돌이 감김을 노이즈로 흐트러뜨려 바람개비처럼 규칙적이지 않게
    jit = (fbm(X * 1.7 + 11, Y * 1.7 - 3, 2, 3) - 0.5) * 2.2
    twist = TH + 2.0 * np.clip(1 - rn, 0, 1) ** 1.3 + rot + jit
    # 바깥으로 늘어날 때는 반지름 방향 좌표를 눌러 줄무늬가 바깥으로 길게
    rr = rn / (1 + stretch * 1.8)
    u = rr * np.cos(twist) * 2.6 + seed_shift
    v = rr * np.sin(twist) * 2.6 - seed_shift * 0.7
    wx = fbm(u * 0.8 + 3.3, v * 0.8, 1, 3) - 0.5
    wy = fbm(u * 0.8, v * 0.8 - 5.1, 2, 3) - 0.5
    u2, v2 = u + wx * 1.6, v + wy * 1.6
    cloud = fbm(u2, v2, 0, 5)
    fil = ridged(u2 * 1.3, v2 * 1.3, 3, 4, 6.0)
    fil2 = ridged(u2 * 2.1 + 9, v2 * 2.1, 1, 3, 8.0)
    inside = smoothstep(1.08, 0.86, rn)
    # 구 느낌: 가운데 쪽 더 밝은 안개, 가장자리는 밝은 테두리 호(끊기며)
    haze = (cloud ** 2.2) * (0.32 * (1 - rn ** 2).clip(0) + 0.14) * inside
    arcs = fbm(np.cos(TH) * 1.6 + rot * 0.5 + seed_shift, np.sin(TH) * 1.6, 2, 3)
    rim = np.exp(-((rn - 0.93) / 0.07) ** 2) * smoothstep(0.42, 0.7, arcs) * 0.9
    strands = (fil * 0.85 + fil2 * 0.45) * smoothstep(1.02, 0.55, rn) * (0.35 + 0.65 * smoothstep(0.05, 0.5, rn)) * (0.4 + cloud)
    I = haze + strands * 0.7 + rim
    if tear > 0:
        # 구멍이 2D 노이즈로 숭숭 뚫리며 찢어짐 (각도만 쓰면 부채꼴 직선 자국이 남음)
        holes = fbm(u * 0.9 + 21, v * 0.9 - 4, 3, 4)
        keep = smoothstep(tear * 0.75 - 0.1, tear * 0.75 + 0.1, holes * 0.6 + cloud * 0.4)
        I = I * keep
    return I


def bolts(count, r_from, r_to, seed, width=1.6, jag=0.09, glow=True):
    """핵에서 바깥으로 뻗는 번개 (2배 해상도로 그려 줄임). 세기 배열 반환"""
    rng = np.random.default_rng(seed)
    S = N * 2
    img = Image.new("L", (S, S), 0)
    d = ImageDraw.Draw(img)
    for _ in range(count):
        a = rng.uniform(0, 2 * math.pi)
        r0 = r_from * rng.uniform(0.6, 1.0)
        r1 = r_to * rng.uniform(0.7, 1.0)
        steps = 14
        pts = []
        ang = a
        for i in range(steps + 1):
            f = i / steps
            r = r0 + (r1 - r0) * f
            ang += rng.normal(0, jag) / max(r, 0.15)
            pts.append(((math.cos(ang) * r + 1) * S / 2, (1 - math.sin(ang) * r) * S / 2))
        for i in range(steps):
            w = max(1, int(round(width * 2 * (1 - 0.7 * i / steps))))
            v = int(255 * (1 - 0.55 * i / steps))
            d.line([pts[i], pts[i + 1]], fill=v, width=w)
            # 곁가지
            if i > 3 and rng.random() < 0.18:
                bx, by = pts[i]
                ba = ang + rng.choice([-1, 1]) * rng.uniform(0.5, 1.1)
                L = rng.uniform(0.06, 0.16) * S / 2
                q = (bx + math.cos(ba) * L, by - math.sin(ba) * L)
                d.line([pts[i], q], fill=int(v * 0.6), width=max(1, w - 1))
    core = np.asarray(img.resize((N, N), Image.LANCZOS), dtype=np.float64) / 255
    if glow:
        g = np.asarray(img.resize((N, N), Image.LANCZOS).filter(ImageFilter.GaussianBlur(4)), dtype=np.float64) / 255
        return np.clip(core + g * 1.4, 0, 1.5)
    return core


# 모임 크기 변화 (Roblox ParticleEmitter Size 와 같은 값): 크게 퍼진 구름이 앞부분에서 빠르게 안으로 압축 → 살짝 튕겨 자리잡음
ORB_SIZE_KEYS = [(0.0, 9.5), (0.12, 8.2), (0.3, 3.9), (0.38, 4.5), (0.48, 4.2), (1.0, 4.2)]


def orb_size(t):
    for (t0, s0), (t1, s1) in zip(ORB_SIZE_KEYS[:-1], ORB_SIZE_KEYS[1:]):
        if t <= t1:
            return s0 + (s1 - s0) * (t - t0) / (t1 - t0)
    return ORB_SIZE_KEYS[-1][1]


def orb_frame(k):
    t = k / 15.0
    c = smoothstep(0.0, 0.32, t)  # 압축 정도 (0 = 넓게 흩어진 구름, 1 = 꽉 찬 구슬)
    radius = ORB_R * (1.12 - 0.12 * c)
    # 압축 중에는 소용돌이가 빨리 감기고(회전 큼), 다 모이면 천천히
    rot = -3.2 * c - 0.8 * t
    shell = plasma_shell(radius, rot=rot, seed_shift=0.0, tear=0.55 * (1 - c), stretch=0.9 * (1 - c))
    I = shell * (0.3 + 0.7 * c)
    # 안으로 빨려 드는 줄기: 각도로 촘촘하고 반지름으로 긴 가닥이 바깥→안으로 흐름
    flow = fbm(np.cos(TH) * 8 + 3, np.sin(TH) * 8 + R * 1.5 + t * 9, 2, 3) ** 3.5 * 2.6
    sucked = flow * smoothstep(0.15, 0.45, R) * smoothstep(1.0, 0.6, R) * (1 - smoothstep(0.25, 0.45, t))
    I = I + sucked
    # 번개: 압축이 끝나 갈 때부터, 갈수록 핵으로 빨려 듦 (짧아짐)
    reach = radius * (0.9 - 0.5 * smoothstep(0.35, 1.0, t))
    I = I + bolts(3 + (k % 2), 0.04, reach, 1000 + k) * 0.75 * smoothstep(0.2, 0.4, t)
    # 핵: 압축되며 생기고 작아지며 밝아짐
    cr = 0.2 - 0.11 * t
    core = (np.exp(-(R / cr) ** 2) * (0.6 + 0.6 * t) + np.exp(-(R / (cr * 2.6)) ** 2) * 0.35) * (0.25 + 0.75 * c)
    I = I + core
    return I * smoothstep(1.0, 0.9, R)


def pop_frame(k):
    t = k / 15.0
    e = 1 - (1 - t) ** 2.2  # 빠르게 퍼지다 느려짐
    # 섬광: 둥근 빛 + 짧은 가시 빛살
    fr = 0.1 + 0.45 * e
    rays = fbm(np.cos(TH) * 9 + 5, np.sin(TH) * 9, 0, 2) ** 3 * 2.2
    flash = (np.exp(-(R / fr) ** 2) * 1.6 + np.exp(-(R / (fr * 2.2)) ** 2) * rays) * (1 - smoothstep(0.0, 0.35, t))
    # 충격파 고리: 얇고 끊기며 울퉁불퉁
    rr = ORB_IN_POP * 0.7 + (0.95 - ORB_IN_POP * 0.7) * e
    rr_n = rr * (1 + 0.05 * (fbm(np.cos(TH) * 2.5, np.sin(TH) * 2.5 + 8, 2, 3) - 0.5))
    wid = 0.018 + 0.045 * t
    ring_n = smoothstep(0.3, 0.65, fbm(np.cos(TH) * 3 + 2, np.sin(TH) * 3, 1, 3))
    ring = np.exp(-((R - rr_n) / wid) ** 2) * (0.25 + 0.75 * ring_n) * (1 - smoothstep(0.15, 0.7, t)) * 1.2
    # 껍질: 구슬 크기에서 조금 더 크게 부풀며 구멍 뚫려 찢어짐
    sr = ORB_IN_POP * 1.05 + (0.8 - ORB_IN_POP * 1.05) * e
    shell = plasma_shell(sr, rot=-1.1 - 0.9 * e, seed_shift=0.0, tear=smoothstep(0.1, 1.0, t), stretch=0.4 * e)
    hollow = smoothstep(sr * (0.1 + 0.45 * e), sr * (0.5 + 0.4 * e), R)  # 가운데가 비어 감
    shell = shell * (0.35 + 0.65 * hollow) * (1.2 - 0.4 * t)
    # 바깥으로 튀는 연기 가닥: 각도로 촘촘·반지름으로 길게
    streak = fbm(np.cos(TH) * 7 + 1, np.sin(TH) * 7 + R * 1.2 - e * 2, 1, 3) ** 4 * 3.0
    band = smoothstep(sr * 0.75, sr * 0.95, R) * smoothstep(sr * 1.25 + 0.05, sr * 0.95, R)
    wisps = streak * band * smoothstep(0.05, 0.3, t) * 0.8
    I = shell + flash + ring + wisps
    if t < 0.45:
        I = I + bolts(6, 0.03, rr * 1.02, 2000 + k, width=1.6, jag=0.12) * (1 - smoothstep(0.12, 0.45, t)) * 1.0
    fade = 1 - smoothstep(0.62, 1.0, t)
    cool = 1 - 0.4 * smoothstep(0.3, 1.0, t)  # 식으며 어두운 보라로
    I = I * fade * cool
    return I * smoothstep(1.0, 0.92, R)


def sheet(fn):
    rgb = np.zeros((N * 4, N * 4, 3))
    a = np.zeros((N * 4, N * 4))
    for k in range(16):
        c, al = colorize(fn(k))
        row, col = divmod(k, 4)
        rgb[row * N:(row + 1) * N, col * N:(col + 1) * N] = c
        a[row * N:(row + 1) * N, col * N:(col + 1) * N] = al
    return rgb, a


def save(name, rgb, a):
    p = os.path.join(OUT, name + ".png")
    Image.fromarray(np.dstack([np.clip(rgb, 0, 255), a * 255]).astype(np.uint8), "RGBA").save(p)
    return p


def preview(orb, pop):
    """확인용: 검은 바탕 위에 더하기 합성 (Roblox LightEmission 1 과 비슷). 위 4줄 orb, 아래 4줄 pop.
    모든 칸을 같은 축척(칸 = 9.5스터드)으로 그려 실제 크기 변화가 보이게"""
    full = max(POP_STUDS, ORB_SIZE_KEYS[0][1])
    out = np.zeros((N * 8, N * 4, 3))
    for i, (rgb, a) in enumerate((orb, pop)):
        for k in range(16):
            row, col = divmod(k, 4)
            cell = rgb[row * N:(row + 1) * N, col * N:(col + 1) * N] * a[row * N:(row + 1) * N, col * N:(col + 1) * N, None]
            studs = orb_size(k / 15) if i == 0 else POP_STUDS
            sz = max(2, int(round(N * studs / full)))
            im = np.asarray(Image.fromarray(np.clip(cell, 0, 255).astype(np.uint8)).resize((sz, sz), Image.LANCZOS), dtype=np.float64)
            oy = i * N * 4 + row * N + (N - sz) // 2
            ox = col * N + (N - sz) // 2
            out[oy:oy + sz, ox:ox + sz] += im
    p = os.path.join(OUT, "_plasma_preview.png")
    Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)).resize((512, 1024), Image.LANCZOS).save(p)
    return p


if __name__ == "__main__":
    orb = sheet(orb_frame)
    pop = sheet(pop_frame)
    save("plasma_orb", *orb)
    save("plasma_pop", *pop)
    print(preview(orb, pop))
