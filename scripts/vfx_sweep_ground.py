# 창 휘두르기(spear_sweep): 바닥 바람 물결 프레임 시트 (위에서 내려다봄, 8x8 = 64칸, 칸 128px)
# 참고 이미지(언리얼 회전 베기)의 바닥에 남는 옅은 물결 고리를 흰+초록으로. 도약 찌르기 충격파 시트 재사용(같은 착지감, AI티) 대신.
#   - 얇은 물결 고리 3개가 시차를 두고 안쪽에서 바깥으로 번짐(처음 빠르고 점점 느림), 고리는 노이즈로 군데군데 끊김
#   - 고리 안쪽은 옅은 바람 연무가 결을 따라 쓸려 나가며 흩어짐
# 둥근 모양이라 방향은 상관없음. 시간 64칸 = 0.7초. 발광만.
# 실행: D:\blender.exe -b --factory-startup --python-expr "exec(open(r'D:\god\scripts\vfx_sheet_kit.py', encoding='utf-8').read()); exec(open(r'D:\god\scripts\vfx_sweep_ground.py', encoding='utf-8').read()); render_sheet('SweepGround')"
import bpy
import math as pymath

FRAMES = 64

for o in list(bpy.data.objects):
    bpy.data.objects.remove(o, do_unlink=True)

sc = vfx_scene("VFX_SweepGround", ortho_scale=2.0, cam_dir=(0, 0, 1))
sc.frame_start, sc.frame_end = 1, FRAMES
sc.cycles.samples = 8
sc.camera.rotation_euler = (0.0, 0.0, 0.0)

bpy.ops.mesh.primitive_plane_add(size=2.0)
plane = bpy.context.active_object
mat = bpy.data.materials.new("GroundMat")
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
    for name, val in (("From Min", lo), ("From Max", hi)):
        if isinstance(val, (int, float)):
            node.inputs[name].default_value = val
        else:
            L(val, node.inputs[name])
    L(v, node.inputs["Value"])
    return node.outputs["Result"]


def value(v):
    node = N("ShaderNodeValue")
    node.outputs[0].default_value = v
    return node.outputs[0]


def noise2(xs, ys, scale=1.0, detail=4.0, rough=0.55):
    vec = N("ShaderNodeCombineXYZ")
    L(xs, vec.inputs["X"])
    L(ys, vec.inputs["Y"])
    n = N("ShaderNodeTexNoise")
    n.noise_dimensions = "2D"
    n.inputs["Scale"].default_value = scale
    n.inputs["Detail"].default_value = detail
    n.inputs["Roughness"].default_value = rough
    L(vec.outputs[0], n.inputs["Vector"])
    return n.outputs["Fac"]


out = N("ShaderNodeOutputMaterial")
tc = N("ShaderNodeTexCoord")
obj = tc.outputs["Object"]
sep = N("ShaderNodeSeparateXYZ")
L(obj, sep.inputs[0])
x, y = sep.outputs["X"], sep.outputs["Y"]
ln = N("ShaderNodeVectorMath"); ln.operation = "LENGTH"; L(obj, ln.inputs[0])
r = ln.outputs["Value"]
theta = m("ARCTAN2", y, x)
# 각도를 원 둘레 좌표로 (cos, sin) 써서 노이즈 이음매 없게
ux = m("COSINE", theta)
uy = m("SINE", theta)

swirl = value(0.0)  # 결이 쓸려 도는 정도 (시간)


def ring(radius_sock, alpha_sock, width, seed):
    """얇은 고리: 반지름 radius, 두께 width, 노이즈로 군데군데 끊김"""
    n = noise2(m("ADD", m("MULTIPLY", ux, 2.6), seed), m("ADD", m("MULTIPLY", uy, 2.6), m("MULTIPLY", swirl, 0.4)), detail=4.0)
    wob = m("MULTIPLY", m("SUBTRACT", n, 0.5), 0.05)
    d = m("ABSOLUTE", m("SUBTRACT", m("ADD", r, wob), radius_sock))
    body = m("SUBTRACT", 1.0, smooth(d, width * 0.2, width))
    # 끊김: 1차는 고른 점선처럼 보여(AI티) → 낮은 주파수 노이즈로 긴 호 몇 개 + 불규칙한 틈, 두께도 둘레 따라 달라짐
    nb = noise2(m("ADD", m("MULTIPLY", ux, 1.1), seed * 1.9), m("ADD", m("MULTIPLY", uy, 1.1), seed), detail=2.0, rough=0.4)
    breaks = smooth(nb, 0.36, 0.5)
    thick = m("ADD", 0.45, m("MULTIPLY", smooth(n, 0.3, 0.7), 0.75))
    return m("MULTIPLY", m("MULTIPLY", m("MULTIPLY", body, breaks), thick), alpha_sock)


rings = []
ring_vals = []
for i, (w, seed) in enumerate([(0.035, 0.0), (0.025, 3.7), (0.05, 8.1)]):
    R = value(0.3)
    A = value(0.0)
    ring_vals.append((R, A))
    rings.append(ring(R, A, w, seed))
total = m("ADD", m("ADD", rings[0], rings[1]), rings[2])

# 안쪽 바람 연무: 결(원 둘레를 따라 늘어난 노이즈)이 쓸려 돌며 옅어짐
hz_n = noise2(m("ADD", m("MULTIPLY", ux, 1.4), m("MULTIPLY", r, 6.0)), m("ADD", m("MULTIPLY", uy, 1.4), swirl), detail=5.0, rough=0.6)
haze_r = value(0.6)
haze_a = value(0.0)
haze = m("MULTIPLY", m("MULTIPLY", m("SUBTRACT", 1.0, smooth(r, m("MULTIPLY", haze_r, 0.6), haze_r)), smooth(r, 0.1, 0.35)), smooth(hz_n, 0.45, 0.75))
total = m("ADD", total, m("MULTIPLY", haze, haze_a))
total = m("MULTIPLY", total, 1.0, clamp=True)

ramp = N("ShaderNodeValToRGB")
els = ramp.color_ramp.elements
els[0].position = 0.0; els[0].color = (0.25, 0.8, 0.4, 1)
els[1].position = 1.0; els[1].color = (0.95, 1.0, 0.96, 1)
e2 = els.new(0.5); e2.color = (0.6, 1.0, 0.7, 1)
L(total, ramp.inputs["Fac"])
emit = N("ShaderNodeEmission"); emit.inputs["Strength"].default_value = 1.0
L(ramp.outputs["Color"], emit.inputs["Color"])
transp = N("ShaderNodeBsdfTransparent")
mix = N("ShaderNodeMixShader")
L(m("MULTIPLY", total, 0.75), mix.inputs["Fac"])  # 바닥 물결이라 전체적으로 옅게
L(transp.outputs[0], mix.inputs[1])
L(emit.outputs[0], mix.inputs[2])
L(mix.outputs[0], out.inputs["Surface"])
plane.data.materials.append(mat)


def key(sock, frame, v):
    sock.default_value = v
    sock.keyframe_insert("default_value", frame=frame)


# 고리 3개: 시작 칸·끝 반지름이 조금씩 다름, ease-out 으로 번지며 옅어짐
for (R, A), (start, r0, r1, a0) in zip(ring_vals, [(1, 0.32, 0.98, 0.9), (8, 0.3, 0.86, 0.75), (16, 0.28, 0.74, 0.55)]):
    span = FRAMES - start
    for j in range(9):
        t = j / 8
        f = start + span * t
        key(R, f, r0 + (r1 - r0) * (1 - (1 - t) ** 2.4))
        key(A, f, a0 * (min(1.0, t * 6.0)) * (1 - t) ** 1.3)
    if start > 1:
        key(A, 1, 0.0)
for f, hr, ha, sw in [(1, 0.35, 0.0, 0.0), (6, 0.6, 0.55, 0.6), (24, 0.85, 0.35, 2.0), (FRAMES, 1.0, 0.0, 3.6)]:
    key(haze_r, f, hr)
    key(haze_a, f, ha)
    key(swirl, f, sw)
print("sweep ground scene ready")
