# Hook Hauler (공장 2번 몬스터, 실내 작업자형) 메쉬 생성
# 실행 (Blender MCP): exec(open(r"D:\god\scripts\monster_kit.py", encoding="utf-8").read()); exec(open(r"D:\god\scripts\hook_hauler_build.py", encoding="utf-8").read())
# 좌표: Blender (x, y, z) = Roblox HRP 기준 (-X, Z, Y). 앞 = -y, 캐릭터 오른쪽 = -x. 게임에서 scale 1.5 로 커짐.
import math
from mathutils import Vector, Matrix

col = reset("HookHauler")
for _n in ("Cube", "Light", "Camera"):
    if bpy.data.objects.get(_n):
        bpy.data.objects.remove(bpy.data.objects[_n], do_unlink=True)
rig_ref()

# ---------------- 몸통 ----------------
TORSO = [(0, 0.03, -0.58, 0.72, 0.45), (0, 0.00, -0.20, 0.82, 0.52), (0, -0.03, 0.25, 0.90, 0.54),
         (0, -0.02, 0.64, 0.96, 0.51), (0, 0.03, 0.88, 0.92, 0.45), (0, 0.06, 1.02, 0.58, 0.34), (0, 0.06, 1.10, 0.30, 0.26)]
loft("UpperTorso__Cloth", TORSO, segs=36, sub=5, expo=0.75, cap0=0.02, cap1=0.02, amp=0.02, freq=5.0, seed=201)
push("UpperTorso__Cloth", (0, 0.50, 0.85), 0.45, 0.10)   # 등 위쪽 굽음(혹)


def torso_pt(theta, z, margin):
    """몸통 단면(초타원 0.75) 위의 점을 margin 만큼 바깥으로. theta: 0 = 캐릭터 왼쪽(+x), -90° = 앞(-y)."""
    ks = TORSO
    if z <= ks[0][2]:
        a = b = ks[0]; t = 0.0
    elif z >= ks[-1][2]:
        a = b = ks[-1]; t = 0.0
    else:
        for i in range(len(ks) - 1):
            if ks[i][2] <= z <= ks[i + 1][2]:
                a, b = ks[i], ks[i + 1]
                t = (z - a[2]) / (b[2] - a[2])
                break
    cy = a[1] + (b[1] - a[1]) * t; rx = a[3] + (b[3] - a[3]) * t; ry = a[4] + (b[4] - a[4]) * t
    c, s = math.cos(theta), math.sin(theta)
    ux = math.copysign(abs(c) ** 0.75, c); uy = math.copysign(abs(s) ** 0.75, s)
    p = Vector((rx * ux, cy + ry * uy, z))
    n = Vector((ux / max(rx, 1e-3), uy / max(ry, 1e-3), 0)).normalized()
    return p + n * margin


loft("UpperTorso__Skin", [(0, 0.08, 0.98, 0.26, 0.24), (0, 0.04, 1.18, 0.25, 0.23), (0, -0.01, 1.32, 0.22, 0.21)], segs=14, sub=2)  # 굵은 목
loft("LowerTorso__Cloth", [(0, 0.03, -0.56, 0.74, 0.46), (0, 0.03, -0.80, 0.84, 0.50), (0, 0.03, -0.98, 0.74, 0.44)],
     segs=24, sub=3, expo=0.75, cap0=0.02, cap1=0.12, amp=0.012, freq=5.0, seed=202)
loft("LowerTorso__Boot", [(0, 0.03, -0.70, 0.80, 0.505), (0, 0.03, -0.58, 0.785, 0.495)], segs=24, sub=1, expo=0.75)   # 벨트
box("LowerTorso__Boot", (0, -0.52, -0.64), (0.22, 0.05, 0.14))                                                        # 버클
box("LowerTorso__Boot", (0.55, -0.30, -0.78), (0.22, 0.14, 0.26), rot=Matrix.Rotation(math.radians(-35), 3, 'Z'))       # 공구 주머니
box("LowerTorso__Boot", (-0.62, -0.10, -0.78), (0.16, 0.24, 0.24), rot=Matrix.Rotation(math.radians(20), 3, 'Z'))

# 찢어진 형광 조끼 + 반사 띠 (몸통 표면에서 떼어 낸 얇은 껍질)
def vest_cut(p):
    """조끼에서 빼는 곳: 앞 지퍼 틈(벌어짐), 팔 구멍, 찢긴 아랫단."""
    if p.y < -0.2 and abs(p.x - 0.03 * math.sin(p.z * 9)) < 0.07 + 0.05 * max(0.0, 0.5 - p.z):
        return True
    if abs(p.x) > 0.66 and p.z > 0.38:
        return True
    if p.z < -0.42 + 0.10 * fbm(Vector((p.x * 3, p.y * 3, 0)), 2, 214):
        return True
    return False


shell("UpperTorso__Vest", "UpperTorso__Cloth", 211, (0, 0, -1), 0.4, 0.55, 0.035, 0.03, mfreq=3.2, holes=0.6, zmin=-0.56, zmax=1.0, cut=vest_cut)
for z0, z1, sd in ((0.02, 0.13, 212), (0.42, 0.53, 213)):
    shell("UpperTorso__Strip", "UpperTorso__Cloth", sd, (0, 0, -1), 0.4, 0.55, 0.068, 0.012, mfreq=3.2, holes=0.6, zmin=z0, zmax=z1, cut=vest_cut)

# ---------------- 머리: 굵은 턱 + 용접 마스크 ----------------
loft("Head__Skin", [(0, -0.18, 1.17, 0.16, 0.10), (0, -0.11, 1.26, 0.30, 0.26), (0, -0.05, 1.42, 0.34, 0.37),
                    (0, -0.02, 1.58, 0.36, 0.42), (0, 0.0, 1.73, 0.37, 0.44), (0, 0.03, 1.88, 0.35, 0.42),
                    (0, 0.04, 2.00, 0.27, 0.33)], segs=24, sub=3, cap0=0.05, cap1=0.10, amp=0.014, freq=7.0, seed=221)
shell("Head__Mask", "Head__Skin", 222, (0, -1, 0), 4.0, 0.15, 0.05, 0.035, mfreq=1.0, holes=0.0, zmin=1.22, zmax=1.83)
box("Head__Dark", (0, -0.50, 1.70), (0.40, 0.035, 0.13))                   # 보안경 유리
blob("Head__Glow", (0.09, -0.525, 1.70), (0.04, 0.012, 0.03), 8, 6)        # 깨진 유리 사이로 보이는 한쪽 눈
blob("Head__Glow", (-0.09, -0.515, 1.70), (0.035, 0.008, 0.025), 8, 6)
loft("Head__Boot", [(0, 0.02, 1.86, 0.40, 0.46), (0, 0.02, 1.93, 0.39, 0.455)], segs=20, sub=1)   # 머리끈
for sx in (1, -1):
    blob("Head__Boot", (sx * 0.39, -0.05, 1.82), (0.04, 0.09, 0.09), 8, 6)  # 마스크 회전 축

# ---------------- 다리 ----------------
for side, sx in (("Left", 0.498), ("Right", -0.498)):
    sd = 231 if sx > 0 else 232
    loft(side + "UpperLeg__Cloth", [(sx, 0.03, -0.84, 0.45, 0.44), (sx, 0.02, -1.15, 0.46, 0.45), (sx, 0.0, -1.55, 0.41, 0.40),
                                    (sx, -0.02, -1.95, 0.37, 0.37), (sx, -0.02, -2.14, 0.35, 0.35)],
         segs=16, sub=2, cap0=0.06, cap1=0.04, amp=0.024, freq=5.0, seed=sd)
    loft(side + "LowerLeg__Cloth", [(sx, -0.02, -1.70, 0.36, 0.36), (sx, 0.01, -2.00, 0.38, 0.38), (sx, 0.0, -2.30, 0.35, 0.35),
                                    (sx, -0.01, -2.50, 0.34, 0.34)], segs=16, sub=2, cap0=0.04, cap1=0.02, amp=0.024, freq=5.0, seed=sd + 2)
    loft(side + "LowerLeg__Boot", [(sx, -0.01, -2.40, 0.38, 0.38), (sx, -0.01, -2.70, 0.36, 0.36), (sx, -0.01, -2.97, 0.37, 0.38)],
         segs=16, sub=2, amp=0.008, freq=6.0, seed=sd + 4)
    loft(side + "Foot__Boot", [(sx, 0.32, -3.03, 0.33, 0.16), (sx, 0.10, -3.03, 0.35, 0.17), (sx, -0.22, -3.06, 0.36, 0.15),
                               (sx, -0.52, -3.08, 0.34, 0.13)], segs=16, sub=2, expo=0.6, cap0=0.05, cap1=0.14)
    for v in PIECES[side + "Foot__Boot"].verts:
        if v.co.z < -3.19:
            v.co.z = -3.19
    blob(side + "Foot__Rust", (sx, -0.55, -3.06), (0.30, 0.13, 0.10), 12, 6, square=0.7)   # 강철 앞코(벗겨진 쇠)
    for v in PIECES[side + "Foot__Rust"].verts:
        if v.co.z < -3.19:
            v.co.z = -3.19

# ---------------- 팔 ----------------
for side, sx in (("Left", 1.0), ("Right", -1.0)):
    loft(side + "UpperArm__Cloth", [(sx * 1.02, 0.03, 1.00, 0.34, 0.36), (sx * 1.14, 0.03, 0.80, 0.41, 0.41), (sx * 1.30, 0.02, 0.40, 0.37, 0.37),
                                    (sx * 1.41, 0.02, 0.0, 0.33, 0.33), (sx * 1.44, 0.02, -0.18, 0.32, 0.32)],
         segs=16, sub=2, cap0=0.13, cap1=0.04, amp=0.022, freq=5.0, seed=241 if sx > 0 else 242)
    loft(side + "LowerArm__Cloth", [(sx * 1.43, 0.02, 0.34, 0.33, 0.33), (sx * 1.45, 0.02, 0.0, 0.34, 0.34), (sx * 1.46, 0.01, -0.40, 0.30, 0.30),
                                    (sx * 1.47, 0.0, -0.66, 0.27, 0.27)], segs=16, sub=2, cap0=0.02, cap1=0.03, amp=0.02, freq=6.0, seed=243 if sx > 0 else 244)
# 두꺼운 가죽 장갑: 왼손은 벌린 손, 오른손은 사슬을 쥔 주먹
loft("LeftHand__Boot", [(1.47, 0.0, -0.62, 0.22, 0.24), (1.48, -0.02, -0.80, 0.15, 0.24), (1.49, -0.04, -0.94, 0.12, 0.23)], segs=12, sub=2, expo=0.8, cap1=0.03)
for k, fy in enumerate((-0.18, -0.07, 0.04, 0.14)):
    finger("LeftHand__Boot", [(1.49, fy - 0.02, -0.95), (1.51, fy * 1.1 - 0.05, -1.10), (1.48, fy * 1.15 - 0.10, -1.22)], 0.06, 0.045)
finger("LeftHand__Boot", [(1.38, -0.18, -0.84), (1.32, -0.28, -0.96), (1.30, -0.33, -1.06)], 0.06, 0.045)
blob("RightHand__Boot", (-1.48, -0.03, -0.88), (0.21, 0.25, 0.20), 14, 10, 0.015, 8.0, 245, square=0.8)  # 주먹
loft("RightHand__Boot", [(-1.47, 0.0, -0.62, 0.22, 0.24), (-1.48, -0.02, -0.76, 0.20, 0.25)], segs=12, sub=1)

# ---------------- 쇠사슬 ----------------
# 몸을 대각선으로 감는 사슬 (왼어깨 → 앞 → 오른 허리 → 등 → 왼어깨)
band = []
for k in range(0, 25):
    th = -2 * math.pi * k / 24
    z = 0.30 + 0.76 * math.cos(th)                      # 어깨 쪽은 목에 가깝게 넘어가 팔과 안 겹침
    band.append(torso_pt(th, z, 0.15 + 0.14 * max(0.0, math.sin(th))))  # 등 쪽은 갈고리 위로 지나가게 더 띄움
chain("UpperTorso__Rust", band, link_len=0.34, link_w=0.20, thick=0.042)
# 왼 팔뚝에 감은 사슬 (나선)
coil = []
for k in range(0, 34):
    a = 2 * math.pi * k / 11
    z = -0.02 - 0.60 * k / 33
    r = 0.44
    coil.append((1.455 + math.cos(a) * r, 0.02 + math.sin(a) * r, z))
chain("LeftLowerArm__Rust", coil, link_len=0.28, link_w=0.17, thick=0.034)
# 오른 주먹에서 늘어진 짧은 사슬 → 갈고리 무기
chain("RightHand__Rust", [(-1.48, -0.03, -1.02), (-1.49, -0.03, -1.18), (-1.50, -0.03, -1.40)], link_len=0.28, link_w=0.17, thick=0.034)
# 손목에 감긴 고리 몇 개
wr = [(-1.47 + math.cos(2 * math.pi * k / 7) * 0.37, 0.0 + math.sin(2 * math.pi * k / 7) * 0.37, -0.56 - 0.02 * k) for k in range(8)]
chain("RightHand__Rust", wr, link_len=0.26, link_w=0.16, thick=0.032)

# 무기 갈고리: 사슬 끝(-1.50, -0.03, -1.36)에서 매달려 아래로
Mw = Matrix.Translation((-1.50, -0.03, -2.20)) @ Matrix.Rotation(math.radians(180), 4, 'Z') @ Matrix.Rotation(math.radians(-8), 4, 'X')
hook("RightHand__Paint", Mw, scale=1.0, shank=0.55, R=0.36, thick=0.13)

# 등에 박힌 크레인 갈고리 (끝이 등 속으로 들어감) + 끊어진 사슬
# 갈고리 굽은 부분(아래)이 등 속에 반쯤 묻히고 축은 오른쪽 어깨 뒤로 비스듬히 솟음
Mb = (Matrix.Translation((-0.22, 0.62, 0.42)) @ Matrix.Rotation(math.radians(18), 4, 'Y')
      @ Matrix.Rotation(math.radians(180), 4, 'Z') @ Matrix.Rotation(math.radians(12), 4, 'X'))
hook("UpperTorso__Paint", Mb, scale=1.1, shank=0.75, R=0.36, thick=0.14)
eye = Mb @ Vector((0, 0, (0.75 + 0.36) * 1.1))
chain("UpperTorso__Rust", [tuple(eye), (eye.x - 0.05, eye.y + 0.10, eye.z + 0.25), (eye.x - 0.10, eye.y + 0.25, eye.z + 0.38)], link_len=0.34, link_w=0.20, thick=0.042)

# 허리 뒤에서 바닥으로 끌리는 사슬
chain("LowerTorso__Rust", [(-0.15, 0.50, -0.68), (-0.22, 0.75, -1.40), (-0.28, 1.05, -2.40), (-0.32, 1.40, -3.08), (-0.36, 1.90, -3.13), (-0.30, 2.30, -3.13)],
      link_len=0.34, link_w=0.20, thick=0.042)

MATCOL = {"Cloth": (0.11, 0.13, 0.16), "Vest": (0.65, 0.28, 0.05), "Strip": (0.55, 0.55, 0.50), "Skin": (0.24, 0.13, 0.10),
          "Boot": (0.09, 0.07, 0.06), "Rust": (0.22, 0.11, 0.06), "Paint": (0.62, 0.44, 0.06), "Mask": (0.10, 0.11, 0.10),
          "Dark": (0.01, 0.01, 0.01), "Glow": (1.0, 0.43, 0.10)}
print(finalize(col, MATCOL, decimate={"Rust": 1.0, "_big": 0.75}, sharp_keys=("Rust", "Paint", "Mask")))
