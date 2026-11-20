# Slag Walker (공장 1번 몬스터) 메쉬 생성 v2 — Blender MCP 안전 모드용 (lambda·exec 없음)
# 좌표: Blender (x, y, z) = Roblox HRP 기준 (-X, Z, Y). 캐릭터 앞 = -y, 캐릭터 오른쪽 = -x.
# 오브젝트 이름 = <R15 부위>__<재질키>  (Cloth, Skin, Slag, Helmet, Boot, Dark, Glow)
# 몸 = 단면 loft(Catmull-Rom 보간), 슬래그 = 몸 표면에서 노이즈 마스크로 떼어 낸 껍질(shell) + 덩어리(boulder)
import bpy, bmesh, math
from mathutils import Vector, Matrix, noise

col = bpy.data.collections.get("SlagWalker")
for o in list(col.objects):
    bpy.data.objects.remove(o, do_unlink=True)

PIECES = {}

def bm_for(name):
    if name not in PIECES:
        PIECES[name] = bmesh.new()
    return PIECES[name]

def fbm(p, octaves, seed):
    s = 0.0; a = 1.0; f = 1.0; tot = 0.0
    for i in range(octaves):
        s += a * noise.noise(p * f + Vector((seed * 7.13 + i * 3.1, seed * 3.7, seed * 1.9)))
        tot += a; a *= 0.5; f *= 2.03
    return s / tot

def rock(p, seed):
    """슬래그 표면: 능선 노이즈 + 계단형 셀 노이즈(깨진 판)."""
    r = 1.0 - abs(fbm(p, 4, seed)) * 2.0
    c = noise.cell(p * 0.8 + Vector((seed * 1.7, 0, 0)))
    return 0.72 * r + 0.28 * (c * 2.0 - 1.0)

def smooth01(e0, e1, x):
    t = max(0.0, min(1.0, (x - e0) / (e1 - e0)))
    return t * t * (3 - 2 * t)

def cr(p0, p1, p2, p3, t):
    t2 = t * t; t3 = t2 * t
    return 0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t2 + (-p0 + 3 * p1 - 3 * p2 + p3) * t3)

def loft(name, keys, segs=16, sub=3, expo=1.0, cap0=0.0, cap1=0.0, amp=0.0, freq=4.0, seed=0):
    """keys = [(x, y, z, rx, ry), ...] 경로를 따라 타원(초타원) 단면을 이음. cap = 끝 둥근 마개 길이."""
    bm = bm_for(name)
    K = [Vector(k) for k in keys]
    Kx = [K[0]] + K + [K[-1]]
    pts = []
    for i in range(1, len(Kx) - 2):
        n = sub if i < len(Kx) - 3 else sub + 1
        for s in range(n):
            t = s / sub
            pts.append(cr(Kx[i - 1], Kx[i], Kx[i + 1], Kx[i + 2], t))
    rows = []
    for j, P in enumerate(pts):
        c = Vector((P[0], P[1], P[2]))
        a = Vector((pts[max(0, j - 1)][0], pts[max(0, j - 1)][1], pts[max(0, j - 1)][2]))
        b = Vector((pts[min(len(pts) - 1, j + 1)][0], pts[min(len(pts) - 1, j + 1)][1], pts[min(len(pts) - 1, j + 1)][2]))
        t = (b - a).normalized()
        xa = Vector((1, 0, 0))
        xa = (xa - t * xa.dot(t)).normalized()
        ya = t.cross(xa)
        if ya.y < 0 and abs(t.z) > 0.5:
            ya = -ya
        row = []
        for i in range(segs):
            ang = 2 * math.pi * i / segs
            ca = math.cos(ang); sa = math.sin(ang)
            ux = math.copysign(abs(ca) ** expo, ca); uy = math.copysign(abs(sa) ** expo, sa)
            p = c + xa * (ux * P[3]) + ya * (uy * P[4])
            if amp > 0:
                d = (xa * ux + ya * uy).normalized()
                p = p + d * amp * fbm(p * freq, 3, seed)
            row.append(bm.verts.new(p))
        rows.append((row, c, t))
    for j in range(len(rows) - 1):
        r0 = rows[j][0]; r1 = rows[j + 1][0]
        for i in range(segs):
            i2 = (i + 1) % segs
            bm.faces.new((r0[i], r0[i2], r1[i2], r1[i]))
    # 마개: 링 하나 + 극점
    for which, capl in ((0, cap0), (1, cap1)):
        row, c, t = rows[0] if which == 0 else rows[-1]
        sgn = -1.0 if which == 0 else 1.0
        inner = []
        for v in row:
            q = c + (v.co - c) * 0.6 + t * sgn * capl * 0.75
            inner.append(bm.verts.new(q))
        pole = bm.verts.new(c + t * sgn * capl)
        for i in range(segs):
            i2 = (i + 1) % segs
            if which == 0:
                bm.faces.new((row[i2], row[i], inner[i], inner[i2]))
                bm.faces.new((inner[i2], inner[i], pole))
            else:
                bm.faces.new((row[i], row[i2], inner[i2], inner[i]))
                bm.faces.new((inner[i], inner[i2], pole))
    return bm

def blob(name, c, r, segs=12, rings=8, amp=0.0, freq=3.0, seed=0, square=1.0, kind="smooth", rot=None):
    bm = bm_for(name)
    res = bmesh.ops.create_uvsphere(bm, u_segments=segs, v_segments=rings, radius=1.0)
    c = Vector(c)
    R = rot if rot is not None else Matrix.Identity(3)
    for v in res["verts"]:
        d = v.co.copy()
        if square != 1.0:
            d = Vector((math.copysign(abs(d.x) ** square, d.x), math.copysign(abs(d.y) ** square, d.y), math.copysign(abs(d.z) ** square, d.z)))
        n = d.normalized() if d.length > 1e-6 else Vector((0, 0, 1))
        p = Vector((d.x * r[0], d.y * r[1], d.z * r[2]))
        if amp > 0:
            w = p + c
            if kind == "rock":
                nz = rock(w * freq, seed)
            else:
                nz = fbm(w * freq, 3, seed)
            p = p + Vector((n.x * r[0], n.y * r[1], n.z * r[2])).normalized() * (amp * nz)
        v.co = R @ p + c
    return res["verts"]

def tube(name, a, b, r0, r1, segs=8, rings=2):
    bm = bm_for(name)
    a = Vector(a); b = Vector(b)
    zd = (b - a).normalized(); L = (b - a).length
    M = Vector((0, 0, 1)).rotation_difference(zd).to_matrix()
    rows = []
    for j in range(rings + 1):
        t = j / rings
        rad = r0 + (r1 - r0) * t
        rows.append([bm.verts.new(M @ Vector((math.cos(2 * math.pi * i / segs) * rad, math.sin(2 * math.pi * i / segs) * rad, t * L)) + a) for i in range(segs)])
    for j in range(rings):
        for i in range(segs):
            i2 = (i + 1) % segs
            bm.faces.new((rows[j][i], rows[j][i2], rows[j + 1][i2], rows[j + 1][i]))
    bm.faces.new(list(reversed(rows[0])))
    tip = bm.verts.new(b + zd * r1)
    for i in range(segs):
        bm.faces.new((rows[-1][i], rows[-1][(i + 1) % segs], tip))

def finger(name, pts, r0, r1):
    """관절 꺾인 손가락: 점 목록을 따라 작은 원기둥들."""
    n = len(pts) - 1
    for i in range(n):
        tube(name, pts[i], pts[i + 1], r0 + (r1 - r0) * i / n, r0 + (r1 - r0) * (i + 1) / n, 6, 1)

def push(name, c, rad, amount):
    bm = PIECES[name]
    bm.normal_update()
    c = Vector(c)
    for v in bm.verts:
        d = (v.co - c).length
        if d < rad:
            f = 1 - d / rad
            v.co += v.normal * amount * f * f * (3 - 2 * f)

def crust(dst, src, seed, bias_dir, bias_k, bias_c, thick, amp, mfreq=2.2, rfreq=5.0, holes=0.55, lumpy=True):
    """src 조각 표면을 복사해 마스크가 양수인 면만 남기고 바깥으로 두껍게 띄운 슬래그 껍질을 dst 에 더함."""
    sb = PIECES[src].copy()
    sb.normal_update()
    bias_dir = Vector(bias_dir)
    mask = {}
    for v in sb.verts:
        mask[v.index] = holes * fbm(v.co * mfreq, 3, seed) + bias_k * bias_dir.dot(v.co) + bias_c
    kill = [f for f in sb.faces if sum(mask[v.index] for v in f.verts) / len(f.verts) < 0.0]
    bmesh.ops.delete(sb, geom=kill, context='FACES')
    loose = [v for v in sb.verts if not v.link_faces]
    bmesh.ops.delete(sb, geom=loose, context='VERTS')
    sb.verts.index_update()
    sb.normal_update()
    # 경계 거리(가장자리일수록 얇게)
    edge = set(v for e in sb.edges if e.is_boundary for v in e.verts)
    ring2 = set()
    for v in edge:
        for e in v.link_edges:
            ring2.add(e.other_vert(v))
    lumps = []
    for v in sb.verts:
        m = 0.3 if v in edge else (0.7 if v in ring2 else 1.0)
        h = thick * m + amp * m * rock(v.co * rfreq, seed)
        nrm = v.normal.copy()
        v.co += nrm * max(0.015, h)
        if lumpy and m == 1.0 and noise.noise(v.co * 9.0 + Vector((seed, 0, 0))) > 0.5:
            lumps.append((v.co.copy(), nrm))
    bmesh.ops.solidify(sb, geom=sb.faces[:], thickness=thick * 1.8)
    me = bpy.data.meshes.new("_tmp")
    sb.to_mesh(me); sb.free()
    dbm = bm_for(dst)
    dbm.from_mesh(me)
    bpy.data.meshes.remove(me)
    # 껍질 위에 흩어진 작은 슬래그 알갱이·덩어리
    taken = []
    for k, (p, nrm) in enumerate(lumps):
        if any((p - q).length < 0.30 for q in taken):
            continue
        taken.append(p)
        sz = 0.06 + 0.07 * (0.5 + 0.5 * noise.noise(p * 5.0))
        blob(dst, p + nrm * sz * 0.25, (sz * 1.2, sz * 1.2, sz), 7, 5, sz * 0.45, 9.0, seed + k, kind="rock")

def drip(name, top, length, r, seed):
    """흘러내리다 굳은 슬래그 방울: 가늘어지는 줄기 + 끝 방울."""
    top = Vector(top)
    loft(name, [(top.x, top.y, top.z, r, r), (top.x, top.y - 0.01, top.z - length * 0.5, r * 0.55, r * 0.55),
                (top.x, top.y - 0.02, top.z - length, r * 0.42, r * 0.42)], segs=8, sub=2, cap0=0.0, cap1=r * 0.5, amp=r * 0.15, freq=12.0, seed=seed)
    blob(name, (top.x, top.y - 0.02, top.z - length - r * 0.1), (r * 0.62, r * 0.62, r * 0.7), 8, 6, r * 0.1, 10.0, seed, kind="rock")

def rotx(deg):
    return Matrix.Rotation(math.radians(deg), 3, 'X')

# ================= 몸 (loft) =================
# 머리: 앞으로 빠진 턱, 광대, 이마. 키 링 (x, y, z, rx, ry)
loft("Head__Skin", [(0, -0.22, 1.17, 0.10, 0.08), (0, -0.14, 1.25, 0.23, 0.22), (0, -0.07, 1.40, 0.30, 0.35),
                    (0, -0.03, 1.56, 0.35, 0.42), (0, 0.0, 1.72, 0.37, 0.45), (0, 0.03, 1.88, 0.36, 0.44),
                    (0, 0.04, 2.01, 0.28, 0.36)], segs=24, sub=3, cap0=0.04, cap1=0.10, amp=0.012, freq=7.0, seed=1)
push("Head__Skin", (0.15, -0.46, 1.70), 0.13, -0.07)    # 눈구멍
push("Head__Skin", (-0.15, -0.46, 1.70), 0.13, -0.07)
push("Head__Skin", (0.16, -0.45, 1.81), 0.10, 0.03)     # 눈썹뼈
push("Head__Skin", (-0.16, -0.45, 1.81), 0.10, 0.03)
push("Head__Skin", (0.0, -0.47, 1.59), 0.08, 0.05)      # 코
push("Head__Skin", (0.0, -0.42, 1.39), 0.10, -0.045)    # 입
push("Head__Skin", (0.26, -0.33, 1.47), 0.11, -0.035)   # 볼 꺼짐
push("Head__Skin", (-0.26, -0.33, 1.47), 0.11, -0.035)
blob("Head__Dark", (0.15, -0.395, 1.70), (0.085, 0.03, 0.06), 10, 6)
blob("Head__Dark", (-0.15, -0.395, 1.70), (0.085, 0.03, 0.06), 10, 6)
blob("Head__Dark", (0.0, -0.385, 1.39), (0.11, 0.03, 0.03), 10, 6)
blob("Head__Glow", (0.15, -0.415, 1.70), (0.035, 0.022, 0.03), 8, 6)
blob("Head__Glow", (-0.15, -0.415, 1.70), (0.035, 0.022, 0.03), 8, 6)

# 녹아 내려앉은 안전모
hv = blob("Head__Helmet", (0.0, 0.0, 0.0), (0.44, 0.50, 0.33), 20, 10, 0.01, 5.0, 3)
for v in hv:
    if v.co.z < 0:
        v.co.z = 0.0
bmh = PIECES["Head__Helmet"]
ring_o = []; ring_i = []
for i in range(24):
    ang = 2 * math.pi * i / 24
    ring_o.append(bmh.verts.new((math.cos(ang) * 0.56, math.sin(ang) * 0.60, -0.02)))
    ring_i.append(bmh.verts.new((math.cos(ang) * 0.56, math.sin(ang) * 0.60, -0.055)))
cen_t = bmh.verts.new((0, 0, -0.02)); cen_b = bmh.verts.new((0, 0, -0.055))
for i in range(24):
    i2 = (i + 1) % 24
    bmh.faces.new((ring_o[i], ring_o[i2], cen_t))
    bmh.faces.new((ring_i[i2], ring_i[i], cen_b))
    bmh.faces.new((ring_o[i2], ring_o[i], ring_i[i], ring_i[i2]))
blob("Head__Helmet", (0.0, 0.0, 0.30), (0.07, 0.44, 0.06), 10, 8, square=0.7)   # 가운데 능선
for v in bmh.verts:
    p = v.co
    if p.y < -0.32 and p.z < 0.01:
        p.y -= 0.10 * min(1.0, (-p.y - 0.32) / 0.28)
    p.z -= max(0.0, p.x) * 0.30 + max(0.0, p.x - 0.25) * 0.7 + 0.03 * fbm(p * 6.0, 2, 4)
    v.co = Matrix.Rotation(math.radians(-8), 3, 'Y') @ p + Vector((0.03, 0.03, 1.86))

# 윗몸통: 허리 → 가슴 → 어깨 → 목 밑
loft("UpperTorso__Cloth", [(0, 0.03, -0.58, 0.64, 0.40), (0, 0.02, -0.20, 0.70, 0.42), (0, -0.01, 0.25, 0.80, 0.46),
                           (0, 0.01, 0.64, 0.86, 0.45), (0, 0.05, 0.88, 0.82, 0.39), (0, 0.07, 1.02, 0.50, 0.30),
                           (0, 0.07, 1.10, 0.27, 0.22)], segs=24, sub=3, expo=0.75, cap0=0.02, cap1=0.02, amp=0.018, freq=5.0, seed=21)
loft("UpperTorso__Skin", [(0, 0.06, 1.00, 0.19, 0.18), (0, 0.02, 1.18, 0.18, 0.17), (0, -0.03, 1.33, 0.17, 0.16)], segs=12, sub=2, cap0=0.0, cap1=0.0)
# 아랫몸통 + 벨트
loft("LowerTorso__Cloth", [(0, 0.03, -0.56, 0.66, 0.41), (0, 0.03, -0.78, 0.77, 0.45), (0, 0.03, -0.96, 0.68, 0.40)],
     segs=24, sub=3, expo=0.75, cap0=0.02, cap1=0.12, amp=0.012, freq=5.0, seed=41)
loft("LowerTorso__Boot", [(0, 0.03, -0.67, 0.735, 0.445), (0, 0.03, -0.57, 0.72, 0.44)], segs=24, sub=1, expo=0.75)
blob("LowerTorso__Boot", (0.0, -0.475, -0.62), (0.12, 0.035, 0.08), 8, 6, square=0.5)

# 다리 (바지 + 장화)
for side, sx in (("Left", 0.498), ("Right", -0.498)):
    sd = 51 if sx > 0 else 52
    loft(side + "UpperLeg__Cloth", [(sx, 0.03, -0.84, 0.40, 0.39), (sx, 0.02, -1.15, 0.41, 0.40), (sx, 0.0, -1.55, 0.37, 0.36),
                                    (sx, -0.02, -1.95, 0.33, 0.33), (sx, -0.02, -2.14, 0.31, 0.31)],
         segs=16, sub=2, cap0=0.06, cap1=0.04, amp=0.022, freq=5.0, seed=sd)
    loft(side + "LowerLeg__Cloth", [(sx, -0.02, -1.70, 0.32, 0.32), (sx, 0.01, -2.00, 0.34, 0.34), (sx, 0.0, -2.30, 0.31, 0.31),
                                    (sx, -0.01, -2.52, 0.30, 0.30)], segs=16, sub=2, cap0=0.04, cap1=0.02, amp=0.022, freq=5.0, seed=sd + 2)
    loft(side + "LowerLeg__Boot", [(sx, -0.01, -2.42, 0.335, 0.335), (sx, -0.01, -2.70, 0.32, 0.32), (sx, -0.01, -2.97, 0.33, 0.34)],
         segs=16, sub=2, cap0=0.0, cap1=0.0, amp=0.008, freq=6.0, seed=sd + 4)
    # 장화 발: 뒤꿈치 → 발가락 (y 방향 loft)
    loft(side + "Foot__Boot", [(sx, 0.30, -3.03, 0.30, 0.15), (sx, 0.10, -3.03, 0.31, 0.16), (sx, -0.20, -3.06, 0.32, 0.13),
                               (sx, -0.48, -3.08, 0.30, 0.11)], segs=16, sub=2, expo=0.6, cap0=0.05, cap1=0.12)
    for v in PIECES[side + "Foot__Boot"].verts:
        if v.co.z < -3.19:
            v.co.z = -3.19

# 팔
for side, sx in (("Left", 1.0), ("Right", -1.0)):
    loft(side + "UpperArm__Cloth", [(sx * 1.00, 0.03, 1.00, 0.30, 0.32), (sx * 1.12, 0.03, 0.80, 0.36, 0.36), (sx * 1.28, 0.02, 0.40, 0.32, 0.32),
                                    (sx * 1.40, 0.02, 0.0, 0.29, 0.29), (sx * 1.43, 0.02, -0.18, 0.28, 0.28)],
         segs=16, sub=2, cap0=0.12, cap1=0.04, amp=0.02, freq=5.0, seed=71 if sx > 0 else 72)
# 왼팔: 걷어 올린 소매 + 마른 팔뚝 + 갈퀴 손
loft("LeftLowerArm__Cloth", [(1.43, 0.02, 0.34, 0.29, 0.29), (1.44, 0.02, 0.10, 0.29, 0.29), (1.445, 0.02, 0.0, 0.34, 0.34),
                             (1.45, 0.02, -0.06, 0.30, 0.30)], segs=16, sub=2, cap0=0.02, cap1=0.02, amp=0.02, freq=6.0, seed=73)
loft("LeftLowerArm__Skin", [(1.445, 0.02, 0.0, 0.20, 0.20), (1.46, 0.01, -0.30, 0.19, 0.18), (1.48, -0.01, -0.62, 0.14, 0.13),
                            (1.48, -0.02, -0.74, 0.13, 0.12)], segs=12, sub=2, cap0=0.0, cap1=0.03, amp=0.012, freq=8.0, seed=75)
loft("LeftHand__Skin", [(1.485, -0.02, -0.74, 0.11, 0.14), (1.49, -0.03, -0.86, 0.10, 0.19), (1.50, -0.04, -0.96, 0.08, 0.18)],
     segs=12, sub=2, expo=0.8, cap0=0.0, cap1=0.03)
for k, fy in enumerate((-0.16, -0.06, 0.04, 0.13)):
    bx = 1.505
    finger("LeftHand__Skin", [(bx, fy - 0.02, -0.97), (bx + 0.02, fy * 1.15 - 0.04, -1.10), (bx - 0.01, fy * 1.25 - 0.09, -1.22 + 0.02 * abs(k - 1.5)),
                               (bx - 0.05, fy * 1.25 - 0.14, -1.28 + 0.02 * abs(k - 1.5))], 0.04, 0.018)
finger("LeftHand__Skin", [(1.42, -0.15, -0.86), (1.36, -0.23, -0.97), (1.33, -0.29, -1.08)], 0.045, 0.02)   # 엄지
# 오른팔 소매(슬래그 밑)
loft("RightLowerArm__Cloth", [(-1.43, 0.02, 0.34, 0.29, 0.29), (-1.445, 0.02, 0.0, 0.285, 0.285), (-1.46, 0.02, -0.20, 0.27, 0.27)],
     segs=16, sub=2, cap0=0.02, cap1=0.05, amp=0.02, freq=6.0, seed=77)

# ================= 작업복 디테일 =================
# 접힌 깃 2장, 가슴 주머니 2개 + 덮개, 지퍼 띠, 무릎 덧댐, 소매 단
blob("UpperTorso__Cloth", (0.17, -0.19, 1.02), (0.17, 0.11, 0.035), 10, 6, square=0.6, rot=Matrix.Rotation(math.radians(30), 3, 'X') @ Matrix.Rotation(math.radians(-25), 3, 'Y'))
blob("UpperTorso__Cloth", (-0.17, -0.19, 1.02), (0.17, 0.11, 0.035), 10, 6, square=0.6, rot=Matrix.Rotation(math.radians(30), 3, 'X') @ Matrix.Rotation(math.radians(25), 3, 'Y'))
for px in (0.36, -0.36):
    blob("UpperTorso__Cloth", (px, -0.455, 0.42), (0.17, 0.03, 0.15), 10, 6, 0.006, 12.0, 23, square=0.45)
    blob("UpperTorso__Cloth", (px, -0.475, 0.55), (0.18, 0.025, 0.045), 10, 6, square=0.45)
loft("UpperTorso__Boot", [(0, -0.47, -0.55, 0.025, 0.02), (0, -0.475, 0.30, 0.025, 0.02), (0, -0.44, 0.92, 0.025, 0.02)], segs=6, sub=3)
for side, sx in (("Left", 0.498), ("Right", -0.498)):
    blob(side + "LowerLeg__Cloth", (sx, -0.33, -1.83), (0.22, 0.06, 0.20), 10, 6, 0.008, 10.0, 24, square=0.5)

# ================= 슬래그 =================
# 껍질 (src 조각 표면에서 떼어 냄): crust(dst, src, seed, bias_dir, bias_k, bias_c, thick, amp)
crust("UpperTorso__Slag", "UpperTorso__Cloth", 31, (-0.55, 1.0, 0.25), 1.7, -0.20, 0.09, 0.09)
crust("Head__Slag", "Head__Skin", 33, (1.0, 0.2, 0.0), 2.6, -0.62, 0.06, 0.06, mfreq=3.5, rfreq=7.0)
crust("RightUpperArm__Slag", "RightUpperArm__Cloth", 34, (0, 0, 1.0), 0.6, 0.45, 0.09, 0.09)
crust("RightLowerArm__Slag", "RightLowerArm__Cloth", 35, (0, 0, -1.0), 0.6, 0.55, 0.10, 0.09)
crust("Head__Slag", "Head__Helmet", 39, (1.0, 0, 0), 2.0, -0.40, 0.04, 0.05, mfreq=3.0, rfreq=7.0, lumpy=False)
# 덩어리: 등 혹, 오른어깨, 곤봉 손
blob("UpperTorso__Slag", (-0.10, 0.40, 0.78), (0.52, 0.26, 0.36), 18, 12, 0.08, 4.0, 41, kind="rock")
blob("UpperTorso__Slag", (-0.62, 0.12, 0.98), (0.34, 0.34, 0.22), 16, 10, 0.07, 4.5, 42, kind="rock")
blob("UpperTorso__Slag", (0.22, 0.58, 1.00), (0.12, 0.10, 0.24), 10, 8, 0.03, 7.0, 43, kind="rock", rot=rotx(-30))
blob("UpperTorso__Slag", (-0.24, 0.62, 0.88), (0.11, 0.10, 0.22), 10, 8, 0.03, 7.0, 44, kind="rock", rot=rotx(-40))
blob("RightUpperArm__Slag", (-1.16, 0.03, 0.80), (0.40, 0.40, 0.30), 16, 10, 0.07, 4.5, 45, kind="rock")
blob("RightLowerArm__Slag", (-1.47, -0.02, -0.40), (0.40, 0.40, 0.34), 16, 10, 0.07, 4.5, 46, kind="rock")
blob("RightHand__Slag", (-1.50, -0.04, -1.10), (0.58, 0.56, 0.58), 22, 14, 0.12, 3.2, 47, kind="rock")
blob("RightHand__Slag", (-1.68, -0.26, -1.46), (0.32, 0.32, 0.28), 16, 10, 0.07, 4.5, 48, kind="rock")
blob("RightHand__Slag", (-1.26, 0.22, -1.34), (0.30, 0.28, 0.30), 16, 10, 0.07, 4.5, 49, kind="rock")
blob("RightHand__Slag", (-1.52, 0.30, -0.80), (0.26, 0.24, 0.24), 14, 8, 0.06, 5.0, 50, kind="rock")
# 몸에 반쯤 묻힌 덩어리 (엉덩이·다리·왼어깨)
blob("LowerTorso__Slag", (-0.64, 0.06, -0.80), (0.22, 0.36, 0.24), 14, 9, 0.06, 5.0, 51, kind="rock")
blob("RightUpperLeg__Slag", (-0.72, -0.10, -1.24), (0.20, 0.30, 0.36), 14, 9, 0.06, 5.0, 52, kind="rock")
blob("RightUpperLeg__Slag", (-0.60, -0.30, -1.62), (0.20, 0.16, 0.22), 12, 8, 0.05, 6.0, 53, kind="rock")
blob("LeftLowerLeg__Slag", (0.70, -0.08, -2.08), (0.16, 0.26, 0.32), 12, 8, 0.05, 6.0, 54, kind="rock")
blob("LeftLowerLeg__Slag", (0.56, -0.30, -2.26), (0.20, 0.14, 0.20), 12, 8, 0.05, 6.0, 55, kind="rock")
blob("LeftUpperArm__Slag", (1.06, 0.10, 1.02), (0.26, 0.26, 0.11), 12, 8, 0.04, 6.0, 56, kind="rock")
# 흘러내리다 굳은 방울
drip("UpperTorso__Slag", (-0.30, -0.47, -0.10), 0.26, 0.05, 61)
drip("UpperTorso__Slag", (0.32, -0.49, 0.14), 0.18, 0.04, 62)
drip("UpperTorso__Slag", (0.12, 0.62, 0.44), 0.30, 0.06, 63)
drip("UpperTorso__Slag", (-0.40, 0.55, 0.30), 0.22, 0.05, 64)
drip("RightLowerArm__Slag", (-1.62, -0.30, -0.62), 0.22, 0.05, 65)
drip("RightHand__Slag", (-1.40, -0.40, -1.55), 0.20, 0.06, 66)
drip("Head__Slag", (0.26, -0.30, 1.22), 0.14, 0.035, 67)
# 곤봉 앞으로 삐져나온 손가락 끝
finger("RightHand__Skin", [(-1.36, -0.44, -0.96), (-1.33, -0.60, -1.00), (-1.31, -0.70, -1.08)], 0.05, 0.025)
finger("RightHand__Skin", [(-1.52, -0.48, -0.88), (-1.51, -0.63, -0.92), (-1.50, -0.73, -1.00)], 0.05, 0.025)

# 곤봉 손이 오른 허벅지를 뚫지 않게 바깥(-x)으로 0.12 이동 (BVH 검사 결과)
for _n in ("RightHand__Slag", "RightHand__Skin"):
    for _v in PIECES[_n].verts:
        _v.co.x -= 0.12

# ================= 메쉬 만들기 =================
MATCOL = {"Cloth": (0.11, 0.13, 0.16), "Skin": (0.24, 0.13, 0.10), "Slag": (0.10, 0.09, 0.09),
          "Helmet": (0.55, 0.42, 0.12), "Boot": (0.09, 0.07, 0.06), "Dark": (0.01, 0.01, 0.01), "Glow": (1.0, 0.43, 0.10)}
for key, c in MATCOL.items():
    m = bpy.data.materials.get("SW_" + key) or bpy.data.materials.new("SW_" + key)
    m.use_nodes = True
    bsdf = next(n for n in m.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    bsdf.inputs["Base Color"].default_value = (c[0], c[1], c[2], 1)
    m.diffuse_color = (c[0], c[1], c[2], 1)

tris = 0
REPORT = []
for name, bm in PIECES.items():
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.0005)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    o = bpy.data.objects.new(name, me)
    col.objects.link(o)
    key = name.split("__")[1]
    me.materials.append(bpy.data.materials["SW_" + key])
    for p in me.polygons:
        p.use_smooth = True
    if key == "Slag":
        # 깨진 판 느낌: 각진 모서리만 날카롭게
        me.validate()
        bm2 = bmesh.new(); bm2.from_mesh(me)
        for e in bm2.edges:
            if len(e.link_faces) == 2 and e.calc_face_angle(0) > math.radians(38):
                e.smooth = False
        bm2.to_mesh(me); bm2.free()
    t = sum(len(p.vertices) - 2 for p in me.polygons)
    tris += t
    REPORT.append(name + ":" + str(t))
print("pieces", len(PIECES), "tris", tris)
# 삼각형 줄이기 (내보낼 때 적용): 슬래그 0.55, 큰 작업복 0.7
for o in col.objects:
    key = o.name.split("__")[1]
    ratio = 0.55 if key == "Slag" else (0.7 if len(o.data.polygons) > 500 else 1.0)
    if ratio < 1.0:
        md = o.modifiers.new("Decimate", 'DECIMATE')
        md.ratio = ratio
        md.use_collapse_triangulate = True
dg = bpy.context.evaluated_depsgraph_get()
tris2 = 0
for o in col.objects:
    ev = o.evaluated_get(dg)
    tris2 += sum(len(p.vertices) - 2 for p in ev.data.polygons)
print("tris after decimate", tris2)
print(", ".join(REPORT))
