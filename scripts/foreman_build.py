# The Foreman (공장 4번 보스) 메쉬 생성
# 실행 (Blender MCP): exec(open(r"D:\god\scripts\monster_kit.py", encoding="utf-8").read()); exec(open(r"D:\god\scripts\foreman_build.py", encoding="utf-8").read())
# 좌표: Blender (x, y, z) = Roblox HRP 기준 (-X, Z, Y). 앞 = -y, 캐릭터 오른쪽 = -x. 게임에서 scale 3.5.
# 2026-11-21 재제작: 상자 같던 몸 -> 구부정한 괴물 실루엣(혹 등, 파묻힌 머리, 굵은 팔다리), 운전실은 작게 기울어 혹에 파묻힘, 등에 파이프·철근·사슬
# 부위 파괴용 이름(정의 breakParts): 2페이즈 "UpperTorso__Glass"(운전실 유리), 분노 "LeftHand__Mega"(확성기)
import math
from mathutils import Vector, Matrix

col = reset("Foreman")
for _n in ("Cube", "Light", "Camera"):
    if bpy.data.objects.get(_n):
        bpy.data.objects.remove(bpy.data.objects[_n], do_unlink=True)
rig_ref()

# ---------------- 몸통: 구부정한 괴물 거구 (2026-11-21 재제작 — "네모난 자동차 같음") ----------------
# 실루엣: 앞으로 숙인 가슴 + 머리 뒤로 솟은 둥근 혹 등(운전실이 박힌 자리) + 넓은 승모근. 상자 느낌을 없애려고 단면을 둥글게(expo 1)
TORSO = [(0, 0.04, -0.58, 0.82, 0.54), (0, 0.02, -0.20, 0.98, 0.64), (0, 0.08, 0.25, 1.12, 0.74),
         (0, 0.18, 0.66, 1.22, 0.84), (0, 0.30, 1.04, 1.14, 0.86), (0, 0.42, 1.38, 0.90, 0.72),
         (0, 0.50, 1.62, 0.56, 0.48), (0, 0.50, 1.74, 0.18, 0.16)]
loft("UpperTorso__Cloth", TORSO, segs=40, sub=5, expo=1.0, cap0=0.02, cap1=0.04, amp=0.05, freq=3.2, seed=401)
# 혹 위 근육 덩어리(승모근) — 어깨에서 혹으로 이어지는 부푼 살
for sx, k in ((-1, 1.18), (1, 0.95)):   # 오른쪽(-x) 승모근이 더 크다 (비대칭)
    blob("UpperTorso__Cloth", (sx * 0.72, 0.20, 1.12 + 0.08 * (k - 1) * 5), (0.52 * k, 0.55 * k, 0.42 * k), 18, 12, 0.04, 4.0, 405 + sx, rot=Matrix.Rotation(sx * math.radians(-18), 3, 'Y'))
# 찢긴 작업복 사이로 드러난 살 (혹 꼭대기·목 뒤)
blob("UpperTorso__Skin", (0.0, 0.55, 1.52), (0.62, 0.50, 0.32), 20, 12, 0.06, 5.0, 407)
blob("UpperTorso__Skin", (-0.55, 0.40, 1.30), (0.30, 0.34, 0.22), 14, 10, 0.05, 6.0, 408)
blob("UpperTorso__Skin", (0.0, -0.08, 1.06), (0.34, 0.30, 0.20), 14, 10, 0.03, 6.0, 409)   # 목(앞으로 숙임)
# 반장 조끼 (앞 열림, 팔 구멍) + 반사 띠 — 몸이 커져도 조끼는 작아 보이게(꽉 낀 느낌)
def fm_cut(p):
    if p.y < -0.2 and abs(p.x) < 0.12:
        return True
    if abs(p.x) > 0.78 and p.z > 0.30:
        return True
    if p.y > 0.55:
        return True     # 등 혹은 덮지 않음
    return p.z < -0.50
shell("UpperTorso__Vest", "UpperTorso__Cloth", 411, (0, 0, -1), 0.3, 0.6, 0.04, 0.03, mfreq=3.0, holes=0.32, zmin=-0.56, zmax=0.95, cut=fm_cut)
for z0, z1, sd in ((-0.05, 0.06, 412), (0.38, 0.49, 413)):
    shell("UpperTorso__Strip", "UpperTorso__Cloth", sd, (0, 0, -1), 0.3, 0.6, 0.075, 0.012, mfreq=3.0, holes=0.32, zmin=z0, zmax=z1, cut=fm_cut)
box("UpperTorso__Helmet", (0.42, -0.70, 0.55), (0.16, 0.02, 0.10), rot=Matrix.Rotation(math.radians(-12), 3, 'X'))     # 가슴 명찰(흰 판)
loft("LowerTorso__Cloth", [(0, 0.04, -0.56, 0.86, 0.56), (0, 0.03, -0.80, 0.92, 0.58), (0, 0.03, -0.98, 0.82, 0.50)],
     segs=28, sub=3, expo=0.9, cap0=0.02, cap1=0.12, amp=0.02, freq=5.0, seed=402)
loft("LowerTorso__Boot", [(0, 0.03, -0.70, 0.91, 0.595), (0, 0.03, -0.58, 0.89, 0.585)], segs=28, sub=1, expo=0.9)   # 벨트
box("LowerTorso__Rust", (0, -0.61, -0.64), (0.26, 0.05, 0.16))                                                     # 버클
# 열쇠 꾸러미 (문을 잠근 열쇠들)
ring = Matrix(((1, 0, 0), (0, 0, 1), (0, 1, 0))).transposed()
torus("LowerTorso__Rust", (-0.54, -0.54, -0.86), 0.10, 0.10, 0.018, ring, 12, 4)
for k in range(5):
    a = math.radians(-60 + 30 * k)
    p = Vector((-0.54 + math.sin(a) * 0.10, -0.57, -0.86 - math.cos(a) * 0.10))
    d = Vector((math.sin(a), 0, -math.cos(a)))
    box("LowerTorso__Rust", tuple(p + d * 0.12), (0.035, 0.012, 0.20), rot=Matrix.Rotation(-a, 3, 'Y'))
    box("LowerTorso__Rust", tuple(p + d * 0.02), (0.07, 0.014, 0.06), rot=Matrix.Rotation(-a, 3, 'Y'))

# ---------------- 머리: 혹 앞에 파묻혀 앞으로 내민 불독 턱 + 금 간 반장 안전모 ----------------
# 리그의 Head 중심(1.67)보다 낮고 앞(-y)에 둔다 → 목 없이 어깨에 파묻힌 모양
HZ = -0.22   # 높이 보정
HY = -0.30   # 앞 보정
def hk(k):
    return (k[0], k[1] + HY, k[2] + HZ, k[3], k[4])
loft("Head__Skin", [hk(k) for k in [(0, -0.26, 1.17, 0.26, 0.14), (0, -0.17, 1.27, 0.40, 0.33), (0, -0.07, 1.43, 0.40, 0.40),
                    (0, -0.02, 1.58, 0.36, 0.40), (0, 0.0, 1.73, 0.33, 0.39), (0, 0.03, 1.84, 0.29, 0.35),
                    (0, 0.04, 1.93, 0.20, 0.25)]], segs=24, sub=3, cap0=0.05, cap1=0.08, amp=0.022, freq=7.0, seed=421)
push("Head__Skin", (0.15, -0.42 + HY, 1.68 + HZ), 0.13, -0.08)
push("Head__Skin", (-0.15, -0.42 + HY, 1.68 + HZ), 0.13, -0.08)
push("Head__Skin", (0.0, -0.43 + HY, 1.78 + HZ), 0.20, 0.06)    # 찌푸린 이마
push("Head__Skin", (0.0, -0.47 + HY, 1.30 + HZ), 0.22, 0.07)    # 앞으로 튀어나온 아래턱
push("Head__Skin", (0.0, -0.45 + HY, 1.40 + HZ), 0.12, -0.06)   # 벌린 입
blob("Head__Dark", (0.0, -0.425 + HY, 1.40 + HZ), (0.15, 0.03, 0.06), 10, 6)
for sx in (-1, 1):   # 아랫니 (튀어나온 송곳니)
    box("Head__Helmet", (sx * 0.10, -0.47 + HY, 1.44 + HZ), (0.035, 0.03, 0.07), rot=Matrix.Rotation(sx * math.radians(8), 3, 'Y'))
blob("Head__Glow", (0.15, -0.39 + HY, 1.68 + HZ), (0.045, 0.02, 0.03), 8, 6)
blob("Head__Glow", (-0.15, -0.39 + HY, 1.68 + HZ), (0.045, 0.02, 0.03), 8, 6)
hv = blob("Head__Helmet", (0.0, 0.0, 0.0), (0.38, 0.44, 0.29), 22, 10, 0.006, 6.0, 422)
for v in hv:
    if v.co.z < 0:
        v.co.z = 0.0
bmh = PIECES["Head__Helmet"]
ro = []; ri = []
for i in range(28):
    a = 2 * math.pi * i / 28
    sy = 0.53 if math.sin(a) < 0 else 0.47
    ro.append(bmh.verts.new((math.cos(a) * 0.47, math.sin(a) * sy, -0.01)))
    ri.append(bmh.verts.new((math.cos(a) * 0.47, math.sin(a) * sy, -0.045)))
ct = bmh.verts.new((0, 0, -0.01)); cb = bmh.verts.new((0, 0, -0.045))
for i in range(28):
    i2 = (i + 1) % 28
    bmh.faces.new((ro[i], ro[i2], ct)); bmh.faces.new((ri[i2], ri[i], cb)); bmh.faces.new((ro[i2], ro[i], ri[i], ri[i2]))
blob("Head__Helmet", (0.0, 0.0, 0.27), (0.07, 0.38, 0.06), 10, 8, square=0.7)
# 안전모: 우그러지고 비뚤어짐 (이빨 상자 2개는 이미 들어 있으니 안전모 꼭짓점만 — 마지막에 만든 것부터 hv 이후 전부)
for v in bmh.verts:
    if v.co.z > -0.1 and abs(v.co.y) < 0.6 and v.co.z < 0.5 and v.co.length < 0.7:
        dent = 0.05 * noise.noise(v.co * 4.0 + Vector((7, 1, 3)))
        v.co = Matrix.Rotation(math.radians(14), 3, 'X') @ Matrix.Rotation(math.radians(-10), 3, 'Y') @ (v.co * (1 + dent)) + Vector((0.04, -0.02 + HY, 1.80 + HZ))
# ---------------- 다리: 짧고 굵어 보이게 (허벅지·종아리 크게, 무릎 아래로 갈수록 좁게) ----------------
for side, sx in (("Left", 0.53), ("Right", -0.53)):
    sd = 431 if sx > 0 else 432
    loft(side + "UpperLeg__Cloth", [(sx, 0.04, -0.84, 0.56, 0.56), (sx, 0.03, -1.15, 0.58, 0.58), (sx, 0.0, -1.55, 0.50, 0.50),
                                    (sx, -0.02, -2.14, 0.40, 0.40)], segs=18, sub=2, cap0=0.06, cap1=0.04, amp=0.035, freq=4.0, seed=sd)
    loft(side + "LowerLeg__Cloth", [(sx, -0.02, -1.70, 0.42, 0.42), (sx, 0.01, -2.00, 0.45, 0.45), (sx, 0.0, -2.30, 0.40, 0.40),
                                    (sx, -0.01, -2.50, 0.38, 0.38)], segs=18, sub=2, cap0=0.04, cap1=0.02, amp=0.03, freq=4.0, seed=sd + 2)
    loft(side + "LowerLeg__Boot", [(sx, -0.01, -2.40, 0.43, 0.43), (sx, -0.01, -2.70, 0.41, 0.41), (sx, -0.01, -2.97, 0.42, 0.43)],
         segs=18, sub=2, amp=0.01, freq=6.0, seed=sd + 4)
    loft(side + "Foot__Boot", [(sx, 0.34, -3.03, 0.38, 0.16), (sx, 0.10, -3.03, 0.40, 0.17), (sx, -0.24, -3.06, 0.41, 0.15),
                               (sx, -0.56, -3.08, 0.39, 0.13)], segs=16, sub=2, expo=0.7, cap0=0.05, cap1=0.14)
    for v in PIECES[side + "Foot__Boot"].verts:
        if v.co.z < -3.19:
            v.co.z = -3.19
    blob(side + "Foot__Rust", (sx, -0.59, -3.06), (0.35, 0.14, 0.10), 12, 6, square=0.7)
    for v in PIECES[side + "Foot__Rust"].verts:
        if v.co.z < -3.19:
            v.co.z = -3.19

# ---------------- 왼팔: 고릴라처럼 굵은 팔 + 녹아 붙은 확성기 ----------------
loft("LeftUpperArm__Cloth", [(1.00, 0.06, 1.02, 0.46, 0.48), (1.16, 0.05, 0.80, 0.56, 0.56), (1.32, 0.03, 0.40, 0.48, 0.48),
                             (1.42, 0.02, 0.0, 0.40, 0.40), (1.45, 0.02, -0.18, 0.38, 0.38)], segs=18, sub=2, cap0=0.15, cap1=0.04, amp=0.035, freq=4.0, seed=441)
loft("LeftLowerArm__Cloth", [(1.43, 0.02, 0.34, 0.40, 0.40), (1.44, 0.02, 0.10, 0.42, 0.42), (1.445, 0.02, 0.0, 0.47, 0.47), (1.45, 0.02, -0.06, 0.43, 0.43)],
     segs=18, sub=2, cap0=0.02, cap1=0.02, amp=0.03, freq=5.0, seed=442)
loft("LeftLowerArm__Skin", [(1.445, 0.02, 0.0, 0.36, 0.36), (1.46, 0.01, -0.30, 0.38, 0.36), (1.48, -0.01, -0.68, 0.27, 0.25)], segs=16, sub=2, cap1=0.03, amp=0.03, freq=6.0, seed=443)
blob("LeftHand__Skin", (1.49, -0.06, -0.86), (0.25, 0.28, 0.24), 14, 10, 0.02, 8.0, 444, square=0.85)   # 확성기 손잡이를 쥔 주먹
# 확성기: 손에서 앞(-y)으로 뻗은 나팔 (조금 더 크게, 찌그러짐)
mega = []
for k, (yy, r) in enumerate(((-0.25, 0.14), (-0.45, 0.15), (-0.70, 0.23), (-0.95, 0.34), (-1.12, 0.44))):
    mega.append((1.49, yy, -0.70, r, r * 0.92))
loft("LeftHand__Mega", mega, segs=20, sub=2, cap0=0.06, cap1=0.0, amp=0.02, freq=5.0, seed=446)
loft("LeftHand__Dark", [(1.49, -1.08, -0.70, 0.40, 0.37), (1.49, -1.06, -0.70, 0.09, 0.09)], segs=20, sub=1)   # 나팔 안쪽
box("LeftHand__Mega", (1.49, -0.36, -0.86), (0.09, 0.11, 0.24))       # 손잡이
loft("LeftHand__Rust", [(1.49, -1.14, -0.70, 0.45, 0.42), (1.49, -1.12, -0.70, 0.45, 0.42)], segs=20, sub=1)   # 나팔 테두리
# 손과 확성기를 녹여 붙인 슬래그 덩어리 (손등까지 덮음)
blob("LeftHand__Rust", (1.49, -0.30, -0.80), (0.20, 0.17, 0.17), 10, 8, 0.04, 9.0, 445, kind="rock")
blob("LeftHand__Rust", (1.60, -0.05, -0.80), (0.14, 0.18, 0.14), 10, 8, 0.04, 9.0, 447, kind="rock")

# ---------------- 오른팔: 굵은 위팔, 팔꿈치 아래는 크레인 붐 ----------------
loft("RightUpperArm__Cloth", [(-1.00, 0.06, 1.02, 0.46, 0.48), (-1.16, 0.05, 0.80, 0.56, 0.56), (-1.32, 0.03, 0.40, 0.48, 0.48),
                              (-1.41, 0.02, 0.06, 0.40, 0.40)], segs=18, sub=2, cap0=0.15, cap1=0.0, amp=0.035, freq=4.0, seed=446)
loft("RightUpperArm__Rust", [(-1.42, 0.02, 0.12, 0.43, 0.43), (-1.43, 0.02, -0.10, 0.42, 0.42)], segs=18, sub=1, cap0=0.02, cap1=0.04)   # 팔 끝 용접 고리
for a in range(0, 360, 45):   # 고리 볼트
    blob("RightUpperArm__Rust", (-1.425 + math.cos(math.radians(a)) * 0.43, 0.02 + math.sin(math.radians(a)) * 0.43, 0.01), (0.04, 0.04, 0.04), 6, 4)
# 위팔에 살을 뚫고 박힌 철판 조각
blob("RightUpperArm__Rust", (-1.30, -0.30, 0.55), (0.18, 0.08, 0.22), 8, 6, 0.03, 8.0, 448, kind="rock")
# 붐: 네 모서리 현재 + 지그재그 가새 (RightLowerArm), 끝은 RightHand — 조금 굵게
w = 0.25
z0, z1 = 0.0, -0.74
for cx, cy in ((w, w), (w, -w), (-w, w), (-w, -w)):
    rod("RightLowerArm__Paint", (-1.46 + cx, 0.02 + cy, z0), (-1.47 + cx, 0.02 + cy, z1 - 0.02), 0.055)
zs = [(z0 - 0.04) + (z1 - z0 + 0.08) * k / 4 for k in range(5)]
for k in range(4):
    za, zb = zs[k], zs[k + 1]
    for (ax, ay), (bx, by) in ((((w, w), (-w, w))), (((-w, w), (-w, -w))), (((-w, -w), (w, -w))), (((w, -w), (w, w)))):
        if k % 2:
            ax, ay, bx, by = bx, by, ax, ay
        rod("RightLowerArm__Paint", (-1.465 + ax, 0.02 + ay, za), (-1.465 + bx, 0.02 + by, zb), 0.03, segs=6)
# 붐 안을 지나는 굵은 유압 호스
rod("RightLowerArm__Rust", (-1.42, -0.05, 0.10), (-1.50, 0.08, -0.75), 0.07, segs=8, amp=0.03, seed=449)
for cx, cy in ((w, w), (w, -w), (-w, w), (-w, -w)):
    rod("RightHand__Paint", (-1.47 + cx, 0.02 + cy, -0.80), (-1.47 + cx * 0.6, 0.02 + cy * 0.6, -1.35), 0.055)
# 도르래 블록 (붐 끝)
box("RightHand__Paint", (-1.47, 0.02, -1.45), (0.24, 0.46, 0.30))
loft("RightHand__Rust", [(-1.65, 0.02, -1.45, 0.20, 0.20), (-1.29, 0.02, -1.45, 0.20, 0.20)], segs=16, sub=1, cap0=0.01, cap1=0.01)   # 도르래
# 사슬 + 큰 갈고리 (위치는 이전과 같음 — 동작 FK 유지)
chain("RightHand__Rust", [(-1.47, 0.02, -1.58), (-1.47, 0.02, -1.80), (-1.47, 0.02, -2.02)], link_len=0.30, link_w=0.20, thick=0.045)
Mh = Matrix.Translation((-1.47, 0.02, -2.80)) @ Matrix.Rotation(math.radians(180), 4, 'Z')
hook("RightHand__Hook", Mh, scale=1.5, shank=0.30, R=0.36, thick=0.15)

# ---------------- 등: 혹에 반쯤 파묻혀 찌그러지고 기운 크레인 운전실 ----------------
# 운전실 부품을 원점 기준으로 만든 뒤, 한꺼번에 우그러뜨리고·기울여 혹 위로 옮긴다
cab_c = Vector((0.0, 0.0, 0.0))
CW, CD, CH = 0.66, 0.46, 0.52   # 반폭·반깊이·반높이 (이전보다 작게)
t = 0.04
cab_pieces = ("UpperTorso__Paint", "UpperTorso__Glass", "UpperTorso__Dark", "UpperTorso__Rust")
before = {n: (len(PIECES[n].verts) if n in PIECES else 0) for n in cab_pieces}
box("UpperTorso__Paint", tuple(cab_c + Vector((0, 0, -CH))), (CW * 2, CD * 2, t * 2))
box("UpperTorso__Paint", tuple(cab_c + Vector((0, 0, CH))), (CW * 2 + 0.08, CD * 2 + 0.08, t * 2))
box("UpperTorso__Paint", tuple(cab_c + Vector((0, -CD, 0))), (CW * 2, t * 2, CH * 2))
for sx in (-1, 1):
    box("UpperTorso__Paint", tuple(cab_c + Vector((sx * CW, 0, -CH * 0.55))), (t * 2, CD * 2, CH * 0.9))   # 옆 아래판
    for py in (-CD, 0.0, CD):
        box("UpperTorso__Paint", tuple(cab_c + Vector((sx * CW, py * 0.97, CH * 0.45))), (t * 2.2, 0.07, CH * 1.1))   # 창 기둥
    box("UpperTorso__Glass", tuple(cab_c + Vector((sx * CW, 0, CH * 0.45))), (0.02, CD * 1.9, CH * 1.0))   # 옆 유리
box("UpperTorso__Paint", tuple(cab_c + Vector((0, CD, -CH * 0.55))), (CW * 2, t * 2, CH * 0.9))   # 뒤 아래판
for px in (-CW, -CW / 3, CW / 3, CW):
    box("UpperTorso__Paint", tuple(cab_c + Vector((px * 0.97, CD, CH * 0.45))), (0.07, t * 2.2, CH * 1.1))
box("UpperTorso__Glass", tuple(cab_c + Vector((0, CD, CH * 0.45))), (CW * 1.9, 0.02, CH * 1.0))
# 날짜를 센 빗금 (옆 아래판 바깥) — 캐릭터 왼쪽(+x) 면
for row in range(3):
    for grp in range(4):
        gx = cab_c.y - CD * 0.75 + grp * 0.22
        gz = cab_c.z - CH * 0.25 - row * 0.17
        for s4 in range(4):
            box("UpperTorso__Dark", (cab_c.x + CW + t + 0.006, gx + s4 * 0.032, gz), (0.008, 0.012, 0.11))
        box("UpperTorso__Dark", (cab_c.x + CW + t + 0.006, gx + 0.05, gz), (0.008, 0.16, 0.012), rot=Matrix.Rotation(math.radians(35), 3, 'X'))
# 운전실 안: 의자 등받이·조종 레버
box("UpperTorso__Dark", tuple(cab_c + Vector((0, 0.12, -0.20))), (0.42, 0.10, 0.50))
for sx in (-0.2, 0.2):
    rod("UpperTorso__Dark", tuple(cab_c + Vector((sx, -0.18, -0.45))), tuple(cab_c + Vector((sx, -0.22, -0.16))), 0.022, segs=6)
# 끊어진 레일 바퀴 (지붕)
for sx in (-1, 1):
    loft("UpperTorso__Rust", [(sx * 0.45, cab_c.y, cab_c.z + CH + 0.08, 0.14, 0.14), (sx * 0.45, cab_c.y, cab_c.z + CH + 0.17, 0.14, 0.14)],
         segs=14, sub=1, cap0=0.01, cap1=0.01, up=(0, 1, 0))
# 변환: 우그러뜨림(노이즈) → 기울임(앞으로 처박힘 + 옆으로) → 혹 위 (반쯤 파묻힘)
CAB_R = Matrix.Rotation(math.radians(-38), 3, 'X') @ Matrix.Rotation(math.radians(22), 3, 'Y') @ Matrix.Rotation(math.radians(-14), 3, 'Z')
CAB_T = Vector((0.18, 0.98, 1.08))
for n in cab_pieces:
    bmc = PIECES.get(n)
    if not bmc:
        continue
    bmc.verts.ensure_lookup_table()
    for v in bmc.verts[before[n]:]:
        co = v.co.copy()
        if co.z > 0.3:   # 지붕 한쪽이 눌려 내려앉음
            co.z -= 0.18 * max(0.0, co.x + 0.2)
        co += Vector((noise.noise(co * 3.1 + Vector((1, 2, 3))), noise.noise(co * 3.1 + Vector((5, 1, 7))), noise.noise(co * 3.1 + Vector((9, 4, 2))))) * 0.05
        v.co = CAB_R @ co + CAB_T
# 운전실 가장자리를 덮으며 자라 오른 살 (운전실이 몸에 먹힌 느낌) + 용접 덩어리
for c, r, sd in (((-0.45, 0.80, 1.05), (0.45, 0.42, 0.38), 454), ((0.65, 0.78, 0.95), (0.40, 0.40, 0.34), 455),
                 ((0.05, 0.62, 1.42), (0.55, 0.36, 0.30), 456), ((0.20, 1.05, 0.70), (0.55, 0.30, 0.28), 457)):
    blob("UpperTorso__Skin", c, r, 16, 10, 0.07, 5.0, sd)
blob("UpperTorso__Rust", (0.10, 0.62, 1.00), (0.70, 0.22, 0.20), 14, 8, 0.05, 6.0, 450, kind="rock")
blob("UpperTorso__Rust", (-0.35, 0.72, 1.45), (0.30, 0.20, 0.18), 10, 8, 0.05, 7.0, 451, kind="rock")

# ---------------- 혹에서 뻗어 나온 파이프·철근·사슬 (실루엣을 깨는 가시) ----------------
SPIKES = (((-0.70, 0.55, 1.35), (-1.20, 1.15, 2.45), 0.08),     # 오른 어깨 뒤 굽은 배관
          ((-0.45, 0.75, 1.50), (-0.60, 1.30, 2.70), 0.055),
          ((-0.95, 0.30, 1.40), (-1.45, 0.55, 2.20), 0.05),      # 오른 어깨 바깥
          ((0.60, 0.65, 1.40), (1.05, 1.35, 2.30), 0.065),       # 왼쪽 뒤
          ((0.35, 0.40, 1.55), (0.50, 0.60, 2.55), 0.035),       # 철근
          ((-0.10, 0.85, 1.20), (-0.25, 1.75, 1.40), 0.045))
for i, (a, b, r) in enumerate(SPIKES):
    rod("UpperTorso__Rust", a, b, r, segs=8, amp=0.02, seed=460 + i)
    blob("UpperTorso__Rust", b, (r * 1.4, r * 1.4, r * 1.4), 8, 6)
# 혹을 가로질러 늘어진 사슬 (등 → 왼쪽 옆구리)
chain("UpperTorso__Rust", [(-0.75, 0.55, 1.25), (-0.30, 0.95, 0.95), (0.30, 0.90, 0.75), (0.80, 0.55, 0.55)], link_len=0.26, link_w=0.17, thick=0.038)
# 어깨 위 슬래그 껍질
for sx, sd in ((1, 452), (-1, 453)):
    blob("UpperTorso__Rust", (sx * 0.85, 0.15, 1.30), (0.32, 0.30, 0.14), 12, 8, 0.06, 7.0, sd, kind="rock", rot=Matrix.Rotation(sx * math.radians(-25), 3, 'Y'))

MATCOL = {"Cloth": (0.11, 0.13, 0.16), "Vest": (0.65, 0.28, 0.05), "Strip": (0.55, 0.55, 0.50), "Skin": (0.24, 0.13, 0.10),
          "Helmet": (0.80, 0.78, 0.72), "Boot": (0.09, 0.07, 0.06), "Rust": (0.22, 0.11, 0.06), "Paint": (0.62, 0.44, 0.06),
          "Hook": (0.62, 0.44, 0.06), "Glass": (0.35, 0.40, 0.42), "Dark": (0.01, 0.01, 0.01), "Glow": (1.0, 0.43, 0.10), "Mega": (0.55, 0.10, 0.07)}
print(finalize(col, MATCOL, decimate={"_big": 0.8}, sharp_keys=("Rust", "Paint", "Hook")))
