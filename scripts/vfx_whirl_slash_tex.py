# 칼날 회오리 베기 메시용 텍스처 (SurfaceAppearance): 색+투명도 맵 / 발광 마스크
# 참고 이미지(사용자, 2026-11-25): 앞날이 하얗게 타고 → 분홍·보라 → 꼬리는 어두운 보라로 끌리며 사라짐, 붓질 결
# UV 규칙 (scripts/blade_whirl_slashes.py): u = 칼날 길이 0(꼬리) → 1(끝, 휘두르는 앞), v = 0(바깥 날) → 1(안쪽)
# 실행(명령줄): D:\blender.exe -b --factory-startup --python-expr "exec(open(r'D:\god\scripts\vfx_whirl_slash_tex.py', encoding='utf-8').read())"
# 결과: D:\god\exports\decals\whirl\SlashColor.png (RGBA), SlashEmissive.png (흑백)
import bpy, math, os, random

W, H = 1024, 256
OUT = r"D:\god\exports\decals\whirl"
os.makedirs(OUT, exist_ok=True)
random.seed(7)

# 값 노이즈 (격자 무작위 + 부드러운 보간), 결이 길이 방향으로 길게 늘어나게 u 주파수를 낮게
GX, GY = 9, 48
grid = [[random.random() for _ in range(GY + 2)] for _ in range(GX + 2)]
grid2 = [[random.random() for _ in range(GY * 2 + 2)] for _ in range(GX * 2 + 2)]


def smooth(t):
    return t * t * (3 - 2 * t)


def vnoise(g, gx, gy, u, v):
    x, y = u * gx, v * gy
    i, j = int(x), int(y)
    fx, fy = smooth(x - i), smooth(y - j)
    a, b = g[i][j], g[i + 1][j]
    c, d = g[i][j + 1], g[i + 1][j + 1]
    return (a + (b - a) * fx) * (1 - fy) + (c + (d - c) * fx) * fy


def sstep(a, b, x):
    t = min(max((x - a) / (b - a), 0.0), 1.0)
    return t * t * (3 - 2 * t)


def lerp(a, b, t):
    return tuple(a[k] + (b[k] - a[k]) * t for k in range(3))


DARK = (0.10, 0.02, 0.20)
PURPLE = (0.48, 0.10, 0.95)
LILAC = (0.90, 0.58, 1.00)
WHITE = (1.0, 0.97, 1.0)


def ramp(i):
    if i < 0.35:
        return lerp(DARK, PURPLE, i / 0.35)
    if i < 0.72:
        return lerp(PURPLE, LILAC, (i - 0.35) / 0.37)
    return lerp(LILAC, WHITE, min((i - 0.72) / 0.22, 1.0))


col = [0.0] * (W * H * 4)
emi = [0.0] * (W * H * 4)
for y in range(H):
    v = (y + 0.5) / H
    for x in range(W):
        u = (x + 0.5) / W
        # 붓질 결: 길이 방향으로 길게 늘어난 줄 (굵기·길이 제각각)
        s = 0.55 * vnoise(grid, GX, GY, u, v) + 0.45 * vnoise(grid2, GX * 2, GY * 2, u, v)
        streak = 0.55 + 0.75 * sstep(0.35, 0.8, s)
        head = sstep(0.05, 0.86, u) ** 1.4  # 앞으로 갈수록 밝음
        edge = math.exp(-v * 3.4)  # 바깥 날 쪽이 밝음
        inten = min(head * edge * streak * 1.35, 1.0)
        c = ramp(inten)
        # 투명도: 꼬리·안쪽으로 사라짐, 결 사이로 조금씩 끊김
        a = (0.2 + 0.8 * head) * (1 - sstep(0.55, 1.0, v)) * sstep(0.0, 0.3, u) * (0.6 + 0.4 * streak)
        a = min(max(a * 1.25, 0.0), 1.0)
        e = min(inten * 1.15, 1.0) ** 1.3
        k = (y * W + x) * 4
        col[k:k + 4] = (c[0], c[1], c[2], a)
        emi[k:k + 4] = (e, e, e, 1.0)


def save(name, px):
    img = bpy.data.images.new(name, W, H, alpha=True)
    img.pixels.foreach_set(px)
    img.filepath_raw = os.path.join(OUT, name + ".png")
    img.file_format = "PNG"
    img.save()
    return img.filepath_raw


print("saved", save("SlashColor", col))
print("saved", save("SlashEmissive", emi))

# 발밑 빛 원 (플레이어 오라, 2026-11-25 사용자 참고 그림 3): 512x512, 가운데 은은한 라일락 빛 + 가는 흰·보라 고리 2겹 + 바깥으로 퍼지는 결
G = 512
gcol = [0.0] * (G * G * 4)
for y in range(G):
    for x in range(G):
        dx, dy = (x + 0.5) / G * 2 - 1, (y + 0.5) / G * 2 - 1
        r = math.sqrt(dx * dx + dy * dy)
        ang = math.atan2(dy, dx) / (2 * math.pi) + 0.5
        fib = 0.6 + 0.4 * vnoise(grid, GX, GY, min(r, 0.999), abs(ang - 0.5) * 1.998)  # 각도를 접어 이음매 없앰
        inner = math.exp(-(r / 0.42) ** 2) * 0.55
        ring1 = math.exp(-((r - 0.78) / 0.035) ** 2)
        ring2 = math.exp(-((r - 0.9) / 0.018) ** 2) * 0.7
        rays = math.exp(-((r - 0.6) / 0.25) ** 2) * 0.35 * fib
        a = min(inner + ring1 + ring2 + rays, 1.0) * (1 - sstep(0.94, 1.0, r))
        hot = min(ring1 * 0.9 + inner * 0.6, 1.0)
        c = lerp(PURPLE, WHITE, hot)
        k = (y * G + x) * 4
        gcol[k:k + 4] = (c[0], c[1], c[2], a)
img = bpy.data.images.new("WhirlGround", G, G, alpha=True)
img.pixels.foreach_set(gcol)
img.filepath_raw = os.path.join(OUT, "WhirlGround.png")
img.file_format = "PNG"
img.save()
print("saved", img.filepath_raw)
