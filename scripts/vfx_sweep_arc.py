# 창 휘두르기(spear_sweep): 회전 궤적 원호 프레임 시트 (위에서 내려다봄, 8x8 = 64칸, 칸 128px)
# 창이 도는 대로 빛의 날이 한 바퀴(위에서 보면 반시계) 그려지고, 앞 날은 날카롭게 희고 뒤는 초록 꼬리로 남았다가 흩어짐.
# 이미지 위쪽 = 시전자가 바라보는 방향(회전 시작), 반시계. 반지름 0.88 = 스킬 반경.
# ⚠ Roblox 눕힌 판(SurfaceGui Top)에서는 그림 오른쪽이 판 앞(-Z)으로 감(90° 돌아감, 뒤집힘 없음 — Studio 고정 칸으로 확인)
#   → Vfx.SpearSweep 이 판을 CFrame.lookAt(정면) * Angles(0, -90°, 0) 로 돌려 그림 위쪽을 정면에 맞춤
# 시간: 64칸 = 0.6초 (회전 0.35초 = 1~37칸, 나머지는 꼬리가 사그라듦). 발광만 써서 빠름.
# 실행(명령줄): D:\blender.exe -b --factory-startup --python-expr "exec(open(r'D:\god\scripts\vfx_sheet_kit.py', encoding='utf-8').read()); exec(open(r'D:\god\scripts\vfx_sweep_arc.py', encoding='utf-8').read()); render_sheet('SweepArc')"
import bpy
import math as pymath

FRAMES = 64
SPIN_END = 37  # 0.35 / 0.6 * 64 ≈ 37
GREEN = (0.22, 1.0, 0.38, 1)
GREEN_DARK = (0.04, 0.4, 0.1, 1)
WHITE = (1.0, 1.0, 0.96, 1)

# 기본 장면 비우기 (창 없이 명령줄로 돌 때)
for o in list(bpy.data.objects):
    bpy.data.objects.remove(o, do_unlink=True)

sc = vfx_scene("VFX_SweepArc", ortho_scale=2.0, cam_dir=(0, 0, 1))
sc.frame_start, sc.frame_end = 1, FRAMES
sc.cycles.samples = 8
# vfx_scene 의 위에서 보는 카메라는 180° 돌아가 있음(오른쪽 = -X) → 회전 없이(오른쪽 +X, 위 +Y) 바로 세움
sc.camera.rotation_euler = (0.0, 0.0, 0.0)

bpy.ops.mesh.primitive_plane_add(size=2.0)
plane = bpy.context.active_object
plane.name = "ArcPlane"

mat = bpy.data.materials.new("ArcMat")
mat.use_nodes = True
nt = mat.node_tree
for n in list(nt.nodes):
    nt.nodes.remove(n)
N = nt.nodes.new
L = nt.links.new


def m(op, a=None, b=None, clamp=False):
    node = N("ShaderNodeMath")
    node.operation = op
    node.use_clamp = clamp
    for i, v in enumerate((a, b)):
        if v is None:
            continue
        if isinstance(v, (int, float)):
            node.inputs[i].default_value = v
        else:
            L(v, node.inputs[i])
    return node.outputs[0]


def smooth(v, lo, hi):
    node = N("ShaderNodeMapRange")
    node.clamp = True
    node.interpolation_type = "SMOOTHSTEP"
    node.inputs["From Min"].default_value = lo
    node.inputs["From Max"].default_value = hi
    L(v, node.inputs["Value"])
    return node.outputs["Result"]


def value(v):
    node = N("ShaderNodeValue")
    node.outputs[0].default_value = v
    return node.outputs[0]


out = N("ShaderNodeOutputMaterial")
tc = N("ShaderNodeTexCoord")
obj = tc.outputs["Object"]
sep = N("ShaderNodeSeparateXYZ")
L(obj, sep.inputs[0])
x, y = sep.outputs["X"], sep.outputs["Y"]
ln = N("ShaderNodeVectorMath"); ln.operation = "LENGTH"; L(obj, ln.inputs[0])
r = ln.outputs["Value"]
theta = m("ARCTAN2", y, x)  # 반시계 +, 위쪽(+Y) = pi/2

# 앞 날 각도 phi (시간), 꼬리 길이 tail_len(라디안), 전체 세기 gain
phi = value(pymath.pi / 2)
tail_len = value(2.6)
gain = value(1.0)

# 앞 날에서 뒤로 잰 각 거리 delta = (phi - theta) mod 2pi  (0 = 앞 날, 클수록 오래전에 지나감)
delta = m("FLOORED_MODULO", m("SUBTRACT", phi, theta), 2 * pymath.pi)
# 아직 안 지나간 곳(delta 가 꼬리보다 큼)은 0
k = m("DIVIDE", delta, tail_len)
tail = m("POWER", m("SUBTRACT", 1.0, k, clamp=True), 2.2)
# 회전 시작 전 자리(시작 방향보다 오른쪽, 아직 창이 안 지나감)는 꼬리에서 뺌: delta <= 지금까지 돈 각도
swept = m("SUBTRACT", phi, pymath.pi / 2)
tail = m("MULTIPLY", tail, m("LESS_THAN", delta, m("ADD", swept, 0.02)))
blade = m("POWER", m("SUBTRACT", 1.0, m("DIVIDE", delta, 0.16), clamp=True), 3.0)

# 반지름 모양 (1차는 가운데까지 꽉 찬 부채꼴이라 밋밋 → 바깥 띠에 몰리게):
#   band = 창날이 지나가는 바깥 띠(0.5~0.98, 0.85 근처가 가장 진함), haze = 안쪽 옅은 바람(0.25~0.6)
band = m("MULTIPLY", smooth(r, 0.48, 0.82), m("SUBTRACT", 1.0, smooth(r, 0.93, 0.995)))
haze = m("MULTIPLY", m("MULTIPLY", smooth(r, 0.22, 0.45), m("SUBTRACT", 1.0, smooth(r, 0.5, 0.72))), 0.18)
radial = m("ADD", band, haze)
rim = m("POWER", m("SUBTRACT", 1.0, m("DIVIDE", m("ABSOLUTE", m("SUBTRACT", r, 0.88)), 0.05), clamp=True), 2.0)

# 동심 줄무늬: 반지름 따라 노이즈 (꼬리 안에 바람 결) — 시간에 따라 조금 흐름
streak_n = N("ShaderNodeTexNoise")
streak_n.noise_dimensions = "2D"
streak_n.inputs["Scale"].default_value = 1.0
streak_n.inputs["Detail"].default_value = 3.0
streak_vec = N("ShaderNodeCombineXYZ")
L(m("MULTIPLY", r, 14.0), streak_vec.inputs["X"])
L(m("MULTIPLY", delta, 0.35), streak_vec.inputs["Y"])
L(streak_vec.outputs[0], streak_n.inputs["Vector"])
streaks = smooth(streak_n.outputs["Fac"], 0.42, 0.78)

# 꼬리는 결(바람 줄)로 끊기며 뒤로 갈수록 빨리 옅어짐, 앞 날은 짧고 하얗게, 테두리 선은 꼬리를 따라 조금 더 남음
tail3 = m("POWER", tail, 1.6)
tail_i = m("MULTIPLY", m("MULTIPLY", tail3, radial), m("ADD", 0.25, m("MULTIPLY", streaks, 0.9)))
tail_i = m("MULTIPLY", tail_i, 1.15)  # 2차: 0.7 은 꼬리가 거의 안 보임
blade_i = m("MULTIPLY", blade, m("ADD", m("MULTIPLY", band, 0.9), m("MULTIPLY", rim, 1.3)))
rim_i = m("MULTIPLY", m("MULTIPLY", rim, tail), 0.8)
inten = m("ADD", m("ADD", tail_i, blade_i), rim_i)
inten = m("MULTIPLY", inten, gain, clamp=True)

ramp = N("ShaderNodeValToRGB")
els = ramp.color_ramp.elements
els[0].position = 0.0; els[0].color = (0.08, 0.75, 0.25, 1)  # 옅은 꼬리도 초록으로 (회색빛 방지)
els[1].position = 1.0; els[1].color = WHITE
e2 = els.new(0.3); e2.color = GREEN
e3 = els.new(0.72); e3.color = (0.78, 1.0, 0.8, 1)
L(inten, ramp.inputs["Fac"])
emit = N("ShaderNodeEmission"); emit.inputs["Strength"].default_value = 1.0
L(ramp.outputs["Color"], emit.inputs["Color"])
transp = N("ShaderNodeBsdfTransparent")
mix = N("ShaderNodeMixShader")
L(inten, mix.inputs["Fac"])
L(transp.outputs[0], mix.inputs[1])
L(emit.outputs[0], mix.inputs[2])
L(mix.outputs[0], out.inputs["Surface"])
plane.data.materials.append(mat)


def key(sock, frame, v):
    sock.default_value = v
    sock.keyframe_insert("default_value", frame=frame)


# 회전: 1~SPIN_END 칸 동안 phi 가 pi/2 → pi/2 + 2pi (일정 속도), 그 뒤 조금 더 돌며 감속
key(phi, 1, pymath.pi / 2)
key(phi, SPIN_END, pymath.pi / 2 + 2 * pymath.pi)
key(phi, FRAMES, pymath.pi / 2 + 2 * pymath.pi + 0.5)
# 꼬리: 회전 중 약 150°, 끝나면 짧아짐 / 세기: 회전 끝 뒤 사그라듦
for f, tl, g in [(1, 2.6, 1.0), (SPIN_END, 2.6, 1.0), (SPIN_END + 10, 1.8, 0.7), (FRAMES, 0.6, 0.0)]:
    key(tail_len, f, tl)
    key(gain, f, g)
# phi 는 회전 구간을 일정 속도로 (기본 베지어면 시작·끝이 느려져 판정 시각과 어긋남)
def all_fcurves(action):
    fcs = list(getattr(action, "fcurves", []) or [])
    for layer in getattr(action, "layers", []):  # Blender 4.4+ 레이어 액션
        for strip in layer.strips:
            for bag in getattr(strip, "channelbags", []):
                fcs.extend(bag.fcurves)
    return fcs


ad = nt.animation_data
n_lin = 0
if ad and ad.action:
    for fc in all_fcurves(ad.action):
        for kp in fc.keyframe_points:
            kp.interpolation = "LINEAR"
            n_lin += 1
print("linear keys:", n_lin)
print("sweep arc scene ready")
