# 빛의 창 v2 재질 (미리보기 + 굽기용 값 노드)
#  LanceMetal: 검은 건메탈(살짝 청록), 금속 0.9, 꼭짓점 Glow=1 인 곳(줄·코어·화살촉 날)은 초록 발광
#  LanceCrystal: 초록 결정 — 가운데 능선과 날끝이 희게 밝고, 안쪽에 흐르는 에너지 줄무늬(노이즈), 살짝 투명
# vfx_leap_lance2.py 다음에 실행. 굽기 노드 이름: BAKE_COLOR / BAKE_ALPHA / BAKE_MASK / BAKE_METAL / BAKE_ROUGH
import bpy

sc = bpy.data.scenes["VFX_LeapLance2"]
GREEN = (0.12, 1.0, 0.32, 1)


def new_mat(name):
    mat = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    mat.use_nodes = True
    try:
        mat.surface_render_method = "BLENDED"
    except Exception:
        pass
    nt = mat.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    return mat, nt


def helpers(nt):
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
    def rgb(c):
        n = N("ShaderNodeRGB"); n.outputs[0].default_value = c; return n.outputs[0]
    def mix(f, a, b):
        x = N("ShaderNodeMix"); x.data_type = "RGBA"; L(f, x.inputs[0]); L(a, x.inputs[6]); L(b, x.inputs[7]); return x.outputs[2]
    return N, L, m, mr, rgb, mix


def finish(nt, N, L, base, alpha, mask, metal, rough, emit_strength):
    bsdf = N("ShaderNodeBsdfPrincipled")
    L(base, bsdf.inputs["Base Color"])
    L(alpha, bsdf.inputs["Alpha"])
    L(metal, bsdf.inputs["Metallic"])
    L(rough, bsdf.inputs["Roughness"])
    bsdf.inputs["Emission Color"].default_value = GREEN
    s = N("ShaderNodeMath"); s.operation = "MULTIPLY"; s.inputs[1].default_value = emit_strength
    L(mask, s.inputs[0]); L(s.outputs[0], bsdf.inputs["Emission Strength"])
    out = N("ShaderNodeOutputMaterial"); L(bsdf.outputs[0], out.inputs["Surface"])
    for name, src in [("BAKE_COLOR", base), ("BAKE_ALPHA", alpha), ("BAKE_MASK", mask), ("BAKE_METAL", metal), ("BAKE_ROUGH", rough)]:
        e = N("ShaderNodeEmission"); e.name = name; L(src, e.inputs["Color"])


# ---- 금속 ----
mat, nt = new_mat("Lance2Metal")
N, L, m, mr, rgb, mix = helpers(nt)
va = N("ShaderNodeVertexColor"); va.layer_name = "Glow"
sep = N("ShaderNodeSeparateColor"); L(va.outputs["Color"], sep.inputs[0])
glow = sep.outputs[0]
tc = N("ShaderNodeTexCoord")
scratch = N("ShaderNodeTexNoise"); scratch.inputs["Scale"].default_value = 22.0; scratch.inputs["Detail"].default_value = 8.0
L(tc.outputs["Object"], scratch.inputs["Vector"])
wear = mr(scratch.outputs["Fac"], 0.45, 0.75)  # 닳은 자국 (조금 밝고 매끈)
base = mix(wear, rgb((0.028, 0.034, 0.033, 1)), rgb((0.075, 0.085, 0.082, 1)))
base = mix(glow, base, rgb((0.7, 1.0, 0.75, 1)))
metal = m("SUBTRACT", 0.92, m("MULTIPLY", glow, 0.92))
rough = m("SUBTRACT", 0.42, m("MULTIPLY", wear, 0.14))
one = N("ShaderNodeValue"); one.outputs[0].default_value = 1.0
finish(nt, N, L, base, one.outputs[0], glow, metal, rough, 6.0)
o = sc.objects["LanceMetal"]; o.data.materials.clear(); o.data.materials.append(mat)

# ---- 결정 ----
mat, nt = new_mat("Lance2Crystal")
N, L, m, mr, rgb, mix = helpers(nt)
tc = N("ShaderNodeTexCoord")
sep = N("ShaderNodeSeparateXYZ"); L(tc.outputs["Object"], sep.inputs[0])
X, Y, Z = sep.outputs["X"], sep.outputs["Y"], sep.outputs["Z"]
# 능선(두께 방향 바깥 = |y| 큼)과 끝(z 작음)이 밝음. 날 길이 방향으로 흐르는 줄무늬
ridge = mr(m("ABSOLUTE", Y), 0.05, 0.2)
st_vec = N("ShaderNodeCombineXYZ"); L(m("MULTIPLY", X, 6.0), st_vec.inputs[0]); L(m("MULTIPLY", Z, 0.7), st_vec.inputs[1])
streak = N("ShaderNodeTexNoise"); streak.inputs["Scale"].default_value = 2.5; streak.inputs["Detail"].default_value = 6.0; streak.inputs["Distortion"].default_value = 0.6
L(st_vec.outputs[0], streak.inputs["Vector"])
flow = mr(streak.outputs["Fac"], 0.38, 0.72)
tipglow = mr(Z, 2.5, 0.0, 0.0, 0.6)
energy = m("ADD", m("MULTIPLY", flow, 0.55), m("ADD", m("MULTIPLY", ridge, 0.35), tipglow), clamp=True)
mask = m("ADD", m("MULTIPLY", energy, 0.85), 0.15, clamp=True)
deep = rgb((0.0, 0.55, 0.16, 1))
bright = rgb((0.78, 1.0, 0.8, 1))
base = mix(energy, deep, bright)
alpha = m("ADD", m("MULTIPLY", energy, 0.12), 0.86, clamp=True)
zero = N("ShaderNodeValue"); zero.outputs[0].default_value = 0.0
rv = N("ShaderNodeValue"); rv.outputs[0].default_value = 0.08
finish(nt, N, L, base, alpha, mask, zero.outputs[0], rv.outputs[0], 11.0)
o = sc.objects["LanceCrystal"]; o.data.materials.clear(); o.data.materials.append(mat)
print("lance2 materials ready")
