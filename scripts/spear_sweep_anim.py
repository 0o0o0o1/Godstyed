# 창 휘두르기(spear_sweep) 플레이어 모션 → exports/anims/SpearSweep.rbxmx
# 실행: python scripts/spear_sweep_anim.py  (그다음 Open Cloud 로 assetType Animation 그룹 업로드)
# 흐름(사용자 결정 2026-11-24): 0 ~ 0.2 당기기 → 0.2 ~ 0.55 한 바퀴(반시계, 왼쪽으로) → 0.55 ~ 0.9 마무리.
# 자세(사용자 결정): 오른손으로 창 끝을 잡고 팔을 옆으로 쭉 뻗어 길게.
# 계산 근거 (Studio 측정, R15 모터 C0/C1 회전이 모두 단위 행렬 → 손 방향 = 어깨 × 팔꿈치 × 손목 Transform):
#   든 창은 손 기준 -Z 방향(창끝 손 앞 10.6). 어깨 Rz(+90) = 팔이 몸 오른쪽(+X), 손목 Rx(-90) = 창이 팔과 같은 +X.
#   몸(LowerTorso) 회전 Ry(θ)에서 창 방향 = (cosθ, 0, -sinθ) → θ = 90 일 때 정면. 서버 판정(spinHits)이
#   castDelay(0.2)에 정면에서 시작해 왼쪽으로 spinTime(0.35) 동안 한 바퀴 → θ 90 → 450 을 90° 간격 선형 키로.
#   키 사이 회전은 짧은 쪽으로 보간되므로 90° 간격, 마무리(115°)에서 쉬는 자세(0°)는 오른쪽으로 115° 되돌아옴.
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import anim_kit

Z = (0, 0, 0)
ARM_OUT = 84  # 어깨 Rz: 90 = 수평, 조금 낮게 (창날이 허리~가슴 높이로 지나감)


def spin_pose(yaw, drop=0.12, lean=-6):
    return {
        "LowerTorso": ((0, -drop, 0), (0, yaw, 0)),
        "UpperTorso": (Z, (lean, 0, 0)),
        "RightUpperArm": (Z, (0, 0, ARM_OUT)),
        "RightLowerArm": (Z, (0, 0, 4)),
        "RightHand": (Z, (-90, 0, 0)),
        "LeftUpperArm": (Z, (0, 0, -70)),
        "LeftLowerArm": (Z, (20, 0, 0)),
        "LeftUpperLeg": (Z, (25, 0, 0)), "LeftLowerLeg": (Z, (-45, 0, 0)), "LeftFoot": (Z, (20, 0, 0)),
        "RightUpperLeg": (Z, (25, 0, 0)), "RightLowerLeg": (Z, (-45, 0, 0)), "RightFoot": (Z, (20, 0, 0)),
    }


# 당기기: 몸을 왼쪽으로 55° 돌리고 윗몸은 오른쪽으로 비틀어 창을 오른쪽 앞에 끌어 둠 (용수철처럼 감음)
WINDUP = spin_pose(55, drop=0.16, lean=-10)
WINDUP["UpperTorso"] = (Z, (-10, -25, 0))
WINDUP["Head"] = (Z, (0, 30, 0))  # 머리는 정면 쪽을 봄

# 마무리: 팔을 그냥 내리면 팔과 한 줄인 창끝이 땅을 파고듦(1차 업로드에서 −3.3) →
# 먼저 팔을 살짝 들고 손목을 풀어 창을 위로 세운 뒤(0.65), 창을 앞으로 눕힌 채 팔을 내림(0.78) → 쉬는 자세
FOLLOW = spin_pose(115, drop=0.1, lean=-3)
FOLLOW["UpperTorso"] = (Z, (-3, 15, 0))
FOLLOW["RightUpperArm"] = (Z, (0, 0, 95))
FOLLOW["RightHand"] = (Z, (-60, 0, 0))

SETTLE = spin_pose(40, drop=0.05, lean=-2)
SETTLE["UpperTorso"] = (Z, (-2, 5, 0))
SETTLE["RightUpperArm"] = (Z, (0, 0, 50))
SETTLE["RightLowerArm"] = (Z, (10, 0, 0))
SETTLE["RightHand"] = (Z, (-10, 0, 0))
SETTLE["LeftUpperArm"] = (Z, (0, 0, -30))
for leg in ("LeftUpperLeg", "RightUpperLeg"):
    SETTLE[leg] = (Z, (10, 0, 0))
for leg in ("LeftLowerLeg", "RightLowerLeg"):
    SETTLE[leg] = (Z, (-18, 0, 0))
for foot in ("LeftFoot", "RightFoot"):
    SETTLE[foot] = (Z, (8, 0, 0))

S0, S1 = 0.2, 0.55  # 회전 시작·끝 (castDelay, castDelay + spinTime)
STEP = (S1 - S0) / 4

KEYS = [
    (0.00, {}, 3, 2, None),
    (0.15, WINDUP, 3, 1, None),
    (S0, spin_pose(90), 0, 0, "Spin"),        # 정면 (판정 시작)
    (S0 + STEP, spin_pose(180), 0, 0, None),   # 왼쪽
    (S0 + STEP * 2, spin_pose(270), 0, 0, None),  # 뒤
    (S0 + STEP * 3, spin_pose(360), 0, 0, None),  # 오른쪽
    (S1, spin_pose(450), 0, 0, None),          # 다시 정면 (한 바퀴 끝)
    (0.65, FOLLOW, 3, 1, None),                # 조금 더 돌며 감속, 창을 위로
    (0.78, SETTLE, 3, 2, None),                # 창을 앞으로 눕힌 채 팔을 내림
    (0.90, {}, 3, 2, None),
]

if __name__ == "__main__":
    p = os.path.join(os.path.dirname(__file__), "..", "exports", "anims", "SpearSweep.rbxmx")
    print("wrote", anim_kit.write("SpearSweep", KEYS, p))
