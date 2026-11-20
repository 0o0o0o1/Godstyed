# Slag Walker 곤봉 내려치기 공격 애니메이션 → KeyframeSequence .rbxmx 생성 (Open Cloud Animation 업로드용)
# 실행: python scripts/slag_walker_anim.py  → exports/anims/SlagWalkerAttack.rbxmx
# 각도는 CFrame.Angles(x, y, z) 도 단위(R15 관절 기준: +X 회전 = 팔·허벅지 앞으로, 허리 -X = 앞으로 숙임).
# 타격 순간 0.58초 (적 정의 attackHitTime = 0.58, 마커 "Impact"). 포즈 값은 Studio FK 계산으로 곤봉·발 높이 확인함.
import math, os

TREE = {  # 부모 → 자식 (R15)
    "HumanoidRootPart": ["LowerTorso"],
    "LowerTorso": ["UpperTorso", "LeftUpperLeg", "RightUpperLeg"],
    "UpperTorso": ["Head", "LeftUpperArm", "RightUpperArm"],
    "LeftUpperArm": ["LeftLowerArm"], "LeftLowerArm": ["LeftHand"],
    "RightUpperArm": ["RightLowerArm"], "RightLowerArm": ["RightHand"],
    "LeftUpperLeg": ["LeftLowerLeg"], "LeftLowerLeg": ["LeftFoot"],
    "RightUpperLeg": ["RightLowerLeg"], "RightLowerLeg": ["RightFoot"],
}

WINDUP = {"LowerTorso": ((0, -0.03, 0.1), (0, 0, 0)), "UpperTorso": ((0, 0, 0), (14, -22, 0)), "Head": ((0, 0, 0), (12, 10, 0)),
          "RightUpperArm": ((0, 0, 0), (155, 0, 15)), "RightLowerArm": ((0, 0, 0), (35, 0, 0)),
          "LeftUpperArm": ((0, 0, 0), (20, 0, -35)), "LeftLowerArm": ((0, 0, 0), (25, 0, 0)),
          "LeftUpperLeg": ((0, 0, 0), (25, 0, 0)), "LeftLowerLeg": ((0, 0, 0), (-30, 0, 0)), "LeftFoot": ((0, 0, 0), (5, 0, 0)),
          "RightUpperLeg": ((0, 0, 0), (-10, 0, 0)), "RightLowerLeg": ((0, 0, 0), (-25, 0, 0)), "RightFoot": ((0, 0, 0), (35, 0, 0))}
HOLD = dict(WINDUP)
HOLD.update({"UpperTorso": ((0, 0, 0), (17, -25, 0)), "RightUpperArm": ((0, 0, 0), (162, 0, 15)), "Head": ((0, 0, 0), (14, 10, 0))})
IMPACT = {"LowerTorso": ((0, -0.5, -0.15), (0, 0, 0)), "UpperTorso": ((0, 0, 0), (-42, 16, 0)), "Head": ((0, 0, 0), (-2, -5, 0)),
          "RightUpperArm": ((0, 0, 0), (12, 0, 6)), "RightLowerArm": ((0, 0, 0), (5, 0, 0)),
          "LeftUpperArm": ((0, 0, 0), (-20, 0, -40)), "LeftLowerArm": ((0, 0, 0), (30, 0, 0)),
          "LeftUpperLeg": ((0, 0, 0), (60, 0, 0)), "LeftLowerLeg": ((0, 0, 0), (-85, 0, 0)), "LeftFoot": ((0, 0, 0), (25, 0, 0)),
          "RightUpperLeg": ((0, 0, 0), (-15, 0, 0)), "RightLowerLeg": ((0, 0, 0), (-48, 0, 0)), "RightFoot": ((0, 0, 0), (25, 0, 0))}
SETTLE = dict(IMPACT)
SETTLE.update({"LowerTorso": ((0, -0.45, -0.12), (0, 0, 0)), "UpperTorso": ((0, 0, 0), (-38, 14, 0)), "RightUpperArm": ((0, 0, 0), (18, 0, 6))})

# PoseEasingStyle: Linear 0, Constant 1, Elastic 2, Cubic 3, Bounce 4 / PoseEasingDirection: In 0, Out 1, InOut 2
KEYS = [  # (시간, 포즈, 스타일, 방향, 마커)
    (0.00, {}, 3, 2, None),
    (0.40, WINDUP, 3, 2, None),
    (0.46, HOLD, 0, 0, None),       # 짧게 멈췄다가 직선으로 빠르게 내려침
    (0.58, IMPACT, 3, 1, "Impact"),
    (0.82, SETTLE, 3, 2, None),
    (1.35, {}, 3, 2, None),
]

def rot(x, y, z):
    x, y, z = math.radians(x), math.radians(y), math.radians(z)
    cx, sx, cy, sy, cz, sz = math.cos(x), math.sin(x), math.cos(y), math.sin(y), math.cos(z), math.sin(z)
    Rx = [[1, 0, 0], [0, cx, -sx], [0, sx, cx]]
    Ry = [[cy, 0, sy], [0, 1, 0], [-sy, 0, cy]]
    Rz = [[cz, -sz, 0], [sz, cz, 0], [0, 0, 1]]
    def mul(a, b):
        return [[sum(a[i][k] * b[k][j] for k in range(3)) for j in range(3)] for i in range(3)]
    return mul(mul(Rx, Ry), Rz)

ref = [0]
def nref():
    ref[0] += 1
    return "RBX%d" % ref[0]

def cframe_xml(name, pos, ang):
    R = rot(*ang)
    s = '<CoordinateFrame name="%s"><X>%g</X><Y>%g</Y><Z>%g</Z>' % (name, pos[0], pos[1], pos[2])
    for i in range(3):
        for j in range(3):
            s += "<R%d%d>%.6f</R%d%d>" % (i, j, R[i][j], i, j)
    return s + "</CoordinateFrame>"

def pose_xml(part, poses, style, direc, ind):
    pos, ang = poses.get(part, ((0, 0, 0), (0, 0, 0)))
    s = ind + '<Item class="Pose" referent="%s"><Properties>' % nref()
    s += '<string name="Name">%s</string>%s' % (part, cframe_xml("CFrame", pos, ang))
    s += '<token name="EasingDirection">%d</token><token name="EasingStyle">%d</token><float name="Weight">1</float></Properties>\n' % (direc, style)
    for ch in TREE.get(part, []):
        s += pose_xml(ch, poses, style, direc, ind + "  ")
    return s + ind + "</Item>\n"

out = ['<roblox xmlns:xmime="http://www.w3.org/2005/05/xmlmime" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" version="4">',
       '<Item class="KeyframeSequence" referent="%s"><Properties><string name="Name">SlagWalkerAttack</string>'
       '<bool name="Loop">false</bool><token name="Priority">2</token></Properties>' % nref()]
for t, poses, style, direc, marker in KEYS:
    out.append('<Item class="Keyframe" referent="%s"><Properties><string name="Name">Keyframe</string><float name="Time">%g</float></Properties>' % (nref(), t))
    out.append(pose_xml("HumanoidRootPart", poses, style, direc, "  ").rstrip("\n"))
    if marker:
        out.append('<Item class="KeyframeMarker" referent="%s"><Properties><string name="Name">%s</string><string name="Value"></string></Properties></Item>' % (nref(), marker))
    out.append("</Item>")
out.append("</Item></roblox>")
os.makedirs(os.path.join(os.path.dirname(__file__), "..", "exports", "anims"), exist_ok=True)
path = os.path.join(os.path.dirname(__file__), "..", "exports", "anims", "SlagWalkerAttack.rbxmx")
open(path, "w", encoding="utf-8").write("\n".join(out))
print("wrote", os.path.abspath(path))
