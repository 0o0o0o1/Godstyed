# 빛의 창 재질: 꼭짓점 값 "Glow"(날 끝·고리 = 1) + 창날 가운데 룬 띠 → 발광 마스크, 자루 위로 갈수록 투명
# 미리보기 재질(LanceMat)과 굽기용 출력 두 가지를 한 노드 트리에 둠: Base Color / Alpha / Emission 마스크
# vfx_leap_lance.py 다음에 실행.
import bpy, math
from mathutils import Vector

sc = bpy.data.scenes["VFX_LeapLance"]
obj = sc.objects["LightLance"]
me = obj.data

BLADE = [(0.0, 0.0), (0.35, 0.16), (1.0, 0.42), (2.0, 0.72), (3.1, 0.92), (4.1, 0.96), (5.0, 0.82), (5.8, 0.55), (6.4, 0.34)]


def half_width(z):
    for (z0, w0), (z1, w1) in zip(BLADE, BLADE[1:]):
        if z0 <= z <= z1:
            return w0 + (w1 - w0) * (z - z0) / max(z1 - z0, 1e-6)
    return 0.34


# 꼭짓점 발광 값
if "Glow" in me.color_attributes:
    me.color_attributes.remove(me.color_attributes["Glow"])
attr = me.color_attributes.new("Glow", "FLOAT_COLOR", "POINT")
for v in me.vertices:
    x, y, z = v.co
    r = math.hypot(x, y)
    g = 0.0
    if z <= 6.45 and abs(x) <= 1.0 and abs(y) <= 0.3:  # 창날
        hw = max(half_width(z), 0.05)
        g = 1.0 if abs(x) / hw > 0.97 else 0.0  # 날 끝 꼭짓점만 (바로 안쪽 0.86w 점까지만 번짐)
        if z < 0.5:
            g = max(g, 1 - z / 0.5)  # 창끝
    elif abs(x) > 0.28 and 5.4 < z < 6.7:  # 날개
        g = 0.75
    elif z > 6.9 and r >= 0.26:  # 고리
        g = 1.0
    elif 8.3 < z < 10.7 and 0.2 <= r <= 0.24:  # 나선 감김
        g = 0.55
    attr.data[v.index].color = (g, g, g, 1)

mat = bpy.data.materials.get("LanceMat") or bpy.data.materials.new("LanceMat")
mat.use_nodes = True
try:
    mat.surface_render_method = "BLENDED"
except Exception:
    pass
nt = mat.node_tree
for n in list(nt.nodes):
    nt.nodes.remove(n)
N = nt.nodes.new
L = nt.links.new


def m(op, a=None, b=None, clamp=False):
    x = N("ShaderNodeMath"); x.operation = op; x.use_clamp = clamp
    for i, v in enumerate((a, b)):
        if v is None: continue
        if isinstance(v, (int, float)): x.inputs[i].default_value = v
        else: L(v, x.inputs[i])
    return x.outputs[0]


def mr(v, a, b, c=0.0, d=1.0):
    x = N("ShaderNodeMapRange"); x.clamp = True; x.interpolation_type = "SMOOTHSTEP"
    x.inputs["From Min"].default_value = a; x.inputs["From Max"].default_value = b
    x.inputs["To Min"].default_value = c; x.inputs["To Max"].default_value = d
    L(v, x.inputs["Value"]); return x.outputs["Result"]


tc = N("ShaderNodeTexCoord")
sep = N("ShaderNodeSeparateXYZ"); L(tc.outputs["Object"], sep.inputs[0])
X, Z = sep.outputs["X"], sep.outputs["Z"]
glow_attr = N("ShaderNodeVertexColor"); glow_attr.layer_name = "Glow"
vglow = glow_attr.outputs["Color"]
vg = N("ShaderNodeSeparateColor"); L(vglow, vg.inputs[0])
edge = vg.outputs[0]

# 룬 띠: 창날 가운데(|x|<0.13), z 1.2~5.6. 보로노이 가장자리로 끊긴 글자 같은 선
absx = m("ABSOLUTE", X)
in_strip = m("MULTIPLY", mr(absx, 0.13, 0.09), m("MULTIPLY", mr(Z, 1.0, 1.4), mr(Z, 5.8, 5.4)))
cmb = N("ShaderNodeCombineXYZ")
L(m("MULTIPLY", X, 9.0), cmb.inputs[0]); L(m("MULTIPLY", Z, 2.6), cmb.inputs[1])
vor = N("ShaderNodeTexVoronoi"); vor.feature = "DISTANCE_TO_EDGE"; vor.voronoi_dimensions = "2D"
vor.inputs["Scale"].default_value = 1.0
L(cmb.outputs[0], vor.inputs["Vector"])
glyph = mr(vor.outputs["Distance"], 0.09, 0.03)
# 글자 사이 끊김
gap = N("ShaderNodeTexNoise"); gap.inputs["Scale"].default_value = 3.0
L(cmb.outputs[0], gap.inputs["Vector"])
runes = m("MULTIPLY", m("MULTIPLY", glyph, mr(gap.outputs["Fac"], 0.42, 0.5)), in_strip)
emit_mask = m("MAXIMUM", edge, runes)
# 자루 끝으로 갈수록 빛이 약해지고(마스크 0.4까지) 투명해짐
alpha = mr(Z, 18.8, 12.5)
emit_mask = m("MULTIPLY", emit_mask, mr(Z, 18.5, 10.0, 0.35, 1.0))

# 바탕색 (대비): 창날 = 은백색 금속, 가운데 홈 = 짙은 녹흑색(룬이 빛남), 자루 = 녹흑색
blade_mask = mr(Z, 6.6, 6.3)  # 1 = 창날
fuller = m("MULTIPLY", mr(absx, 0.17, 0.12), m("MULTIPLY", mr(Z, 0.7, 1.1), mr(Z, 6.1, 5.7)))
def rgba(c):
    n = N("ShaderNodeRGB"); n.outputs[0].default_value = c; return n.outputs[0]
def mix(fac, a, b):
    x = N("ShaderNodeMix"); x.data_type = "RGBA"; L(fac, x.inputs[0]); L(a, x.inputs[6]); L(b, x.inputs[7]); return x.outputs[2]
steel = rgba((0.82, 0.86, 0.85, 1))
groove = rgba((0.035, 0.07, 0.05, 1))
haft = rgba((0.03, 0.05, 0.04, 1))
blade_col = mix(fuller, steel, groove)
base_col = mix(blade_mask, haft, blade_col)
# 발광하는 곳은 흰 초록으로 밝게
base_col = mix(emit_mask, base_col, rgba((0.75, 1.0, 0.8, 1)))
metal = m("ADD", m("MULTIPLY", m("MULTIPLY", blade_mask, m("SUBTRACT", 1.0, fuller)), 0.6), 0.3)
rough = m("ADD", m("MULTIPLY", blade_mask, -0.25), 0.5)
bsdf = N("ShaderNodeBsdfPrincipled")
L(base_col, bsdf.inputs["Base Color"])
L(rough, bsdf.inputs["Roughness"])
L(metal, bsdf.inputs["Metallic"])
bsdf.inputs["Coat Weight"].default_value = 0.4
L(alpha, bsdf.inputs["Alpha"])
bsdf.inputs["Emission Color"].default_value = (0.15, 1.0, 0.3, 1)
L(m("MULTIPLY", emit_mask, 3.0), bsdf.inputs["Emission Strength"])
out = N("ShaderNodeOutputMaterial")
L(bsdf.outputs[0], out.inputs["Surface"])
# 굽기용 값 노드 (이름으로 찾음)
bake_alpha = N("ShaderNodeEmission"); bake_alpha.name = "BAKE_ALPHA"; L(alpha, bake_alpha.inputs["Color"])
bake_mask = N("ShaderNodeEmission"); bake_mask.name = "BAKE_MASK"; L(emit_mask, bake_mask.inputs["Color"])
bake_col = N("ShaderNodeEmission"); bake_col.name = "BAKE_COLOR"; L(base_col, bake_col.inputs["Color"])
bake_metal = N("ShaderNodeEmission"); bake_metal.name = "BAKE_METAL"; L(metal, bake_metal.inputs["Color"])
bake_rough = N("ShaderNodeEmission"); bake_rough.name = "BAKE_ROUGH"; L(rough, bake_rough.inputs["Color"])
me.materials.clear()
me.materials.append(mat)
print("lance material ready")
