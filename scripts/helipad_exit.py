# -*- coding: utf-8 -*-
# 탈출구 헬리패드 (Helipad_Exit) — 레이드 탈출구 A·B·C 외형 (2026-11-27, 사용자 "C안(헬기장) 좋다", 헬기 없이 패드만)
# 실행: exec(open(r"D:\god\scripts\helipad_exit.py", encoding="utf-8").read())
# 규칙: .claude/skills/blender-to-roblox (1 unit = 1 stud, Z 위, 원점 = 바닥 중앙, 부품 하나 = 머티리얼 하나, 이름 = 설정)
# 구성 (탈출 구역 반지름 15 = 지름 30 이 판 안에 들어가게):
#   Slab    : 위 34×34 / 아래 36×36 (가장자리 경사로 걸어서 올라섬), 높이 0.8, 모서리 깎음        Concrete
#   Ring    : 노란 원 테두리 (반지름 12.4~13.6), 판 위 0.05                                    Hazard, NoCollide
#   H       : 큰 H (높이 10, 획 1.6), 판 위 0.05                                               Hazard, NoCollide
#   LampBase: 가장자리 유도등 받침 8개                                                         DarkSteel, NoCollide
#   Lens    : 유도등 렌즈 8개 (Studio 에서 Neon + 상태 색: 열림 초록 / 곧 닫힘 빨강)            Glass, NoCollide
#   Pole/PoleFoot/Sock : 북동쪽 모서리 바깥 바람자루 (기둥·받침·주황/흰 줄무늬 자루)
#   Rubble  : 깨진 콘크리트 조각 몇 개 (판 가장자리 바깥)                                     Concrete, NoCollide

import bpy
import bmesh
import math
from mathutils import Vector, Matrix

ASSET = "Helipad_Exit"
SLAB_H = 0.8
PAINT_H = 0.05


def _scene():
    sc = bpy.data.scenes.get("Helipad") or bpy.data.scenes.new("Helipad")
    bpy.context.window.scene = sc
    sc.unit_settings.system = "NONE"
    col = bpy.data.collections.get(ASSET)
    if col:
        for o in list(col.objects):
            bpy.data.objects.remove(o, do_unlink=True)
    else:
        col = bpy.data.collections.new(ASSET)
    if col.name not in sc.collection.children:
        sc.collection.children.link(col)
    return sc, col


def _mat(key):
    rgb = PALETTE[key]
    name = "M_" + key
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = next(n for n in m.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    bsdf.inputs[0].default_value = (*[(c / 255) ** 2.2 for c in rgb], 1)  # Blender 미리보기용 (Studio 색은 이름의 팔레트 키로)
    return m


def _obj(col, name, bm, key):
    bmesh.ops.triangulate(bm, faces=[f for f in bm.faces if len(f.verts) > 4])
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new(name, me)
    ob.data.materials.append(_mat(key))
    col.objects.link(ob)
    return ob


def _chamfer_square(half, cut, z):
    # 모서리를 cut 만큼 깎은 정사각형 (8각), 반시계
    pts = [(half, -half + cut), (half, half - cut), (half - cut, half), (-half + cut, half),
           (-half, half - cut), (-half, -half + cut), (-half + cut, -half), (half - cut, -half)]
    return [Vector((x, y, z)) for x, y in pts]


def make_slab(col):
    bm = bmesh.new()
    bottom = [bm.verts.new(v) for v in _chamfer_square(18.0, 2.6, 0.0)]
    top = [bm.verts.new(v) for v in _chamfer_square(17.0, 1.8, SLAB_H)]
    bm.faces.new(top)                          # 윗면
    n = len(top)
    for i in range(n):                          # 경사진 옆면
        j = (i + 1) % n
        bm.faces.new([bottom[i], bottom[j], top[j], top[i]])
    # 밑면은 땅에 묻히므로 만들지 않음
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    return _obj(col, ASSET + "_Slab__Concrete", bm, "Concrete")


def make_ring(col, r_in=12.4, r_out=13.6, seg=64):
    bm = bmesh.new()
    z0, z1 = SLAB_H, SLAB_H + PAINT_H
    rings = []
    for r, z in ((r_out, z0), (r_out, z1), (r_in, z1), (r_in, z0)):
        rings.append([bm.verts.new((r * math.cos(2 * math.pi * k / seg), r * math.sin(2 * math.pi * k / seg), z)) for k in range(seg)])
    for a in range(3):  # 바깥 옆, 윗면, 안쪽 옆 (밑면은 판에 닿아 안 보임)
        for k in range(seg):
            m = (k + 1) % seg
            bm.faces.new([rings[a][k], rings[a][m], rings[a + 1][m], rings[a + 1][k]])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    return _obj(col, ASSET + "_Ring__Hazard__NoCollide", bm, "Hazard")


def _extrude_outline(bm, pts, z0, z1):
    low = [bm.verts.new((x, y, z0)) for x, y in pts]
    high = [bm.verts.new((x, y, z1)) for x, y in pts]
    bm.faces.new(high)
    n = len(pts)
    for i in range(n):
        j = (i + 1) % n
        bm.faces.new([low[i], low[j], high[j], high[i]])


def make_h(col):
    # H 외곽선 (반시계). 획 굵기 w, 전체 높이 h, 전체 폭 W. +Y 가 H 의 위쪽
    w, h, W = 1.6, 10.0, 7.6
    x0, x1 = W / 2, W / 2 - w
    y0, c = h / 2, w / 2
    pts = [(x0, -y0), (x0, y0), (x1, y0), (x1, c), (-x1, c), (-x1, y0), (-x0, y0), (-x0, -y0),
           (-x1, -y0), (-x1, -c), (x1, -c), (x1, -y0)]
    bm = bmesh.new()
    _extrude_outline(bm, pts, SLAB_H, SLAB_H + PAINT_H)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    return _obj(col, ASSET + "_H__Hazard__NoCollide", bm, "Hazard")


def _cylinder(bm, center, r, h, seg, cap_top=True, cap_bottom=False, r_top=None):
    r_top = r if r_top is None else r_top
    lo = [bm.verts.new(center + Vector((r * math.cos(2 * math.pi * k / seg), r * math.sin(2 * math.pi * k / seg), 0))) for k in range(seg)]
    hi = [bm.verts.new(center + Vector((r_top * math.cos(2 * math.pi * k / seg), r_top * math.sin(2 * math.pi * k / seg), h))) for k in range(seg)]
    for k in range(seg):
        m = (k + 1) % seg
        bm.faces.new([lo[k], lo[m], hi[m], hi[k]])
    if cap_top:
        bm.faces.new(hi)
    if cap_bottom:
        bm.faces.new(list(reversed(lo)))
    return lo, hi


def _dome(bm, center, r, h, seg=10, rings=3):
    # 낮은 반구 렌즈 (밑면 없음)
    prev = [bm.verts.new(center + Vector((r * math.cos(2 * math.pi * k / seg), r * math.sin(2 * math.pi * k / seg), 0))) for k in range(seg)]
    for i in range(1, rings + 1):
        t = i / (rings + 1)
        rr = r * math.cos(t * math.pi / 2)
        zz = h * math.sin(t * math.pi / 2)
        cur = [bm.verts.new(center + Vector((rr * math.cos(2 * math.pi * k / seg), rr * math.sin(2 * math.pi * k / seg), zz))) for k in range(seg)]
        for k in range(seg):
            m = (k + 1) % seg
            bm.faces.new([prev[k], prev[m], cur[m], cur[k]])
        prev = cur
    tip = bm.verts.new(center + Vector((0, 0, h)))
    for k in range(seg):
        bm.faces.new([prev[k], prev[(k + 1) % seg], tip])


def lamp_spots():
    # 판 윗면 가장자리 안쪽: 변 가운데 4 (중심에서 15.6) + 모서리 4 (±13.4, ±13.4 — 깎인 모서리 안쪽, 노란 원 밖)
    s = []
    for x, y in ((15.6, 0), (0, 15.6), (-15.6, 0), (0, -15.6), (13.4, 13.4), (-13.4, 13.4), (-13.4, -13.4), (13.4, -13.4)):
        s.append(Vector((x, y, SLAB_H)))
    return s


def make_lamps(col):
    base = bmesh.new()
    lens = bmesh.new()
    for p in lamp_spots():
        _cylinder(base, p, 0.42, 0.22, 10)
        _dome(lens, p + Vector((0, 0, 0.22)), 0.3, 0.26)
    bmesh.ops.recalc_face_normals(base, faces=base.faces)
    bmesh.ops.recalc_face_normals(lens, faces=lens.faces)
    a = _obj(col, ASSET + "_LampBase__DarkSteel__NoCollide", base, "DarkSteel")
    b = _obj(col, ASSET + "_Lens__Glass__NoCollide", lens, "Glass")
    return a, b


def make_windsock(col):
    at = Vector((19.6, 19.6, 0))  # 북동쪽 모서리 바깥 (판 아래 36×36 밖)
    foot = bmesh.new()
    # 콘크리트 받침 1.2×1.2×0.5
    _extrude_outline(foot, [(at.x + 0.6, at.y - 0.6), (at.x + 0.6, at.y + 0.6), (at.x - 0.6, at.y + 0.6), (at.x - 0.6, at.y - 0.6)], 0.0, 0.5)
    bmesh.ops.recalc_face_normals(foot, faces=foot.faces)
    _obj(col, ASSET + "_PoleFoot__Concrete", foot, "Concrete")
    pole = bmesh.new()
    _cylinder(pole, at + Vector((0, 0, 0.5)), 0.16, 9.5, 8)
    # 꼭대기 고리
    _cylinder(pole, at + Vector((0, 0, 9.4)), 0.3, 0.25, 8, cap_bottom=True)
    bmesh.ops.recalc_face_normals(pole, faces=pole.faces)
    _obj(col, ASSET + "_Pole__DarkSteel__NoCollide", pole, "DarkSteel")
    # 자루: 고리에서 판 바깥쪽(+X, 약간 처짐)으로 뻗는 원뿔대 4칸, 색 번갈아 (주황 = RustRed, 흰 = DirtyWhite)
    bands = {"RustRed": bmesh.new(), "DirtyWhite": bmesh.new()}
    seg = 10
    start = at + Vector((0.3, 0, 9.5))
    length, r0, r1, droop = 3.6, 0.55, 0.22, 0.9
    n = 4
    rot = Matrix.Rotation(math.radians(90), 4, "Y")  # 원기둥 축 Z -> X
    for i in range(n):
        t0, t1 = i / n, (i + 1) / n
        ra, rb = r0 + (r1 - r0) * t0, r0 + (r1 - r0) * t1
        bm = bands["RustRed" if i % 2 == 0 else "DirtyWhite"]
        ca = start + Vector((length * t0, 0, -droop * t0 * t0))
        cb = start + Vector((length * t1, 0, -droop * t1 * t1))
        lo = [bm.verts.new(ca + (rot @ Vector((ra * math.cos(2 * math.pi * k / seg), ra * math.sin(2 * math.pi * k / seg), 0)))) for k in range(seg)]
        hi = [bm.verts.new(cb + (rot @ Vector((rb * math.cos(2 * math.pi * k / seg), rb * math.sin(2 * math.pi * k / seg), 0)))) for k in range(seg)]
        for k in range(seg):
            m = (k + 1) % seg
            bm.faces.new([lo[k], lo[m], hi[m], hi[k]])
    for key, bm in bands.items():
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
        _obj(col, ASSET + "_Sock" + ("A" if key == "RustRed" else "B") + "__" + key + "__NoCollide", bm, key)


def make_rubble(col):
    bm = bmesh.new()
    chunks = [((-19.4, 6.0), 0.9, 0.35, 15), ((-19.0, 8.2), 0.6, 0.3, 50), ((7.5, -19.5), 1.1, 0.4, -20),
              ((10.0, -19.2), 0.55, 0.25, 35), ((-12.0, 19.4), 0.8, 0.3, 70)]
    for (x, y), s, h, ang in chunks:
        a = math.radians(ang)
        pts = []
        for k in range(5):  # 불규칙 5각형
            t = a + 2 * math.pi * k / 5
            r = s * (0.75 + 0.25 * ((k * 37) % 5) / 4)
            pts.append((x + r * math.cos(t), y + r * math.sin(t)))
        _extrude_outline(bm, pts, 0.0, h)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    return _obj(col, ASSET + "_Rubble__Concrete__NoCollide", bm, "Concrete")


def build():
    sc, col = _scene()
    make_slab(col)
    make_ring(col)
    make_h(col)
    make_lamps(col)
    make_windsock(col)
    make_rubble(col)
    tris = sum(len(o.data.polygons) for o in col.objects)
    return "built %s: %d objects" % (ASSET, len(col.objects))


exec(open(r"D:\god\.claude\skills\blender-to-roblox\scripts\blender_helpers.py", encoding="utf-8").read())
EXPORT_DIR = r"D:\god\exports"
print(build())
