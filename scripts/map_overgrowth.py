# 마을 맵 건물과 같은 방식의 덩굴·이끼 생성 (Blender, exec → grow(컬렉션, ...))
# 맵 건물(HP_/PlazaBuildings/영묘)의 덩굴·이끼를 분석한 결과를 그대로 따름:
#   <에셋>_IvyLeaves : 잎 하나 = 육각 카드(약 1.4 스터드), 텍스처 rbxassetid://77669247244330 (잎 4장이 2×2 로 든 아틀라스),
#                      Plastic, DoubleSided. 카드 UV = 사분면 하나 안의 육각형.
#   <에셋>_IvyStems  : 줄기 = 가는 관, Wood + MaterialVariant Tree_Bark, 색 149,140,130.
#   <에셋>_Moss      : 이끼 = 윗면에 붙은 원판, 이끼 SurfaceAppearance(88648852029370, 가장자리 투명), UV 중심 0.5.
# 모든 잎·줄기·이끼는 표면에서 띄우고(잎 0.3, 줄기 0.15, 이끼 0.04) BVH 로 거리 검사해서 메시를 뚫지 않게 함.
# 좌표는 Blender (Z 위). 컬렉션 안 메시 전체를 표면으로 씀.
import bpy, bmesh, math, random
from mathutils import Vector, Matrix
from mathutils.bvhtree import BVHTree

LEAF_HEX = [(0.5, 0.02), (0.14, 0.40), (0.20, 0.76), (0.5, 0.98), (0.80, 0.76), (0.86, 0.40)]   # 사분면 안 정규화 UV
LEAF_POS = [(0.0, -0.56), (-0.47, -0.12), (-0.40, 0.33), (0.0, 0.62), (0.40, 0.33), (0.47, -0.12)]  # 잎 모양 (크기 1 기준)
QUADS = [(0.0, 0.5), (0.5, 0.5), (0.0, 0.0), (0.5, 0.0)]


def _tree(col):
    # 꼭짓점·면 목록으로 BVH (bmesh 를 free 한 뒤 BVH 를 쓰면 Blender 가 죽음 — 실제로 겪음)
    verts, polys = [], []
    for ob in col.all_objects:
        if ob.type != 'MESH' or ob.name.endswith(("_IvyLeaves", "_IvyStems", "_Moss")):
            continue
        base = len(verts); mw = ob.matrix_world
        verts += [(mw @ v.co).copy() for v in ob.data.vertices]
        polys += [[base + i for i in p.vertices] for p in ob.data.polygons]
    t = BVHTree.FromPolygons(verts, polys)
    mn = Vector((1e9, 1e9, 1e9)); mx = Vector((-1e9, -1e9, -1e9))
    for v in verts:
        mn = Vector(map(min, mn, v)); mx = Vector(map(max, mx, v))
    return t, mn, mx


def _frame(n):
    n = n.normalized()
    up = Vector((0, 0, 1)) if abs(n.z) < 0.9 else Vector((1, 0, 0))
    t = up.cross(n).normalized(); b = n.cross(t).normalized()
    return t, b, n


class Grower:
    def __init__(self, asset, col, seed):
        self.asset, self.col = asset, col
        self.rng = random.Random(seed)
        self.tree, self.mn, self.mx = _tree(col)
        self.leaves = bmesh.new(); self.luv = self.leaves.loops.layers.uv.new("UVMap")
        self.stems = bmesh.new(); self.suv = self.stems.loops.layers.uv.new("UVMap")
        self.moss = bmesh.new(); self.muv = self.moss.loops.layers.uv.new("UVMap")
        self.nleaf = self.nstem = self.nmoss = 0
        self.mosses = []
        self.lps = 4       # 한 걸음마다 잎 수 (맵 건물 덩굴만큼 빽빽하게)   # (중심, 반지름) — 이끼끼리 겹쳐 깜빡이지 않게

    def clear(self, p, d):
        hit = self.tree.find_nearest(p)
        return hit[0] is None or hit[3] >= d

    # ---- 잎 ----
    def leaf(self, c, n, size):
        t, b, n = _frame(n)
        a = self.rng.uniform(0, 2 * math.pi)
        tilt = self.rng.uniform(-0.25, 0.25)
        rt = t * math.cos(a) + b * math.sin(a); rb = n.cross(rt)
        rn = (n + rt * tilt).normalized()
        rb = rn.cross(rt).normalized(); rt = rb.cross(rn).normalized()
        pts = [c + (rt * x + rb * y) * size for x, y in LEAF_POS]
        if not all(self.clear(p, 0.06) for p in pts):
            return False
        q = QUADS[self.rng.randrange(4)]
        vs = [self.leaves.verts.new(p) for p in pts]
        f = self.leaves.faces.new(vs)
        for lp, (u, v) in zip(f.loops, LEAF_HEX):
            lp[self.luv].uv = (q[0] + u * 0.5, q[1] + v * 0.5)
        self.nleaf += 1
        return True

    # ---- 줄기 ----
    def tube(self, pts, r):
        seg = 5
        rings = []
        for i, p in enumerate(pts):
            d = (pts[min(i + 1, len(pts) - 1)] - pts[max(i - 1, 0)]).normalized()
            t, b, _ = _frame(d)
            rings.append([self.stems.verts.new(p + (t * math.cos(2 * math.pi * k / seg) + b * math.sin(2 * math.pi * k / seg)) * r) for k in range(seg)])
        for i in range(len(rings) - 1):
            for k in range(seg):
                k2 = (k + 1) % seg
                f = self.stems.faces.new([rings[i][k], rings[i][k2], rings[i + 1][k2], rings[i + 1][k]])
                for lp, uv in zip(f.loops, ((k / seg, i), ((k + 1) / seg, i), ((k + 1) / seg, i + 1), (k / seg, i + 1))):
                    lp[self.suv].uv = uv
        self.nstem += 1

    def climb(self, start, normal, max_h, down=False, step=0.45, leaf_every=1):
        """벽을 따라 위(또는 아래)로 자라는 줄기 + 잎. start = 표면 위 점, normal = 표면 노멀."""
        pts, p, n = [], start.copy(), normal.normalized()
        drift = Vector((self.rng.uniform(-1, 1), self.rng.uniform(-1, 1), 0)) * 0.35
        h0 = start.z
        for i in range(200):
            sp = p + n * 0.16
            if not self.clear(sp, 0.12):
                break
            pts.append(sp)
            if (i % leaf_every) == 0:
                for _ in range(self.lps):
                    t, b, _n = _frame(n)
                    off = t * self.rng.uniform(-0.8, 0.8) + b * self.rng.uniform(-0.5, 0.5)
                    self.leaf(p + n * self.rng.uniform(0.28, 0.42) + off, n, self.rng.uniform(0.85, 1.3))
            # 다음 점: 위(아래) + 옆으로 흔들림, 표면에 다시 붙임
            dirv = Vector((0, 0, -1 if down else 1)) + drift + Vector((self.rng.uniform(-0.4, 0.4), self.rng.uniform(-0.4, 0.4), 0))
            dirv -= n * dirv.dot(n)
            if dirv.length < 1e-4:
                break
            q = p + dirv.normalized() * step
            hit = self.tree.ray_cast(q + n * 0.8, -n, 1.6)
            if hit[0] is None or hit[1].dot(n) < 0.8:
                if not down:
                    break
                # 아래로 늘어질 때는 벽이 끝나도 공중으로 계속 늘어뜨림 (벽에서 조금씩 떨어지며)
                p = p + Vector((self.rng.uniform(-0.1, 0.1), self.rng.uniform(-0.1, 0.1), -step)) + n * 0.03
                if (h0 - p.z > max_h):
                    break
                continue
            p, n = hit[0], hit[1]
            if (not down and p.z - h0 > max_h) or (down and h0 - p.z > max_h):
                break
        if len(pts) >= 2:
            self.tube(pts, 0.07)
        return len(pts)

    def ivy_walls(self, count, max_h=(4, 12), z_start=None, tries=40):
        """바닥 근처에서 벽을 타고 올라가는 덩굴 count 줄."""
        made = 0
        cx, cy = (self.mn.x + self.mx.x) / 2, (self.mn.y + self.mx.y) / 2
        for _ in range(count * tries):
            if made >= count:
                break
            ang = self.rng.uniform(0, 2 * math.pi)
            far = max(self.mx.x - self.mn.x, self.mx.y - self.mn.y)
            zs = (self.mn.z + 0.4) if z_start is None else self.rng.uniform(*z_start)
            o = Vector((cx + math.cos(ang) * far, cy + math.sin(ang) * far, zs))
            tgt = Vector((cx + self.rng.uniform(-0.4, 0.4) * (self.mx.x - self.mn.x), cy + self.rng.uniform(-0.4, 0.4) * (self.mx.y - self.mn.y), zs))
            hit = self.tree.ray_cast(o, (tgt - o).normalized(), far * 2)
            if hit[0] is None or abs(hit[1].z) > 0.3:
                continue
            if self.climb(hit[0], hit[1], self.rng.uniform(*max_h)) >= 3:
                made += 1
        return made

    def ivy_hang(self, count, z_edge, max_len=(2, 6), tries=40):
        """높이 z_edge 근처 바깥 면에서 아래로 늘어지는 덩굴."""
        made = 0
        cx, cy = (self.mn.x + self.mx.x) / 2, (self.mn.y + self.mx.y) / 2
        far = max(self.mx.x - self.mn.x, self.mx.y - self.mn.y)
        for _ in range(count * tries):
            if made >= count:
                break
            ang = self.rng.uniform(0, 2 * math.pi)
            zs = self.rng.uniform(*z_edge)
            o = Vector((cx + math.cos(ang) * far, cy + math.sin(ang) * far, zs))
            hit = self.tree.ray_cast(o, (Vector((cx, cy, zs)) - o).normalized(), far * 2)
            if hit[0] is None or abs(hit[1].z) > 0.3:
                continue
            if self.climb(hit[0], hit[1], self.rng.uniform(*max_len), down=True) >= 3:
                made += 1
        return made

    def moss_tops(self, count, r=(1.2, 3.5), min_nz=0.6, tries=30, zmin=None):
        made = 0
        for _ in range(count * tries):
            if made >= count:
                break
            x = self.rng.uniform(self.mn.x, self.mx.x); y = self.rng.uniform(self.mn.y, self.mx.y)
            hit = self.tree.ray_cast(Vector((x, y, self.mx.z + 5)), Vector((0, 0, -1)), 1e4)
            if hit[0] is None or hit[1].z < min_nz or (zmin is not None and hit[0].z < zmin):
                continue
            c, n = hit[0], hit[1].normalized()
            t, b, n = _frame(n)
            rad = self.rng.uniform(*r)
            seg = 10
            ok = False
            while rad >= 0.8:
                rim = [c + (t * math.cos(2 * math.pi * k / seg) + b * math.sin(2 * math.pi * k / seg)) * rad for k in range(seg)]
                good = True
                for p in rim:
                    h = self.tree.ray_cast(p + n * 0.5, -n, 0.62)
                    if h[0] is None or h[1].dot(n) < 0.95:
                        good = False; break
                if good:
                    ok = True; break
                rad *= 0.75
            if not ok:
                continue
            if any((c - c2).length < rad + r2 + 0.1 for c2, r2 in self.mosses):
                continue
            if not all(self.clear(p + n * 0.04, 0.03) for p in rim + [c]):
                continue
            self.mosses.append((c.copy(), rad))
            cen = self.moss.verts.new(c + n * 0.04)
            ring = [self.moss.verts.new(p + n * 0.04) for p in rim]
            s = 0.44 / rad
            for k in range(seg):
                k2 = (k + 1) % seg
                f = self.moss.faces.new([cen, ring[k], ring[k2]])
                for lp, vtx in zip(f.loops, (None, k, k2)):
                    if vtx is None:
                        lp[self.muv].uv = (0.5, 0.5)
                    else:
                        a = 2 * math.pi * vtx / seg
                        lp[self.muv].uv = (0.5 + math.cos(a) * rad * s, 0.5 + math.sin(a) * rad * s)
            self.nmoss += 1
            made += 1
        return made

    def finish(self):
        out = []
        for suffix, bm, rgb in (("_IvyLeaves", self.leaves, (0.2, 0.35, 0.12)), ("_IvyStems", self.stems, (0.3, 0.25, 0.2)), ("_Moss", self.moss, (0.25, 0.35, 0.15))):
            name = self.asset + suffix
            old = bpy.data.objects.get(name)
            if old:
                bpy.data.objects.remove(old, do_unlink=True)
            if len(bm.faces) == 0:
                bm.free(); continue
            # 줄기 관·이끼 원판은 만들 때 바깥/위를 보게 감음 (열린 면이라 recalc 하면 뒤집힐 수 있음)
            me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
            ob = bpy.data.objects.new(name, me); self.col.objects.link(ob)
            m = bpy.data.materials.get("M" + suffix) or bpy.data.materials.new("M" + suffix)
            m.diffuse_color = (rgb[0], rgb[1], rgb[2], 1); ob.data.materials.append(m)
            out.append("%s faces %d" % (name, len(me.polygons)))
        return "leaves %d, stems %d, moss %d | %s" % (self.nleaf, self.nstem, self.nmoss, ", ".join(out))
