# 칼날 회오리(단검) 초승달 베기 메시 3종 — Vfx.BladeWhirl 의 SlashA / SlashB / SlashC (각각 자식 Core = 흰 심)
# 실행 (Blender MCP 또는 Blender Python 콘솔):
#   exec(open(r"D:\god\scripts\blade_whirl_slashes.py", encoding="utf-8").read())
# 결과: 컬렉션 BladeWhirlSlashes, FBX D:\god\exports\BladeWhirlSlashes.fbx (Roblox 업로드용, 저장소에는 안 올라감)
#
# v2 (2026-11-25): 화면에서 선처럼 가늘어 보여 폭을 약 1.8배로 (A 0.42→0.78, B 0.82→1.30, C 0.55→0.95)
# 공통 규칙 (Roblox 에서 돌리기 쉽게):
#   - 칼날은 Blender XY 평면(두께 = Z)의 호. **원점 = 호의 중심(휘두르는 축)** → Roblox 에서 PivotOffset 을 이 점으로 두고
#     피벗을 법선(로컬 Y) 둘레로 돌리면 칼날이 자기 호를 따라 휘둘러짐
#   - 칼날 가운데가 Blender +X 방향(각 0), 끝(앞) 쪽이 반시계(+각). Roblox 로 오면 가운데 = 로컬 -X, 휘두르는 방향 = 로컬 +Y 축 양의 회전
#   - 단면: 바깥 날은 얇고 안쪽으로 갈수록 두꺼워지는 쐐기(위·아래 볼록) + 길이 방향으로 살짝 휘어 오름(평면이 아님)
#   - 폭은 끝으로 갈수록 0 (양 끝 날카로움). 모양마다 가장 넓은 곳·휘어짐·길이를 다르게
#   A 기본: 반지름 3.6, 호 150°, 최대 폭 0.78 (가운데), 대칭 초승달
#   B 강조: 반지름 4.4, 호 175°, 최대 폭 1.30 (62% 지점, 앞이 두툼), 길이 방향으로 나선처럼 0.6 들림
#   C 마무리: 반지름 7.0, 호 72° (거의 곧은 긴 대각 베기, 현 길이 약 8.2), 최대 폭 0.95 (45%), 끝이 아주 날카로움
import bpy, bmesh, math

COL = "BladeWhirlSlashes"
EXPORT = r"D:\god\exports\BladeWhirlSlashes.fbx"

SPECS = {
    # name: (반지름, 호(도), 최대 폭, 가장 넓은 곳(0~1), 두께, 끝 날카로움 지수, 길이 방향 들림, 가운데 활 높이)
    "SlashA": (3.6, 150, 0.78, 0.50, 0.10, 1.1, 0.00, 0.10),
    "SlashB": (4.4, 175, 1.30, 0.62, 0.14, 0.9, 0.60, 0.16),
    "SlashC": (7.0, 72, 0.95, 0.45, 0.12, 1.5, 0.00, 0.08),
}
STATIONS = 40


def profile(u, peak, sharp):
    # 0(꼬리) ~ 1(끝): 가운데(peak)에서 1, 양 끝 0. sharp 가 클수록 끝이 가늘게 오래 뻗음
    if u <= peak:
        k = u / peak
    else:
        k = (1 - u) / (1 - peak)
    return math.sin(k * math.pi / 2) ** sharp


def slash(name, r, span_deg, wmax, peak, thick, sharp, rise, bow, wscale=1.0, tscale=1.0, u0=0.0, u1=1.0, inset=0.0):
    span = math.radians(span_deg)
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    rings = []
    for i in range(STATIONS + 1):
        s = i / STATIONS
        u = u0 + (u1 - u0) * s
        a = -span / 2 + span * u
        w = wmax * wscale * profile(u, peak, sharp)
        t = thick * tscale * max(profile(u, peak, sharp), 0.08) / 2
        z0 = rise * (u - 0.5) + bow * math.sin(math.pi * u)  # 길이 방향 들림 + 가운데 활
        c, sn = math.cos(a), math.sin(a)
        ro = r - inset  # 바깥 날
        if i == 0 or i == STATIONS:
            rings.append([bm.verts.new((ro * c, ro * sn, z0))])
            continue
        rm = ro - w * 0.55  # 능선 (안쪽으로 치우침 → 바깥 날이 얇은 쐐기)
        ri = ro - w
        rings.append([
            bm.verts.new((ro * c, ro * sn, z0)),
            bm.verts.new((rm * c, rm * sn, z0 + t)),
            bm.verts.new((ri * c, ri * sn, z0 + t * 0.15)),
            bm.verts.new((rm * c, rm * sn, z0 - t)),
        ])
    for a_, b_ in zip(rings[:-1], rings[1:]):
        if len(a_) == 1:
            for j in range(4):
                bm.faces.new((a_[0], b_[j], b_[(j + 1) % 4]))
        elif len(b_) == 1:
            for j in range(4):
                bm.faces.new((a_[j], a_[(j + 1) % 4], b_[0]))
        else:
            for j in range(4):
                bm.faces.new((a_[j], a_[(j + 1) % 4], b_[(j + 1) % 4], b_[j]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(me)
    bm.free()
    return bpy.data.objects.new(name, me)


def mat(name, rgb):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.diffuse_color = (*rgb, 1)
    return m


def build():
    col = bpy.data.collections.get(COL)
    if col:
        for o in list(col.objects):
            bpy.data.objects.remove(o, do_unlink=True)
    else:
        col = bpy.data.collections.new(COL)
        bpy.context.scene.collection.children.link(col)
    for other in ("ShadowStepBlade", "BladeWhirl"):
        c = bpy.data.collections.get(other)
        if c:
            c.hide_viewport = True
    out = []
    purple, white = mat("M_SlashPurple", (0.35, 0.05, 1.0)), mat("M_SlashWhite", (1, 1, 1))
    x = 0
    for name, (r, span, w, peak, th, sharp, rise, bow) in SPECS.items():
        outer = slash(name, r, span, w, peak, th, sharp, rise, bow)
        core = slash(name + "_Core", r, span, w, peak, th, sharp, rise, bow,
                     wscale=0.42, tscale=0.55, u0=0.06, u1=0.94, inset=w * 0.12)
        for ob, m in ((outer, purple), (core, white)):
            col.objects.link(ob)
            ob.data.materials.clear()
            ob.data.materials.append(m)
        out += [outer, core]
    return out


def export(objs):
    bpy.ops.object.select_all(action="DESELECT")
    for o in objs:
        o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]
    bpy.ops.export_scene.fbx(
        filepath=EXPORT, use_selection=True, object_types={"MESH"},
        apply_unit_scale=True, apply_scale_options="FBX_SCALE_ALL",
        axis_forward="-Z", axis_up="Y", use_mesh_modifiers=True,
        use_triangles=True, mesh_smooth_type="FACE", add_leaf_bones=False, bake_anim=False,
    )


_objs = build()
for o in _objs:
    vs = [v.co for v in o.data.vertices]
    mn = [min(v[i] for v in vs) for i in range(3)]
    mx = [max(v[i] for v in vs) for i in range(3)]
    ctr = [(a + b) / 2 for a, b in zip(mn, mx)]
    tris = sum(len(p.vertices) - 2 for p in o.data.polygons)
    # bbox 가운데 (호 중심 = 원점 기준). Roblox 피벗 = -(이 값을 Roblox 축으로 옮긴 것)
    print(o.name, "tris", tris, "dims", tuple(round(b - a, 3) for a, b in zip(mn, mx)), "bboxCenter", tuple(round(c, 4) for c in ctr))
export(_objs)
print("exported", EXPORT)
