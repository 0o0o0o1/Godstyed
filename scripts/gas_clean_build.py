# 고로 가스 정제 시설 (Lot_025, 용광로 블록 북서쪽 삼각 부지) — 2026-11-21
# 실행 (Blender MCP, 안전 모드 꺼짐):
#   exec(open(r"D:\god\.claude\skills\blender-to-roblox\scripts\factory_kit.py", encoding="utf-8").read())
#   exec(open(r"D:\god\scripts\gas_clean_build.py", encoding="utf-8").read())
# 좌표는 전부 Roblox 월드 (X, Y 위, Z). factory_kit 의 TB() 가 Blender 로 바꿈 (공통 프레임 FX -881, FZ 881, FY 0.5).
# 메쉬 이름 Gc<부품>__<팔레트>__NoCollide[__TEX]. 충돌은 S['col'] → string.pb_colstr() 로 출력해 Studio 에서 투명 파트로 만듦.
# 구성: 집진기(DC, 북동 띠) → 반가스 주관이 배관 다리 J 타워로 / 집진기 → 지상 9.5 높이 관 → 세정탑 2기(S2→S1, 꼭대기 연결관)
#       세정탑 사이 작업대(높이 14) + 2단 계단 / 정제 가스관(높이 9, 밑으로 지나감) → 서쪽 끝 막힘 플랜지
#       펌프동(들어감, 문 2) + 펌프 3 + 급수관 → 세정탑 / 슬러지 침전조 / 드럼·가스병·관 토막
# 비워 둔 곳: 레이드 스폰 Spawn_A2 (-1002, 960) 반경 20, 컨베이어 전환탑·갤러리 받침·석탄 더미, J 타워.
import math
G = 0.5
Y = V(0, 1, 0); XA = V(1, 0, 0); ZA = V(0, 0, 1)
PRE = 'Gc'
CON = PRE + 'Con_Concrete__CoolConcrete__NoCollide__TEX'
FTG = PRE + 'Con_Footings__CoolConcrete__NoCollide__TEX'
STL = PRE + 'Stl_Steel__SteelOxide__NoCollide__TEX'
RST = PRE + 'Rst_Shells__FurnaceRust__NoCollide__TEX'
GRY = PRE + 'Gry_Shells__StoveGrey__NoCollide__TEX'
YEL = PRE + 'Yel_Rails__RailYellow__NoCollide__TEX'
DRK = PRE + 'Drk_Parts__DarkSteel__NoCollide'
PLT = PRE + 'Plt_Grating__DiamondPlate__NoCollide'
SLD = PRE + 'Sld_Sludge__Sludge__NoCollide'
ROOF = PRE + 'Rf_Roof__RoofZinc__NoCollide__TEX'
DRM = PRE + 'Drm_Drums__ShutterOrange__NoCollide__TEX'
GLS = PRE + 'Gls_Glass__Glass__NoCollide'

S['bms'] = {}; S['col'] = []


def ring_faces(name, c, y0, y1, r0, r1, seg=24, inward=False, cyl=1):
    """원뿔대 옆면 (c = 월드 xz 중심). 원통 UV"""
    bm = bm_of(name); T = tile_of(name)
    if isinstance(T, tuple): T = T[0]
    lo = []; hi = []
    for k in range(seg + 1):
        a = 2 * math.pi * k / seg
        lo.append(bm.verts.new(TB(V(c.x + math.cos(a) * r0, y0, c.z + math.sin(a) * r0))))
        hi.append(bm.verts.new(TB(V(c.x + math.cos(a) * r1, y1, c.z + math.sin(a) * r1))))
    slant = math.hypot(y1 - y0, r1 - r0)
    for k in range(seg):
        u0 = 2 * math.pi * max(r0, r1) * k / seg / T; u1 = 2 * math.pi * max(r0, r1) * (k + 1) / seg / T
        q = [lo[k], lo[k + 1], hi[k + 1], hi[k]]
        if inward: q = list(reversed(q))
        _face(bm, q, cyl, [(u0, 0), (u1, 0), (u1, slant / T), (u0, slant / T)] if not inward else [(u0, slant / T), (u1, slant / T), (u1, 0), (u0, 0)])
    return lo, hi


def disc(name, c, y, r, seg=24, up=True):
    bm = bm_of(name)
    vs = [bm.verts.new(TB(V(c.x + math.cos(2 * math.pi * k / seg) * r, y, c.z + math.sin(2 * math.pi * k / seg) * r))) for k in range(seg)]
    _face(bm, vs if not up else list(reversed(vs)))


def vtank(name, c, y0, y1, r, seg=24, top=True, bot=True):
    ring_faces(name, c, y0, y1, r, r, seg)
    if top: disc(name, c, y1, r, seg, True)
    if bot: disc(name, c, y0, r, seg, False)


def wall(name, a, b, y0, y1, t, holes=(), col=True):
    """수직 벽 a→b (월드 xz), 두께 t, 구멍 [(s0, s1, ya, yb)] (s = a 에서의 거리). 구멍마다 조각내고 충돌도 조각마다"""
    d = (b - a); L = d.length; u = d.normalized(); n = u.cross(Y).normalized()
    cuts = sorted(set([0.0, L] + [h[0] for h in holes] + [h[1] for h in holes]))
    for i in range(len(cuts) - 1):
        s0, s1 = cuts[i], cuts[i + 1]
        if s1 - s0 < 1e-3: continue
        hole = None
        for h in holes:
            if h[0] <= s0 + 1e-4 and s1 <= h[1] + 1e-4: hole = h
        spans = [(y0, y1)] if hole is None else [(y0, hole[2]), (hole[3], y1)]
        for ya, yb in spans:
            if yb - ya < 1e-3: continue
            c = a + u * ((s0 + s1) / 2); c = V(c.x, (ya + yb) / 2, c.z)
            obox(name, c, u, Y, n, (s1 - s0) / 2, (yb - ya) / 2, t / 2)
            if col: colbox(c, u, Y, (s1 - s0) / 2, (yb - ya) / 2, t / 2)


def sleeper(c, top, w=1.2):
    """관 받침 (콘크리트 기둥 + 쇠 받침대)"""
    obox(FTG, V(c.x, (G + top - 0.3) / 2, c.z), XA, Y, ZA, w / 2, (top - 0.3 - G) / 2, w / 2)
    obox(DRK, V(c.x, top - 0.15, c.z), XA, Y, ZA, w / 2 + 0.15, 0.15, w / 2 + 0.15)
    colbox(V(c.x, (G + top) / 2, c.z), XA, Y, w / 2, (top - G) / 2, w / 2)


def flange(c, axis, r):
    pipe(DRK, [c - axis * 0.15, c + axis * 0.15], r * 1.35, seg=16, collide=False)


# ================= 1. 집진기 (Dust catcher) — 북동 띠 =================
DC = V(-922, 0, 993)
for sx in (-1, 1):
    for sz in (-1, 1):
        p = V(DC.x + sx * 4.3, 0, DC.z + sz * 4.3)
        obox(FTG, V(p.x, G + 0.5, p.z), XA, Y, ZA, 1.0, 0.5, 1.0)
        ibeam(STL, V(p.x, G + 1.0, p.z), V(p.x, 12.4, p.z), 0.9, 0.9, up=XA)
        colbox(V(p.x, (G + 12.4) / 2, p.z), XA, Y, 0.45, (12.4 - G) / 2, 0.45)
# 링 거더 + X 가새 2단
legs = [V(DC.x - 4.3, 0, DC.z - 4.3), V(DC.x + 4.3, 0, DC.z - 4.3), V(DC.x + 4.3, 0, DC.z + 4.3), V(DC.x - 4.3, 0, DC.z + 4.3)]
for i in range(4):
    a = legs[i]; b = legs[(i + 1) % 4]
    beam(STL, V(a.x, 12.0, a.z), V(b.x, 12.0, b.z), 0.8, 0.8, ext=0.4)
    beam(STL, V(a.x, 6.0, a.z), V(b.x, 6.0, b.z), 0.4, 0.4)
    for y0, y1 in ((1.6, 6.0), (6.0, 11.6)):
        beam(STL, V(a.x, y0, a.z), V(b.x, y1, b.z), 0.24, 0.14)
        if i != 1 or y0 > 2:     # 한 칸 가새 빠짐 (부식)
            beam(STL, V(b.x, y0, b.z), V(a.x, y1, a.z), 0.24, 0.14)
# 몸통 (녹슨 철판) + 아래 원뿔 + 위 원뿔 + 보강 띠
ring_faces(RST, DC, 12.0, 21.0, 5.5, 5.5, 28)
ring_faces(RST, DC, 6.0, 12.0, 1.0, 5.5, 28)
ring_faces(RST, DC, 21.0, 24.4, 5.5, 1.25, 28)
for yb in (12.0, 16.5, 21.0):
    ring_faces(STL, DC, yb - 0.25, yb + 0.25, 5.72, 5.72, 28); ring_faces(STL, DC, yb + 0.25, yb + 0.25, 5.72, 5.5, 28)
    ring_faces(STL, DC, yb - 0.25, yb - 0.25, 5.5, 5.72, 28)
S['col'].append(('C', V(DC.x, 12.0, DC.z), V(DC.x, 21.0, DC.z), 5.5))
S['col'].append(('C', V(DC.x, 7.0, DC.z), V(DC.x, 12.0, DC.z), 3.4))
S['col'].append(('C', V(DC.x, 21.0, DC.z), V(DC.x, 24.4, DC.z), 3.4))
# 아래: 먼지 배출 밸브 + 슈트 + 먼지 통
pipe(STL, [V(DC.x, 6.1, DC.z), V(DC.x, 4.2, DC.z)], 1.0, seg=16)
valve(PRE, V(DC.x, 5.1, DC.z), Y, 1.0, up=XA)
obox(STL, V(DC.x, G + 1.5, DC.z), XA, Y, ZA, 1.6, 1.5, 1.6)
obox(DRK, V(DC.x, G + 3.05, DC.z), XA, Y, ZA, 1.7, 0.08, 1.7)
colbox(V(DC.x, G + 1.55, DC.z), XA, Y, 1.7, 1.55, 1.7)
# 맨 위 노즐 → 반가스 주관 (J 타워 안 높이 27로 들어감)
RAW = [V(DC.x, 24.2, DC.z), V(DC.x, 27.0, DC.z), V(-910.0, 27.0, 1000.0), V(-880.5, 27.0, 1000.0)]
pipe(RST, RAW, 1.2, seg=18, R=2.6)
flange(V(-905.0, 27.0, 1000.0), XA, 1.2); flange(V(-884.6, 27.0, 1000.0), XA, 1.2)
bent2(PRE, V(-897.0, 0, 1000.0), XA, ZA, G, 25.8, 2.2)
# 옆 출구 → 지상 높이 9.5 관 → 세정탑 S2
OUT = [V(DC.x - 5.4, 18.0, DC.z), V(-938.0, 18.0, DC.z), V(-938.0, 9.5, DC.z), V(-938.0, 9.5, 941.0), V(-955.5, 9.5, 926.5), V(-958.9, 9.5, 923.6)]
pipe(STL, OUT, 1.1, seg=18, R=2.4)
valve(PRE, V(-938.0, 13.5, DC.z), Y, 1.1, up=ZA)
for zz in (979.0, 958.0, 946.0):
    tbent(PRE, V(-938.0, 0, zz), ZA, XA, G, 8.4, half=1.5)
tbent(PRE, V(-947.0, 0, 933.5), V(-0.77, 0, -0.64), V(0.64, 0, -0.77), G, 8.4, half=1.5)

# ================= 2. 세정탑 2기 + 꼭대기 연결관 =================
S1 = V(-975.0, 0, 912.0); S2 = V(-962.0, 0, 922.0)
for c in (S1, S2):
    vtank(CON, c, G, 1.3, 4.6, 24)
    S['col'].append(('C', V(c.x, G, c.z), V(c.x, 1.3, c.z), 4.6))
    ring_faces(GRY, c, 1.3, 30.0, 3.5, 3.5, 24)
    ring_faces(GRY, c, 30.0, 33.0, 3.5, 0.9, 24)
    S['col'].append(('C', V(c.x, 1.3, c.z), V(c.x, 30.0, c.z), 3.5))
    S['col'].append(('C', V(c.x, 30.0, c.z), V(c.x, 33.0, c.z), 2.0))
    for yb in (8.0, 16.0, 24.0):
        ring_faces(STL, c, yb - 0.2, yb + 0.2, 3.68, 3.68, 24); ring_faces(STL, c, yb + 0.2, yb + 0.2, 3.68, 3.5, 24)
        ring_faces(STL, c, yb - 0.2, yb - 0.2, 3.5, 3.68, 24)
    # 맨홀 (아래쪽) + 측정 노즐
    pipe(DRK, [V(c.x - 3.4, 3.2, c.z), V(c.x - 4.1, 3.2, c.z)], 0.75, seg=14, collide=False)
    flange(V(c.x - 4.1, 3.2, c.z), XA, 0.75)
    for yy in (11.0, 19.0, 27.0):
        pipe(DRK, [V(c.x, yy, c.z + 3.4), V(c.x, yy, c.z + 4.0)], 0.22, seg=8, collide=False)
pipe(STL, [V(S2.x, 32.6, S2.z), V(S2.x, 35.5, S2.z), V(S1.x, 35.5, S1.z), V(S1.x, 32.6, S1.z)], 0.9, seg=16, R=2.0)
flange(V((S1.x + S2.x) / 2, 35.5, (S1.z + S2.z) / 2), (S1 - S2).normalized(), 0.9)
# 물 분사 관 (세정탑 옆으로 올라가는 가는 관)
for c in (S1, S2):
    pipe(STL, [V(c.x + 3.9, 4.5, c.z), V(c.x + 3.9, 28.0, c.z), V(c.x + 3.0, 28.0, c.z)], 0.28, seg=8, R=0.8, collide=False)
    for yy in (10.0, 18.0, 26.0):
        beam(DRK, V(c.x + 3.5, yy, c.z), V(c.x + 3.9, yy, c.z), 0.16, 0.16)

# ================= 3. 작업대 (높이 14) + 2단 계단 =================
DY = 14.0
X0, X1, Z0, Z1 = -983.0, -955.0, 914.0, 921.0
obox(PLT, V((X0 + X1) / 2, DY - 0.2, (Z0 + Z1) / 2), XA, Y, ZA, (X1 - X0) / 2, 0.2, (Z1 - Z0) / 2)
colbox(V((X0 + X1) / 2, DY - 0.25, (Z0 + Z1) / 2), XA, Y, (X1 - X0) / 2, 0.25, (Z1 - Z0) / 2)
for zz in (Z0, Z1):
    beam(STL, V(X0, DY - 0.75, zz), V(X1, DY - 0.75, zz), 0.35, 0.7, ext=0.2)
for xx in (X0 + 0.4, -969.0, X1 - 0.4):
    beam(STL, V(xx, DY - 0.75, Z0), V(xx, DY - 0.75, Z1), 0.3, 0.6)
    for zz in (Z0 + 0.4, Z1 - 0.4):
        if xx == -969.0 and zz < 916: continue          # 세정탑 S1 근처 기둥 생략
        obox(FTG, V(xx, G + 0.4, zz), XA, Y, ZA, 0.6, 0.4, 0.6)
        ibeam(STL, V(xx, G + 0.8, zz), V(xx, DY - 1.1, zz), 0.6, 0.6, up=XA)
        colbox(V(xx, (G + DY - 1.1) / 2, zz), XA, Y, 0.3, (DY - 1.1 - G) / 2, 0.3)
    # X 가새 (x 방향 줄마다)
for zz in (Z0 + 0.4, Z1 - 0.4):
    beam(STL, V(X0 + 0.4, 1.5, zz), V(-969.5, DY - 1.4, zz), 0.2, 0.12)
# 세정탑에 물린 받침 브래킷
for c, side in ((S1, 1), (S2, -1)):
    beam(STL, V(c.x, DY - 0.6, c.z + side * 3.5), V(c.x, DY - 0.6, c.z + side * (3.5 + 1.2)), 0.3, 0.5)
# 난간 (세정탑이 지나는 곳은 끊음, 계단 들어오는 서쪽 남쪽 칸은 열림)
rail(PRE, V(X0, 0, Z1), V(-965.6, 0, Z1), DY)
rail(PRE, V(-958.4, 0, Z1), V(X1, 0, Z1), DY)
rail(PRE, V(-971.9, 0, Z0), V(X1, 0, Z0), DY)
rail(PRE, V(-978.1, 0, Z0), V(X0, 0, Z0), DY)
rail(PRE, V(X1, 0, Z0), V(X1, 0, Z1), DY)
rail(PRE, V(X0, 0, Z0 + 3.0), V(X0, 0, Z1), DY)
# 계단: 작업대 서쪽 끝 (x -983, z 914..917) 에서 서쪽으로 내려감. 1단 10칸 → 층계참(높이 7) → 2단 10칸 → 땅
SW0, SW1 = Z0 + 0.15, Z0 + 2.85
def flight(xtop, ytop, ybot, n, run):
    rise = (ytop - ybot) / n
    for k in range(n):
        yt = ytop - rise * (k + 1); xa = xtop - run * k; xb = xa - run
        obox(PLT, V((xa + xb) / 2, yt - 0.1, (SW0 + SW1) / 2), XA, Y, ZA, run / 2 + 0.05, 0.1, (SW1 - SW0) / 2)
        colbox(V((xa + xb) / 2, (yt + ybot) / 2 - 0.0 if k == n - 1 else yt - 0.25, (SW0 + SW1) / 2), XA, Y, run / 2, ((yt - ybot) / 2 if k == n - 1 else 0.25), (SW1 - SW0) / 2)
    xb = xtop - run * n
    for zz in (SW0 - 0.12, SW1 + 0.12):
        beam(STL, V(xtop, ytop - 0.5, zz), V(xb, ybot - 0.2, zz), 0.18, 0.5)
        # 기울어진 난간
        n_p = max(2, int(n / 3) + 1)
        for i in range(n_p + 1):
            t = i / n_p; p = V(xtop + (xb - xtop) * t, ytop + (ybot - ytop) * t, zz)
            beam(YEL, p, p + V(0, 3.4, 0), 0.14, 0.14)
        beam(YEL, V(xtop, ytop + 3.5, zz), V(xb, ybot + 3.5, zz), 0.16, 0.16, ext=0.1)
        beam(YEL, V(xtop, ytop + 1.8, zz), V(xb, ybot + 1.8, zz), 0.1, 0.1)
        d = V(xb - xtop, ybot - ytop, 0).normalized()
        colbox(V((xtop + xb) / 2, (ytop + ybot) / 2 + 1.9, zz), d, Y, (V(xb - xtop, ybot - ytop, 0)).length / 2, 1.9, 0.12)
    return xb
xl = flight(X0, DY, 7.0, 10, 1.0)
LX0 = xl - 3.0
obox(PLT, V((xl + LX0) / 2, 6.8, (SW0 + SW1) / 2), XA, Y, ZA, 1.5, 0.2, (SW1 - SW0) / 2 + 0.1)
colbox(V((xl + LX0) / 2, 6.75, (SW0 + SW1) / 2), XA, Y, 1.5, 0.25, (SW1 - SW0) / 2)
for xx in (xl, LX0):
    for zz in (SW0, SW1):
        ibeam(STL, V(xx, G, zz), V(xx, 6.6, zz), 0.4, 0.4, up=XA)
rail(PRE, V(LX0, 0, SW1 + 0.12), V(LX0, 0, SW0 - 0.12), 7.0)
xg = flight(LX0, 7.0, G, 10, 1.0)
obox(FTG, V(xg - 0.6, G + 0.1, (SW0 + SW1) / 2), XA, Y, ZA, 0.8, 0.1, (SW1 - SW0) / 2 + 0.3)

# ================= 4. 정제 가스관 (높이 9, 밑으로 지나감) → 서쪽 끝 막힘 =================
CLN = [V(S1.x - 2.9, 9.0, 910.0), V(-990.0, 9.0, 910.0), V(-1011.0, 9.0, 910.0)]
pipe(STL, CLN, 0.9, seg=16)
flange(V(-1011.0, 9.0, 910.0), XA, 0.9)
pipe(DRK, [V(-1011.15, 9.0, 910.0), V(-1011.35, 9.0, 910.0)], 1.3, seg=16, collide=False)   # 막힘판
valve(PRE, V(-1000.0, 9.0, 910.0), XA, 0.9)
for xx in (-990.0, -1007.0):
    tbent(PRE, V(xx, 0, 910.0), XA, ZA, G, 8.0, half=1.3)

# ================= 5. 펌프동 (들어감) =================
PX0, PX1, PZ0, PZ1 = -1013.0, -995.0, 882.0, 902.0
WT = 0.5; FY = 0.8; WY = 8.5
slab(CON, [V(PX0 - 0.3, 0, PZ0 - 0.3), V(PX1 + 0.3, 0, PZ0 - 0.3), V(PX1 + 0.3, 0, PZ1 + 0.3), V(PX0 - 0.3, 0, PZ1 + 0.3)], G, FY)
colbox(V((PX0 + PX1) / 2, (G + FY) / 2, (PZ0 + PZ1) / 2), XA, Y, (PX1 - PX0) / 2 + 0.3, (FY - G) / 2, (PZ1 - PZ0) / 2 + 0.3)
WALL = PRE + 'Con_Walls__CoolConcrete__NoCollide__TEX'
# 남 (z 882): 창 2
wall(WALL, V(PX0, 0, PZ0 + WT / 2), V(PX1, 0, PZ0 + WT / 2), FY, WY, WT, [(2.5, 5.0, 4.0, 6.5), (11.0, 13.5, 4.0, 6.5)])
# 북 (z 902): 문 (x -1008..-1004) + 창
wall(WALL, V(PX0, 0, PZ1 - WT / 2), V(PX1, 0, PZ1 - WT / 2), FY, WY, WT, [(5.0, 9.0, FY, 7.3), (12.0, 15.0, 4.0, 6.5)])
# 동 (x -995): 문 (z 887..892) + 창
wall(WALL, V(PX1 - WT / 2, 0, PZ0 + WT), V(PX1 - WT / 2, 0, PZ1 - WT), FY, WY, WT, [(4.5, 9.5, FY, 7.3), (13.5, 16.0, 4.0, 6.5)])
# 서 (x -1013): 창
wall(WALL, V(PX0 + WT / 2, 0, PZ0 + WT), V(PX0 + WT / 2, 0, PZ1 - WT), FY, WY, WT, [(7.5, 10.5, 4.0, 6.5)])
# 지붕 + 난간벽
slab(ROOF, [V(PX0 - 0.2, 0, PZ0 - 0.2), V(PX1 + 0.2, 0, PZ0 - 0.2), V(PX1 + 0.2, 0, PZ1 + 0.2), V(PX0 - 0.2, 0, PZ1 + 0.2)], WY, WY + 0.45)
colbox(V((PX0 + PX1) / 2, WY + 0.22, (PZ0 + PZ1) / 2), XA, Y, (PX1 - PX0) / 2 + 0.2, 0.23, (PZ1 - PZ0) / 2 + 0.2)
for a, b in ((V(PX0 - 0.2, 0, PZ0 - 0.05), V(PX1 + 0.2, 0, PZ0 - 0.05)), (V(PX0 - 0.2, 0, PZ1 + 0.05), V(PX1 + 0.2, 0, PZ1 + 0.05)),
             (V(PX0 - 0.05, 0, PZ0), V(PX0 - 0.05, 0, PZ1)), (V(PX1 + 0.05, 0, PZ0), V(PX1 + 0.05, 0, PZ1))):
    wall(CON, a, b, WY + 0.45, WY + 1.2, 0.3, col=False)
# 문틀·창틀 (어두운 쇠) + 떨어진 문짝
for (a, b, y1) in ((V(-1008.0, 0, PZ1), V(-1004.0, 0, PZ1), 7.3), (V(PX1, 0, 886.5), V(PX1, 0, 891.5), 7.3)):
    d = (b - a).normalized(); n = d.cross(Y)
    for p in (a, b):
        obox(DRK, V(p.x, (FY + y1) / 2, p.z), d, Y, n, 0.12, (y1 - FY) / 2, WT / 2 + 0.08)
    obox(DRK, V((a.x + b.x) / 2, y1 + 0.12, (a.z + b.z) / 2), d, Y, n, (b - a).length / 2 + 0.12, 0.12, WT / 2 + 0.08)
obox(DRK, V(-991.5, G + 0.12, 889.0), V(0.95, 0, 0.31).normalized(), Y, V(-0.31, 0, 0.95).normalized(), 1.25, 0.08, 3.1)   # 쓰러진 문짝
colbox(V(-991.5, G + 0.12, 889.0), V(0.95, 0, 0.31).normalized(), Y, 1.25, 0.1, 3.1)
# 깨진 창 유리 조각 (창틀 아래 몇 장만)
for (cx, cz, ru) in ((-1010.0, PZ0 + 0.1, XA), (-1001.5, PZ0 + 0.1, XA)):
    obox(GLS, V(cx, 5.8, cz), ru, Y, ru.cross(Y), 0.6, 0.6, 0.02)
# 지붕 환기 굴뚝
pipe(STL, [V(-999.0, WY + 0.45, 886.0), V(-999.0, WY + 3.4, 886.0)], 0.5, seg=12, collide=False)
pipe(DRK, [V(-999.0, WY + 3.4, 886.0), V(-999.0, WY + 3.9, 886.0)], 0.75, seg=12, collide=False)
# 실내: 펌프 3대 (남쪽 벽 앞) + 제어반 + 헤더관
for i, px in enumerate((-1009.5, -1004.5, -999.5)):
    obox(CON, V(px, FY + 0.3, 885.6), XA, Y, ZA, 0.9, 0.3, 1.6)
    pipe(GRY, [V(px, FY + 1.3, 884.2), V(px, FY + 1.3, 886.0)], 0.62, seg=14, collide=False)     # 모터
    pipe(STL, [V(px - 0.45, FY + 1.3, 886.9), V(px + 0.45, FY + 1.3, 886.9)], 0.85, seg=16, collide=False)  # 볼류트
    pipe(STL, [V(px, FY + 1.3, 887.7), V(px, FY + 1.3, 889.4), V(px, 4.9, 889.4), V(px, 4.9, 884.4)], 0.32, seg=10, R=0.7, collide=False)
    pipe(STL, [V(px + 0.9, FY + 1.3, 886.9), V(px + 0.9, FY + 1.3, 882.6)], 0.3, seg=10, collide=False)   # 흡입 (벽으로)
    colbox(V(px, FY + 1.0, 886.2), XA, Y, 0.95, 1.0, 1.9)
pipe(STL, [V(-1011.5, 4.9, 884.4), V(PX1 + 0.3, 4.9, 884.4)], 0.45, seg=12, collide=False)
obox(GRY, V(-1012.3, FY + 1.3, 897.5), XA, Y, ZA, 0.35, 1.3, 1.6)                             # 제어반
obox(DRK, V(-1011.9, FY + 1.6, 897.5), XA, Y, ZA, 0.05, 0.8, 1.2)
colbox(V(-1012.3, FY + 1.3, 897.5), XA, Y, 0.35, 1.3, 1.6)
obox(GRY, V(-1006.0, FY + 0.45, 899.8), XA, Y, ZA, 1.0, 0.45, 0.6)                            # 공구 상자
colbox(V(-1006.0, FY + 0.45, 899.8), XA, Y, 1.0, 0.45, 0.6)

# ================= 6. 급수관: 펌프동 동쪽 벽 → 세정탑 아래 =================
W1 = [V(PX1 - 0.3, 4.9, 884.4), V(-975.0, 4.9, 884.4), V(-975.0, 4.9, 908.3)]
W2 = [V(-975.0, 4.9, 884.4), V(-962.0, 4.9, 884.4), V(-962.0, 4.9, 918.3)]
pipe(STL, W1, 0.45, seg=12, R=1.0); pipe(STL, W2, 0.45, seg=12, R=1.0, cap0=False)
for c in (V(-987.0, 0, 884.4), V(-968.5, 0, 884.4), V(-975.0, 0, 897.0), V(-962.0, 0, 897.0), V(-962.0, 0, 910.0)):
    sleeper(c, 4.4, 0.8)

# ================= 7. 슬러지 침전조 =================
TK = V(-1005.0, 0, 867.0)
ring_faces(CON, TK, G, 3.5, 7.0, 7.0, 32)
ring_faces(CON, TK, G, 3.5, 6.6, 6.6, 32, inward=True)
lo_, hi_ = None, None
bm = bm_of(CON)
outer = [bm.verts.new(TB(V(TK.x + math.cos(2 * math.pi * k / 32) * 7.0, 3.5, TK.z + math.sin(2 * math.pi * k / 32) * 7.0))) for k in range(32)]
inner = [bm.verts.new(TB(V(TK.x + math.cos(2 * math.pi * k / 32) * 6.6, 3.5, TK.z + math.sin(2 * math.pi * k / 32) * 6.6))) for k in range(32)]
for k in range(32):
    k2 = (k + 1) % 32
    _face(bm, [outer[k], inner[k], inner[k2], outer[k2]])
disc(SLD, TK, 2.4, 6.62, 32, True)
for k in range(16):
    a = 2 * math.pi * (k + 0.5) / 16
    colbox(V(TK.x + math.cos(a) * 6.8, 2.0, TK.z + math.sin(a) * 6.8), V(-math.sin(a), 0, math.cos(a)), Y, 1.4, 1.5, 0.25)
colbox(V(TK.x, 1.45, TK.z), XA, Y, 6.6, 0.95, 6.6)
# 가운데 기둥 + 긁개 다리 (한쪽만 벽에 걸침) + 난간
pipe(GRY, [V(TK.x, 2.4, TK.z), V(TK.x, 4.6, TK.z)], 0.7, seg=14)
obox(PLT, V(TK.x + 3.4, 4.4, TK.z), XA, Y, ZA, 3.7, 0.12, 0.7)
colbox(V(TK.x + 3.4, 4.35, TK.z), XA, Y, 3.7, 0.17, 0.7)
for zz in (TK.z - 0.7, TK.z + 0.7):
    beam(STL, V(TK.x, 4.05, zz), V(TK.x + 7.1, 4.05, zz), 0.2, 0.45)
    rail(PRE, V(TK.x + 0.6, 0, zz), V(TK.x + 7.0, 0, zz), 4.5, col=False)
beam(DRK, V(TK.x + 0.8, 3.0, TK.z), V(TK.x + 5.8, 2.6, TK.z), 0.25, 0.25)        # 긁개 팔 (슬러지에 잠김)
# 펌프동에서 오는 슬러지 관 (남쪽 벽 → 수조 위)
pipe(STL, [V(-1004.0, 4.2, PZ0 - 0.1), V(-1004.0, 4.2, 870.5)], 0.35, seg=10, collide=False)
pipe(STL, [V(-1004.0, 4.2, 870.5), V(-1004.0, 3.2, 869.8)], 0.35, seg=10, collide=False)
sleeper(V(-1004.0, 0, 877.5), 3.85, 0.6)

# ================= 8. 소품: 드럼통·가스병 거치대·관 토막 =================
DRUMS = [(-989.0, 897.5, 0), (-987.6, 898.6, 0), (-988.5, 900.0, 1), (-986.7, 896.9, 0),
         (-948.0, 940.5, 0), (-946.6, 941.4, 2), (-930.0, 985.0, 0), (-931.2, 986.3, 0), (-929.0, 986.6, 1)]
for (x, z, kind) in DRUMS:
    if kind == 2:      # 쓰러진 통
        pipe(DRM, [V(x - 1.4, G + 0.9, z), V(x + 1.4, G + 0.9, z)], 0.9, seg=14)
    else:
        pipe(DRM, [V(x, G, z), V(x, G + 2.8, z)], 0.9, seg=14)
        if kind == 1:
            pipe(DRK, [V(x, G + 2.8, z), V(x, G + 2.9, z)], 0.92, seg=14, collide=False)
# 가스병 거치대 (펌프동 동쪽 벽 옆)
obox(STL, V(-993.3, G + 1.6, 896.5), ZA, Y, XA, 2.0, 0.08, 0.35)
obox(STL, V(-993.3, G + 0.08, 896.5), ZA, Y, XA, 2.0, 0.08, 0.35)
for k in range(5):
    zz = 894.9 + k * 0.8
    pipe(GRY, [V(-993.3, G + 0.16, zz), V(-993.3, G + 2.9, zz)], 0.3, seg=10, collide=False)
    pipe(DRK, [V(-993.3, G + 2.9, zz), V(-993.3, G + 3.25, zz)], 0.12, seg=6, collide=False)
colbox(V(-993.3, G + 1.6, 896.5), ZA, Y, 2.0, 1.6, 0.4)
# 바닥에 굴러다니는 관 토막
for (a, b, r) in ((V(-958.0, 0, 905.0), V(-952.5, 0, 908.5), 0.9), (V(-961.0, 0, 902.0), V(-956.0, 0, 905.6), 0.9), (V(-1009.0, 0, 925.0), V(-1004.0, 0, 931.0), 0.6)):
    pipe(STL, [V(a.x, G + r, a.z), V(b.x, G + r, b.z)], r, seg=14)
print(finalize('GasClean'))
print('colliders', len(S['col']))
