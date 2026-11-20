# R15 KeyframeSequence .rbxmx 생성 공용 (Open Cloud Animation 업로드용, 일반 python 으로 실행)
# 포즈: {"부위": ((x, y, z), (rx, ry, rz))}  각도 = CFrame.Angles(x, y, z) 도 단위.
# keys: [(시간, 포즈, EasingStyle, EasingDirection, 마커 이름 또는 None), ...]
#   PoseEasingStyle: Linear 0, Constant 1, Elastic 2, Cubic 3, Bounce 4 / PoseEasingDirection: In 0, Out 1, InOut 2
import math, os

TREE = {
    "HumanoidRootPart": ["LowerTorso"],
    "LowerTorso": ["UpperTorso", "LeftUpperLeg", "RightUpperLeg"],
    "UpperTorso": ["Head", "LeftUpperArm", "RightUpperArm"],
    "LeftUpperArm": ["LeftLowerArm"], "LeftLowerArm": ["LeftHand"],
    "RightUpperArm": ["RightLowerArm"], "RightLowerArm": ["RightHand"],
    "LeftUpperLeg": ["LeftLowerLeg"], "LeftLowerLeg": ["LeftFoot"],
    "RightUpperLeg": ["RightLowerLeg"], "RightLowerLeg": ["RightFoot"],
}


def rot(x, y, z):
    x, y, z = math.radians(x), math.radians(y), math.radians(z)
    cx, sx, cy, sy, cz, sz = math.cos(x), math.sin(x), math.cos(y), math.sin(y), math.cos(z), math.sin(z)
    Rx = [[1, 0, 0], [0, cx, -sx], [0, sx, cx]]
    Ry = [[cy, 0, sy], [0, 1, 0], [-sy, 0, cy]]
    Rz = [[cz, -sz, 0], [sz, cz, 0], [0, 0, 1]]
    def mul(a, b):
        return [[sum(a[i][k] * b[k][j] for k in range(3)) for j in range(3)] for i in range(3)]
    return mul(mul(Rx, Ry), Rz)


def write(name, keys, out_path, priority=2):
    ref = [0]

    def nref():
        ref[0] += 1
        return "RBX%d" % ref[0]

    def cframe_xml(pos, ang):
        R = rot(*ang)
        s = '<CoordinateFrame name="CFrame"><X>%g</X><Y>%g</Y><Z>%g</Z>' % tuple(pos)
        for i in range(3):
            for j in range(3):
                s += "<R%d%d>%.6f</R%d%d>" % (i, j, R[i][j], i, j)
        return s + "</CoordinateFrame>"

    def pose_xml(part, poses, style, direc, ind):
        pos, ang = poses.get(part, ((0, 0, 0), (0, 0, 0)))
        s = ind + '<Item class="Pose" referent="%s"><Properties><string name="Name">%s</string>%s' % (nref(), part, cframe_xml(pos, ang))
        s += '<token name="EasingDirection">%d</token><token name="EasingStyle">%d</token><float name="Weight">1</float></Properties>\n' % (direc, style)
        for ch in TREE.get(part, []):
            s += pose_xml(ch, poses, style, direc, ind + "  ")
        return s + ind + "</Item>\n"

    out = ['<roblox xmlns:xmime="http://www.w3.org/2005/05/xmlmime" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" version="4">',
           '<Item class="KeyframeSequence" referent="%s"><Properties><string name="Name">%s</string>'
           '<bool name="Loop">false</bool><token name="Priority">%d</token></Properties>' % (nref(), name, priority)]
    for t, poses, style, direc, marker in keys:
        out.append('<Item class="Keyframe" referent="%s"><Properties><string name="Name">Keyframe</string><float name="Time">%g</float></Properties>' % (nref(), t))
        out.append(pose_xml("HumanoidRootPart", poses, style, direc, "  ").rstrip("\n"))
        if marker:
            out.append('<Item class="KeyframeMarker" referent="%s"><Properties><string name="Name">%s</string><string name="Value"></string></Properties></Item>' % (nref(), marker))
        out.append("</Item>")
    out.append("</Item></roblox>")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    return os.path.abspath(out_path)
