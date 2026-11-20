# The Foreman (공장 4번 보스) 메쉬 생성
# 실행 (Blender MCP): exec(open(r"D:\god\scripts\monster_kit.py", encoding="utf-8").read()); exec(open(r"D:\god\scripts\foreman_build.py", encoding="utf-8").read())
# 좌표: Blender (x, y, z) = Roblox HRP 기준 (-X, Z, Y). 앞 = -y, 캐릭터 오른쪽 = -x. 게임에서 scale 2.
# 부위 파괴용 이름(정의 breakParts): 2페이즈 "UpperTorso__Glass"(운전실 유리), 분노 "LeftHand__Mega"(확성기)
import math
from mathutils import Vector, Matrix

col = reset("Foreman")
for _n in ("Cube", "Light", "Camera"):
    if bpy.data.objects.get(_n):
        bpy.data.objects.remove(bpy.data.objects[_n], do_unlink=True)
rig_ref()

# ---------------- 몸통 (배 나온 거구) ----------------
TORSO = [(0, 0.02, -0.58, 0.76, 0.50), (0, -0.04, -0.20, 0.86, 0.60), (0, -0.04, 0.25, 0.92, 0.58),
         (0, -0.01, 0.64, 0.97, 0.52), (0, 0.03, 0.88, 0.93, 0.46), (0, 0.06, 1.02, 0.60, 0.35), (0, 0.06, 1.10, 0.31, 0.27)]
loft("UpperTorso__Cloth", TORSO, segs=36, sub=5, expo=0.8, cap0=0.02, cap1=0.02, amp=0.02, freq=5.0, seed=401)
loft("UpperTorso__Skin", [(0, 0.08, 0.98, 0.28, 0.26), (0, 0.04, 1.18, 0.27, 0.25), (0, -0.01, 1.32, 0.24, 0.23)], segs=14, sub=2)
# 반장 조끼 (앞 열림, 팔 구멍) + 반사 띠
def fm_cut(p):
    if p.y < -0.2 and abs(p.x) < 0.10:
        return True
    if abs(p.x) > 0.70 and p.z > 0.40:
        return True
    return p.z < -0.50
shell("UpperTorso__Vest", "UpperTorso__Cloth", 411, (0, 0, -1), 0.3, 0.6, 0.035, 0.03, mfreq=3.0, holes=0.25, zmin=-0.56, zmax=1.0, cut=fm_cut)
for z0, z1, sd in ((-0.05, 0.06, 412), (0.38, 0.49, 413)):
    shell("UpperTorso__Strip", "UpperTorso__Cloth", sd, (0, 0, -1), 0.3, 0.6, 0.068, 0.012, mfreq=3.0, holes=0.25, zmin=z0, zmax=z1, cut=fm_cut)
box("UpperTorso__Helmet", (0.40, -0.60, 0.62), (0.16, 0.02, 0.10))     # 가슴 명찰(흰 판)
loft("LowerTorso__Cloth", [(0, 0.02, -0.56, 0.80, 0.52), (0, 0.02, -0.80, 0.86, 0.54), (0, 0.03, -0.98, 0.76, 0.46)],
     segs=28, sub=3, expo=0.8, cap0=0.02, cap1=0.12, amp=0.012, freq=5.0, seed=402)
loft("LowerTorso__Boot", [(0, 0.02, -0.70, 0.85, 0.555), (0, 0.02, -0.58, 0.83, 0.545)], segs=28, sub=1, expo=0.8)   # 벨트
box("LowerTorso__Rust", (0, -0.57, -0.64), (0.24, 0.05, 0.15))                                                     # 버클
# 열쇠 꾸러미 (문을 잠근 열쇠들)
ring = Matrix(((1, 0, 0), (0, 0, 1), (0, 1, 0))).transposed()
torus("LowerTorso__Rust", (-0.50, -0.50, -0.86), 0.10, 0.10, 0.018, ring, 12, 4)
for k in range(5):
    a = math.radians(-60 + 30 * k)
    p = Vector((-0.50 + math.sin(a) * 0.10, -0.53, -0.86 - math.cos(a) * 0.10))
    d = Vector((math.sin(a), 0, -math.cos(a)))
    box("LowerTorso__Rust", tuple(p + d * 0.12), (0.035, 0.012, 0.20), rot=Matrix.Rotation(-a, 3, 'Y'))
    box("LowerTorso__Rust", tuple(p + d * 0.02), (0.07, 0.014, 0.06), rot=Matrix.Rotation(-a, 3, 'Y'))

# ---------------- 머리: 불독 턱 + 하얀 반장 안전모 ----------------
loft("Head__Skin", [(0, -0.20, 1.17, 0.20, 0.12), (0, -0.12, 1.27, 0.34, 0.30), (0, -0.05, 1.43, 0.37, 0.39),
                    (0, -0.02, 1.58, 0.37, 0.42), (0, 0.0, 1.73, 0.36, 0.43), (0, 0.03, 1.86, 0.33, 0.40),
                    (0, 0.04, 1.97, 0.24, 0.30)], segs=24, sub=3, cap0=0.05, cap1=0.09, amp=0.016, freq=7.0, seed=421)
push("Head__Skin", (0.15, -0.44, 1.70), 0.12, -0.06)
push("Head__Skin", (-0.15, -0.44, 1.70), 0.12, -0.06)
push("Head__Skin", (0.0, -0.45, 1.80), 0.18, 0.04)    # 찌푸린 이마
push("Head__Skin", (0.0, -0.46, 1.58), 0.08, 0.05)    # 코
push("Head__Skin", (0.0, -0.41, 1.38), 0.12, -0.05)   # 벌린 입
blob("Head__Dark", (0.0, -0.385, 1.38), (0.13, 0.03, 0.05), 10, 6)
blob("Head__Glow", (0.15, -0.405, 1.70), (0.04, 0.02, 0.03), 8, 6)
blob("Head__Glow", (-0.15, -0.405, 1.70), (0.04, 0.02, 0.03), 8, 6)
hv = blob("Head__Helmet", (0.0, 0.0, 0.0), (0.42, 0.48, 0.32), 22, 10, 0.006, 6.0, 422)
for v in hv:
    if v.co.z < 0:
        v.co.z = 0.0
bmh = PIECES["Head__Helmet"]
ro = []; ri = []
for i in range(28):
    a = 2 * math.pi * i / 28
    sy = 0.58 if math.sin(a) < 0 else 0.52
    ro.append(bmh.verts.new((math.cos(a) * 0.52, math.sin(a) * sy, -0.01)))
    ri.append(bmh.verts.new((math.cos(a) * 0.52, math.sin(a) * sy, -0.045)))
ct = bmh.verts.new((0, 0, -0.01)); cb = bmh.verts.new((0, 0, -0.045))
for i in range(28):
    i2 = (i + 1) % 28
    bmh.faces.new((ro[i], ro[i2], ct)); bmh.faces.new((ri[i2], ri[i], cb)); bmh.faces.new((ro[i2], ro[i], ri[i], ri[i2]))
blob("Head__Helmet", (0.0, 0.0, 0.29), (0.07, 0.42, 0.06), 10, 8, square=0.7)
for v in bmh.verts:
    v.co = Matrix.Rotation(math.radians(6), 3, 'X') @ v.co + Vector((0.0, 0.02, 1.86))

# ---------------- 다리 ----------------
for side, sx in (("Left", 0.498), ("Right", -0.498)):
    sd = 431 if sx > 0 else 432
    loft(side + "UpperLeg__Cloth", [(sx, 0.03, -0.84, 0.46, 0.45), (sx, 0.02, -1.15, 0.47, 0.46), (sx, 0.0, -1.55, 0.42, 0.41),
                                    (sx, -0.02, -2.14, 0.36, 0.36)], segs=16, sub=2, cap0=0.06, cap1=0.04, amp=0.024, freq=5.0, seed=sd)
    loft(side + "LowerLeg__Cloth", [(sx, -0.02, -1.70, 0.37, 0.37), (sx, 0.01, -2.00, 0.39, 0.39), (sx, 0.0, -2.30, 0.36, 0.36),
                                    (sx, -0.01, -2.50, 0.35, 0.35)], segs=16, sub=2, cap0=0.04, cap1=0.02, amp=0.024, freq=5.0, seed=sd + 2)
    loft(side + "LowerLeg__Boot", [(sx, -0.01, -2.40, 0.39, 0.39), (sx, -0.01, -2.70, 0.37, 0.37), (sx, -0.01, -2.97, 0.38, 0.39)],
         segs=16, sub=2, amp=0.008, freq=6.0, seed=sd + 4)
    loft(side + "Foot__Boot", [(sx, 0.32, -3.03, 0.34, 0.16), (sx, 0.10, -3.03, 0.36, 0.17), (sx, -0.22, -3.06, 0.37, 0.15),
                               (sx, -0.52, -3.08, 0.35, 0.13)], segs=16, sub=2, expo=0.6, cap0=0.05, cap1=0.14)
    for v in PIECES[side + "Foot__Boot"].verts:
        if v.co.z < -3.19:
            v.co.z = -3.19
    blob(side + "Foot__Rust", (sx, -0.55, -3.06), (0.31, 0.13, 0.10), 12, 6, square=0.7)
    for v in PIECES[side + "Foot__Rust"].verts:
        if v.co.z < -3.19:
            v.co.z = -3.19

# ---------------- 왼팔: 사람 팔 + 녹아 붙은 확성기 ----------------
loft("LeftUpperArm__Cloth", [(1.02, 0.03, 1.00, 0.35, 0.37), (1.14, 0.03, 0.80, 0.42, 0.42), (1.30, 0.02, 0.40, 0.38, 0.38),
                             (1.41, 0.02, 0.0, 0.34, 0.34), (1.44, 0.02, -0.18, 0.33, 0.33)], segs=16, sub=2, cap0=0.13, cap1=0.04, amp=0.02, freq=5.0, seed=441)
loft("LeftLowerArm__Cloth", [(1.43, 0.02, 0.34, 0.34, 0.34), (1.44, 0.02, 0.10, 0.34, 0.34), (1.445, 0.02, 0.0, 0.39, 0.39), (1.45, 0.02, -0.06, 0.35, 0.35)],
     segs=16, sub=2, cap0=0.02, cap1=0.02, amp=0.02, freq=6.0, seed=442)
loft("LeftLowerArm__Skin", [(1.445, 0.02, 0.0, 0.26, 0.26), (1.46, 0.01, -0.35, 0.25, 0.24), (1.48, -0.01, -0.68, 0.20, 0.19)], segs=14, sub=2, cap1=0.03, amp=0.015, freq=7.0, seed=443)
blob("LeftHand__Skin", (1.49, -0.06, -0.86), (0.20, 0.24, 0.20), 14, 10, 0.012, 9.0, 444, square=0.8)   # 확성기 손잡이를 쥔 주먹
# 확성기: 손에서 앞(-y)으로 뻗은 나팔. 손잡이 + 몸통 + 벌어진 입
mega = []
for k, (yy, r) in enumerate(((-0.25, 0.12), (-0.45, 0.13), (-0.70, 0.20), (-0.95, 0.30), (-1.10, 0.38))):
    mega.append((1.49, yy, -0.70, r, r))
loft("LeftHand__Mega", mega, segs=20, sub=2, cap0=0.06, cap1=0.0)
loft("LeftHand__Dark", [(1.49, -1.06, -0.70, 0.35, 0.35), (1.49, -1.04, -0.70, 0.08, 0.08)], segs=20, sub=1)   # 나팔 안쪽
box("LeftHand__Mega", (1.49, -0.36, -0.86), (0.08, 0.10, 0.22))       # 손잡이
loft("LeftHand__Rust", [(1.49, -1.12, -0.70, 0.39, 0.39), (1.49, -1.10, -0.70, 0.39, 0.39)], segs=20, sub=1)   # 나팔 테두리
# 손과 확성기를 녹여 붙인 슬래그 덩어리
blob("LeftHand__Rust", (1.49, -0.30, -0.80), (0.16, 0.14, 0.14), 10, 8, 0.03, 9.0, 445, kind="rock")

# ---------------- 오른팔: 위팔은 사람, 팔꿈치 아래는 크레인 붐 ----------------
loft("RightUpperArm__Cloth", [(-1.02, 0.03, 1.00, 0.35, 0.37), (-1.14, 0.03, 0.80, 0.42, 0.42), (-1.30, 0.02, 0.40, 0.38, 0.38),
                              (-1.41, 0.02, 0.06, 0.34, 0.34)], segs=16, sub=2, cap0=0.13, cap1=0.0, amp=0.02, freq=5.0, seed=446)
loft("RightUpperArm__Rust", [(-1.42, 0.02, 0.10, 0.37, 0.37), (-1.43, 0.02, -0.10, 0.36, 0.36)], segs=16, sub=1, cap0=0.02, cap1=0.04)   # 팔 끝 용접 고리
for a in range(0, 360, 60):   # 고리 볼트
    blob("RightUpperArm__Rust", (-1.425 + math.cos(math.radians(a)) * 0.37, 0.02 + math.sin(math.radians(a)) * 0.37, 0.0), (0.035, 0.035, 0.035), 6, 4)
# 붐: 네 모서리 현재 + 지그재그 가새 (RightLowerArm), 끝은 RightHand
w = 0.22
z0, z1 = 0.0, -0.74
for cx, cy in ((w, w), (w, -w), (-w, w), (-w, -w)):
    rod("RightLowerArm__Paint", (-1.46 + cx, 0.02 + cy, z0), (-1.47 + cx, 0.02 + cy, z1 - 0.02), 0.045)
zs = [(z0 - 0.04) + (z1 - z0 + 0.08) * k / 4 for k in range(5)]
for k in range(4):
    za, zb = zs[k], zs[k + 1]
    for (ax, ay), (bx, by) in ((((w, w), (-w, w))), (((-w, w), (-w, -w))), (((-w, -w), (w, -w))), (((w, -w), (w, w)))):
        if k % 2:
            ax, ay, bx, by = bx, by, ax, ay
        rod("RightLowerArm__Paint", (-1.465 + ax, 0.02 + ay, za), (-1.465 + bx, 0.02 + by, zb), 0.025, segs=6)
for cx, cy in ((w, w), (w, -w), (-w, w), (-w, -w)):
    rod("RightHand__Paint", (-1.47 + cx, 0.02 + cy, -0.80), (-1.47 + cx * 0.6, 0.02 + cy * 0.6, -1.35), 0.045)
# 도르래 블록 (붐 끝)
box("RightHand__Paint", (-1.47, 0.02, -1.45), (0.20, 0.42, 0.26))
loft("RightHand__Rust", [(-1.62, 0.02, -1.45, 0.18, 0.18), (-1.32, 0.02, -1.45, 0.18, 0.18)], segs=16, sub=1, cap0=0.01, cap1=0.01)   # 도르래
# 사슬 + 큰 갈고리
chain("RightHand__Rust", [(-1.47, 0.02, -1.58), (-1.47, 0.02, -1.80), (-1.47, 0.02, -2.02)], link_len=0.30, link_w=0.20, thick=0.042)
Mh = Matrix.Translation((-1.47, 0.02, -2.80)) @ Matrix.Rotation(math.radians(180), 4, 'Z')
hook("RightHand__Hook", Mh, scale=1.5, shank=0.30, R=0.36, thick=0.14)

# ---------------- 등: 박힌 크레인 운전실 ----------------
cab_c = Vector((0.0, 0.95, 0.55))
CW, CD, CH = 0.80, 0.55, 0.65   # 반폭·반깊이·반높이
t = 0.04
# 바닥·지붕·뒤판(등에 붙는 쪽 = 앞쪽 -y 판은 몸에 박힘)
box("UpperTorso__Paint", tuple(cab_c + Vector((0, 0, -CH))), (CW * 2, CD * 2, t * 2))
box("UpperTorso__Paint", tuple(cab_c + Vector((0, 0, CH))), (CW * 2 + 0.08, CD * 2 + 0.08, t * 2))
box("UpperTorso__Paint", tuple(cab_c + Vector((0, -CD, 0))), (CW * 2, t * 2, CH * 2))
# 옆판·뒤판: 창틀만 (기둥 + 위아래 띠), 그 사이 유리
for sx in (-1, 1):
    box("UpperTorso__Paint", tuple(cab_c + Vector((sx * CW, 0, -CH * 0.55))), (t * 2, CD * 2, CH * 0.9))   # 옆 아래판
    for py in (-CD, 0.0, CD):
        box("UpperTorso__Paint", tuple(cab_c + Vector((sx * CW, py * 0.97, CH * 0.45))), (t * 2.2, 0.07, CH * 1.1))   # 창 기둥
    box("UpperTorso__Glass", tuple(cab_c + Vector((sx * CW, 0, CH * 0.45))), (0.02, CD * 1.9, CH * 1.0))   # 옆 유리
box("UpperTorso__Paint", tuple(cab_c + Vector((0, CD, -CH * 0.55))), (CW * 2, t * 2, CH * 0.9))   # 뒤 아래판
for px in (-CW, -CW / 3, CW / 3, CW):
    box("UpperTorso__Paint", tuple(cab_c + Vector((px * 0.97, CD, CH * 0.45))), (0.07, t * 2.2, CH * 1.1))
box("UpperTorso__Glass", tuple(cab_c + Vector((0, CD, CH * 0.45))), (CW * 1.9, 0.02, CH * 1.0))
# 날짜를 센 빗금 (옆 아래판 바깥, 5개 묶음 × 여러 줄) — 캐릭터 왼쪽(+x) 면
for row in range(3):
    for grp in range(5):
        gx = cab_c.y - CD * 0.75 + grp * 0.24
        gz = cab_c.z - CH * 0.25 - row * 0.20
        for s in range(4):
            box("UpperTorso__Dark", (cab_c.x + CW + t + 0.006, gx + s * 0.035, gz), (0.008, 0.012, 0.13))
        box("UpperTorso__Dark", (cab_c.x + CW + t + 0.006, gx + 0.05, gz), (0.008, 0.18, 0.012), rot=Matrix.Rotation(math.radians(35), 3, 'X'))
# 운전실과 등을 잇는 용접 받침 + 끊어진 레일 바퀴
box("UpperTorso__Rust", (0.0, 0.55, 0.30), (1.00, 0.20, 0.20))
box("UpperTorso__Rust", (0.0, 0.55, 0.85), (0.70, 0.20, 0.16))
for sx in (-1, 1):
    loft("UpperTorso__Rust", [(sx * 0.55, cab_c.y, cab_c.z + CH + 0.10, 0.16, 0.16), (sx * 0.55, cab_c.y, cab_c.z + CH + 0.20, 0.16, 0.16)],
         segs=16, sub=1, cap0=0.01, cap1=0.01, up=(0, 1, 0))
# 운전실 안: 의자 등받이·조종 레버 (어둡게)
box("UpperTorso__Dark", tuple(cab_c + Vector((0, 0.15, -0.25))), (0.50, 0.12, 0.60))
for sx in (-0.25, 0.25):
    rod("UpperTorso__Dark", tuple(cab_c + Vector((sx, -0.20, -0.55))), tuple(cab_c + Vector((sx, -0.25, -0.20))), 0.025, segs=6)

MATCOL = {"Cloth": (0.11, 0.13, 0.16), "Vest": (0.65, 0.28, 0.05), "Strip": (0.55, 0.55, 0.50), "Skin": (0.24, 0.13, 0.10),
          "Helmet": (0.80, 0.78, 0.72), "Boot": (0.09, 0.07, 0.06), "Rust": (0.22, 0.11, 0.06), "Paint": (0.62, 0.44, 0.06),
          "Hook": (0.62, 0.44, 0.06), "Glass": (0.35, 0.40, 0.42), "Dark": (0.01, 0.01, 0.01), "Glow": (1.0, 0.43, 0.10), "Mega": (0.55, 0.10, 0.07)}
print(finalize(col, MATCOL, decimate={"_big": 0.8}, sharp_keys=("Rust", "Paint", "Hook")))
