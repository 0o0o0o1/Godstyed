# The Foreman 보스 동작 3종 → exports/anims/Foreman*.rbxmx
# 실행: python scripts/foreman_anim.py
# FK 확인(Studio): 쉬는 자세 갈고리 땅 위 0.09(갈고리 용접 +0.45 올림), 내려찍기 때 갈고리 땅 위 0.15·몸 앞 2.9.
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import anim_kit

Z = (0, 0, 0)

# 1) 갈고리 내려찍기 (KnuckleSmash, CoilDrop 땅 내리치기) — 타격 0.80 "Impact"
UP = {"LowerTorso": ((0, 0.05, 0.1), Z), "UpperTorso": (Z, (14, -10, 0)), "Head": (Z, (10, 5, 0)),
      "RightUpperArm": (Z, (165, 0, 10)), "RightLowerArm": (Z, (20, 0, 0)),
      "LeftUpperArm": (Z, (15, 0, -25)), "LeftLowerArm": (Z, (20, 0, 0)),
      "LeftUpperLeg": (Z, (10, 0, 0)), "RightUpperLeg": (Z, (-8, 0, 0)), "RightLowerLeg": (Z, (-10, 0, 0))}
UP2 = dict(UP); UP2.update({"UpperTorso": (Z, (18, -12, 0)), "RightUpperArm": (Z, (172, 0, 10))})
DOWN = {"LowerTorso": ((0, -0.25, -0.15), Z), "UpperTorso": (Z, (-25, 8, 0)), "Head": (Z, (10, 0, 0)),
        "RightUpperArm": (Z, (50, 0, 5)), "RightLowerArm": (Z, (10, 0, 0)),
        "LeftUpperArm": (Z, (-25, 0, -35)), "LeftLowerArm": (Z, (25, 0, 0)),
        "LeftUpperLeg": (Z, (45, 0, 0)), "LeftLowerLeg": (Z, (-60, 0, 0)), "LeftFoot": (Z, (15, 0, 0)),
        "RightUpperLeg": (Z, (-15, 0, 0)), "RightLowerLeg": (Z, (-30, 0, 0)), "RightFoot": (Z, (20, 0, 0))}
SMASH = [(0.00, {}, 3, 2, None), (0.55, UP, 3, 2, None), (0.68, UP2, 0, 0, None), (0.80, DOWN, 3, 1, "Impact"),
         (1.20, DOWN, 3, 2, None), (1.70, {}, 3, 2, None)]

# 2) 갈고리 던지기 (HookThrow) — 던지는 순간 0.90 "Throw", 1.0~1.7 팔 뻗은 채 유지(갈고리 날아갔다 돌아옴), 2.1 복귀
BACK = {"LowerTorso": ((0, 0.0, 0.1), (0, -20, 0)), "UpperTorso": (Z, (5, -30, 0)), "Head": (Z, (0, 20, 0)),
        "RightUpperArm": (Z, (-35, 0, 20)), "RightLowerArm": (Z, (40, 0, 0)), "LeftUpperArm": (Z, (35, 0, -20)),
        "LeftUpperLeg": (Z, (10, 20, 0)), "RightUpperLeg": (Z, (-10, 20, 0)), "RightLowerLeg": (Z, (-15, 0, 0))}
OUT = {"LowerTorso": ((0, -0.15, -0.1), (0, 10, 0)), "UpperTorso": (Z, (-15, 15, 0)),
       "RightUpperArm": (Z, (95, 0, 5)), "RightLowerArm": (Z, (0, 0, 0)), "LeftUpperArm": (Z, (-20, 0, -30)),
       "LeftUpperLeg": (Z, (30, -10, 0)), "LeftLowerLeg": (Z, (-35, 0, 0)), "LeftFoot": (Z, (5, 0, 0)),
       "RightUpperLeg": (Z, (-15, -10, 0)), "RightLowerLeg": (Z, (-15, 0, 0)), "RightFoot": (Z, (15, 0, 0))}
PULL = dict(OUT); PULL.update({"UpperTorso": (Z, (5, 5, 0)), "RightUpperArm": (Z, (60, 0, 10)), "RightLowerArm": (Z, (45, 0, 0)),
                               "LowerTorso": ((0, -0.1, 0.1), (0, 0, 0))})
THROW = [(0.00, {}, 3, 2, None), (0.70, BACK, 3, 2, None), (0.90, OUT, 3, 1, "Throw"), (1.40, OUT, 3, 2, None),
         (1.75, PULL, 3, 1, "Pull"), (2.20, {}, 3, 2, None)]

# 3) 확성기 사이렌 (MegaSiren) — 0.90 "Siren", 2.4까지 확성기를 앞으로 겨눈 채 몸을 젖힘, 2.9 복귀
AIM = {"LowerTorso": ((0, -0.05, 0.05), Z), "UpperTorso": (Z, (12, -15, 0)), "Head": (Z, (5, -10, 0)),
       "LeftUpperArm": (Z, (85, 0, 10)), "LeftLowerArm": (Z, (10, 0, 0)), "LeftHand": (Z, (-95, 0, 0)),
       "RightUpperArm": (Z, (-10, 0, 15)), "LeftUpperLeg": (Z, (-8, 0, 0)), "RightUpperLeg": (Z, (18, 0, 0)), "RightLowerLeg": (Z, (-20, 0, 0))}
BLARE = dict(AIM); BLARE.update({"UpperTorso": (Z, (18, -18, 0)), "Head": (Z, (-5, -10, 0))})
SIREN = [(0.00, {}, 3, 2, None), (0.70, AIM, 3, 2, None), (0.90, BLARE, 3, 1, "Siren"), (2.40, BLARE, 0, 0, None),
         (2.90, {}, 3, 2, None)]

if __name__ == "__main__":
    d = os.path.join(os.path.dirname(__file__), "..", "exports", "anims")
    for name, keys in (("ForemanSmash", SMASH), ("ForemanThrow", THROW), ("ForemanSiren", SIREN)):
        print("wrote", anim_kit.write(name, keys, os.path.join(d, name + ".rbxmx")))
