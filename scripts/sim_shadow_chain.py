# 그림자 연쇄(가칭, 단검 5번 소켓) 연쇄 규칙 시험 — Luau 로 옮기기 전에 수치를 정하기 위한 Python 시뮬레이션
# 실행: python scripts/sim_shadow_chain.py  → 표는 화면에, 예시 그림은 exports/vfx/shadow_chain/sim_*.png
#
# 규칙 (사용자 결정 2026-11-26):
#   첫 대상 = 내 주변 가장 가까운 적 (maxDistance 안, 그림자 발걸음과 같음)
#   다음 대상 = "방금 벤 적" 주변 반경 R 안, 아직 안 벤 적 중 가장 가까운 적 (벽은 여기서는 무시)
#   한 번 벤 적은 다시 안 벰 / 최대 6명 (첫 대상 포함) / 후보가 없으면 끝 → 첫 대상에게 돌아가 처형
#   첫 대상이 연쇄 중 죽으면 처형 생략 / 스킬 내내 캐릭터는 안 보임 (이 시험과는 무관)
# 시간 모형: 첫 타 castDelay, 그다음 건너뛰기마다 HOP, 마지막 적 → 첫 대상 귀환 RETURN, 처형 준비 EXECUTE

import math
import os
import random

MAX_TARGETS = 6
FIRST_RANGE = 30  # 첫 대상 찾는 거리 (shadow_step.maxDistance 와 같게)
CAST_DELAY, HOP, RETURN, EXECUTE = 0.15, 0.18, 0.25, 0.3
RADII = [8, 10, 12, 14, 16, 20]
TRIALS = 4000

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "exports", "vfx", "shadow_chain")
os.makedirs(OUT, exist_ok=True)


# ---------- 적 배치 상황 (스터드, 플레이어는 원점) ----------
def pack(rng, n, spread, cx, cz):
    return [(cx + rng.gauss(0, spread), cz + rng.gauss(0, spread)) for _ in range(n)]


def scene_tight(rng):  # 밀집 무리: 5~8마리, 퍼짐 4
    return pack(rng, rng.randint(5, 8), 4, rng.uniform(-6, 6), rng.uniform(10, 18))


def scene_loose(rng):  # 넓게 퍼진 무리: 4~7마리, 퍼짐 9
    return pack(rng, rng.randint(4, 7), 9, rng.uniform(-6, 6), rng.uniform(10, 20))


def scene_corridor(rng):  # 복도 일렬: 5~8마리가 앞으로 6~11 간격
    n = rng.randint(5, 8)
    z, out = rng.uniform(6, 12), []
    for _ in range(n):
        out.append((rng.gauss(0, 1.5), z))
        z += rng.uniform(6, 11)
    return out


def scene_two_packs(rng):  # 무리 두 개: 가까운 무리 3~5, 18~30 떨어진 무리 3~5
    a = pack(rng, rng.randint(3, 5), 3.5, 0, rng.uniform(8, 14))
    ang = rng.uniform(-1.2, 1.2)
    d = rng.uniform(18, 30)
    b = pack(rng, rng.randint(3, 5), 3.5, a[0][0] + math.sin(ang) * d, a[0][1] + math.cos(ang) * d)
    return a + b


SCENES = [("밀집 무리", scene_tight), ("넓은 무리", scene_loose), ("복도 일렬", scene_corridor), ("무리 두 개", scene_two_packs)]


def dist(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])


def chain(enemies, radius):
    """반환: 벤 순서(인덱스 목록)"""
    me = (0.0, 0.0)
    near = [i for i, e in enumerate(enemies) if dist(me, e) <= FIRST_RANGE]
    if not near:
        return []
    first = min(near, key=lambda i: dist(me, enemies[i]))
    order = [first]
    hit = {first}
    cur = first
    while len(order) < MAX_TARGETS:
        cands = [i for i, e in enumerate(enemies) if i not in hit and dist(enemies[cur], e) <= radius]
        if not cands:
            break
        nxt = min(cands, key=lambda i: dist(enemies[cur], enemies[i]))
        order.append(nxt)
        hit.add(nxt)
        cur = nxt
    return order


def duration(n):
    return CAST_DELAY + (n - 1) * HOP + RETURN + EXECUTE


def run():
    print(f"시험 {TRIALS}회씩, 최대 {MAX_TARGETS}명, 시간 = 첫 타 {CAST_DELAY} + 건너뛰기 {HOP}×(n-1) + 귀환 {RETURN} + 처형 {EXECUTE}")
    print()
    summary = {}
    for name, fn in SCENES:
        print(f"[{name}]  (상황마다 적 수 평균은 아래 '적')")
        print(" 반경R | 평균 벤 수 | 6명 다 참 | 전원 벰 | 마지막 적-첫 대상 거리(귀환) 평균/최대 | 평균 시간")
        for r in RADII:
            rng = random.Random(1000 + r)
            tot = full = allhit = 0
            back = []
            secs = 0.0
            nen = 0
            for _ in range(TRIALS):
                en = fn(rng)
                nen += len(en)
                o = chain(en, r)
                if not o:
                    continue
                tot += len(o)
                full += len(o) == MAX_TARGETS
                allhit += len(o) == min(len(en), MAX_TARGETS)
                back.append(dist(en[o[-1]], en[o[0]]))
                secs += duration(len(o))
            avg = tot / TRIALS
            summary[(name, r)] = avg
            print(f"  {r:>3}  |   {avg:4.2f}    |  {full / TRIALS * 100:5.1f}%  | {allhit / TRIALS * 100:5.1f}% |"
                  f"            {sum(back) / len(back):5.1f} / {max(back):5.1f}             |  {secs / TRIALS:4.2f}초")
        print(f"  적 평균 {nen / TRIALS / len(RADII):.1f}마리" if False else "")
    return summary


# ---------- 처형 피해 ----------
def execute_table():
    print("처형 배율 = 기본 + 잃은 체력 비율 × 계수 (첫 대상이 연쇄 첫 타를 맞은 뒤의 체력 기준)")
    base, k, boss_cap = 2.0, 3.0, 1.0
    print(" 남은 체력 | 일반 적 배율 | 보스 배율 (잃은 체력 몫 최대 +1.0)")
    for left in [1.0, 0.8, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1]:
        lost = 1 - left
        print(f"   {left * 100:4.0f}%   |    ×{base + lost * k:4.2f}    |   ×{base + min(lost * k, boss_cap):4.2f}")
    print()
    print("연쇄 한 타 배율 c 에 따른 스킬 전체 배율 (6명 다 찼을 때 = 한 명당 c, 첫 대상은 c + 처형)")
    for c in [0.8, 1.0, 1.2, 1.5]:
        print(f"  c = {c}:  첫 대상 혼자 ×{c + 2.0:.1f}~×{c + 4.7:.1f} / 나머지 5명 각 ×{c} / 합계 약 ×{6 * c + 2.0 + 1.5:.1f} (첫 대상 반피 기준)")
    print("  비교: 그림자 발걸음 단일 ×2.4 (쿨 8), 칼날 회오리 광역 ×2.8 (쿨 9)")


# ---------- 예시 그림 ----------
def draw_examples():
    from PIL import Image, ImageDraw, ImageFont
    try:
        font = ImageFont.truetype(r"C:\Windows\Fonts\malgun.ttf", 14)  # 한글 (기본 글꼴은 네모로 깨짐)
    except OSError:
        font = ImageFont.load_default()
    rng = random.Random(7)
    cells = []
    for name, fn in SCENES:
        en = fn(rng)
        for r in (12, 16):
            cells.append((name, r, en, chain(en, r)))
    S, PAD = 360, 10
    cols = 4
    rows = math.ceil(len(cells) / cols)
    img = Image.new("RGB", (cols * S, rows * S), (30, 30, 38))
    d = ImageDraw.Draw(img)
    scale = S / 80  # 화면 80 스터드
    for k, (name, r, en, o) in enumerate(cells):
        ox, oy = (k % cols) * S, (k // cols) * S
        def P(p):
            return (ox + S / 2 + p[0] * scale, oy + S - 30 - p[1] * scale)
        d.rectangle([ox + 1, oy + 1, ox + S - 2, oy + S - 2], outline=(60, 60, 75))
        # 반경 원 (벤 적마다 연하게)
        for i in o[:-1]:
            c = P(en[i])
            rr = r * scale
            d.ellipse([c[0] - rr, c[1] - rr, c[0] + rr, c[1] + rr], outline=(70, 45, 100))
        me = P((0, 0))
        d.ellipse([me[0] - 5, me[1] - 5, me[0] + 5, me[1] + 5], fill=(240, 240, 240))
        path = [me] + [P(en[i]) for i in o]
        for a, b in zip(path, path[1:]):
            d.line([a, b], fill=(160, 90, 255), width=3)
        if o:
            d.line([P(en[o[-1]]), P(en[o[0]])], fill=(255, 255, 255), width=1)  # 귀환
        for i, e in enumerate(en):
            c = P(e)
            col = (255, 80, 80) if i in o else (120, 120, 120)
            d.ellipse([c[0] - 4, c[1] - 4, c[0] + 4, c[1] + 4], fill=col)
        for n, i in enumerate(o):
            c = P(en[i])
            d.text((c[0] + 5, c[1] - 14), str(n + 1), fill=(230, 210, 255), font=font)
        d.text((ox + PAD, oy + PAD), f"{name}  R={r}  벤 수 {len(o)}  (보라 = 연쇄, 흰 선 = 귀환)", fill=(230, 230, 230), font=font)
    p = os.path.join(OUT, "sim_examples.png")
    img.save(p)
    return p


if __name__ == "__main__":
    run()
    print()
    execute_table()
    print()
    print(draw_examples())
