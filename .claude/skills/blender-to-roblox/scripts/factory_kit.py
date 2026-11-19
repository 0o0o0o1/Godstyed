# Factory kit for Blender MCP SAFE MODE (2026-11-19).
# Paste this whole file into execute_blender_code once per Blender session. It registers every helper as an
# attribute of the stdlib module `string` (string.pb_*), which survives between MCP calls; later scripts call
# string.pb_pipe(...), string.pb_truss(...) etc. (safe mode forbids lambdas, walrus, driver_namespace and calling
# a function through a variable, but allows calling attributes of imported modules).
# All geometry is written in Roblox WORLD coordinates (X, Y up, Z); TB() maps to Blender for the common frame
# Blender (x,y,z) -> world (-881 - x, 0.5 + z, 881 + y). Mesh names: <Prefix><Part>__<PaletteKey>__NoCollide[__TEX].
# Colliders are collected in string.pb_S['col'] and printed by string.pb_colstr():
#   'C ax ay az bx by bz r' cylinder,  '<B|T|W> cx cy cz ux uy uz vx vy vz hu hv hw' oriented box / truss / wedge.
import bpy, bmesh, math, string
from mathutils import Vector

FX, FZ, FY = -881.0, 881.0, 0.5
def V(x, y, z): return Vector((x, y, z))
def TB(p): return Vector((FX - p.x, p.z - FZ, p.y - FY))
def P(p, y): return Vector((p.x, y, p.z))
TILE = {'FurnaceRust': 16, 'StoveGrey': 16, 'SteelOxide': 8, 'RailYellow': 8, 'CoolConcrete': 16,
        'RoofZinc': (24, 30), 'SidingTeal': (24, 30), 'ShutterOrange': (24, 30)}
S = {'bms': {}, 'col': []}

def bm_of(name):
    d = S['bms']
    if name not in d:
        bm = bmesh.new(); bm.loops.layers.uv.new('UVMap'); bm.faces.layers.int.new('cyl')
        d[name] = bm
    return d[name]

def _face(bm, vs, cyl=0, uvs=None):
    try:
        f = bm.faces.new(vs)
    except ValueError:
        return None
    f[bm.faces.layers.int['cyl']] = cyl
    if uvs:
        uvl = bm.loops.layers.uv['UVMap']
        for l, uv in zip(f.loops, uvs):
            l[uvl].uv = uv
    return f

def obox(name, c, u, v, w, hu, hv, hw):
    bm = bm_of(name); vs = []
    for sx in (-1, 1):
        for sy in (-1, 1):
            for sz in (-1, 1):
                vs.append(bm.verts.new(TB(c + u * (sx * hu) + v * (sy * hv) + w * (sz * hw))))
    for f in ((0, 1, 3, 2), (4, 6, 7, 5), (0, 4, 5, 1), (2, 3, 7, 6), (0, 2, 6, 4), (1, 5, 7, 3)):
        _face(bm, [vs[i] for i in f])

def frame(d, up=None):
    d = d.normalized(); up = up if up is not None else V(0, 1, 0)
    if abs(d.dot(up)) > 0.99: up = V(1, 0, 0)
    s = up.cross(d).normalized(); t = d.cross(s).normalized()
    return d, s, t

def beam(name, a, b, w, h, up=None, ext=0.0):
    d = b - a; L = d.length
    if L < 1e-4: return
    u, s, t = frame(d, up)
    obox(name, (a + b) / 2, u, s, t, L / 2 + ext, w / 2, h / 2)

def ibeam(name, a, b, depth, bf, up=None, tw=0.14, tf=0.14):
    d = b - a; L = d.length; u, s, t = frame(d, up); c = (a + b) / 2
    obox(name, c, u, s, t, L / 2, tw / 2, depth / 2 - tf)
    obox(name, c + t * (depth / 2 - tf / 2), u, s, t, L / 2, bf / 2, tf / 2)
    obox(name, c - t * (depth / 2 - tf / 2), u, s, t, L / 2, bf / 2, tf / 2)

def slab(name, q, y0, y1):
    bm = bm_of(name)
    lo = [bm.verts.new(TB(V(p.x, y0, p.z))) for p in q]
    hi = [bm.verts.new(TB(V(p.x, y1, p.z))) for p in q]
    n = len(q)
    _face(bm, list(reversed(lo))); _face(bm, hi)
    for i in range(n):
        j = (i + 1) % n
        _face(bm, [lo[i], lo[j], hi[j], hi[i]])

def slab3(name, top, t):
    """polygon with per-vertex heights (world points), thickness t downward"""
    bm = bm_of(name)
    hi = [bm.verts.new(TB(p)) for p in top]
    lo = [bm.verts.new(TB(p - V(0, t, 0))) for p in top]
    n = len(top)
    _face(bm, hi); _face(bm, list(reversed(lo)))
    for i in range(n):
        j = (i + 1) % n
        _face(bm, [lo[i], lo[j], hi[j], hi[i]])

def prism(name, prof, a, b, lat):
    """extrude 2D profile [(lateral, up)] from a to b; lat = lateral unit"""
    bm = bm_of(name)
    A = [bm.verts.new(TB(a + lat * q[0] + V(0, q[1], 0))) for q in prof]
    B = [bm.verts.new(TB(b + lat * q[0] + V(0, q[1], 0))) for q in prof]
    n = len(prof)
    _face(bm, list(reversed(A))); _face(bm, B)
    for i in range(n):
        j = (i + 1) % n
        _face(bm, [A[i], A[j], B[j], B[i]])

def tile_of(name):
    return TILE.get(name.split('__')[1], 8)

def pipe(name, pts, r, seg=16, R=None, cap0=True, cap1=True, jag0=0.0, jag1=0.0, collide=True):
    """tube along a polyline with bent elbows (bend radius R, default 2r); cylindrical UVs"""
    rings = []
    for i in range(len(pts)):
        if i == 0:
            rings.append((pts[0], (pts[1] - pts[0]).normalized())); continue
        if i == len(pts) - 1:
            rings.append((pts[-1], (pts[-1] - pts[-2]).normalized())); continue
        d1 = (pts[i] - pts[i - 1]).normalized(); d2 = (pts[i + 1] - pts[i]).normalized()
        th = d1.angle(d2)
        if th < 1e-3: continue
        Rr = R if R else 2 * r
        tt = Rr * math.tan(th / 2)
        A = pts[i] - d1 * tt
        nr = (d2 - d1 * d1.dot(d2)).normalized()
        C = A + nr * Rr
        n = max(2, int(math.degrees(th) / 15) + 1)
        for k in range(n + 1):
            ph = th * k / n
            rings.append((C - nr * (Rr * math.cos(ph)) + d1 * (Rr * math.sin(ph)), (d1 * math.cos(ph) + nr * math.sin(ph)).normalized()))
    bm = bm_of(name); T = tile_of(name)
    if isinstance(T, tuple): T = T[0]
    ref = None; dist = 0.0; prevc = None; rv = []
    for idx in range(len(rings)):
        c, t = rings[idx]
        if ref is None:
            ref = V(0, 1, 0) if abs(t.y) < 0.9 else V(1, 0, 0)
        ref = (ref - t * ref.dot(t)).normalized(); b2 = t.cross(ref)
        if prevc is not None: dist += (c - prevc).length
        prevc = c; vs = []
        for k in range(seg):
            a = 2 * math.pi * k / seg
            p = c + (ref * math.cos(a) + b2 * math.sin(a)) * r
            j = jag0 if idx == 0 else (jag1 if idx == len(rings) - 1 else 0)
            if j: p = p + t * (j * ((((k * 7919 + idx * 31) % 13) / 12.0) - 0.5) * 2)
            vs.append(bm.verts.new(TB(p)))
        rv.append((vs, dist))
    circ = 2 * math.pi * r
    for i in range(len(rv) - 1):
        A_, da = rv[i]; B_, db = rv[i + 1]
        for k in range(seg):
            k2 = (k + 1) % seg; u0 = circ * k / seg / T; u1 = circ * (k + 1) / seg / T
            _face(bm, [A_[k], A_[k2], B_[k2], B_[k]], 1, [(u0, da / T), (u1, da / T), (u1, db / T), (u0, db / T)])
    if cap0: _face(bm, list(reversed(rv[0][0])))
    if cap1: _face(bm, rv[-1][0])
    if collide:
        for i in range(len(pts) - 1):
            S['col'].append(('C', pts[i], pts[i + 1], r))

def colbox(c, u, v, hu, hv, hw, kind='B'):
    S['col'].append((kind, c, u.normalized(), v.normalized(), hu, hv, hw))

def rail(pre, a, b, y, col=True):
    """handrail (posts, top/mid rail, toe board) along a->b at platform top y"""
    Y = pre + 'Yel_Rails__RailYellow__NoCollide__TEX'
    A = V(a.x, y, a.z); B_ = V(b.x, y, b.z); L = (B_ - A).length
    n = max(1, int(math.ceil(L / 2.2)))
    for i in range(n + 1):
        p = A.lerp(B_, i / n)
        beam(Y, p, p + V(0, 3.41, 0), 0.16, 0.16)
    beam(Y, A + V(0, 3.5, 0), B_ + V(0, 3.5, 0), 0.18, 0.18, ext=0.08)
    beam(Y, A + V(0, 1.8, 0), B_ + V(0, 1.8, 0), 0.12, 0.12)
    beam(Y, A + V(0, 0.15, 0), B_ + V(0, 0.15, 0), 0.06, 0.3)
    if col:
        d = (B_ - A).normalized()
        colbox((A + B_) / 2 + V(0, 1.85, 0), d, V(0, 1, 0), L / 2, 1.85, 0.15)

def ladder(pre, base, out, side, y0, y1):
    """caged ladder; base = point on the face plane, out = outward unit, side = along-face unit. Adds a 'T' collider
    (remove 'T' entries from S['col'] when the ladder must not be climbable)."""
    Y = pre + 'Yel_Ladders__RailYellow__NoCollide__TEX'
    c = base + out * 0.75
    for s in (-0.8, 0.8):
        p = c + side * s
        beam(Y, V(p.x, y0, p.z), V(p.x, y1 + 3.6, p.z), 0.18, 0.3)
    y = y0 + 0.6
    while y < y1 - 0.2:
        beam(Y, V(c.x, y, c.z) - side * 0.71, V(c.x, y, c.z) + side * 0.71, 0.12, 0.12)
        y += 1.0
    yb = y0 + 3.0
    while yb < y1:
        for s in (-0.8, 0.8):
            p = c + side * s
            beam(Y, V(p.x, yb, p.z) - out * 0.75, V(p.x, yb, p.z) - out * 0.15, 0.12, 0.2)
        yb += 5.0
    hc = c + out * 0.8; hoops = []
    yh = y0 + 7.0
    while yh <= y1 + 3.0:
        chain = [V((c - side * 0.8).x, yh, (c - side * 0.8).z)]
        for k in range(7):
            a = math.pi * k / 6
            q = hc - side * (math.cos(a) * 1.0) + out * (math.sin(a) * 1.05)
            chain.append(V(q.x, yh, q.z))
        chain.append(V((c + side * 0.8).x, yh, (c + side * 0.8).z))
        for i in range(len(chain) - 1):
            beam(Y, chain[i], chain[i + 1], 0.08, 0.2)
        hoops.append(chain)
        yh += 2.4
    if len(hoops) > 1:
        for k in (2, 4, 6):
            beam(Y, hoops[0][k], hoops[-1][k], 0.1, 0.1)
    colbox(V(c.x, (y0 + y1 + 1.0) / 2, c.z), side, V(0, 1, 0), 1.0, (y1 + 1.0 - y0) / 2, 0.5, 'T')

def truss(pre, L0, L1, R0, R1, deck, H, panels, walk=None, gaps=(), skipbot=(), shoes=(), noshoe=(), col=True):
    """pipe-bridge Pratt truss between chord lines L and R (XZ), deck = crossbeam top"""
    St = pre + 'Stl_Truss__SteelOxide__NoCollide__TEX'
    Gr = pre + 'Grt_Walk__DiamondPlate__NoCollide'
    Dk = pre + 'Drk_Shoes__DarkSteel__NoCollide'
    yb = deck - 0.4; yt = deck + H - 0.4
    for A, B in ((L0, L1), (R0, R1)):
        beam(St, P(A, yb), P(B, yb), 0.7, 0.8)
        beam(St, P(A, yt), P(B, yt), 0.7, 0.8)
    Ls = []; Rs = []
    for i in range(panels + 1):
        Ls.append(L0.lerp(L1, i / panels)); Rs.append(R0.lerp(R1, i / panels))
    ax = ((L1 + R1) / 2 - (L0 + R0) / 2); ax.y = 0; ax = ax.normalized()
    for i in range(panels + 1):
        for p in (Ls[i], Rs[i]):
            beam(St, P(p, deck), P(p, deck + H - 0.8), 0.45, 0.45)
        a = Ls[i]; b = Rs[i]; d = b - a; d.y = 0; dn = d.normalized()
        beam(St, P(a + dn * 0.35, deck - 0.3), P(b - dn * 0.35, deck - 0.3), 0.45, 0.6)
        beam(St, P(a + dn * 0.35, yt), P(b - dn * 0.35, yt), 0.4, 0.5)
        for k in range(len(shoes)):
            lat, r = shoes[k]
            if (i, k) in noshoe: continue
            q = a + dn * lat
            obox(Dk, P(q, deck + 0.15), ax, V(0, 1, 0), dn, 0.3, 0.15, max(0.25, r * 0.55))
    half = panels / 2.0
    for i in range(panels):
        for side in (Ls, Rs):
            if i < half: beam(St, P(side[i], deck), P(side[i + 1], deck + H - 0.8), 0.35, 0.35)
            else: beam(St, P(side[i], deck + H - 0.8), P(side[i + 1], deck), 0.35, 0.35)
        if i % 2 == 0: beam(St, P(Ls[i], yt), P(Rs[i + 1], yt), 0.3, 0.2)
        else: beam(St, P(Rs[i], yt), P(Ls[i + 1], yt), 0.3, 0.2)
        if i not in skipbot:
            if i % 2 == 0: beam(St, P(Ls[i], deck - 0.7), P(Rs[i + 1], deck - 0.7), 0.3, 0.2)
            else: beam(St, P(Rs[i], deck - 0.7), P(Ls[i + 1], deck - 0.7), 0.3, 0.2)
    segs = []
    t0 = 0.0
    for g0, g1 in sorted(gaps):
        segs.append((t0, g0)); t0 = g1
    segs.append((t0, 1.0))
    if walk:
        w0, w1 = walk
        for s0, s1 in segs:
            la = L0.lerp(L1, s0); lb = L0.lerp(L1, s1)
            dA = (R0.lerp(R1, s0) - la); dA.y = 0; dA = dA.normalized()
            dB = (R0.lerp(R1, s1) - lb); dB.y = 0; dB = dB.normalized()
            slab(Gr, [la + dA * w0, lb + dB * w0, lb + dB * w1, la + dA * w1], deck, deck + 0.15)
    if col:
        C0 = (L0 + R0) / 2; C1 = (L1 + R1) / 2
        W = (R0 - L0); W.y = 0; W = W.length
        for s0, s1 in segs:
            a = C0.lerp(C1, s0); b = C0.lerp(C1, s1)
            colbox(P((a + b) / 2, deck - 0.325), ax, V(0, 1, 0), (b - a).length / 2, 0.475, W / 2)
        for A, B in ((L0, L1), (R0, R1)):
            colbox(P((A + B) / 2, deck + 0.15 + (H - 0.15) / 2), ax, V(0, 1, 0), (B - A).length / 2, (H - 0.15) / 2, 0.25)
        colbox(P((C0 + C1) / 2, deck + H - 0.35), ax, V(0, 1, 0), (C1 - C0).length / 2, 0.35, W / 2)
    return Ls, Rs

def tower(pre, c, u, n, D, W, deck, ground, plat=(), rails=(), ladders=(), shoes=(), noface=(), col=True):
    """4-leg braced tower; u along route (depth D), n lateral (width W). plat/rails in local (a along u, b along n)."""
    St = pre + 'Stl_Towers__SteelOxide__NoCollide__TEX'
    Cc = pre + 'Con_Footings__CoolConcrete__NoCollide__TEX'
    Gr = pre + 'Grt_Walk__DiamondPlate__NoCollide'
    Dk = pre + 'Drk_Shoes__DarkSteel__NoCollide'
    Y = V(0, 1, 0)
    ca = D / 2 - 0.5; cb = W / 2 - 0.5
    corners = [(-ca, -cb), (-ca, cb), (ca, cb), (ca, -cb)]
    ytc = deck - 1.6; yg = ground + 1.05
    for a, b in corners:
        p = c + u * a + n * b
        obox(Cc, P(p, ground + 0.5), u, Y, n, 0.9, 0.55, 0.9)
        ibeam(St, P(p, yg), P(p, ytc), 1.0, 1.0, up=u)
        if col: colbox(P(p, (ground + ytc) / 2), u, Y, 0.5, (ytc - ground) / 2, 0.5)
    for i in range(4):
        a1, b1 = corners[i]; a2, b2 = corners[(i + 1) % 4]
        beam(St, P(c + u * a1 + n * b1, deck - 1.2), P(c + u * a2 + n * b2, deck - 1.2), 0.7, 0.8, ext=0.5)
    for sb in (-1, 1):
        beam(St, P(c - u * (D / 2) + n * (sb * (W / 2 - 0.35)), deck - 0.4), P(c + u * (D / 2) + n * (sb * (W / 2 - 0.35)), deck - 0.4), 0.7, 0.8)
    for sa in (-1, 1):
        beam(St, P(c + u * (sa * (D / 2 - 0.5)) - n * (W / 2 - 0.7), deck - 0.3), P(c + u * (sa * (D / 2 - 0.5)) + n * (W / 2 - 0.7), deck - 0.3), 0.45, 0.6)
        for b, r in shoes:
            obox(Dk, P(c + u * (sa * (D / 2 - 0.5)) + n * b, deck + 0.15), n, Y, u, max(0.25, r * 0.55), 0.15, 0.3)
    hh = ytc - yg
    nseg = max(1, int(round(hh / 8.0)))
    lv = [yg + hh * k / nseg for k in range(nseg + 1)]
    for k in range(1, nseg):
        for i in range(4):
            a1, b1 = corners[i]; a2, b2 = corners[(i + 1) % 4]
            beam(St, P(c + u * a1 + n * b1, lv[k]), P(c + u * a2 + n * b2, lv[k]), 0.45, 0.45)
    for i in range(4):
        if i in noface: continue
        a1, b1 = corners[i]; a2, b2 = corners[(i + 1) % 4]
        pA = c + u * a1 + n * b1; pB = c + u * a2 + n * b2
        for k in range(nseg):
            beam(St, P(pA, lv[k] + 0.3), P(pB, lv[k + 1] - 0.3), 0.28, 0.14)
            beam(St, P(pB, lv[k] + 0.3), P(pA, lv[k + 1] - 0.3), 0.28, 0.14)
    for a0, a1, b0, b1 in plat:
        q = [c + u * a0 + n * b0, c + u * a1 + n * b0, c + u * a1 + n * b1, c + u * a0 + n * b1]
        slab(Gr, q, deck, deck + 0.15)
        if col: colbox(P(c + u * ((a0 + a1) / 2) + n * ((b0 + b1) / 2), deck - 0.3), u, Y, abs(a1 - a0) / 2, 0.45, abs(b1 - b0) / 2)
    for (a0, b0), (a1, b1) in rails:
        rail(pre, c + u * a0 + n * b0, c + u * a1 + n * b1, deck + 0.15)
    for kind, sgn, pos in ladders:
        if kind == 'u':
            base = c + u * (sgn * D / 2) + n * pos; out = u * sgn; side = n
        else:
            base = c + n * (sgn * W / 2) + u * pos; out = n * sgn; side = u
        ladder(pre, base, out, side, ground, deck + 0.15)

def tbent(pre, c, along, lat, ground, top, half=1.6, col=True):
    """single-column T support; top = cap beam top"""
    St = pre + 'Stl_Towers__SteelOxide__NoCollide__TEX'
    Cc = pre + 'Con_Footings__CoolConcrete__NoCollide__TEX'
    Y = V(0, 1, 0)
    obox(Cc, P(c, ground + 0.5), along, Y, lat, 0.8, 0.55, 0.8)
    ibeam(St, P(c, ground + 1.05), P(c, top - 0.6), 0.8, 0.8, up=along)
    beam(St, P(c - lat * half, top - 0.3), P(c + lat * half, top - 0.3), 0.6, 0.6, up=Y)
    for s in (-1, 1):
        beam(St, P(c + lat * (s * 0.4), top - 2.6), P(c + lat * (s * (half - 0.3)), top - 0.6), 0.25, 0.14)
    if col: colbox(P(c, (ground + top) / 2), along, Y, 0.4, (top - ground) / 2, 0.4)

def bent2(pre, c, along, lat, ground, top, halfw, col=True):
    """two-leg braced trestle; top = cap beam top"""
    St = pre + 'Stl_Bents__SteelOxide__NoCollide__TEX'
    Cc = pre + 'Con_Footings__CoolConcrete__NoCollide__TEX'
    Y = V(0, 1, 0)
    yt = top - 0.6; yg = ground + 1.05
    legs = [c - lat * halfw, c + lat * halfw]
    for p in legs:
        obox(Cc, P(p, ground + 0.5), along, Y, lat, 1.0, 0.55, 1.0)
        ibeam(St, P(p, yg), P(p, yt), 0.9, 0.9, up=along)
        if col: colbox(P(p, (ground + yt) / 2), along, Y, 0.45, (yt - ground) / 2, 0.45)
    beam(St, P(c - lat * (halfw + 0.6), top - 0.3), P(c + lat * (halfw + 0.6), top - 0.3), 0.7, 0.6, up=Y)
    hh = yt - yg; ns = max(1, int(round(hh / 8.0)))
    lv = [yg + hh * k / ns for k in range(ns + 1)]
    for k in range(1, ns):
        beam(St, P(legs[0], lv[k]), P(legs[1], lv[k]), 0.45, 0.45)
    for k in range(ns):
        beam(St, P(legs[0], lv[k] + 0.3), P(legs[1], lv[k + 1] - 0.3), 0.28, 0.14, up=along)
        beam(St, P(legs[1], lv[k] + 0.3), P(legs[0], lv[k + 1] - 0.3), 0.28, 0.14, up=along)

def shoe(pre, c, along, lat, y, r):
    obox(pre + 'Drk_Shoes__DarkSteel__NoCollide', P(c, y + 0.15), along, V(0, 1, 0), lat, 0.3, 0.15, max(0.25, r * 0.55))

def valve(pre, c, axis, r, up=None):
    """gate valve on a pipe axis with a hand wheel"""
    Dk = pre + 'Drk_Valves__DarkSteel__NoCollide'
    Ye = pre + 'Yel_Wheels__RailYellow__NoCollide__TEX'
    axis = axis.normalized()
    if up is None:
        upv = V(0, 1, 0) if abs(axis.y) < 0.9 else V(1, 0, 0)
    else:
        upv = up
    upv = (upv - axis * upv.dot(axis)).normalized()
    for s in (-1, 1):
        pipe(Dk, [c + axis * (s * 0.9 * r), c + axis * (s * (0.9 * r + 0.25))], r * 1.45, seg=12, collide=False)
    side = axis.cross(upv)
    obox(Dk, c, axis, upv, side, 0.9 * r, 1.25 * r, 1.05 * r)
    top = c + upv * (1.25 * r)
    pipe(Dk, [top, top + upv * (1.4 * r + 0.6)], max(0.22, r * 0.45), seg=10, collide=False)
    stem_top = top + upv * (1.4 * r + 1.4)
    pipe(Dk, [top + upv * (1.4 * r + 0.6), stem_top], 0.1, seg=6, collide=False)
    wr = max(0.7, r * 1.1); wc = stem_top - upv * 0.15
    pts = []
    for k in range(10):
        a = 2 * math.pi * k / 10
        pts.append(wc + (axis * math.cos(a) + side * math.sin(a)) * wr)
    for k in range(10):
        beam(Ye, pts[k], pts[(k + 1) % 10], 0.12, 0.12, up=upv)
    for k in (0, 5):
        beam(Ye, wc, pts[k], 0.09, 0.09, up=upv)

def collar(pre, c, ground, r):
    obox(pre + 'Con_Footings__CoolConcrete__NoCollide__TEX', V(c.x, ground + 0.2, c.z), V(1, 0, 0), V(0, 1, 0), V(0, 0, 1), r + 0.6, 0.25, r + 0.6)

def gallery2(pre, C0, d, Ls_dir, HW, sL0, sR0, sL1, sR1, yfun, H, panels, wallskip=(), roofskip=(), beltgap=None, col=True):
    """covered conveyor gallery along axis C0 + d*s; Ls_dir = unit toward the walkway side; side lines may end at
    different s (mitred ends); yfun = (s0, y0, s1, y1) floor height along the axis; beltgap = (s0, s1) torn belt."""
    St = pre + 'Stl_Truss__SteelOxide__NoCollide__TEX'
    Gr = pre + 'Grt_Walk__DiamondPlate__NoCollide'
    Wl = pre + 'Sid_Walls__RoofZinc__NoCollide__TEX'
    Rf = pre + 'Rof_Roof__RoofZinc__NoCollide__TEX'
    Dk = pre + 'Drk_Belt__DarkSteel__NoCollide'
    Rb = pre + 'Rub_Belt__Rubber__NoCollide'
    Co = pre + 'Coal_Load__Coke__NoCollide'
    up = V(0, 1, 0)
    pl = -Ls_dir
    s0_, y0_, s1_, y1_ = yfun
    def at(p):
        s = (p - C0).dot(d); return P(p, y0_ + (y1_ - y0_) * (s - s0_) / (s1_ - s0_))
    def Lp(s): return at(C0 + Ls_dir * HW + d * s)
    def Rp(s): return at(C0 - Ls_dir * HW + d * s)
    sa = max(sL0, sR0); sb = min(sL1, sR1)
    Ls = []; Rs = []
    for k in range(panels + 1):
        s = sa + (sb - sa) * k / panels
        Ls.append(Lp(s)); Rs.append(Rp(s))
    Ls[0] = Lp(sL0); Rs[0] = Rp(sR0); Ls[-1] = Lp(sL1); Rs[-1] = Rp(sR1)
    W = 2 * HW
    for side in (Ls, Rs):
        beam(St, side[0] - up * 0.4, side[-1] - up * 0.4, 0.7, 0.8)
        beam(St, side[0] + up * (H - 0.4), side[-1] + up * (H - 0.4), 0.7, 0.8)
    half = panels / 2.0
    fb = 0.66
    for i in range(panels + 1):
        a = Ls[i]; b = Rs[i]
        e = b - a; e.y = 0; en = e.normalized()
        for p in (a, b):
            beam(St, p, p + up * (H - 0.8), 0.45, 0.45)
        beam(St, a + en * 0.35 - up * 0.3, b - en * 0.35 - up * 0.3, 0.45, 0.6)
        beam(St, a + en * 0.35 + up * (H - 0.4), b - en * 0.35 + up * (H - 0.4), 0.4, 0.5)
        mid = (a + b) / 2
        beam(St, a - pl * 0.35 + up * H, mid + up * (H + 0.85), 0.25, 0.3)
        beam(St, b + pl * 0.35 + up * H, mid + up * (H + 0.85), 0.25, 0.3)
        if 0 < i < panels:
            for so in (-1.6, 1.6):
                q = at(a + pl * (W * fb + so))
                beam(Dk, q, q + up * 0.85, 0.2, 0.2)
    for i in range(panels):
        for side in (Ls, Rs):
            if i < half: beam(St, side[i], side[i + 1] + up * (H - 0.8), 0.35, 0.35)
            else: beam(St, side[i] + up * (H - 0.8), side[i + 1], 0.35, 0.35)
        if i % 2 == 0: beam(St, Ls[i] - up * 0.7, Rs[i + 1] - up * 0.7, 0.3, 0.2)
        else: beam(St, Rs[i] - up * 0.7, Ls[i + 1] - up * 0.7, 0.3, 0.2)
    def edge_pt(A_, B_, w):
        return at(A_ + (B_ - A_) * (w / W))
    slab3(Gr, [edge_pt(Ls[0], Rs[0], 0.35) + up * 0.15, edge_pt(Ls[-1], Rs[-1], 0.35) + up * 0.15,
               edge_pt(Ls[-1], Rs[-1], 2.75) + up * 0.15, edge_pt(Ls[0], Rs[0], 2.75) + up * 0.15], 0.15)
    A = edge_pt(Ls[0], Rs[0], W * fb); B = edge_pt(Ls[-1], Rs[-1], W * fb)
    A = at(A + d * 0.9); B = at(B - d * 0.9)
    for so in (-1.6, 1.6):
        beam(Dk, A + pl * so + up * 0.95, B + pl * so + up * 0.95, 0.25, 0.25)
    segs = [(0.0, 1.0)]
    if beltgap:
        L = (B - A).length; sA = (A - C0).dot(d)
        segs = [(0.0, (beltgap[0] - sA) / L), ((beltgap[1] - sA) / L, 1.0)]
    nId = int((B - A).length / 4.0)
    for k in range(nId + 1):
        c = A.lerp(B, k / nId)
        for (u0, h0), (u1, h1) in (((-1.45, 1.55), (-0.55, 1.1)), ((-0.55, 1.1), (0.55, 1.1)), ((0.55, 1.1), (1.45, 1.55))):
            pipe(Dk, [c + pl * u0 + up * h0, c + pl * u1 + up * h1], 0.16, seg=6, collide=False)
        pipe(Dk, [c + pl * (-1.45) + up * 0.45, c + pl * 1.45 + up * 0.45], 0.14, seg=6, collide=False)
    prof = [(-1.5, 1.73), (-0.6, 1.28), (0.6, 1.28), (1.5, 1.73), (1.5, 1.83), (0.6, 1.38), (-0.6, 1.38), (-1.5, 1.83)]
    load = [(-0.6, 1.38), (0.6, 1.38), (0.3, 1.78), (-0.3, 1.78)]
    for t0, t1 in segs:
        a = A.lerp(B, t0); b = A.lerp(B, t1)
        prism(Rb, prof, a, b, pl)
        if t1 - t0 > 0.05: prism(Co, load, a.lerp(b, 0.02), b.lerp(a, 0.02), pl)
        prism(Rb, [(-1.4, 0.6), (1.4, 0.6), (1.4, 0.66), (-1.4, 0.66)], a, b, pl)
    bmw = bm_of(Wl)
    for i in range(panels):
        for si in (0, 1):
            side = Ls if si == 0 else Rs; sg = -1 if si == 0 else 1
            if (i, si) in wallskip: continue
            o = pl * (0.48 * sg)
            p0 = side[i] + o; p1 = side[i + 1] + o
            q = [p0 - up * 0.85, p1 - up * 0.85, p1 + up * (H + 0.02), p0 + up * (H + 0.02)]
            nrm = pl * (0.1 * sg)
            vs = [bmw.verts.new(TB(x)) for x in q] + [bmw.verts.new(TB(x + nrm)) for x in q]
            for f in ((0, 1, 2, 3), (7, 6, 5, 4), (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)):
                _face(bmw, [vs[j] for j in f])
        for si in (0, 1):
            sg = -1 if si == 0 else 1
            if (i, si) in roofskip: continue
            sA = Ls[i] if sg < 0 else Rs[i]; sB = Ls[i + 1] if sg < 0 else Rs[i + 1]
            eA = sA + pl * (0.62 * sg) + up * H; eB = sB + pl * (0.62 * sg) + up * H
            rA = (Ls[i] + Rs[i]) / 2 + up * (H + 1.0); rB = (Ls[i + 1] + Rs[i + 1]) / 2 + up * (H + 1.0)
            slab3(Rf, [eA + up * 0.28, eB + up * 0.28, rB + up * 0.28, rA + up * 0.28], 0.1)
    if col:
        Cm0 = (Ls[0] + Rs[0]) / 2; Cm1 = (Ls[-1] + Rs[-1]) / 2
        ax3 = (Cm1 - Cm0); Lg = ax3.length; ax3 = ax3.normalized()
        upn = ax3.cross(pl)
        if upn.y < 0: upn = -upn
        upn = upn.normalized()
        mid = (Cm0 + Cm1) / 2
        colbox(mid - upn * 0.35, ax3, upn, Lg / 2, 0.5, HW + 0.3)
        for sg in (-1, 1):
            colbox(mid + pl * (sg * (HW + 0.3)) + upn * (H / 2), ax3, upn, Lg / 2, H / 2 + 0.2, 0.3)
        colbox(mid + upn * (H + 3.0), ax3, upn, Lg / 2, 2.8, HW + 0.6)
        colbox(mid + pl * (W * fb - HW) + upn * 0.9, ax3, upn, Lg / 2 - 1.0, 0.95, 1.6)
    return Ls, Rs, A, B

def finalize(collname):
    """turn every pending bmesh into an object in collection collname: normals recalculated, UVs for non-tube faces
    (vertical faces: horizontal tangent projection; others: box projection) using the palette tile size."""
    col = bpy.data.collections.get(collname)
    if col is None:
        col = bpy.data.collections.new(collname); bpy.context.scene.collection.children.link(col)
    res = []
    for name in list(S['bms'].keys()):
        bm = S['bms'][name]
        pal = name.split('__')[1]
        bm.normal_update()
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
        bm.normal_update()
        T = TILE.get(pal, 8)
        if isinstance(T, tuple): tu, tv = T
        else: tu, tv = T, T
        uvl = bm.loops.layers.uv['UVMap']; cl = bm.faces.layers.int['cyl']
        for f in bm.faces:
            if f[cl]: continue
            n = f.normal
            if abs(n.z) < 0.35:
                hz = Vector((n.x, n.y, 0.0)).normalized()
                tg = Vector((-hz.y, hz.x, 0.0))
                for l in f.loops:
                    co = l.vert.co
                    l[uvl].uv = (co.dot(tg) / tu, co.z / tv)
                continue
            if abs(n.x) >= abs(n.y) and abs(n.x) >= abs(n.z): ax = 0
            elif abs(n.y) >= abs(n.z): ax = 1
            else: ax = 2
            for l in f.loops:
                co = l.vert.co
                if ax == 0: l[uvl].uv = (co.y / tu, co.z / tv)
                elif ax == 1: l[uvl].uv = (co.x / tu, co.z / tv)
                else: l[uvl].uv = (co.x / tu, co.y / tv)
        old = bpy.data.objects.get(name)
        if old: bpy.data.objects.remove(old, do_unlink=True)
        me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
        ob = bpy.data.objects.new(name, me); col.objects.link(ob)
        mat = bpy.data.materials.get('M_' + pal) or bpy.data.materials.new('M_' + pal)
        me.materials.append(mat)
        res.append((name, sum(len(p.vertices) - 2 for p in me.polygons)))
    S['bms'] = {}
    return res

def colstr():
    L = []
    for e in S['col']:
        if e[0] == 'C':
            a, b = e[1], e[2]
            L.append('C %.3f %.3f %.3f %.3f %.3f %.3f %.3f' % (a.x, a.y, a.z, b.x, b.y, b.z, e[3]))
        else:
            c, u, v = e[1], e[2], e[3]
            L.append('%s %.3f %.3f %.3f %.4f %.4f %.4f %.4f %.4f %.4f %.3f %.3f %.3f' % (e[0], c.x, c.y, c.z, u.x, u.y, u.z, v.x, v.y, v.z, e[4], e[5], e[6]))
    S['col'] = []
    return '\n'.join(L)

string.pb_V = V; string.pb_TB = TB; string.pb_P = P; string.pb_S = S; string.pb_bm_of = bm_of
string.pb_obox = obox; string.pb_frame = frame; string.pb_beam = beam; string.pb_ibeam = ibeam
string.pb_slab = slab; string.pb_slab3 = slab3; string.pb_prism = prism; string.pb_pipe = pipe
string.pb_colbox = colbox; string.pb_rail = rail; string.pb_ladder = ladder; string.pb_truss = truss
string.pb_tower = tower; string.pb_tbent = tbent; string.pb_bent2 = bent2; string.pb_shoe = shoe
string.pb_valve = valve; string.pb_collar = collar; string.pb_gallery2 = gallery2
string.pb_finalize = finalize; string.pb_colstr = colstr
sc = bpy.context.scene
sc.unit_settings.system = 'METRIC'; sc.unit_settings.scale_length = 1.0
print('factory kit ready')
