# 신의 창(god_spear) 하늘에서 떨어지는 거대한 빛의 창 — 블록아웃 (2026-11-24)
# 결정(사용자): 순수한 빛 결정 / 길고 가느다란 잎사귀형 날 / 길이 약 40 / 장식 없이 창 모양만
# 1 Blender unit = 1 stud. Z = 창 축. 창끝(아래, 꽂히는 쪽) z = 0, 꼬리 z = 40. XY 중앙 = 축.
# 부품 = 오브젝트 하나 = 재질 하나 (Roblox 에서 색·재질을 이름으로 정함)
#   GodSpear_Blade  결정 날 (잎사귀형, 마름모 단면 — 가운데 능선 + 양날)
#   GodSpear_Core   날 속 빛의 심 (능선을 따라 가는 빛, Neon)
#   GodSpear_Collar 날과 자루 잇는 짧은 목 (결정 마디)
#   GodSpear_Shaft  자루 (8각 결정 기둥, 끝으로 갈수록 가늘게)
#   GodSpear_Butt   꼬리 끝 (짧은 결정 촉)
# 실행: exec(open(r"D:\god\scripts\vfx_god_spear.py", encoding="utf-8").read())
import bpy, bmesh, math, random

# AI티 줄이기 ⑥ (2026-11-24): 결정 면 위치·폭·좌우를 조금씩 불규칙하게, 날에 작은 이 빠짐, 자루·마디 꼭짓점 흔들기 (같은 결과가 나오게 시드 고정)
RNG = random.Random(7)

P = dict(
    length=40.0,
    blade_len=14.0,      # 창끝 0 → 14
    blade_w=1.6,         # 날 최대 반폭 (최대 폭 3.2) — v1 1.45 → v2 2.0(통통함) → 1.6 (사용자)
    blade_wmax_at=0.62,  # 날 길이 중 가장 넓은 곳 (끝에서 비율)
    blade_th=0.42,       # 능선 두께 / 반폭 비
    neck_w=0.62,         # 날 뿌리 반폭
    collar_len=2.6,      # 결정 마디 (사용자: 조금 크게, 결정 마디로)
    collar_r=1.25,
    shaft_r0=0.56,       # 목 쪽 반지름 (굵기 1.1)
    shaft_r1=0.46,       # 꼬리 쪽 반지름
    butt_len=1.8,
    rings=48,            # 날 길이 방향 단면 수
)

COLL = "GodSpear"

def clear():
    if COLL in bpy.data.collections:
        c = bpy.data.collections[COLL]
        for o in list(c.objects):
            bpy.data.objects.remove(o, do_unlink=True)
    else:
        c = bpy.data.collections.new(COLL)
        bpy.context.scene.collection.children.link(c)
    for n in ("Cube",):
        o = bpy.data.objects.get(n)
        if o:
            bpy.data.objects.remove(o, do_unlink=True)
    return c

def smooth(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)

def blade_half_width(t):
    # t: 0 = 창끝, 1 = 날 뿌리. 끝은 길고 가늘게, 최대 폭 뒤로 목까지 부드럽게 좁아짐
    m = P["blade_wmax_at"]
    W = P["blade_w"]
    if t <= m:
        u = t / m
        return W * (math.sin(u * math.pi / 2) ** 1.35)  # 끝: 길고 뾰족
    u = (t - m) / (1 - m)
    return P["neck_w"] + (W - P["neck_w"]) * (1 - smooth(u)) ** 1.1

def mat(name, rgb, emit):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = next(n for n in m.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    bsdf.inputs["Base Color"].default_value = (*rgb, 1)
    bsdf.inputs["Roughness"].default_value = 0.15
    bsdf.inputs["Emission Color"].default_value = (*rgb, 1)
    bsdf.inputs["Emission Strength"].default_value = emit
    m.diffuse_color = (*rgb, 1)
    return m

def finish(bm, name, coll, material):
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    for p in me.polygons:
        p.use_smooth = False  # 결정: 각진 면
    ob = bpy.data.objects.new(name, me)
    coll.objects.link(ob)
    me.materials.append(material)
    return ob

def loft(rings, cap_start_point=None, cap_end_point=None):
    """rings: [(z, [(x,y),...]), ...] 같은 꼭짓점 수. 끝은 한 점으로 모으거나 면으로 닫음"""
    bm = bmesh.new()
    vr = [[bm.verts.new((x, y, z)) for x, y in pts] for z, pts in rings]
    n = len(vr[0])
    for a, b in zip(vr, vr[1:]):
        for i in range(n):
            bm.faces.new((a[i], a[(i + 1) % n], b[(i + 1) % n], b[i]))
    if cap_start_point is not None:
        tip = bm.verts.new(cap_start_point)
        for i in range(n):
            bm.faces.new((tip, vr[0][(i + 1) % n], vr[0][i]))
    else:
        bm.faces.new(list(reversed(vr[0])))
    if cap_end_point is not None:
        tip = bm.verts.new(cap_end_point)
        for i in range(n):
            bm.faces.new((vr[-1][i], vr[-1][(i + 1) % n], tip))
    else:
        bm.faces.new(vr[-1])
    return bm

def diamond(hw, th):
    # 마름모 단면: 양날(±X) + 앞뒤 능선(±Y). 능선 옆 반폭 지점에 꺾임을 하나 더 둬서 면이 한 장으로 밋밋하지 않게
    return [(hw, 0), (hw * 0.45, th * 0.82), (0, th), (-hw * 0.45, th * 0.82),
            (-hw, 0), (-hw * 0.45, -th * 0.82), (0, -th), (hw * 0.45, -th * 0.82)]

def poly(r, n=8, rot=0.0):
    return [(r * math.cos(rot + 2 * math.pi * i / n), r * math.sin(rot + 2 * math.pi * i / n)) for i in range(n)]

def build():
    coll = clear()
    m_crystal = mat("GS_Crystal", (0.78, 1.0, 0.86), 2.0)
    m_core = mat("GS_Core", (0.55, 1.0, 0.65), 12.0)

    m_edge = mat("GS_Edge", (0.85, 1.0, 0.9), 16.0)
    L, BL = P["length"], P["blade_len"]
    # 날: 결정 면 나눔 (사용자). 길이 방향은 띠 몇 개(FACET_T)로만 끊어 면이 평평한 결정 판이 되게,
    # 단면 꺾임은 띠마다 번갈아 조금씩 옮겨서 면이 삼각 결정면으로 갈라지게
    FACET_T = [0.07, 0.17, 0.29, 0.42, 0.54, 0.64, 0.75, 0.87, 1.0]
    FACET_T = [t if t in (0.07, 1.0) else t + RNG.uniform(-0.025, 0.025) for t in FACET_T]
    nicks = {3: 0.9, 6: 0.93}  # 이 빠진 자리 (띠 번호: 그쪽 날 폭 비율)
    rings, edge_rings = [], []
    for k, t in enumerate(FACET_T):
        hw = blade_half_width(t)
        th = max(hw * P["blade_th"], 0.05)
        # 꺾임 위치·높이를 띠마다 무작위 (번갈아 반복하던 규칙 대신)
        a, b = RNG.uniform(0.6, 0.74), RNG.uniform(0.24, 0.4)
        ya, yb = RNG.uniform(0.52, 0.64), RNG.uniform(0.85, 0.95)
        # 좌우 날 폭 조금 다르게 + 가끔 이 빠짐, 능선은 살짝 옆으로
        hr = hw * RNG.uniform(0.96, 1.04) * (nicks.get(k, 1.0) if RNG.random() < 0.5 else 1.0)
        hl = hw * RNG.uniform(0.96, 1.04) * (nicks.get(k, 1.0))
        rx = hw * RNG.uniform(-0.05, 0.05)
        sec = [(hr, 0), (a * hr, ya * th), (rx + b * hr, yb * th), (rx, th),
               (rx - b * hl, yb * th), (-a * hl, ya * th), (-hl, 0),
               (-a * hl, -ya * th), (rx - b * hl, -yb * th), (rx, -th), (rx + b * hr, -yb * th), (a * hr, -ya * th)]
        hw = (hr + hl) / 2
        rings.append((t * BL, sec))
        # 빛나는 날 테두리: 양날 가장자리를 감싸는 얇은 V 띠 (면 위로 0.02 띄움)
        e = []
        for s, hh in ((1, hr), (-1, hl)):
            d = min(0.2, 0.32 * hh)
            x = hh - d
            yf = ya * th * (hh - x) / max(hh - a * hh, 1e-4)  # 가장자리 ~ 첫 꺾임 사이 면의 높이
            e.append([(s * x, yf + 0.025), (s * (hh + 0.03), 0), (s * x, -yf - 0.025)])
        edge_rings.append((t * BL, e))
    bm = loft(rings, cap_start_point=(0, 0, 0))
    bmesh.ops.triangulate(bm, faces=bm.faces)  # 꺾인 면을 삼각 결정면으로
    finish(bm, "GodSpear_Blade", coll, m_crystal)

    # 테두리 띠 메시: 창끝 한 점에서 시작해 뿌리까지, 양쪽 날
    bm = bmesh.new()
    for side in (0, 1):
        tip = bm.verts.new((0, 0, -0.02))
        prev = None
        for z, e in edge_rings:
            cur = [bm.verts.new((x, y, z)) for x, y in e[side]]
            if prev is None:
                bm.faces.new((tip, cur[1], cur[0]))
                bm.faces.new((tip, cur[2], cur[1]))
            else:
                bm.faces.new((prev[0], prev[1], cur[1], cur[0]))
                bm.faces.new((prev[1], prev[2], cur[2], cur[1]))
            prev = cur
    finish(bm, "GodSpear_Edge", coll, m_edge)

    # 심: 능선을 따라 가는 빛 (날 안쪽, 끝 0.8 ~ 뿌리)
    crings = []
    for i in range(1, 25):
        t = 0.06 + 0.94 * i / 24
        hw = blade_half_width(t) * 0.22
        crings.append((t * BL, poly(max(hw, 0.04), 6)))
    finish(loft(crings, cap_start_point=(0, 0, 0.06 * BL - 0.3)), "GodSpear_Core", coll, m_core)

    # 목(결정 마디): 6각 쌍뿔 결정 — 날 쪽은 짧고 가파르게, 가운데 띠(적도), 자루 쪽은 길게 좁아짐
    z0 = BL
    cl = P["collar_len"]
    cr = P["collar_r"]
    rot = math.pi / 6
    def jag6(r, z):
        return [(x * RNG.uniform(0.92, 1.08), y * RNG.uniform(0.92, 1.08)) for x, y in poly(r, 6, rot + RNG.uniform(-0.06, 0.06))]
    collar = [(z0 - 0.2, poly(P["neck_w"] * 0.95, 6, rot)),
              (z0 + cl * RNG.uniform(0.25, 0.32), jag6(cr, 0)),
              (z0 + cl * RNG.uniform(0.4, 0.46), jag6(cr * RNG.uniform(0.94, 1.0), 0)),
              (z0 + cl, poly(P["shaft_r0"] * 1.05, 6, rot))]
    finish(loft(collar), "GodSpear_Collar", coll, m_crystal)

    # 자루: 8각, 끝으로 가늘게
    zs, ze = z0 + cl, L - P["butt_len"]
    srings = []
    for i in range(11):
        k = i / 10
        r = P["shaft_r0"] + (P["shaft_r1"] - P["shaft_r0"]) * k
        # 꼭짓점마다 반지름 ±6%, 띠마다 살짝 비틀림 (완전한 8각 기둥이라 너무 반듯했음)
        pts = poly(r, 8, k * 0.35 + RNG.uniform(-0.05, 0.05))
        pts = [(x * RNG.uniform(0.94, 1.06), y * RNG.uniform(0.94, 1.06)) for x, y in pts]
        srings.append((zs + (ze - zs) * k, pts))
    finish(loft(srings), "GodSpear_Shaft", coll, m_crystal)

    # 꼬리 촉
    br = [(ze - 0.05, poly(P["shaft_r1"] * 1.5, 8, math.pi / 8)), (ze + 0.35, poly(P["shaft_r1"] * 1.5, 8, math.pi / 8))]
    finish(loft(br, cap_end_point=(0, 0, L)), "GodSpear_Butt", coll, m_crystal)

    tris = 0
    for o in coll.objects:
        tris += sum(len(p.vertices) - 2 for p in o.data.polygons)
    print("GodSpear parts", [o.name for o in coll.objects], "tris", tris)

def fix_outward():
    # 열린 띠(테두리)·닫힌 부품 모두 면 노멀이 축에서 바깥을 보게 (Roblox MeshPart 는 한쪽 면만 그림)
    flipped = 0
    for o in bpy.data.collections[COLL].objects:
        me = o.data
        for p in me.polygons:
            c = p.center
            out = c.copy(); out.z = 0
            if out.length < 1e-4:
                continue
            if p.normal.dot(out.normalized()) < -0.05 and o.name == "GodSpear_Edge":
                p.flip(); flipped += 1
        me.update()
    print("edge faces flipped", flipped)

def export():
    import os
    coll = bpy.data.collections[COLL]
    os.makedirs(r"D:\god\exports\vfx", exist_ok=True)
    bpy.ops.object.select_all(action="DESELECT")
    for o in coll.objects:
        o.select_set(True)
    bpy.context.view_layer.objects.active = coll.objects[0]
    path = r"D:\god\exports\vfx\GodSpear.fbx"
    wanted = dict(filepath=path, use_selection=True, object_types={"MESH"}, apply_unit_scale=True,
                  apply_scale_options="FBX_SCALE_ALL", axis_forward="-Z", axis_up="Y", bake_space_transform=False,
                  use_mesh_modifiers=True, use_triangles=True, mesh_smooth_type="FACE", add_leaf_bones=False, bake_anim=False)
    valid = {p.identifier for p in bpy.ops.export_scene.fbx.get_rna_type().properties}
    bpy.ops.export_scene.fbx(**{k: v for k, v in wanted.items() if k in valid})
    print("exported", path)

build()
fix_outward()
