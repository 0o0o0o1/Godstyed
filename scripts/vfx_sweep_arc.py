# 창 휘두르기(spear_sweep): 회전 궤적 원호 프레임 시트 v3 (위에서 내려다봄, 8x8 = 64칸, 칸 128px)
# 2026-11-24 사용자 참고 이미지(언리얼 회전 베기, 불꽃색) 스타일로 다시: 색만 흰+초록.
#   - 앞머리가 굵고 하얗게 타는 심(core) → 뒤로 갈수록 가늘어지고 붓질 결이 끊기며 갈라져(침식) 사라지는 초승달
#   - 결 = 원을 따라 길게 늘어난 붓질(길이·굵기 제각각) — v2 의 같은 간격 동심 줄무늬(레코드판 같음, AI티) 대신
#   - 겹: 바깥에 옅고 넓은 테(가장자리가 타 들어간 종이처럼 들쭉날쭉) + 안쪽 옅은 바람 테 → 판 한 장이어도 두께감
#   - 회전 속도: 처음 빠르고 끝에 느려짐(ease-out quad). 서버 판정(Skill.spinHits)·몸 회전(Vfx.SpearSweep)과 같은 식:
#       돈 각도 = 2pi * (1 - (1 - k)^2), k = 회전 경과 비율
# 이미지 위쪽 = 시전자가 바라보는 방향(회전 시작), 반시계. 반지름 0.86 = 스킬 반경(앞머리 심).
# ⚠ Roblox 눕힌 판(SurfaceGui Top)에서는 그림 오른쪽이 판 앞(-Z)으로 감(90° 돌아감) → Vfx.SpearSweep 이 판을 -90° 돌림
# 시간: 64칸 = 0.6초 (회전 0.35초 = 1~37칸, 나머지는 꼬리가 갈라지며 사그라듦). 발광만 써서 빠름.
# 실행(명령줄): D:\blender.exe -b --factory-startup --python-expr "exec(open(r'D:\god\scripts\vfx_sheet_kit.py', encoding='utf-8').read()); exec(open(r'D:\god\scripts\vfx_sweep_arc.py', encoding='utf-8').read()); render_sheet('SweepArc')"
import bpy
import math as pymath

FRAMES = 64
SPIN_END = 37  # 0.35 / 0.6 * 64 ≈ 37
RC = 0.86  # 앞머리 심 반지름 (= 스킬 반경)

for o in list(bpy.data.objects):
    bpy.data.objects.remove(o, do_unlink=True)

sc = vfx_scene("VFX_SweepArc", ortho_scale=2.0, cam_dir=(0, 0, 1))
sc.frame_start, sc.frame_end = 1, FRAMES
sc.cycles.samples = 8
sc.camera.rotation_euler = (0.0, 0.0, 0.0)  # 오른쪽 +X, 위 +Y

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
    """lo 이하 0 → hi 이상 1. lo, hi 는 숫자 또는 소켓"""
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

# 시간 값: 앞머리 각도 phi, 꼬리 길이 tail_len, 침식 erode(0 → 1 이면 다 갈라져 없어짐), 전체 세기 gain
phi = value(pymath.pi / 2)
tail_len = value(3.0)
erode = value(0.0)
gain = value(1.0)

delta = m("FLOORED_MODULO", m("SUBTRACT", phi, theta), 2 * pymath.pi)  # 0 = 앞머리
swept = m("SUBTRACT", phi, pymath.pi / 2)
seen = m("LESS_THAN", delta, m("ADD", swept, 0.02))  # 창이 지나간 곳만
k = m("DIVIDE", delta, tail_len)  # 0 앞머리 → 1 꼬리 끝
alive = m("MULTIPLY", m("SUBTRACT", 1.0, k, clamp=True), seen)
# 앞머리 끝을 칼로 자른 듯 딱 끊기지 않게 아주 짧게 번짐 (~3°)
alive = m("MULTIPLY", alive, smooth(delta, 0.0, 0.05))

# 붓질 결: 원을 따라 길게 늘인 노이즈 (반지름 방향은 촘촘, 각 방향은 길게) — 두 겹을 섞어 길이·굵기 제각각
s1 = noise2(m("MULTIPLY", r, 34.0), m("MULTIPLY", delta, 1.1), detail=5.0)
s2 = noise2(m("ADD", m("MULTIPLY", r, 13.0), 7.3), m("MULTIPLY", delta, 0.55), detail=3.0)
strokes = m("ADD", 0.35, m("MULTIPLY", m("MULTIPLY", smooth(s1, 0.36, 0.7), m("ADD", 0.45, m("MULTIPLY", smooth(s2, 0.35, 0.7), 0.8))), 0.9))

# 침식(갈라짐): 큰 덩어리 노이즈가 꼬리 쪽부터, 시간이 지날수록(erode) 문턱을 넘어 구멍 남
e_n = noise2(m("MULTIPLY", r, 7.0), m("MULTIPLY", delta, 2.4), detail=6.0, rough=0.65)
thresh = m("ADD", m("MULTIPLY", m("POWER", k, 1.6), 0.5), m("MULTIPLY", erode, 0.75))
eroded = smooth(e_n, m("SUBTRACT", thresh, 0.04), m("ADD", thresh, 0.06))

# ① 주 초승달: 앞머리에서 굵고(반폭 0.13) 꼬리로 가늘어짐(0.03), 가장자리는 결에 따라 들쭉날쭉
half = m("ADD", 0.045, m("MULTIPLY", m("POWER", m("SUBTRACT", 1.0, k, clamp=True), 1.3), 0.15))  # v3a 0.03+0.10 은 너무 가늘었음
dr = m("ABSOLUTE", m("SUBTRACT", r, RC))
edge_wobble = m("MULTIPLY", m("SUBTRACT", s2, 0.5), 0.05)
band = m("SUBTRACT", 1.0, smooth(m("ADD", dr, edge_wobble), m("MULTIPLY", half, 0.35), half))
main = m("MULTIPLY", m("MULTIPLY", band, alive), m("MULTIPLY", strokes, eroded))
main = m("MULTIPLY", main, m("ADD", 0.55, m("MULTIPLY", m("POWER", m("SUBTRACT", 1.0, k, clamp=True), 1.2), 1.1)))

# ② 하얀 심: 앞머리 ~30° 안, 띠 가운데
head = m("POWER", m("SUBTRACT", 1.0, m("DIVIDE", delta, 0.55), clamp=True), 2.2)
core_band = m("SUBTRACT", 1.0, smooth(dr, 0.0, m("MULTIPLY", half, 0.55)))
core = m("MULTIPLY", m("MULTIPLY", head, core_band), m("MULTIPLY", seen, 1.4))

# ③ 바깥 옅은 테 (0.93~1.0): 넓게 번진 빛, 가장자리는 타 들어간 종이처럼 들쭉날쭉
o_n = noise2(m("MULTIPLY", r, 5.0), m("MULTIPLY", delta, 1.6), detail=6.0, rough=0.7)
outer_r = m("MULTIPLY", smooth(r, 0.9, 0.94), m("SUBTRACT", 1.0, smooth(m("ADD", r, m("MULTIPLY", m("SUBTRACT", o_n, 0.5), 0.08)), 0.96, 0.995)))
outer = m("MULTIPLY", m("MULTIPLY", outer_r, alive), m("MULTIPLY", smooth(o_n, m("ADD", 0.3, m("MULTIPLY", erode, 0.5)), m("ADD", 0.45, m("MULTIPLY", erode, 0.5))), 0.5))

# ④ 안쪽 옅은 바람 테 (0.5~0.72): 결만 살짝
inner_r = m("MULTIPLY", smooth(r, 0.48, 0.58), m("SUBTRACT", 1.0, smooth(r, 0.64, 0.74)))
inner = m("MULTIPLY", m("MULTIPLY", inner_r, alive), m("MULTIPLY", m("MULTIPLY", strokes, eroded), 0.3))

inten = m("ADD", m("ADD", main, core), m("ADD", outer, inner))
inten = m("MULTIPLY", inten, gain, clamp=True)

ramp = N("ShaderNodeValToRGB")
els = ramp.color_ramp.elements
els[0].position = 0.0; els[0].color = (0.03, 0.42, 0.14, 1)   # 짙은 초록 (옅은 테·꼬리 끝)
els[1].position = 1.0; els[1].color = (1.0, 1.0, 0.97, 1)     # 하얀 심
e2 = els.new(0.28); e2.color = (0.12, 0.9, 0.32, 1)           # 초록
e3 = els.new(0.62); e3.color = (0.55, 1.0, 0.62, 1)           # 밝은 연두
e4 = els.new(0.85); e4.color = (0.86, 1.0, 0.88, 1)
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


# 회전: ease-out quad (처음 빠르고 끝에 느림) — 12구간 선형 키로 근사
STEPS = 12
for i in range(STEPS + 1):
    kk = i / STEPS
    f = 1 + (SPIN_END - 1) * kk
    key(phi, f, pymath.pi / 2 + 2 * pymath.pi * (1 - (1 - kk) ** 2))
key(phi, FRAMES, pymath.pi / 2 + 2 * pymath.pi + 0.35)  # 끝난 뒤 아주 조금 더 밀림
# 꼬리 길이·침식·세기
for f, tl, er, g in [(1, 3.0, 0.0, 1.0), (SPIN_END, 3.2, 0.05, 1.0), (SPIN_END + 9, 3.0, 0.25, 0.95), (FRAMES - 6, 2.6, 0.7, 0.55), (FRAMES, 2.4, 1.0, 0.0)]:
    key(tail_len, f, tl)
    key(erode, f, er)
    key(gain, f, g)


def all_fcurves(action):
    fcs = list(getattr(action, "fcurves", []) or [])
    for layer in getattr(action, "layers", []):
        for strip in layer.strips:
            for bag in getattr(strip, "channelbags", []):
                fcs.extend(bag.fcurves)
    return fcs


ad = nt.animation_data
if ad and ad.action:
    for fc in all_fcurves(ad.action):
        for kp in fc.keyframe_points:
            kp.interpolation = "LINEAR"
print("sweep arc v3 scene ready")
