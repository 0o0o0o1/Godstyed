# 착지 연기 고리 (신의 창·도약 찌르기 공용, 2026-11-24)
# 사용자 참고 그림: 바닥에 낮게 깔려 바깥으로 퍼지는 가늘고 찢어진 연기 고리 (지금 뭉게 덩이는 "방귀 같다")
# 시트 두 장 (8x8 = 64칸, 칸 128px):
#   SmokeWisp  옆에서 본 낮고 긴 연기 가닥 — 파티클로 원 테두리에서 바깥으로 낮게 뿌려 고리의 두께·높이를 만듦
#              가로로 늘어난 결(바깥으로 밀려가는 느낌) + 위쪽 가장자리가 말려 올라가며 찢어짐, 아래는 바닥에 붙어 평평
#   SmokeRing  위에서 본 연기 고리 — 바닥 SurfaceGui 로 깔아 고리 모양(가운데 빔)을 잡음. 반지름이 커지며 얇아지고 찢어져 사라짐
# 먼저 vfx_sheet_kit.py 를 exec 한 뒤 실행. 렌더는 명령줄 Blender 병렬 (인수인계 문서 참고).
import bpy, bmesh

FRAMES = 64


def _vol_nodes(mat):
    nt = mat.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    return nt, nt.nodes.new, nt.links.new


def _math(N, op, a=None, b=None):
    m = N("ShaderNodeMath")
    m.operation = op
    if a is not None:
        m.inputs[0].default_value = a
    if b is not None:
        m.inputs[1].default_value = b
    return m


def _maprange(N, fmin, fmax, tmin=0.0, tmax=1.0, smooth=True):
    r = N("ShaderNodeMapRange")
    r.inputs["From Min"].default_value = fmin
    r.inputs["From Max"].default_value = fmax
    r.inputs["To Min"].default_value = tmin
    r.inputs["To Max"].default_value = tmax
    r.clamp = True
    if smooth:
        r.interpolation_type = "SMOOTHSTEP"
    return r


def key(sock, frame, value):
    sock.default_value = value
    sock.keyframe_insert("default_value", frame=frame)


def _light(sc, name, energy, rot, color=(1, 1, 1)):
    sun = bpy.data.lights.new(name, "SUN")
    sun.energy = energy
    sun.color = color
    sun.angle = 0.5
    o = bpy.data.objects.new(name, sun)
    o.rotation_euler = rot
    sc.collection.objects.link(o)


def _box(sc, name, size):
    mesh = bpy.data.meshes.new(name + "Mesh")
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=2.0)
    bm.to_mesh(mesh)
    bm.free()
    ob = bpy.data.objects.new(name, mesh)
    ob.scale = size
    sc.collection.objects.link(ob)
    return ob, mesh


def _setup(sc, samples=48):
    sc.frame_start, sc.frame_end = 1, FRAMES
    sc.cycles.samples = samples
    try:
        sc.cycles.volume_step_rate = 1.0
        sc.cycles.volume_max_steps = 256
    except Exception:
        pass
    bg = next(n for n in sc.world.node_tree.nodes if n.type == "BACKGROUND")
    bg.inputs[0].default_value = (0.7, 0.72, 0.75, 1)
    bg.inputs[1].default_value = 1.0  # 밝은 주변광 → 그늘도 회백색 (Roblox 에서 색은 Color 로 물들임)


def build_wisp():
    """옆에서 본 낮고 긴 연기 가닥. 화면 가로 = 바깥으로 밀려가는 방향, 아래 = 바닥"""
    sc = vfx_scene("VFX_SmokeWisp", ortho_scale=2.4, cam_dir=(0, -1, 0.1))
    _setup(sc)
    _light(sc, "WispSun", 6.0, (0.9, -0.4, 0.5))
    ob, mesh = _box(sc, "Wisp", (1.15, 0.45, 0.6))
    ob.location = (0, 0, -0.35)
    floor_z = -1.15  # 화면 아래 가장자리 근처 = 바닥
    mat = bpy.data.materials.new("WispVolume")
    mat.use_nodes = True
    nt, N, L = _vol_nodes(mat)
    out = N("ShaderNodeOutputMaterial")
    vol = N("ShaderNodeVolumePrincipled")
    vol.inputs["Color"].default_value = (0.95, 0.95, 0.95, 1)
    vol.inputs["Anisotropy"].default_value = 0.25
    tc = N("ShaderNodeTexCoord")
    # 소용돌이: 좌표를 큰 노이즈로 휘게 (말려 올라가는 결)
    warp = N("ShaderNodeTexNoise"); warp.noise_dimensions = "4D"
    warp.inputs["Scale"].default_value = 1.6; warp.inputs["Detail"].default_value = 2.0
    wsub = N("ShaderNodeVectorMath"); wsub.operation = "SUBTRACT"; wsub.inputs[1].default_value = (0.5, 0.5, 0.5)
    wamp = N("ShaderNodeVectorMath"); wamp.operation = "SCALE"; wamp.inputs["Scale"].default_value = 1.4
    wadd = N("ShaderNodeVectorMath"); wadd.operation = "ADD"
    L(tc.outputs["Object"], warp.inputs["Vector"])
    L(warp.outputs["Color"], wsub.inputs[0])
    L(wsub.outputs[0], wamp.inputs[0])
    L(tc.outputs["Object"], wadd.inputs[0])
    L(wamp.outputs[0], wadd.inputs[1])
    # 가로 결: X 로 늘린 노이즈 (스케일 X 작게)
    streak_map = N("ShaderNodeMapping"); streak_map.inputs["Scale"].default_value = (0.35, 2.2, 3.2)
    streak = N("ShaderNodeTexNoise"); streak.noise_dimensions = "4D"
    streak.inputs["Scale"].default_value = 2.4; streak.inputs["Detail"].default_value = 6.0; streak.inputs["Roughness"].default_value = 0.6
    L(wadd.outputs[0], streak_map.inputs["Vector"])
    L(streak_map.outputs[0], streak.inputs["Vector"])
    # 덩치: 타원 기울기 (아래쪽 평평하게: Z 가 음수면 1, 위로 갈수록 빠르게 0)
    grad = N("ShaderNodeTexGradient"); grad.gradient_type = "SPHERICAL"
    L(wadd.outputs[0], grad.inputs["Vector"])
    sep = N("ShaderNodeSeparateXYZ")
    L(tc.outputs["Object"], sep.inputs[0])
    floor = _maprange(N, -1.0, -0.4, 0.0, 1.0)  # 아래로 갈수록 서서히 옅어짐 (사용자 2026-11-24: 바닥에서 뚝 끊겨 어색 → -0.82 에서 -0.4)
    top = _maprange(N, 0.1, 0.95, 1.0, 0.0)  # 위로 갈수록 옅어짐
    L(sep.outputs["Z"], floor.inputs["Value"])
    L(sep.outputs["Z"], top.inputs["Value"])
    # field = grad*1.3 + (streak-0.5)*1.4  → 문턱(시간 따라 올림)
    g13 = _math(N, "MULTIPLY", b=1.3)
    ssub = _math(N, "SUBTRACT", b=0.5)
    samp = _math(N, "MULTIPLY", b=2.2)
    fadd = _math(N, "ADD")
    L(grad.outputs["Fac"], g13.inputs[0])
    L(streak.outputs["Fac"], ssub.inputs[0])
    L(ssub.outputs[0], samp.inputs[0])
    L(g13.outputs[0], fadd.inputs[0])
    L(samp.outputs[0], fadd.inputs[1])
    thr = _maprange(N, 0.2, 0.32)
    L(fadd.outputs[0], thr.inputs["Value"])
    # 가는 결 (찢어진 가장자리)
    fine = N("ShaderNodeTexNoise"); fine.noise_dimensions = "4D"
    fine.inputs["Scale"].default_value = 9.0; fine.inputs["Detail"].default_value = 8.0; fine.inputs["Roughness"].default_value = 0.7
    fmap = N("ShaderNodeMapping"); fmap.inputs["Scale"].default_value = (0.5, 1.5, 1.8)
    L(wadd.outputs[0], fmap.inputs["Vector"])
    L(fmap.outputs[0], fine.inputs["Vector"])
    fr = _maprange(N, 0.38, 0.68, 0.25, 1.0)
    L(fine.outputs["Fac"], fr.inputs["Value"])
    # 상자 경계에서 0 이 되는 타원 마스크 (휜 좌표가 상자 면에 닿아 각지게 잘리던 문제)
    edge = N("ShaderNodeTexGradient"); edge.gradient_type = "SPHERICAL"
    L(tc.outputs["Object"], edge.inputs["Vector"])
    em = _maprange(N, 0.0, 0.3)
    L(edge.outputs["Fac"], em.inputs["Value"])
    m1 = _math(N, "MULTIPLY"); m2 = _math(N, "MULTIPLY"); m3 = _math(N, "MULTIPLY"); m4 = _math(N, "MULTIPLY")
    dens = _math(N, "MULTIPLY", b=18.0)
    L(thr.outputs["Result"], m1.inputs[0]); L(fr.outputs["Result"], m1.inputs[1])
    L(m1.outputs[0], m2.inputs[0]); L(floor.outputs["Result"], m2.inputs[1])
    L(m2.outputs[0], m3.inputs[0]); L(top.outputs["Result"], m3.inputs[1])
    L(m3.outputs[0], m4.inputs[0]); L(em.outputs["Result"], m4.inputs[1])
    L(m4.outputs[0], dens.inputs[0])
    L(dens.outputs[0], vol.inputs["Density"])
    L(vol.outputs["Volume"], out.inputs["Volume"])
    mesh.materials.append(mat)
    # 시간: 빠르게 가로로 밀려 나가며(앞 1/4) 늘어나고, 위가 말려 올라가며 찢어지고, 옅어짐
    # 상자 아래 면이 늘 바닥(floor_z)에 붙도록 위치 = floor_z + 높이
    for f, sx, sz, t0, d, w in [
        (1, 0.45, 0.16, 0.10, 22.0, 0.0),
        (6, 0.85, 0.24, 0.16, 20.0, 0.3),
        (16, 1.05, 0.32, 0.26, 16.0, 0.8),
        (32, 1.15, 0.40, 0.38, 11.0, 1.4),
        (48, 1.18, 0.46, 0.50, 6.0, 1.9),
        (64, 1.20, 0.50, 0.62, 2.0, 2.3),
    ]:
        ob.scale = (sx, 0.45, sz)
        ob.keyframe_insert("scale", frame=f)
        ob.location = (0, 0, floor_z + sz)
        ob.keyframe_insert("location", frame=f)
        key(thr.inputs["From Min"], f, t0)
        key(thr.inputs["From Max"], f, t0 + 0.12)
        key(dens.inputs[1], f, d)
        for nz, k in ((warp, 1.0), (streak, 1.3), (fine, 1.8)):
            key(nz.inputs["W"], f, w * k)
    print("wisp scene ready")
    return sc


def build_ring():
    """위에서 본 연기 고리 (바닥에 깔 시트). 칸 가운데 = 꽂힌 자리, 칸 끝(반지름 1) = 시트 판 끝"""
    sc = vfx_scene("VFX_SmokeRing", ortho_scale=2.0, cam_dir=(0, 0, 1))
    _setup(sc, samples=40)
    # 낮은 각도 빛 + 약한 주변광 → 덩이마다 밝은 면·그늘이 생겨 뭉게뭉게 보임
    bg = next(n for n in sc.world.node_tree.nodes if n.type == "BACKGROUND")
    bg.inputs[1].default_value = 0.45
    _light(sc, "RingSun", 9.0, (1.05, 0.0, 0.8))
    ob, mesh = _box(sc, "Ring", (1.0, 1.0, 0.22))  # 덩이가 둥글게 보이게 높이 0.16 → 0.22
    mat = bpy.data.materials.new("RingVolume")
    mat.use_nodes = True
    nt, N, L = _vol_nodes(mat)
    out = N("ShaderNodeOutputMaterial")
    vol = N("ShaderNodeVolumePrincipled")
    vol.inputs["Color"].default_value = (0.95, 0.95, 0.95, 1)
    vol.inputs["Anisotropy"].default_value = 0.2
    tc = N("ShaderNodeTexCoord")
    # 소용돌이로 휜 좌표
    warp = N("ShaderNodeTexNoise"); warp.noise_dimensions = "4D"
    warp.inputs["Scale"].default_value = 2.2; warp.inputs["Detail"].default_value = 2.0
    wsub = N("ShaderNodeVectorMath"); wsub.operation = "SUBTRACT"; wsub.inputs[1].default_value = (0.5, 0.5, 0.5)
    wamp = N("ShaderNodeVectorMath"); wamp.operation = "SCALE"; wamp.inputs["Scale"].default_value = 0.3
    wadd = N("ShaderNodeVectorMath"); wadd.operation = "ADD"
    L(tc.outputs["Object"], warp.inputs["Vector"])
    L(warp.outputs["Color"], wsub.inputs[0]); L(wsub.outputs[0], wamp.inputs[0])
    L(tc.outputs["Object"], wadd.inputs[0]); L(wamp.outputs[0], wadd.inputs[1])
    # 반지름 거리 (XY)
    sep = N("ShaderNodeSeparateXYZ")
    L(wadd.outputs[0], sep.inputs[0])
    comb = N("ShaderNodeCombineXYZ")
    L(sep.outputs["X"], comb.inputs["X"]); L(sep.outputs["Y"], comb.inputs["Y"])
    rlen = N("ShaderNodeVectorMath"); rlen.operation = "LENGTH"
    L(comb.outputs[0], rlen.inputs[0])
    # d = 거리 - R(t). 바깥 가장자리는 날카롭게, 안쪽은 길게 끌리며 옅어짐
    R = _math(N, "SUBTRACT", b=0.3)
    L(rlen.outputs["Value"], R.inputs[0])
    inner = _maprange(N, -0.35, 0.0, 0.0, 1.0)
    outer = _maprange(N, 0.0, 0.07, 1.0, 0.0)
    L(R.outputs[0], inner.inputs["Value"]); L(R.outputs[0], outer.inputs["Value"])
    prof = _math(N, "MINIMUM")
    L(inner.outputs["Result"], prof.inputs[0]); L(outer.outputs["Result"], prof.inputs[1])
    # 높이: 바닥 쪽이 진함
    zr = _maprange(N, -1.0, 0.6, 1.0, 0.0)
    L(sep.outputs["Z"], zr.inputs["Value"])
    # 찢어짐: 방사로 늘어난 노이즈 (각도 방향으로 빠르게 변함) + 가는 결
    # 방사 결: 노이즈 좌표 = (방향 단위벡터 × 3.5, 반지름 × 0.9) → 바깥쪽으로 길게 늘어난 가닥
    unit = N("ShaderNodeVectorMath"); unit.operation = "NORMALIZE"
    L(comb.outputs[0], unit.inputs[0])
    us = N("ShaderNodeVectorMath"); us.operation = "SCALE"; us.inputs["Scale"].default_value = 3.5
    L(unit.outputs[0], us.inputs[0])
    rz = _math(N, "MULTIPLY", b=0.9)
    L(rlen.outputs["Value"], rz.inputs[0])
    rvec = N("ShaderNodeCombineXYZ")
    rz2 = _math(N, "ADD")
    L(rz.outputs[0], rz2.inputs[0]); L(sep.outputs["Z"], rz2.inputs[1])
    L(rz2.outputs[0], rvec.inputs["Z"])
    polar = N("ShaderNodeVectorMath"); polar.operation = "ADD"
    L(us.outputs[0], polar.inputs[0]); L(rvec.outputs[0], polar.inputs[1])
    # 뭉게뭉게 (사용자 2026-11-24: "고리를 더 뭉게뭉게"): 방사 결은 약하게(0.25)만 섞고 휜 좌표의 둥근 덩이 위주
    # 덩이 = 큰 노이즈(낮은 거칠기 → 둥근 콜리플라워) + 가는 결은 아래 fine 이 맡음
    pmix = N("ShaderNodeVectorMath"); pmix.operation = "SCALE"; pmix.inputs["Scale"].default_value = 0.25
    L(polar.outputs[0], pmix.inputs[0])
    wmix = N("ShaderNodeVectorMath"); wmix.operation = "SCALE"; wmix.inputs["Scale"].default_value = 1.6
    L(wadd.outputs[0], wmix.inputs[0])
    bvec = N("ShaderNodeVectorMath"); bvec.operation = "ADD"
    L(pmix.outputs[0], bvec.inputs[0]); L(wmix.outputs[0], bvec.inputs[1])
    breakup = N("ShaderNodeTexNoise"); breakup.noise_dimensions = "4D"
    breakup.inputs["Scale"].default_value = 1.9; breakup.inputs["Detail"].default_value = 4.0; breakup.inputs["Roughness"].default_value = 0.55
    L(bvec.outputs[0], breakup.inputs["Vector"])
    br = _maprange(N, 0.46, 0.56)
    L(breakup.outputs["Fac"], br.inputs["Value"])
    fine = N("ShaderNodeTexNoise"); fine.noise_dimensions = "4D"
    fine.inputs["Scale"].default_value = 9.0; fine.inputs["Detail"].default_value = 8.0; fine.inputs["Roughness"].default_value = 0.65
    L(bvec.outputs[0], fine.inputs["Vector"])
    fr = _maprange(N, 0.35, 0.7, 0.45, 1.0)
    L(fine.outputs["Fac"], fr.inputs["Value"])
    m1 = _math(N, "MULTIPLY"); m2 = _math(N, "MULTIPLY"); m3 = _math(N, "MULTIPLY")
    dens = _math(N, "MULTIPLY", b=40.0)
    L(prof.outputs[0], m1.inputs[0]); L(zr.outputs["Result"], m1.inputs[1])
    L(m1.outputs[0], m2.inputs[0]); L(br.outputs["Result"], m2.inputs[1])
    L(m2.outputs[0], m3.inputs[0]); L(fr.outputs["Result"], m3.inputs[1])
    L(m3.outputs[0], dens.inputs[0])
    L(dens.outputs[0], vol.inputs["Density"])
    L(vol.outputs["Volume"], out.inputs["Volume"])
    mesh.materials.append(mat)
    # 시간: 반지름 0.12 → 0.9 (빠르게 퍼졌다 느려짐), 안쪽 꼬리 길어짐, 찢어짐 문턱 올라가며 사라짐
    for f, r, tail, b0, d, w in [
        (1, 0.12, 0.10, 0.30, 24.0, 0.0),
        (6, 0.38, 0.20, 0.34, 22.0, 0.2),
        (16, 0.60, 0.30, 0.40, 16.0, 0.6),
        (32, 0.76, 0.38, 0.48, 11.0, 1.1),
        (48, 0.85, 0.42, 0.56, 6.0, 1.5),
        (64, 0.90, 0.45, 0.66, 2.0, 1.9),
    ]:
        key(R.inputs[1], f, r)
        key(inner.inputs["From Min"], f, -tail)
        key(br.inputs["From Min"], f, b0)
        key(br.inputs["From Max"], f, b0 + 0.2)
        key(dens.inputs[1], f, d)
        for nz, k in ((warp, 1.0), (breakup, 1.3), (fine, 1.8)):
            key(nz.inputs["W"], f, w * k)
    print("ring scene ready")
    return sc
