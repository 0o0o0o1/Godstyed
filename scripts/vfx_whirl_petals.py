# 칼날 회오리 마무리 — 꽃잎 플립북 (Python numpy·Pillow 판, 2026-11-26)
# 사용자: "마지막 X 베기를 빼고 꽃잎이 날리면서 터지는 느낌", 보라 + 흰 끝, 소용돌이쳐 퍼진 뒤 흩날림, 많고 작게.
# Blender 렌더판(vfx_whirl_petals_blender.py)과 비교해 좋은 쪽을 씀.
# 방식: 꽃잎 곡면(오목하게 휘고 끝이 살짝 말린, 끝이 조금 파인 잎)을 점 구름으로 만들어 돌리면서 투영(z 버퍼),
#   면 방향으로 빛·뒷면·가장자리 빛(반투명 느낌)을 칠하고 3배로 그려 줄임 → 은은한 빛 번짐을 더함.
#   16칸 = 기울어진 축으로 한 바퀴 (반복 재생해도 이어짐). 색이 들어간 RGBA (Roblox 에서 Color 흰색).
# 실행: python scripts/vfx_whirl_petals.py → exports/vfx/blade_whirl/petal_py_<a|b>.png + _petal_py_preview.png

import math
import os
import numpy as np
from PIL import Image, ImageFilter

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "exports", "vfx", "blade_whirl")
os.makedirs(OUT, exist_ok=True)
CELL = 256
SS = 3  # 크게 그려 줄임
FRAMES = 16

# 색: 꽃잎 밑동 진보라 → 가운데 보라 → 가장자리·끝 흰 라일락
DEEP = np.array([60, 8, 130], dtype=np.float64)
MID = np.array([135, 40, 255], dtype=np.float64)
TIP = np.array([245, 232, 255], dtype=np.float64)


def petal_surface(shape: str, nu=520, nv=260):
    u = np.linspace(0.0, 1.0, nu)[:, None] * np.ones((1, nv))
    v = np.ones((nu, 1)) * np.linspace(-1.0, 1.0, nv)[None, :]
    if shape == "a":  # 밑동이 좁고 끝이 둥근 잎, 끝 가운데가 살짝 파임 (꽃잎다운 모양)
        uc = np.clip(u, 0, 1)
        grow = 0.42 * (np.clip(uc / 0.68, 0, 1) ** 0.75)
        round_tip = 0.42 * np.sqrt(np.clip(1 - ((uc - 0.68) / 0.32) ** 2, 0, 1))
        width = np.where(uc < 0.68, grow, round_tip)
        notch = 0.09 * np.exp(-(v / 0.2) ** 2)
        cup, curl = 0.55, 0.22
    else:  # 가늘고 긴 잎, 끝이 뾰족
        width = 0.30 * np.sin(np.pi * np.clip(u, 0, 1) ** 0.62) ** 1.1
        notch = 0.0 * v
        cup, curl = 0.45, 0.32
    length = 1.0 - notch
    uu = u * length
    x = v * width
    y = uu - 0.5
    z = cup * (x ** 2) * 2.2 - curl * (uu ** 2.2) + 0.04 * np.sin(v * 3.1 + uu * 4.0)  # 오목 + 끝 말림 + 잔물결
    # 색
    edge = np.clip(np.abs(v), 0, 1) ** 4.0
    tipw = np.clip(uu, 0, 1) ** 3.0
    base = np.clip(1 - uu / 0.35, 0, 1) ** 1.5
    t_mid = np.clip(uu / 0.55, 0, 1)
    col = DEEP[None, None, :] * (1 - t_mid[..., None]) + MID[None, None, :] * t_mid[..., None]
    whiten = np.clip(edge * 0.6 + tipw * 0.8, 0, 1)
    col = col * (1 - whiten[..., None]) + TIP[None, None, :] * whiten[..., None]
    col = col * (1 - 0.35 * base[..., None])
    # 잎맥: 가운데 + 양쪽 가는 줄 (끝으로 갈수록 옅게)
    vein = np.zeros_like(u)
    for k, s in ((0.0, 0.035), (-0.45, 0.025), (0.45, 0.025), (-0.75, 0.02), (0.75, 0.02)):
        vein = np.maximum(vein, np.exp(-((v - k * (0.6 + 0.4 * uu)) / s) ** 2) * (0.7 if k == 0 else 0.45))
    vein *= np.clip(1 - uu * 1.1, 0, 1) * (1 - edge)
    col = col * (1 - 0.28 * vein[..., None])
    return np.stack([x, y, z], -1), col


def normals(P):
    du = np.gradient(P, axis=0)
    dv = np.gradient(P, axis=1)
    n = np.cross(du, dv)
    n /= np.linalg.norm(n, axis=-1, keepdims=True) + 1e-9
    return n


def rot(axis, ang):
    axis = np.asarray(axis, dtype=np.float64)
    axis /= np.linalg.norm(axis)
    x, y, z = axis
    c, s = math.cos(ang), math.sin(ang)
    C = 1 - c
    return np.array([[c + x * x * C, x * y * C - z * s, x * z * C + y * s],
                     [y * x * C + z * s, c + y * y * C, y * z * C - x * s],
                     [z * x * C - y * s, z * y * C + x * s, c + z * z * C]])


LIGHT = np.array([0.35, 0.75, 0.55])
LIGHT /= np.linalg.norm(LIGHT)
VIEW = np.array([0.0, 0.0, 1.0])


def render_frame(P, col, N, k, shape):
    ang = 2 * math.pi * k / FRAMES
    # 기울어진 축으로 한 바퀴 + 다른 축으로 살짝 흔들림(한 바퀴에 정수 번이라 이어짐)
    R = rot((0.55, 0.35, 0.75) if shape == "a" else (0.25, 0.6, 0.7), ang) @ rot((1, 0, 0), 0.35 * math.sin(2 * ang))
    Q = P.reshape(-1, 3) @ R.T
    n = N.reshape(-1, 3) @ R.T
    c = col.reshape(-1, 3)
    ndl = n @ LIGHT
    ndv = n @ VIEW
    back = ndv < 0
    lam = np.abs(ndl)
    # 앞면 빛 + 뒷면은 빛이 비쳐 보이게(반투명), 가장자리 빛
    shade = 0.42 + 0.68 * lam
    shade = np.where(back, 0.55 + 0.35 * lam, shade)
    rim = (1 - np.abs(ndv)) ** 2.5
    rgb = c * shade[:, None] + np.array([235, 215, 255]) * (0.32 * rim)[:, None]
    # 투영
    S = CELL * SS
    scale = S * 0.78
    px = (Q[:, 0] * scale + S / 2).astype(np.int64)
    py = (-Q[:, 1] * scale + S / 2).astype(np.int64)
    ok = (px >= 0) & (px < S) & (py >= 0) & (py < S)
    px, py, z, rgb = px[ok], py[ok], Q[ok, 2], rgb[ok]
    order = np.argsort(z)  # 먼 것 → 가까운 것 (나중이 이김)
    img = np.zeros((S, S, 3))
    a = np.zeros((S, S))
    img[py[order], px[order]] = rgb[order]
    a[py[order], px[order]] = 1.0
    # 점 사이 빈틈 메우기 (작은 최대값 필터) 후 줄임
    A = Image.fromarray((a * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.GaussianBlur(1.2))
    Cimg = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(3))
    A = np.asarray(A.resize((CELL, CELL), Image.LANCZOS), dtype=np.float64) / 255
    C = np.asarray(Cimg.resize((CELL, CELL), Image.LANCZOS), dtype=np.float64)
    # 색을 알파로 나눠 가장자리 검은 테 없앰
    cov = np.asarray(Image.fromarray((a * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(3)).resize((CELL, CELL), Image.LANCZOS), dtype=np.float64) / 255
    C = C / np.maximum(cov, 1e-3)[..., None]
    C = np.clip(C, 0, 255)
    # 은은한 빛 번짐 (라일락)
    glow = np.asarray(Image.fromarray((A * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(7)), dtype=np.float64) / 255
    halo = np.clip(glow * 0.45 - A, 0, 1)
    out_a = np.clip(A + halo, 0, 1)
    lil = np.array([200, 150, 255], dtype=np.float64)
    out_c = (C * A[..., None] + lil * halo[..., None]) / np.maximum(out_a, 1e-3)[..., None]
    return np.clip(out_c, 0, 255), out_a


def sheet(shape):
    P, col = petal_surface(shape)
    N = normals(P)
    rgb = np.zeros((CELL * 4, CELL * 4, 3))
    alpha = np.zeros((CELL * 4, CELL * 4))
    for k in range(FRAMES):
        c, a = render_frame(P, col, N, k, shape)
        r, cc = divmod(k, 4)
        rgb[r * CELL:(r + 1) * CELL, cc * CELL:(cc + 1) * CELL] = c
        alpha[r * CELL:(r + 1) * CELL, cc * CELL:(cc + 1) * CELL] = a
    p = os.path.join(OUT, f"petal_py_{shape}.png")
    Image.fromarray(np.dstack([rgb, alpha * 255]).astype(np.uint8), "RGBA").save(p)
    return rgb, alpha


def preview(sheets, name):
    """확인용: 어두운 바탕에 칸 전부 + 작게 흩뿌린 장면 (더하기 + 덮기 섞음)"""
    bg = np.array([22, 18, 30], dtype=np.float64)
    W = CELL * 4
    canvas = np.ones((W * len(sheets) + 512, W, 3)) * bg
    for i, (rgb, a) in enumerate(sheets):
        canvas[i * W:(i + 1) * W] = canvas[i * W:(i + 1) * W] * (1 - a[..., None]) + rgb * a[..., None]
    # 흩뿌린 장면: 크기 18~40px 꽃잎 300장
    rng = np.random.default_rng(3)
    y0 = W * len(sheets)
    for _ in range(300):
        rgb, a = sheets[rng.integers(len(sheets))]
        k = rng.integers(FRAMES)
        r, cc = divmod(k, 4)
        cell_c = rgb[r * CELL:(r + 1) * CELL, cc * CELL:(cc + 1) * CELL]
        cell_a = a[r * CELL:(r + 1) * CELL, cc * CELL:(cc + 1) * CELL]
        s = int(rng.integers(18, 40))
        ci = Image.fromarray(np.dstack([cell_c, cell_a * 255]).astype(np.uint8), "RGBA").rotate(float(rng.uniform(0, 360)), expand=False).resize((s, s), Image.LANCZOS)
        arr = np.asarray(ci, dtype=np.float64)
        x = int(rng.integers(0, W - s))
        y = int(rng.integers(0, 512 - s))
        reg = canvas[y0 + y:y0 + y + s, x:x + s]
        al = arr[..., 3:4] / 255
        canvas[y0 + y:y0 + y + s, x:x + s] = reg * (1 - al) + arr[..., :3] * al
    p = os.path.join(OUT, name)
    Image.fromarray(np.clip(canvas, 0, 255).astype(np.uint8)).resize((512, int(canvas.shape[0] / 2)), Image.LANCZOS).save(p)
    return p


def finish_blender(shape):
    """최종 = Blender 렌더(petal_bl_*, 3D 빛) + 이 파일의 은은한 라일락 빛 번짐 → petal_<a|b>.png
    (2026-11-26 비교: Blender 판은 돌 때 빛을 받아 반짝이는 게 좋고, Python 판은 빛 번짐·색이 좋아서 합침)"""
    src = np.asarray(Image.open(os.path.join(OUT, f"petal_bl_{shape}.png")).convert("RGBA"), dtype=np.float64)
    rgb, A = src[..., :3], src[..., 3] / 255
    out_rgb = np.zeros_like(rgb)
    out_a = np.zeros_like(A)
    lil = np.array([200, 150, 255], dtype=np.float64)
    for k in range(FRAMES):
        r, c = divmod(k, 4)
        sl = (slice(r * CELL, (r + 1) * CELL), slice(c * CELL, (c + 1) * CELL))
        a = A[sl]
        glow = np.asarray(Image.fromarray((a * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(7)), dtype=np.float64) / 255
        halo = np.clip(glow * 0.45 - a, 0, 1)
        oa = np.clip(a + halo, 0, 1)
        out_rgb[sl] = (rgb[sl] * a[..., None] + lil * halo[..., None]) / np.maximum(oa, 1e-3)[..., None]
        out_a[sl] = oa
    p = os.path.join(OUT, f"petal_{shape}.png")
    Image.fromarray(np.dstack([np.clip(out_rgb, 0, 255), out_a * 255]).astype(np.uint8), "RGBA").save(p)
    return np.clip(out_rgb, 0, 255), out_a


if __name__ == "__main__":
    import sys
    if "final" in sys.argv:  # Blender 렌더 뒤: python scripts/vfx_whirl_petals.py final
        print(preview([finish_blender("a"), finish_blender("b")], "_petal_final_preview.png"))
    else:
        s = [sheet("a"), sheet("b")]
        print(preview(s, "_petal_py_preview.png"))
