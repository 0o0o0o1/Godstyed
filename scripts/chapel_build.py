# 마을 place 묘지 옆 작은 성당 (Blender, exec → build_chapel())
# 좌표는 Roblox 모델 로컬(원점 = 바닥 중앙, 월드 (-71, 0.5, -130), 회전 없음)로 쓰고 B() 로 Blender 로 바꿈:
#   Roblox (X, Y, Z) -> Blender (-X, Z, Y).  +Z = 남쪽(입구, 로터리 쪽), -Z = 북쪽(제단, 묘지 쪽), -X = 서쪽(종탑).
# 오브젝트(머티리얼) = Studio 재질:
#   CH_stone  = 영묘 돌 SA (117495829238370, UV 8 스터드)      CH_trim = 영묘 테두리 SA (124399009663796, UV 10)
#   CH_roof   = MaterialVariant Town_Slate (UV 16)             CH_wood = Wood,  CH_metal = 종·철물
# 충돌 상자는 COLS 에 모아 colstr() 로 Luau 문자열 출력 (회전 상자는 CFrame 행렬).
import bpy, bmesh, math
from mathutils import Vector, Matrix

UVS = {"CH_stone": 8.0, "CH_trim": 10.0, "CH_roof": 16.0, "CH_wood": 4.0, "CH_metal": 4.0}
RGB = {"CH_stone": (0.45, 0.43, 0.40), "CH_trim": (0.55, 0.53, 0.50), "CH_roof": (0.20, 0.21, 0.23),
       "CH_wood": (0.25, 0.17, 0.10), "CH_metal": (0.12, 0.10, 0.08)}
COLS = []


def B(p):
    return Vector((-p.x, p.z, p.y))


class Obj:
    def __init__(self, name):
        self.name = name; self.s = UVS[name]
        self.bm = bmesh.new(); self.uv = self.bm.loops.layers.uv.new("UVMap")

    def poly(self, pts, uvmode=None):
        v = [self.bm.verts.new(B(p)) for p in pts]
        f = self.bm.faces.new(v)
        f.normal_update()
        n = f.normal  # Blender 좌표
        ax = max(range(3), key=lambda i: abs(n[i]))
        for lp in f.loops:
            c = lp.vert.co
            uv = (c.y, c.z) if ax == 0 else ((c.x, c.z) if ax == 1 else (c.x, c.y))
            lp[self.uv].uv = (uv[0] / self.s, uv[1] / self.s)
        return f

    def solid(self, bot, top):
        """bot/top: 같은 개수의 Roblox 점 목록(밑면 다각형 + 밀어낸 윗면). 면 방향을 직접 바깥으로 맞춤.
        (면마다 꼭짓점을 따로 만들어서 recalc_face_normals 가 방향을 못 잡음 → 장미창 등이 뒤집혀 깜빡였음)"""
        n = len(bot)
        bb = [B(p) for p in bot]; tb = [B(p) for p in top]       # Blender 좌표(거울 변환 뒤)에서 방향 계산
        e = tb[0] - bb[0]
        nw = Vector((0, 0, 0))                                    # Newell 법선
        for i in range(n):
            a, c = bb[i], bb[(i + 1) % n]
            nw += Vector(((a.y - c.y) * (a.z + c.z), (a.z - c.z) * (a.x + c.x), (a.x - c.x) * (a.y + c.y)))
        if nw.dot(e) < 0:
            bot = list(reversed(bot)); top = list(reversed(top))
        # 이제 bot 순서는 e 기준 반시계(Blender) → 윗면 그대로(+e), 밑면 뒤집기(-e), 옆면 [bi,bj,tj,ti] 바깥
        self.poly(list(reversed(bot))); self.poly(top)
        for i in range(n):
            j = (i + 1) % n
            self.poly([bot[i], bot[j], top[j], top[i]])

    def box(self, x0, x1, y0, y1, z0, z1, M=None, col=True):
        cs = ((x0, z0), (x1, z0), (x1, z1), (x0, z1))
        bot = [Vector((x, y0, z)) for (x, z) in cs]; top = [Vector((x, y1, z)) for (x, z) in cs]
        if M is not None:
            bot = [M @ p for p in bot]; top = [M @ p for p in top]
        self.solid(bot, top)
        if col:
            C = Matrix.Translation(((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2))
            if M is not None:
                C = M @ C
            COLS.append((C, (x1 - x0, y1 - y0, z1 - z0)))

    def prism(self, pts2, plane, a0, a1, col=False):
        """pts2 = 2D 다각형, plane: 'XY'(Z 로 밀기) | 'ZY'(X 로 밀기) | 'XZ'(Y 로 밀기)."""
        def mk(u, v, a):
            if plane == 'XY':
                return Vector((u, v, a))
            if plane == 'ZY':
                return Vector((a, v, u))
            return Vector((u, a, v))
        self.solid([mk(u, v, a0) for u, v in pts2], [mk(u, v, a1) for u, v in pts2])

    def cyl(self, c, r, h, seg=10, r2=None):
        r2 = r if r2 is None else r2
        bot = [Vector((c.x + r * math.cos(2 * math.pi * i / seg), c.y, c.z + r * math.sin(2 * math.pi * i / seg))) for i in range(seg)]
        top = [Vector((c.x + r2 * math.cos(2 * math.pi * i / seg), c.y + h, c.z + r2 * math.sin(2 * math.pi * i / seg))) for i in range(seg)]
        self.solid(bot, top)

    def finish(self, col):
        # 면 방향은 solid() 에서 이미 바깥으로 맞춤 (recalc 하면 떨어진 면을 마구 뒤집음)
        me = bpy.data.meshes.new(self.name); self.bm.to_mesh(me); self.bm.free()
        ob = bpy.data.objects.new(self.name, me); col.objects.link(ob)
        m = bpy.data.materials.get("M_" + self.name) or bpy.data.materials.new("M_" + self.name)
        c = RGB[self.name]; m.diffuse_color = (c[0], c[1], c[2], 1)
        ob.data.materials.append(m)
        return ob


def rot(axis, deg, pivot):
    pv = Vector(pivot)
    return Matrix.Translation(pv) @ Matrix.Rotation(math.radians(deg), 4, axis) @ Matrix.Translation(-pv)


def side_wall(S, T, x0, x1, z0, z1, wins, H=14.0, sill=4.5, head=11.5, door=None):
    """X 쪽 벽 (z 방향으로 긴 벽). wins = 창 중심 z 목록 (폭 3), door = (zc, 폭, 높이)."""
    S.box(x0, x1, 0, sill, z0, z1)
    S.box(x0, x1, head + 1.0, H, z0, z1)
    edges = [z0]
    for zc in wins:
        edges += [zc - 1.5, zc + 1.5]
    edges.append(z1)
    for i in range(0, len(edges), 2):
        if edges[i + 1] > edges[i]:
            S.box(x0, x1, sill, head + 1.0, edges[i], edges[i + 1])
    for zc in wins:
        # 뾰족 아치: 창 위 양쪽 모서리를 삼각으로 채움 (head..head+1)
        S.prism([(zc - 1.5, head), (zc - 1.5, head + 1.0), (zc, head + 1.0)], 'ZY', x0, x1)
        S.prism([(zc + 1.5, head), (zc, head + 1.0), (zc + 1.5, head + 1.0)], 'ZY', x0, x1)
        # 창턱 (바깥으로 0.35)
        out = x1 + 0.35 if x1 > 0 else x0 - 0.35
        a, b = sorted((out, x1 if x1 > 0 else x0))
        T.box(a, b, sill - 0.35, sill, zc - 1.9, zc + 1.9, col=False)


def build_chapel():
    COLS.clear()
    col = bpy.data.collections.get("Chapel")
    if col is None:
        col = bpy.data.collections.new("Chapel"); bpy.context.scene.collection.children.link(col)
    for o in list(col.objects):
        bpy.data.objects.remove(o, do_unlink=True)
    S, T, R, W, M = Obj("CH_stone"), Obj("CH_trim"), Obj("CH_roof"), Obj("CH_wood"), Obj("CH_metal")
    H, TH = 14.0, 1.6
    XO, XI = 12.0, 12.0 - TH           # 본당 바깥/안쪽 x
    ZN, ZS = -22.0, 18.0                # 북/남 바깥 z
    WINS = [-16.0, -8.0, 0.0, 6.0]
    # ---- 옆벽 ----
    side_wall(S, T, XI, XO, ZN + TH, ZS - TH, WINS)                    # 동쪽 벽
    # 서쪽 벽: 종탑 쪽(z 9..16.4)에 종탑 문(폭 3, 높이 7, z 12..15)
    side_wall(S, T, -XO, -XI, ZN + TH, 9.0, WINS[:3])
    S.box(-XO, -XI, 0, H, 9.0, 12.0); S.box(-XO, -XI, 0, H, 15.0, ZS - TH); S.box(-XO, -XI, 7.0, H, 12.0, 15.0)
    # ---- 남쪽 벽 (입구) + 박공 ----
    S.box(-XO, -3.0, 0, H, ZS - TH, ZS); S.box(3.0, XO, 0, H, ZS - TH, ZS); S.box(-3.0, 3.0, 10.5, H, ZS - TH, ZS)
    S.prism([(-3.0, 9.0), (-3.0, 10.5), (0.0, 10.5)], 'XY', ZS - TH, ZS)
    S.prism([(3.0, 9.0), (0.0, 10.5), (3.0, 10.5)], 'XY', ZS - TH, ZS)
    S.prism([(-XO, H), (XO, H), (0.0, 24.0)], 'XY', ZS - TH, ZS)
    # 문틀·장미창 장식(테두리 고리, 구멍 없음)·처마 띠
    T.box(-3.8, -3.0, 0.4, 10.5, ZS, ZS + 0.4); T.box(3.0, 3.8, 0.4, 10.5, ZS, ZS + 0.4); T.box(-3.8, 3.8, 10.5, 11.3, ZS, ZS + 0.4)
    for i in range(8):
        a0 = 2 * math.pi * i / 8; a1 = 2 * math.pi * (i + 1) / 8
        p = [(2.6 * math.cos(a0), 18.5 + 2.6 * math.sin(a0)), (2.6 * math.cos(a1), 18.5 + 2.6 * math.sin(a1)),
             (3.3 * math.cos(a1), 18.5 + 3.3 * math.sin(a1)), (3.3 * math.cos(a0), 18.5 + 3.3 * math.sin(a0))]
        T.prism(p, 'XY', ZS, ZS + 0.35)
    e = 2.6 - 0.5 * math.tan(math.pi / 8)     # 팔각 안쪽 변까지 (막대 모서리가 고리에 닿기만)
    T.prism([(-0.5, 18.5 - e), (0.5, 18.5 - e), (0.5, 18.5 + e), (-0.5, 18.5 + e)], 'XY', ZS, ZS + 0.3)
    T.prism([(-e, 18.0), (-0.5, 18.0), (-0.5, 19.0), (-e, 19.0)], 'XY', ZS, ZS + 0.3)
    T.prism([(0.5, 18.0), (e, 18.0), (e, 19.0), (0.5, 19.0)], 'XY', ZS, ZS + 0.3)
    # ---- 북쪽 벽 + 부서진 박공 ----
    S.box(-XO, XO, 0, H, ZN, ZN + TH)
    S.prism([(-XO, H), (XO, H), (XO, H + 1.0), (7.0, 17.5), (4.0, 16.0), (0.5, 19.8), (-3.0, 17.0), (-7.5, 18.6), (-XO, H + 1.5)], 'XY', ZN, ZN + TH)
    # 처마 띠(옆벽 위)
    for (a, b) in ((XO, XO + 0.4), (-XO - 0.4, -XO)):
        T.box(a, b, H - 1.0, H - 0.4, ZN, 9.0 if a < 0 else ZS, col=False)
    # 버팀벽 (창 사이, 바깥)
    for zc in (-20.0, -12.0, -4.0, 3.0):
        for s in (-1, 1):
            if s < 0 and zc > 8:
                continue
            a, b = sorted((s * XO, s * (XO + 1.4)))
            S.box(a, b, 0, 7.5, zc - 0.7, zc + 0.7)
            S.prism([(a if s > 0 else b, 7.5), (b if s > 0 else a, 7.5), (a if s > 0 else b, 10.0)], 'XY', zc - 0.7, zc + 0.7)
    # ---- 바닥·계단·제단 ----
    T.box(-XI, XI, 0.0, 0.4, ZN + TH, ZS - TH)
    T.box(-4.5, 4.5, 0.0, 0.4, ZS, ZS + 2.2)
    T.box(-XI, XI, 0.4, 1.2, ZN + TH, -15.0)
    S.box(-3.0, 3.0, 1.2, 4.4, -19.5, -17.5)
    T.box(-3.4, 3.4, 4.4, 4.8, -19.8, -17.2, col=False)
    # ---- 지붕 (남쪽 절반만 남음) ----
    th = math.atan2(10.0, 12.0)
    d = Vector((math.cos(th), -math.sin(th))); n = Vector((math.sin(th), math.cos(th)))
    def slab(sign, z0, z1, xs_end, t0=0.0, t1=1.0, thick=0.8):
        """sign=+1 동쪽 경사. t0..t1 = 마루→처마 사이 비율 구간. xs_end = 처마 끝 x(절대값)."""
        L = xs_end / math.cos(th)
        P0 = Vector((0.0, 24.0)) + d * (L * t0); P1 = Vector((0.0, 24.0)) + d * (L * t1)
        pts = [P0, P1, Vector((P1.x, P1.y + thick / math.cos(th))), P0 + n * thick]
        R.prism([(sign * p.x, p.y) for p in pts], 'XY', z0, z1)
        cx = sign * (P0.x + P1.x) / 2; cy = (P0.y + P1.y) / 2 + thick / 2
        C = Matrix.Translation((cx, cy, (z0 + z1) / 2)) @ Matrix.Rotation(-sign * th, 4, 'Z')
        COLS.append((C, ((P1 - P0).length, thick, z1 - z0)))
    # 동쪽: 띠 3개, 북쪽 끝이 들쭉날쭉
    slab(1, -3.0, ZS + 0.8, 13.0, 0.0, 0.34); slab(1, -5.5, ZS + 0.8, 13.0, 0.34, 0.68); slab(1, -1.5, ZS + 0.8, 13.0, 0.68, 1.0)
    # 서쪽: 종탑 구간(z 9..18.8)은 처마 없이 x=12 까지
    slab(-1, -2.0, 9.0, 13.0, 0.0, 0.5); slab(-1, -6.0, 9.0, 13.0, 0.5, 1.0)
    slab(-1, 9.0, ZS + 0.8, 12.0, 0.0, 1.0)
    yt = lambda x: 24.0 - 10.0 / 12.0 * x + 0.8 / math.cos(th)     # 지붕판 윗면 (x>=0.512)
    T.prism([(0.0, 24.0), (0.8 * math.sin(th), 24.0 + 0.8 * math.cos(th)), (0.9, yt(0.9)), (0.9, yt(0.9) + 0.3), (0.0, 25.05),
             (-0.9, yt(0.9) + 0.3), (-0.9, yt(0.9)), (-0.8 * math.sin(th), 24.0 + 0.8 * math.cos(th))], 'XY', -2.0, ZS + 0.8)   # 용마루
    COLS.append((Matrix.Translation((0.0, 24.6, (ZS + 0.8 - 2.0) / 2)), (1.8, 0.8, ZS + 2.8)))
    # 무너진 쪽: 남은 서까래·마룻대(나무), 떨어진 지붕판
    W.box(-0.35, 0.35, 22.5, 23.2, -14.0, -6.5)
    for zr, ln in ((-8.5, 1.0), (-12.5, 0.55)):
        for s in (-1, 1):
            Lr = (11.0 - 0.35) / math.cos(th) * ln
            A = Vector((0.35, 22.9)); Bp = A + d * Lr
            pts = [(s * A.x, A.y), (s * Bp.x, Bp.y), (s * (Bp + n * 0.5).x, (Bp + n * 0.5).y), (s * (A + n * 0.5).x, (A + n * 0.5).y)]
            W.prism(pts, 'XY', zr - 0.3, zr + 0.3)
    fall = rot('X', -38, (6.0, 0.4, -12.0)) @ rot('Z', 6, (1.5, 0.4, -12.0))
    R.box(1.5, 10.0, 0.4, 1.2, -12.0, -3.0, M=fall)
    # ---- 긴 의자 (남쪽 줄은 서 있고, 북쪽은 넘어지거나 없음) ----
    def pew(x0, z, M=None):
        W.box(x0, x0 + 6.0, 1.8, 2.2, z - 0.7, z + 0.7, M=M)
        W.box(x0, x0 + 6.0, 2.2, 4.2, z + 0.5, z + 0.8, M=M)
        for xx in (x0 + 0.3, x0 + 5.3):
            W.box(xx, xx + 0.4, 0.4, 1.8, z - 0.6, z + 0.6, M=M, col=False)
    for z in (13.0, 9.4, 5.8, 2.2):
        pew(-8.0, z); pew(2.0, z)
    pew(-8.0, -1.4, rot('Y', 9, (-5, 0, -1.4)))
    pew(-8.0, -8.6, rot('Y', -22, (-5, 0, -8.6)))
    # ---- 문짝 (하나는 안으로 열림, 하나는 계단 위에 쓰러짐) ----
    W.box(-3.0, -0.05, 0.4, 9.0, ZS - TH - 0.3, ZS - TH, M=rot('Y', 55, (-3.0, 0, ZS - TH)))
    W.box(-0.5, 2.45, 0.0, 0.3, ZS + 3.0, ZS + 11.9, M=rot('Y', -12, (1.0, 0, ZS + 7.5)))
    # ---- 종탑 (서쪽 앞, x -21..-12, z 9..18) ----
    TX0, TX1, TZ0, TZ1, TT, TH2 = -21.0, -12.0, 9.0, 18.0, 1.2, 36.0
    BEL0, BEL1 = 30.0, 35.0
    def tower_wall(axis, fixed0, fixed1, a0, a1):
        """axis='X': x 고정(fixed0..fixed1), z a0..a1 / axis='Z' 반대. 종 칸 구멍(폭 3) 남김."""
        am = (a0 + a1) / 2
        for (b0, b1, y0, y1) in ((a0, a1, 0, BEL0), (a0, a1, BEL1, TH2), (a0, am - 1.5, BEL0, BEL1), (am + 1.5, a1, BEL0, BEL1)):
            if axis == 'X':
                S.box(fixed0, fixed1, y0, y1, b0, b1)
            else:
                S.box(b0, b1, y0, y1, fixed0, fixed1)
        if axis == 'X':
            S.prism([(am - 1.5, BEL1 - 1.0), (am - 1.5, BEL1), (am, BEL1)], 'ZY', fixed0, fixed1)
            S.prism([(am + 1.5, BEL1 - 1.0), (am, BEL1), (am + 1.5, BEL1)], 'ZY', fixed0, fixed1)
        else:
            S.prism([(am - 1.5, BEL1 - 1.0), (am - 1.5, BEL1), (am, BEL1)], 'XY', fixed0, fixed1)
            S.prism([(am + 1.5, BEL1 - 1.0), (am, BEL1), (am + 1.5, BEL1)], 'XY', fixed0, fixed1)
    tower_wall('X', TX0, TX0 + TT, TZ0, TZ1)                 # 서쪽
    tower_wall('Z', TZ0, TZ0 + TT, TX0 + TT, TX1 - TT)       # 북쪽
    tower_wall('Z', TZ1 - TT, TZ1, TX0 + TT, TX1 - TT)       # 남쪽
    # 동쪽: 아래 14 까지는 본당 서쪽 벽과 붙은 두께 1.2 벽(문 구멍 z 12..15, 높이 7), 위는 종 칸 구멍
    S.box(TX1 - TT, TX1, 0, H, TZ0, 12.0); S.box(TX1 - TT, TX1, 0, H, 15.0, TZ1); S.box(TX1 - TT, TX1, 7.0, H, 12.0, 15.0)
    am = (TZ0 + TZ1) / 2
    S.box(TX1 - TT, TX1, H, BEL0, TZ0, TZ1); S.box(TX1 - TT, TX1, BEL1, TH2, TZ0, TZ1)
    S.box(TX1 - TT, TX1, BEL0, BEL1, TZ0, am - 1.5); S.box(TX1 - TT, TX1, BEL0, BEL1, am + 1.5, TZ1)
    S.prism([(am - 1.5, BEL1 - 1.0), (am - 1.5, BEL1), (am, BEL1)], 'ZY', TX1 - TT, TX1)
    S.prism([(am + 1.5, BEL1 - 1.0), (am, BEL1), (am + 1.5, BEL1)], 'ZY', TX1 - TT, TX1)
    # 종탑 처마·피라미드 지붕
    T.box(TX0 - 0.4, TX1 + 0.4, TH2, TH2 + 0.6, TZ0 - 0.4, TZ1 + 0.4, col=False)
    COLS.append((Matrix.Translation(((TX0 + TX1) / 2, TH2 + 0.3, (TZ0 + TZ1) / 2)), (TX1 - TX0 + 0.8, 0.6, TZ1 - TZ0 + 0.8)))
    cx, cz = (TX0 + TX1) / 2, (TZ0 + TZ1) / 2
    base = [Vector((TX0 - 0.2, TH2 + 0.6, TZ0 - 0.2)), Vector((TX1 + 0.2, TH2 + 0.6, TZ0 - 0.2)),
            Vector((TX1 + 0.2, TH2 + 0.6, TZ1 + 0.2)), Vector((TX0 - 0.2, TH2 + 0.6, TZ1 + 0.2))]
    apex = Vector((cx, TH2 + 9.0, cz))
    vb = [R.bm.verts.new(B(p)) for p in base]; va = R.bm.verts.new(B(apex))
    cen = (sum((v.co for v in vb), Vector()) / 4 + va.co) / 2
    for i in range(4):
        f = R.bm.faces.new([vb[i], vb[(i + 1) % 4], va])
        f.normal_update()
        if f.normal.dot(f.calc_center_median() - cen) < 0:
            f.normal_flip()
        for lp in f.loops:
            c = lp.vert.co; lp[R.uv].uv = ((c.x + c.y) / 16.0, c.z / 16.0)
    f = R.bm.faces.new(list(vb)); f.normal_update()
    if f.normal.dot(f.calc_center_median() - cen) < 0:
        f.normal_flip()
    # 층 바닥(나무) + 뚜껑 구멍, 사다리(나무 보이는 것) — 실제 오르기는 Studio 에서 투명 TrussPart
    IX0, IX1, IZ0, IZ1 = TX0 + TT, TX1 - TT, TZ0 + TT, TZ1 - TT
    for (fy, hx0, hx1, hz0, hz1) in ((15.0, IX0, IX0 + 2.2, 12.3, 14.7), (BEL0 - 0.4, IX1 - 3.3, IX1 - 1.1, IZ0, IZ0 + 2.2)):
        # 구멍을 뺀 네 조각
        W.box(IX0, IX1, fy, fy + 0.4, IZ0, hz0)
        W.box(IX0, IX1, fy, fy + 0.4, hz1, IZ1)
        if hx0 > IX0:
            W.box(IX0, hx0, fy, fy + 0.4, hz0, hz1)
        if hx1 < IX1:
            W.box(hx1, IX1, fy, fy + 0.4, hz0, hz1)
    def ladder(x, z0, y0, y1, along):
        """along='Z': 레일이 z 방향 폭. 벽에 붙은 나무 사다리 (충돌 없음)."""
        for s in (-0.8, 0.8):
            if along == 'Z':
                W.box(x - 0.15, x + 0.15, y0, y1, z0 + s - 0.12, z0 + s + 0.12, col=False)
            else:
                W.box(x + s - 0.12, x + s + 0.12, y0, y1, z0 - 0.15, z0 + 0.15, col=False)
        y = y0 + 0.8
        while y < y1 - 0.3:
            if along == 'Z':
                W.box(x - 0.1, x + 0.1, y, y + 0.18, z0 - 0.68, z0 + 0.68, col=False)
            else:
                W.box(x - 0.68, x + 0.68, y, y + 0.18, z0 - 0.1, z0 + 0.1, col=False)
            y += 1.2
    ladder(IX0 + 0.35, 13.5, 0.0, 15.4, 'Z')
    ladder(IX1 - 2.2, IZ0 + 0.35, 15.4, BEL0, 'X')
    # 종 + 종 들보
    W.box(IX0, IX1, 33.6, 34.2, cz - 0.35, cz + 0.35, col=False)
    M.cyl(Vector((cx, 31.2, cz)), 1.6, 2.2, seg=12, r2=0.9)
    M.cyl(Vector((cx, 33.4, cz)), 0.9, 0.2, seg=12, r2=0.5)
    obs = [o.finish(col) for o in (S, T, R, W, M)]
    tris = sum(sum(len(p.vertices) - 2 for p in o.data.polygons) for o in obs)
    return "chapel objects %d, tris %d, colliders %d" % (len(obs), tris, len(COLS))


def colstr():
    out = []
    for C, s in COLS:
        p = C.to_translation(); r = C.to_3x3()
        out.append("%.3f,%.3f,%.3f,%.3f,%.3f,%.3f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f" % (
            p.x, p.y, p.z, s[0], s[1], s[2], r[0][0], r[0][1], r[0][2], r[1][0], r[1][1], r[1][2], r[2][0], r[2][1], r[2][2]))
    return ";".join(out)
