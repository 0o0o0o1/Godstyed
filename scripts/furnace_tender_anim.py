# Furnace Tender / Warden 개공봉 찌르기 공격 → exports/anims/FurnaceTenderAttack.rbxmx
# 실행: python scripts/furnace_tender_anim.py
# 타격 0.55초(마커 "Impact", 적 정의 attackHitTime = 0.55). Studio FK 확인: 찌를 때 개공봉 끝이 몸 앞 4.6, 땅 위 약 2.7
# (경비 scale 1.5 → 약 4 = 플레이어 가슴 높이), 거의 수평. 팔을 앞으로 뻗으면 막대가 들리므로 손목(RightHand) -62°로 수평 맞춤.
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import anim_kit

Z = (0, 0, 0)
WINDUP = {"LowerTorso": ((0, 0.0, 0.1), (0, -15, 0)), "UpperTorso": (Z, (8, -25, 0)), "Head": (Z, (-5, 15, 0)),
          "RightUpperArm": (Z, (-20, 0, 15)), "RightLowerArm": (Z, (65, 0, 0)), "RightHand": (Z, (-30, 0, 0)),
          "LeftUpperArm": (Z, (30, 0, -15)), "LeftLowerArm": (Z, (40, 0, 0)),
          "LeftUpperLeg": (Z, (20, 15, 0)), "LeftLowerLeg": (Z, (-20, 0, 0)),
          "RightUpperLeg": (Z, (-10, 15, 0)), "RightLowerLeg": (Z, (-15, 0, 0)), "RightFoot": (Z, (10, 0, 0))}
HOLD = dict(WINDUP)
HOLD.update({"UpperTorso": (Z, (10, -28, 0)), "RightUpperArm": (Z, (-25, 0, 15))})
THRUST = {"LowerTorso": ((0, -0.1, -0.25), (0, 5, 0)), "UpperTorso": (Z, (-18, 5, 0)), "Head": (Z, (12, -5, 0)),
          "RightUpperArm": (Z, (50, 10, 5)), "RightLowerArm": (Z, (5, 0, 0)), "RightHand": (Z, (-62, 0, 0)),
          "LeftUpperArm": (Z, (-30, 0, -25)), "LeftLowerArm": (Z, (20, 0, 0)),
          "LeftUpperLeg": (Z, (40, -5, 0)), "LeftLowerLeg": (Z, (-40, 0, 0)), "LeftFoot": (Z, (5, 0, 0)),
          "RightUpperLeg": (Z, (-25, -5, 0)), "RightLowerLeg": (Z, (-10, 0, 0)), "RightFoot": (Z, (25, 0, 0))}
EXTEND = dict(THRUST)
EXTEND.update({"LowerTorso": ((0, -0.08, -0.22), (0, 5, 0)), "UpperTorso": (Z, (-15, 5, 0)), "RightUpperArm": (Z, (52, 10, 5))})

KEYS = [
    (0.00, {}, 3, 2, None),
    (0.35, WINDUP, 3, 2, None),
    (0.45, HOLD, 0, 0, None),          # 당겼다가 직선으로 빠르게 찌름
    (0.55, THRUST, 3, 1, "Impact"),
    (0.78, EXTEND, 3, 2, None),
    (1.25, {}, 3, 2, None),
]

if __name__ == "__main__":
    p = os.path.join(os.path.dirname(__file__), "..", "exports", "anims", "FurnaceTenderAttack.rbxmx")
    print("wrote", anim_kit.write("FurnaceTenderAttack", KEYS, p))
