# 마을 place 병원 앞 구급차 진입 차양 (Blender, exec 로 실행 → build_canopy())
# 좌표는 Roblox 기준(모델 로컬, 원점 = 차양 중심 바로 아래 바닥, 월드 (-519, 0.5, -82))로 쓰고 B() 로 Blender 로 바꿈:
#   Roblox (X, Y, Z) -> Blender (-X, Z, Y).  Studio 로 가져오면 회전 없이 그대로 Roblox (X, Y, Z).
# 재질은 병원과 같은 SurfaceAppearance 를 Studio 에서 붙임 (이름 접두사 AC_, 뒤 키 = part/trim):
#   AC_part = 콘크리트(SA 125301297105006), AC_trim = 테두리(SA 115364150156490). UV = 박스 투영 16 스터드/UV.
import bpy, bmesh, math
from mathutils import Vector, Matrix

UVS = 16.0


def B(x, y, z):
    return Vector((-x, z, y))


def _mat(name, rgb):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.diffuse_color = (rgb[0], rgb[1], rgb[2], 1)
    return m


class Obj:
    def __init__(self, name, rgb):
        self.name, self.rgb = name, rgb
        self.bm = bmesh.new(); self.uv = self.bm.loops.layers.uv.new("UVMap")

    def box(self, x0, x1, y0, y1, z0, z1, rot=None, pivot=None):
        """Roblox 좌표 상자. rot = (축 'X'|'Y'|'Z', 도) 목록, pivot = 회전 중심 (Roblox)."""
        cs = [(x, y, z) for z in (z0, z1) for y in (y0, y1) for x in (x0, x1)]
        M = Matrix.Identity(4)
        if rot:
            pv = Vector(pivot)
            for ax, deg in rot:
                M = Matrix.Rotation(math.radians(deg), 4, ax) @ M
            M = Matrix.Translation(pv) @ M @ Matrix.Translation(-pv)
        pts = [M @ Vector(c) for c in cs]
        v = [self.bm.verts.new(B(p.x, p.y, p.z)) for p in pts]
        quads = ((0, 2, 3, 1), (4, 5, 7, 6), (0, 1, 5, 4), (2, 6, 7, 3), (0, 4, 6, 2), (1, 3, 7, 5))
        for q in quads:
            f = self.bm.faces.new([v[i] for i in q])
            f.normal_update()
            n = f.normal
            ax = max(range(3), key=lambda i: abs(n[i]))
            for lp in f.loops:
                c = lp.vert.co
                if ax == 0:
                    uv = (c.y / UVS, c.z / UVS)
                elif ax == 1:
                    uv = (c.x / UVS, c.z / UVS)
                else:
                    uv = (c.x / UVS, c.y / UVS)
                lp[self.uv].uv = uv

    def tube(self, a, b, r, seg=6):
        a, b = Vector(a), Vector(b)
        d = (b - a).normalized()
        t = d.cross(Vector((0, 1, 0)))
        if t.length < 1e-3:
            t = d.cross(Vector((1, 0, 0)))
        t.normalize(); s = d.cross(t)
        ra, rb = [], []
        for i in range(seg):
            ang = 2 * math.pi * i / seg
            o = (t * math.cos(ang) + s * math.sin(ang)) * r
            pa, pb = a + o, b + o
            ra.append(self.bm.verts.new(B(pa.x, pa.y, pa.z))); rb.append(self.bm.verts.new(B(pb.x, pb.y, pb.z)))
        for i in range(seg):
            j = (i + 1) % seg
            self.bm.faces.new([ra[i], ra[j], rb[j], rb[i]])
        self.bm.faces.new(list(reversed(ra))); self.bm.faces.new(rb)

    def finish(self, col):
        bmesh.ops.recalc_face_normals(self.bm, faces=self.bm.faces)
        me = bpy.data.meshes.new(self.name); self.bm.to_mesh(me); self.bm.free()
        ob = bpy.data.objects.new(self.name, me); col.objects.link(ob)
        ob.data.materials.append(_mat("M_" + self.name.split("__")[0], self.rgb))
        return ob


def build_canopy():
    col = bpy.data.collections.get("HospitalCanopy")
    if col is None:
        col = bpy.data.collections.new("HospitalCanopy"); bpy.context.scene.collection.children.link(col)
    for o in list(col.objects):
        bpy.data.objects.remove(o, do_unlink=True)
    conc, trim = (0.42, 0.41, 0.40), (0.55, 0.54, 0.52)
    P = Obj("AC_part", conc)       # 지붕판 + 기둥 + 받침
    T = Obj("AC_trim", trim)       # 테두리 보(파사드) + 기둥머리
    YS0, YS1 = 18.5, 20.0          # 지붕판 아래·위 (기존 병원 포치: 아래 18.5, 위 20, 앞 z -98, x -551..-487)
    # 지붕판: 앞쪽 동쪽 모서리(X 26..32, Z 9..16) 가 깨져 나감 → 계단식으로
    P.box(-32, 26, YS0, YS1, -16, 16)
    P.box(26, 32, YS0, YS1, -16, 8.5)
    P.box(26, 28.6, YS0, YS1, 8.5, 12.4)
    P.box(28.6, 30.4, YS0 + 0.5, YS1, 8.5, 10.2)
    P.box(26, 27.3, YS0 + 0.6, YS1, 12.4, 14.6)
    # 기둥 3개 (앞줄 Z 13) + 받침
    for x in (-29.5, 0.0, 29.5):
        P.box(x - 1.6, x + 1.6, 0.0, 1.0, 11.4, 14.6)
        P.box(x - 1.2, x + 1.2, 1.0, 15.6, 11.8, 14.2)
        T.box(x - 1.6, x + 1.6, 15.6, 16.5, 11.4, 14.6)
    # 테두리 보: 서쪽 옆면, 앞면(동쪽 끝 6 칸 부서짐), 동쪽 옆면(앞쪽 7.5 부서짐)
    T.box(-33.2, -32, 16.5, 20.4, -16, 17.2)
    T.box(-32, 20.5, 16.5, 20.4, 16, 17.2)
    T.box(20.5, 23.0, 17.6, 20.4, 16, 17.2)       # 깨진 끝 (아래가 떨어져 나감)
    T.box(23.0, 24.4, 18.9, 20.4, 16, 16.9)
    T.box(32, 33.2, 16.5, 20.4, -16, 7.0)
    T.box(32, 33.0, 17.9, 20.4, 7.0, 8.4)
    # 앞 보 아래 기둥 위 받침 보(기둥머리와 맞닿음): 기둥머리 위 ~ 지붕판 아래
    T.box(-31, 31, 16.5, YS0, 12.6, 13.4)
    obs = [P.finish(col), T.finish(col)]
    # 철근: 깨진 모서리에서 삐져나옴
    R = Obj("AC_rebar", (0.18, 0.12, 0.09))
    for (x, z, dx, dz, dy) in ((27.0, 12.4, 0.6, 2.2, -0.8), (27.9, 12.4, 0.3, 1.8, -1.4), (28.6, 10.2, 1.9, 0.6, -0.9),
                               (29.6, 10.2, 1.4, 1.2, -0.3), (26.0, 14.6, 0.9, 1.9, -1.6), (31.0, 8.5, 0.5, 2.1, -0.6)):
        y = YS0 + 0.9
        R.tube((x, y, z), (x + dx, y + dy, z + dz), 0.12)
    for (x, y) in ((20.6, 17.9), (21.4, 18.3), (22.3, 17.8)):
        R.tube((x, y, 16.6), (x + 0.4, y - 1.1, 16.9), 0.1)
    obs.append(R.finish(col))
    # 천장 매립 조명(꺼짐)
    L = Obj("AC_lights", (0.12, 0.12, 0.12))
    for x in (-20, 0, 20):
        for z in (-6, 4):
            L.box(x - 2.5, x + 2.5, YS0 - 0.25, YS0, z - 0.7, z + 0.7)
    obs.append(L.finish(col))
    # 떨어진 조각 (땅 위, 동쪽 앞 모서리 아래)
    C1 = Obj("AC_chunkA", conc)
    C1.box(27.0, 33.0, 0.0, 1.8, 12.0, 16.5, rot=[('Z', 14), ('Y', 23)], pivot=(30, 0.0, 14))
    obs.append(C1.finish(col))
    C2 = Obj("AC_chunkB", trim)
    C2.box(21.0, 27.5, 0.0, 1.2, 19.0, 22.9, rot=[('X', -8), ('Y', -17)], pivot=(24, 0.0, 21))
    obs.append(C2.finish(col))
    tris = sum(sum(len(p.vertices) - 2 for p in o.data.polygons) for o in obs)
    return "canopy objects %d, tris %d" % (len(obs), tris)
