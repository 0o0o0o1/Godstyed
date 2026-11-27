# 마을 place 아파트 남쪽 1층 상가 줄 (Blender, exec → build_shoprow())
# 좌표 = Roblox 모델 로컬 (원점 월드 (-451, 0.5, 302), 회전 없음). +Z = 남쪽(큰길), -Z = 북쪽(아파트·뒤 계단).
# 맵의 상가 건물 S1~S4 와 같은 재질(Studio 에서 SA 복사):
#   SR_gwall = 1층 벽 콘크리트 SA 125301297105006 (UV 9)    SR_trim  = 테두리 SA 115364150156490 (UV 10)
#   SR_floor = 바닥 SA 107024354157527 (UV 9)                 SR_roof  = 지붕 콘크리트 SA 125301297105006 (UV 9)
#   SR_metal = 구호텐트 철물 SA 80247272746742 (UV 7)          SR_canvas = 구호텐트 천 SA 138422372252634 (UV 3)
#   SR_glass = Glass, SR_wood = WoodPlanks, SR_signA/B/C = 바랜 간판 색
# 면 방향은 solid() 에서 직접 바깥으로 감음 (recalc 금지 — 성당 장미창 깜빡임 원인이었음).
import bpy, bmesh, math
from mathutils import Vector, Matrix

UVS = {"SR_gwall": 9.0, "SR_trim": 10.0, "SR_floor": 9.0, "SR_roof": 9.0, "SR_metal": 7.0, "SR_canvas": 3.0,
       "SR_glass": 4.0, "SR_wood": 4.0, "SR_signA": 4.0, "SR_signB": 4.0, "SR_signC": 4.0}
RGB = {"SR_gwall": (0.6, 0.6, 0.58), "SR_trim": (0.75, 0.74, 0.72), "SR_floor": (0.4, 0.4, 0.4), "SR_roof": (0.45, 0.45, 0.44),
       "SR_metal": (0.25, 0.25, 0.26), "SR_canvas": (0.35, 0.3, 0.2), "SR_glass": (0.1, 0.12, 0.13), "SR_wood": (0.3, 0.2, 0.12),
       "SR_signA": (0.45, 0.12, 0.1), "SR_signB": (0.12, 0.2, 0.35), "SR_signC": (0.6, 0.55, 0.4)}
COLS = []


def B(p):
    return Vector((-p.x, p.z, p.y))


class Obj:
    def __init__(self, name):
        self.name = name; self.s = UVS[name]
        self.bm = bmesh.new(); self.uv = self.bm.loops.layers.uv.new("UVMap")

    def poly(self, pts):
        v = [self.bm.verts.new(B(p)) for p in pts]
        f = self.bm.faces.new(v)
        f.normal_update(); n = f.normal
        ax = max(range(3), key=lambda i: abs(n[i]))
        for lp in f.loops:
            c = lp.vert.co
            uv = (c.y, c.z) if ax == 0 else ((c.x, c.z) if ax == 1 else (c.x, c.y))
            lp[self.uv].uv = (uv[0] / self.s, uv[1] / self.s)

    def solid(self, bot, top):
        n = len(bot)
        bb = [B(p) for p in bot]; tb = [B(p) for p in top]
        e = tb[0] - bb[0]
        nw = Vector((0, 0, 0))
        for i in range(n):
            a, c = bb[i], bb[(i + 1) % n]
            nw += Vector(((a.y - c.y) * (a.z + c.z), (a.z - c.z) * (a.x + c.x), (a.x - c.x) * (a.y + c.y)))
        if nw.dot(e) < 0:
            bot = list(reversed(bot)); top = list(reversed(top))
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

    def prism_xy(self, pts2, z0, z1):
        self.solid([Vector((u, v, z0)) for u, v in pts2], [Vector((u, v, z1)) for u, v in pts2])

    def finish(self, col):
        if len(self.bm.faces) == 0:
            self.bm.free(); return None
        me = bpy.data.meshes.new(self.name); self.bm.to_mesh(me); self.bm.free()
        ob = bpy.data.objects.new(self.name, me); col.objects.link(ob)
        m = bpy.data.materials.get("M_" + self.name) or bpy.data.materials.new("M_" + self.name)
        c = RGB[self.name]; m.diffuse_color = (c[0], c[1], c[2], 1)
        ob.data.materials.append(m)
        return ob


def rot(axis, deg, pivot):
    pv = Vector(pivot)
    return Matrix.Translation(pv) @ Matrix.Rotation(math.radians(deg), 4, axis) @ Matrix.Translation(-pv)


def build_shoprow():
    COLS.clear()
    col = bpy.data.collections.get("ShopRow")
    if col is None:
        col = bpy.data.collections.new("ShopRow"); bpy.context.scene.collection.children.link(col)
    for o in list(col.objects):
        bpy.data.objects.remove(o, do_unlink=True)
    O = {k: Obj(k) for k in UVS}
    G, T, F, R, M, C, GL, W = (O[k] for k in ("SR_gwall", "SR_trim", "SR_floor", "SR_roof", "SR_metal", "SR_canvas", "SR_glass", "SR_wood"))
    XW, ZB, ZF, H = 72.0, -20.0, 20.0, 16.0
    SHOPS = [(-72.0, -36.0, "open", "SR_signA"), (-36.0, 0.0, "shut", "SR_signB"), (0.0, 36.0, "open", "SR_signC"), (36.0, 72.0, "shut", "SR_signA")]
    # ---- 바닥·벽 ----
    F.box(-XW + 1, XW - 1, 0.0, 0.4, ZB + 1, ZF - 1)
    G.box(-XW, -XW + 1, 0.0, H, ZB + 1, ZF - 1); G.box(XW - 1, XW, 0.0, H, ZB + 1, ZF - 1)
    doors = [(-54.0, 4.0), (18.0, 4.0)]                    # 뒷문 (가운데 x, 폭)
    xs = [-XW]
    for dx, dw in doors:
        xs += [dx - dw / 2, dx + dw / 2]
    xs.append(XW)
    for i in range(0, len(xs), 2):
        G.box(xs[i], xs[i + 1], 0.0, H, ZB, ZB + 1)
    for dx, dw in doors:
        G.box(dx - dw / 2, dx + dw / 2, 8.5, H, ZB, ZB + 1)
        M.box(dx - dw / 2, dx + dw / 2, 0.4, 8.5, ZB - 0.15, ZB, col=True)       # 닫힌 철문 (벽 바깥에 붙음)
    for xb in (-36.0, 0.0, 36.0):
        G.box(xb - 0.3, xb + 0.3, 0.4, H, ZB + 1, ZF - 1)                         # 칸막이 벽
    # ---- 지붕·난간벽 ----
    R.box(-XW, XW, H, H + 0.8, ZB, ZF)
    T.box(-XW, XW, H, H + 0.8, ZF, ZF + 1.0)                                     # 앞 처마 띠
    T.box(-XW, XW, H + 0.8, H + 2.6, ZF - 1.0, ZF)                               # 앞 난간벽
    T.box(-XW, 42.0, H + 0.8, H + 2.6, ZB, ZB + 1.0); T.box(46.0, XW, H + 0.8, H + 2.6, ZB, ZB + 1.0)   # 뒤 (계단 쪽 틈)
    T.box(-XW, -XW + 1.0, H + 0.8, H + 2.6, ZB + 1.0, ZF - 1.0); T.box(XW - 1.0, XW, H + 0.8, H + 2.6, ZB + 1.0, ZF - 1.0)
    for x in (-40.0, 10.0):                                                       # 지붕 실외기
        M.box(x - 2.5, x + 2.5, H + 0.8, H + 3.8, -6.0, -2.5)
    M.box(-20.6, -19.4, H + 0.8, H + 3.0, 8.0, 9.2)                               # 환기구
    # ---- 앞면: 기둥·간판띠·가게별 ----
    for xb in (-XW, -36.0, 0.0, 36.0, XW):
        a, b = max(xb - 1.0, -XW), min(xb + 1.0, XW)
        T.box(a, b, 0.0, H, ZF, ZF + 1.0)
    for (a, b, kind, sign) in SHOPS:
        a1, b1 = a + 1.0, b - 1.0
        G.box(a1, b1, 11.0, H, ZF - 1.0, ZF)                                      # 간판띠(벽)
        S = O[sign]
        if sign == "SR_signA" and a > 0:                                          # 마지막 가게 간판은 떨어져 셔터에 기댐
            fall = rot('X', 58, (0, 0.0, ZF + 2.25))      # 바닥 쪽은 길에, 위 끝은 셔터에 닿게 기댐
            S.box(a + 4.0, b - 4.0, 0.0, 0.3, ZF - 0.75, ZF + 2.25, M=fall)
        else:
            S.box(a + 3.0, b - 3.0, 12.0, 15.0, ZF, ZF + 0.3)
        if kind == "open":
            dx0, dx1 = a1 + 3.0, a1 + 9.0                                         # 문 자리 (문짝 없음)
            G.box(a1, dx0, 0.0, 2.5, ZF - 1.0, ZF); G.box(dx1, b1, 0.0, 2.5, ZF - 1.0, ZF)
            T.box(dx0, dx0 + 0.5, 0.0, 11.0, ZF - 0.8, ZF - 0.2, col=False)       # 문 옆 기둥(문 구멍 안쪽)
            T.box(dx1 - 0.5, dx1, 0.0, 11.0, ZF - 0.8, ZF - 0.2, col=False)
            mm = (dx1 + b1) / 2
            T.box(mm - 0.25, mm + 0.25, 2.5, 11.0, ZF - 0.8, ZF - 0.2, col=False)
            T.box(dx0 + 0.5, dx1 - 0.5, 9.0, 9.5, ZF - 0.8, ZF - 0.2, col=False)  # 문 위 가로대
            # 깨진 유리 조각 (모서리에 남음)
            for (x0, x1, y0, y1) in ((dx1, mm - 0.25, 2.5, 11.0), (mm + 0.25, b1, 2.5, 11.0)):
                GL.prism_xy([(x0, y1), (x0 + 2.2, y1), (x0, y1 - 3.1)], ZF - 0.55, ZF - 0.45)
                GL.prism_xy([(x1, y0), (x1, y0 + 2.4), (x1 - 1.6, y0)], ZF - 0.55, ZF - 0.45)
            # 실내: 계산대, 뒷벽 선반 2개, 상자
            W.box(b1 - 14.0, b1 - 3.0, 0.4, 3.8, 0.0, 2.2, M=rot("Y", 8 if a == 0.0 else 0, (b1 - 8.5, 0, 1.1)))
            for (sx0, sx1) in ((a1 + 2.0, a1 + 12.0), (a1 + 14.0, a1 + 24.0)):
                W.box(sx0, sx0 + 0.4, 0.4, 8.0, ZB + 1.3, ZB + 3.3); W.box(sx1 - 0.4, sx1, 0.4, 8.0, ZB + 1.3, ZB + 3.3)
                for yb in (0.4, 2.8, 5.2, 7.6):
                    W.box(sx0 + 0.4, sx1 - 0.4, yb, yb + 0.25, ZB + 1.3, ZB + 3.3, col=(yb < 1))
            for (cx, cz, s) in ((a1 + 6.0, 6.0, 1.6), (a1 + 8.2, 4.5, 1.2), (a1 + 20.0, -8.0, 1.4)):
                W.box(cx - s / 2, cx + s / 2, 0.4, 0.4 + s, cz - s / 2, cz + s / 2, col=False)
            if a == 0.0:   # 3번째 가게(x 0..36): 찢긴 차양 + 받침 팔
                for (x0, x1, ln) in ((a1 + 1.0, a1 + 11.0, 5.0), (a1 + 11.0, a1 + 22.0, 3.2), (a1 + 22.0, b1 - 1.0, 4.4)):
                    C.box(x0, x1, 0.0, 0.15, 0.0, ln, M=Matrix.Translation((0, 11.0, ZF + 0.31)) @ Matrix.Rotation(math.radians(22), 4, 'X'), col=False)
                for xx in (a1 + 1.5, b1 - 1.5):
                    M.box(xx - 0.12, xx + 0.12, -0.14, 0.0, 0.0, 3.0, M=Matrix.Translation((0, 11.0, ZF + 0.31)) @ Matrix.Rotation(math.radians(22), 4, 'X'), col=False)
        else:
            # 말림 셔터: 판 + 가로 골(앞에 붙은 얇은 띠) + 셔터 상자 + 아래 막대
            M.box(a1, b1, 0.0, 11.0, ZF + 0.2, ZF + 0.5)
            y = 1.2
            while y < 10.6:
                M.box(a1, b1, y, y + 0.12, ZF + 0.5, ZF + 0.58, col=False)
                y += 1.2
            M.box(a1, b1, 11.0, 12.0, ZF, ZF + 1.2)
            M.box(a1, b1, 0.0, 0.5, ZF + 0.5, ZF + 0.7, col=False)
    # ---- 뒤 철제 계단 (동쪽 끝, 바깥) ----
    nst, rise, run = 21, 0.8, 1.15
    z0, z1 = ZB - 3.8, ZB - 0.5
    x_top = XW - 2.0 - nst * run                       # 꼭대기 계단 끝 x
    for k in range(nst):
        xa = XW - 2.0 - (k + 1) * run; xb = xa + run
        yt = (k + 1) * rise
        M.box(xa, xb, yt - 0.15, yt, z0 + 0.2, z1 - 0.2)
    # 옆판(stringer): 디딤판 끝 아래 양쪽, 디딤판 선보다 0.15 아래부터 0.9 두께 (디딤판과 안 겹치게 z 는 바깥 0.2)
    for (za, zb) in ((z0, z0 + 0.2), (z1 - 0.2, z1)):
        p0 = (XW - 2.0, 0.0); p1 = (x_top, nst * rise - 0.15)
        M.prism_xy([p0, p1, (p1[0], p1[1] - 0.9), (p0[0], max(p0[1] - 0.9, 0.0))], za, zb)
    # 난간 (바깥 쪽 z0)
    for k in range(0, nst + 1, 4):
        xp = XW - 2.0 - k * run; yb = k * rise
        M.box(xp - 0.12, xp + 0.12, yb, yb + 3.4 - 0.12 * rise / run, z0 - 0.24, z0, col=False)   # 위 끝은 경사 난간 아래선에 맞춤
    p0 = Vector((XW - 2.0, 3.4)); p1 = Vector((x_top, nst * rise + 3.4))
    dd = (p1 - p0); nn = Vector((dd.y, -dd.x)).normalized() * 0.2   # 위쪽 법선 (기둥 위에 얹힘)
    M.prism_xy([(p0.x, p0.y), (p1.x, p1.y), (p1.x + nn.x, p1.y + nn.y), (p0.x + nn.x, p0.y + nn.y)], z0 - 0.24, z0)
    # 꼭대기 발판 → 지붕
    M.box(42.0, x_top, H + 0.65, H + 0.8, z0 + 0.2, ZB)
    for xp in (42.2, x_top - 0.4):
        M.box(xp, xp + 0.25, 0.0, H + 0.65, z0 + 0.2, z0 + 0.45, col=False)
    obs = [o.finish(col) for o in O.values()]
    obs = [o for o in obs if o]
    tris = sum(sum(len(p.vertices) - 2 for p in o.data.polygons) for o in obs)
    return "shoprow objects %d, tris %d, colliders %d" % (len(obs), tris, len(COLS))


def colstr():
    out = []
    for Cm, s in COLS:
        p = Cm.to_translation(); r = Cm.to_3x3()
        out.append(",".join("%g" % round(v, 4) for v in (p.x, p.y, p.z, s[0], s[1], s[2], r[0][0], r[0][1], r[0][2], r[1][0], r[1][1], r[1][2], r[2][0], r[2][1], r[2][2])))
    return ";".join(out)
