# 도약 찌르기: 바닥 충격파 고리 프레임 시트 (위에서 내려다봄, 8x8 = 64칸, 칸 128px)
# 날카롭게 밝은 앞쪽 가장자리(흰) + 뒤로 길게 끌리는 초록 기운, 둘레를 따라 밝기가 들쭉날쭉,
# 기운 안에 바깥으로 뻗는 방사 줄기. 발광만 써서 빠름. Roblox 에선 바닥에 눕힌 판에서 칸을 넘겨 재생.
# 먼저 vfx_sheet_kit.py 를 exec 한 뒤 실행.
import bpy

FRAMES = 64
GREEN = (0.22, 1.0, 0.38, 1)
GREEN_DARK = (0.05, 0.45, 0.12, 1)
WHITE = (1.0, 1.0, 0.96, 1)

sc = vfx_scene("VFX_LeapShock", ortho_scale=2.0, cam_dir=(0, 0, 1))
sc.frame_start, sc.frame_end = 1, FRAMES
sc.cycles.samples = 8

bpy.ops.mesh.primitive_plane_add(size=2.0)
plane = bpy.context.active_object
plane.name = "ShockPlane"

mat = bpy.data.materials.new("ShockMat")
mat.use_nodes = True
nt = mat.node_tree
for n in list(nt.nodes):
    nt.nodes.remove(n)
N = nt.nodes.new
L = nt.links.new


def math(op, a=None, b=None, clamp=False):
    m = N("ShaderNodeMath")
    m.operation = op
    m.use_clamp = clamp
    for i, v in enumerate((a, b)):
        if v is None:
            continue
        if isinstance(v, (int, float)):
            m.inputs[i].default_value = v
        else:
            L(v, m.inputs[i])
    return m.outputs[0]


def maprange(v, fmin, fmax, tmin=0.0, tmax=1.0, smooth=False):
    m = N("ShaderNodeMapRange")
    m.clamp = True
    if smooth:
        m.interpolation_type = "SMOOTHSTEP"
    m.inputs["From Min"].default_value = fmin
    m.inputs["From Max"].default_value = fmax
    m.inputs["To Min"].default_value = tmin
    m.inputs["To Max"].default_value = tmax
    L(v, m.inputs["Value"])
    return m


def noise4(vec, scale, detail, rough=0.55):
    n = N("ShaderNodeTexNoise")
    n.noise_dimensions = "4D"
    n.inputs["Scale"].default_value = scale
    n.inputs["Detail"].default_value = detail
    n.inputs["Roughness"].default_value = rough
    L(vec, n.inputs["Vector"])
    return n


out = N("ShaderNodeOutputMaterial")
tc = N("ShaderNodeTexCoord")
obj = tc.outputs["Object"]
ln = N("ShaderNodeVectorMath"); ln.operation = "LENGTH"; L(obj, ln.inputs[0])
r = ln.outputs["Value"]
nrm = N("ShaderNodeVectorMath"); nrm.operation = "NORMALIZE"; L(obj, nrm.inputs[0])
ang = nrm.outputs["Vector"]  # 각도만의 함수 (방사 무늬용)

# 가장자리 일렁임
wob_n = noise4(obj, 3.2, 5.0)
wob_amp = N("ShaderNodeValue"); wob_amp.outputs[0].default_value = 0.05
rr = math("ADD", r, math("MULTIPLY", math("SUBTRACT", wob_n.outputs["Fac"], 0.5), wob_amp.outputs[0]))

Rv = N("ShaderNodeValue"); Rv.outputs[0].default_value = 0.3  # 반지름
d = math("SUBTRACT", rr, Rv.outputs[0])  # + 바깥 / - 안쪽
win = N("ShaderNodeValue"); win.outputs[0].default_value = 0.3  # 안쪽 꼬리 길이
wout = N("ShaderNodeValue"); wout.outputs[0].default_value = 0.025  # 바깥 날 두께
# 바깥: 1 - d/wout (d>=0) / 안쪽: 1 + d/win (d<0)
outside = math("SUBTRACT", 1.0, math("DIVIDE", d, wout.outputs[0]), clamp=True)
inside = math("ADD", 1.0, math("DIVIDE", d, win.outputs[0]), clamp=True)
is_in = math("LESS_THAN", d, 0.0)
is_out = math("SUBTRACT", 1.0, is_in)
edge = math("ADD", math("MULTIPLY", outside, is_out), math("MULTIPLY", math("POWER", inside, 2.5), is_in))
# 날(가장 밝은 선): edge^6
blade = math("POWER", edge, 6.0)
# 꼬리 기운: edge 가 낮은 부분까지 (edge^1.5 * 0.55)
tail = math("MULTIPLY", math("POWER", edge, 1.5), 0.55)

# 둘레 밝기 들쭉날쭉 + 방사 줄기
arc_n = noise4(ang, 2.2, 2.0)
arc = maprange(arc_n.outputs["Fac"], 0.32, 0.68, 0.35, 1.0).outputs["Result"]
ray_n = noise4(ang, 14.0, 1.0, 0.4)
rays = maprange(ray_n.outputs["Fac"], 0.55, 0.72, 0.0, 1.0, smooth=True).outputs["Result"]
tail_rays = math("MULTIPLY", tail, math("ADD", 0.45, math("MULTIPLY", rays, 1.1)))

inten = math("MULTIPLY", math("ADD", blade, tail_rays), arc, clamp=False)
gain = N("ShaderNodeValue"); gain.outputs[0].default_value = 1.0  # 전체 세기 (시간)
inten = math("MULTIPLY", inten, gain.outputs[0], clamp=True)

ramp = N("ShaderNodeValToRGB")
els = ramp.color_ramp.elements
els[0].position = 0.0; els[0].color = GREEN_DARK
els[1].position = 1.0; els[1].color = WHITE
e2 = els.new(0.45); e2.color = GREEN
e3 = els.new(0.8); e3.color = (0.75, 1.0, 0.78, 1)
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


def key(sock, frame, value):
    sock.default_value = value
    sock.keyframe_insert("default_value", frame=frame)


# 앞 10프레임에 빠르게 퍼지고 점점 느려짐, 꼬리는 길어졌다 얇아짐, 끝에 옅어짐
for f, R, wi, wo, g, wob, t in [
    (1, 0.05, 0.05, 0.02, 1.0, 0.02, 0.0),
    (5, 0.34, 0.22, 0.03, 1.0, 0.04, 0.3),
    (12, 0.55, 0.32, 0.028, 1.0, 0.06, 0.7),
    (26, 0.72, 0.30, 0.022, 0.75, 0.08, 1.2),
    (44, 0.81, 0.22, 0.016, 0.35, 0.09, 1.7),
    (64, 0.85, 0.15, 0.012, 0.0, 0.1, 2.1),
]:
    key(Rv.outputs[0], f, R)
    key(win.outputs[0], f, wi)
    key(wout.outputs[0], f, wo)
    key(gain.outputs[0], f, g)
    key(wob_amp.outputs[0], f, wob)
    for n in (wob_n, arc_n, ray_n):
        key(n.inputs["W"], f, t)
print("shock scene ready")
