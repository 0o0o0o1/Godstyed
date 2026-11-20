# Hook Hauler 갈고리 옆으로 휘두르기 공격 → exports/anims/HookHaulerAttack.rbxmx
# 실행: python scripts/hook_hauler_anim.py
# 타격 0.70초(마커 "Impact", 적 정의 attackHitTime = 0.70). Studio FK 로 확인: 들어 올림 때 갈고리 오른쪽 뒤 위,
# 타격 때 몸 앞(앞 3.2·왼 0.9, 땅 위 3.6 = 가슴 높이), 따라 휘두름 왼쪽. 발 높이 보정(엉덩이 Y).
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import anim_kit

Z = (0, 0, 0)
WINDUP = {"LowerTorso": ((0, 0.05, 0.05), (0, -15, 0)), "UpperTorso": (Z, (4, -35, 0)), "Head": (Z, (0, 20, 0)),
          "RightUpperArm": (Z, (0, -15, 80)), "RightLowerArm": (Z, (25, 0, 0)),
          "LeftUpperArm": (Z, (-15, 0, -30)), "LeftLowerArm": (Z, (30, 0, 0)),
          "LeftUpperLeg": (Z, (10, 15, 0)), "LeftLowerLeg": (Z, (-15, 0, 0)),
          "RightUpperLeg": (Z, (-5, 15, 0)), "RightLowerLeg": (Z, (-20, 0, 0)), "RightFoot": (Z, (10, 0, 0))}
HOLD = dict(WINDUP)
HOLD.update({"UpperTorso": (Z, (5, -40, 0)), "RightUpperArm": (Z, (0, -22, 82))})
IMPACT = {"LowerTorso": ((0, -0.03, -0.05), (0, 15, 0)), "UpperTorso": (Z, (-8, 28, 0)), "Head": (Z, (0, -15, 0)),
          "RightUpperArm": (Z, (80, 10, 0)), "RightLowerArm": (Z, (8, 0, 0)),
          "LeftUpperArm": (Z, (10, 0, -40)), "LeftLowerArm": (Z, (25, 0, 0)),
          "LeftUpperLeg": (Z, (22, -15, 0)), "LeftLowerLeg": (Z, (-28, 0, 0)), "LeftFoot": (Z, (8, 0, 0)),
          "RightUpperLeg": (Z, (-12, -15, 0)), "RightLowerLeg": (Z, (-22, 0, 0)), "RightFoot": (Z, (20, 0, 0))}
FOLLOW = dict(IMPACT)
FOLLOW.update({"LowerTorso": ((0, -0.02, -0.05), (0, 25, 0)), "UpperTorso": (Z, (-6, 40, 0)), "Head": (Z, (0, -20, 0)),
               "RightUpperArm": (Z, (75, 45, 0)), "RightLowerArm": (Z, (15, 0, 0)), "LeftUpperArm": (Z, (15, 0, -45)),
               "LeftUpperLeg": (Z, (22, -25, 0)), "RightUpperLeg": (Z, (-12, -25, 0))})

KEYS = [
    (0.00, {}, 3, 2, None),
    (0.50, WINDUP, 3, 2, None),
    (0.58, HOLD, 0, 0, None),        # 잠깐 멈췄다가 직선으로 빠르게 휘두름
    (0.70, IMPACT, 0, 0, "Impact"),
    (0.92, FOLLOW, 3, 1, None),
    (1.50, {}, 3, 2, None),
]

if __name__ == "__main__":
    p = os.path.join(os.path.dirname(__file__), "..", "exports", "anims", "HookHaulerAttack.rbxmx")
    print("wrote", anim_kit.write("HookHaulerAttack", KEYS, p))
