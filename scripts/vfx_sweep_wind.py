# 창 휘두르기(spear_sweep): 몸을 감는 바람 띠(Beam)용 결 텍스처 한 장 (1024x256, 흰색 + 알파, 색은 Roblox Beam.Color 로)
# 2026-11-24 사용자: "바닥에만 깔려 옆에서 보면 입체감 없음, 몸 주변에도 / 뚝뚝 끊기면 안 됨"
#   → 시트(플립북) 대신 Beam 마디를 매 프레임 옮기는 방식. 마디 이음매가 안 보이게 결은 가로(리본 방향)로 긴 줄 위주,
#     가로로 이어 붙여도 이음매 없게(가로 좌표를 원 둘레로 써서 노이즈가 한 바퀴에 맞물림).
#   - 세로: 위·아래 가장자리로 갈수록 옅고 들쭉날쭉(바람 가장자리), 가운데 굵은 줄 몇 개 + 가는 줄 여러 개
# 실행: D:\blender.exe -b --factory-startup --python-expr "exec(open(r'D:\god\scripts\vfx_sheet_kit.py', encoding='utf-8').read()); exec(open(r'D:\god\scripts\vfx_sweep_wind.py', encoding='utf-8').read())"
import bpy
import os
import math as pymath

W, H = 1024, 256

for o in list(bpy.data.objects):
    bpy.data.objects.remove(o, do_unlink=True)

sc = vfx_scene("VFX_SweepWind", ortho_scale=4.0, cam_dir=(0, 0, 1))
sc.cycles.samples = 16
sc.camera.rotation_euler = (0.0, 0.0, 0.0)  # 오른쪽 +X, 위 +Y
sc.render.resolution_x, sc.render.resolution_y = W, H
sc.render.resolution_percentage = 100

bpy.ops.mesh.primitive_plane_add(size=1.0)
plane = bpy.context.active_object
plane.scale = (4.0, 1.0, 1.0)  # 가로 4 x 세로 1 (카메라 폭 4 = 1024, 높이 1 = 256)
bpy.ops.object.transform_apply(scale=True)

mat = bpy.data.materials.new("WindMat")
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


def noise4(xs, ys, zs, w, scale, detail, rough=0.55):
    vec = N("ShaderNodeCombineXYZ")
    for sock, val in ((vec.inputs["X"], xs), (vec.inputs["Y"], ys), (vec.inputs["Z"], zs)):
        if isinstance(val, (int, float)):
            sock.default_value = val
        else:
            L(val, sock)
    n = N("ShaderNodeTexNoise")
    n.noise_dimensions = "4D"
    n.inputs["Scale"].default_value = scale
    n.inputs["Detail"].default_value = detail
    n.inputs["Roughness"].default_value = rough
    n.inputs["W"].default_value = w
    L(vec.outputs[0], n.inputs["Vector"])
    return n.outputs["Fac"]


out = N("ShaderNodeOutputMaterial")
tc = N("ShaderNodeTexCoord")
sep = N("ShaderNodeSeparateXYZ")
L(tc.outputs["Object"], sep.inputs[0])
x, y = sep.outputs["X"], sep.outputs["Y"]  # x -2..2, y -0.5..0.5
v = m("ADD", y, 0.5)  # 0 아래 → 1 위
# 가로를 원 둘레로: 이음매 없이 반복
ang = m("MULTIPLY", m("ADD", x, 2.0), pymath.pi / 2.0)  # 0..2pi
cx = m("COSINE", ang)
cy = m("SINE", ang)

# 가는 줄: 세로 방향으로 촘촘(v*스케일 큼), 가로로 길게(원 둘레 반지름 작게)
fine = noise4(m("MULTIPLY", cx, 0.9), m("MULTIPLY", cy, 0.9), m("MULTIPLY", v, 38.0), 1.3, 1.0, 4.0)
fine = smooth(fine, 0.45, 0.72)
# 굵은 줄: 덜 촘촘, 더 밝음
thick = noise4(m("MULTIPLY", cx, 0.6), m("MULTIPLY", cy, 0.6), m("MULTIPLY", v, 11.0), 7.7, 1.0, 2.0)
thick = smooth(thick, 0.5, 0.68)
# 줄 밝기가 가로로 천천히 달라짐 (끊김 없이 길게)
along = noise4(m("MULTIPLY", cx, 1.4), m("MULTIPLY", cy, 1.4), 3.0, 2.2, 1.0, 3.0)
along = smooth(along, 0.3, 0.7)
streak = m("ADD", m("MULTIPLY", fine, 0.55), m("MULTIPLY", thick, 0.9))
streak = m("MULTIPLY", streak, m("ADD", 0.45, m("MULTIPLY", along, 0.75)))
# 위·아래 가장자리: 옅어지며 들쭉날쭉
edge_n = noise4(m("MULTIPLY", cx, 2.0), m("MULTIPLY", cy, 2.0), 5.0, 4.4, 1.0, 4.0)
dv = m("ABSOLUTE", m("SUBTRACT", v, 0.5))
dv = m("ADD", dv, m("MULTIPLY", m("SUBTRACT", edge_n, 0.5), 0.16))
edge = m("SUBTRACT", 1.0, smooth(dv, 0.18, 0.47))
alpha = m("MULTIPLY", m("MULTIPLY", streak, edge), 1.15, clamp=True)
# 가운데는 옅은 바탕 빛 (리본 몸통이 비어 보이지 않게)
alpha = m("ADD", alpha, m("MULTIPLY", m("SUBTRACT", 1.0, smooth(dv, 0.05, 0.4)), 0.12), clamp=True)

emit = N("ShaderNodeEmission")
emit.inputs["Color"].default_value = (1, 1, 1, 1)
emit.inputs["Strength"].default_value = 1.0
transp = N("ShaderNodeBsdfTransparent")
mix = N("ShaderNodeMixShader")
L(alpha, mix.inputs["Fac"])
L(transp.outputs[0], mix.inputs[1])
L(emit.outputs[0], mix.inputs[2])
L(mix.outputs[0], out.inputs["Surface"])
plane.data.materials.append(mat)

path = os.path.join(EXPORT_DIR, "SweepWind.png")
sc.render.filepath = path
bpy.ops.render.render(write_still=True)
print("wind texture saved:", path)
