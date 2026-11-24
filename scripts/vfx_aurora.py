# 신의 창 오로라 텍스처 (2026-11-24, 사용자: 단색 창이 아니라 "오로라치는" 영롱한 창)
# 색: 흰·초록 중심 + 가장자리에 청록·엷은 보라 (창 무기 색 규칙 흰+초록 유지)
# 그림 두 장 (가로 = 띠 길이 방향, 가로로 이음매 없이 반복 → Roblox Beam TextureMode Wrap + TextureSpeed 로 흐르게):
#   AuroraCurtain 1024x256  창을 감는 오로라 커튼. 아래 가장자리가 밝은 초록·흰 띠, 위로 세로 빛살이 청록 → 엷은 보라로 옅어짐
#   AuroraFlow    1024x128  날 속을 흐르는 빛. 가운데가 흰빛, 바깥으로 초록 → 청록·보라, 길이 방향으로 물결치는 결
# 2D 셰이더를 정사영 평면에 그려 렌더 (Cycles, 발광만). 가로 이음매: x 를 원(cos, sin)으로 감아 노이즈에 넣음.
# 명령줄: blender -b --factory-startup --python-expr "exec(open(r'D:\god\scripts\vfx_aurora.py', encoding='utf-8').read())"
import bpy, math, os

OUT = r"D:\god\exports\vfx"
os.makedirs(OUT, exist_ok=True)


def scene(name, w, h):
    if name in bpy.data.scenes:
        bpy.data.scenes.remove(bpy.data.scenes[name])
    sc = bpy.data.scenes.new(name)
    if bpy.context.window:
        bpy.context.window.scene = sc
    sc.render.engine = "CYCLES"
    sc.cycles.samples = 16
    sc.cycles.use_denoising = False
    sc.render.film_transparent = True
    sc.render.resolution_x, sc.render.resolution_y = w, h
    sc.render.resolution_percentage = 100
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGBA"
    sc.view_settings.view_transform = "Standard"
    world = bpy.data.worlds.new(name + "W")
    sc.world = world
    cam = bpy.data.cameras.new(name + "Cam")
    cam.type = "ORTHO"
    cam.ortho_scale = 2.0  # 가로 2 (x -1..1)
    co = bpy.data.objects.new(name + "Cam", cam)
    co.location = (0, 0, 5)
    sc.collection.objects.link(co)
    sc.camera = co
    # 평면: x -1..1 (가로 전체), y -h/w..h/w
    me = bpy.data.meshes.new(name + "Plane")
    a = h / w
    me.from_pydata([(-1, -a, 0), (1, -a, 0), (1, a, 0), (-1, a, 0)], [], [(0, 1, 2, 3)])
    me.uv_layers.new()
    uv = me.uv_layers[0].data
    for i, (u, v) in enumerate([(0, 0), (1, 0), (1, 1), (0, 1)]):
        uv[i].uv = (u, v)
    ob = bpy.data.objects.new(name + "Plane", me)
    sc.collection.objects.link(ob)
    return sc, ob


class G:
    """노드 짜기 도우미"""

    def __init__(self, mat):
        mat.use_nodes = True
        self.nt = mat.node_tree
        for n in list(self.nt.nodes):
            self.nt.nodes.remove(n)

    def n(self, t, **inputs):
        node = self.nt.nodes.new(t)
        for k, v in inputs.items():
            node.inputs[k].default_value = v
        return node

    def math(self, op, a=None, b=None):
        m = self.nt.nodes.new("ShaderNodeMath")
        m.operation = op
        for i, v in ((0, a), (1, b)):
            if isinstance(v, (int, float)):
                m.inputs[i].default_value = v
            elif v is not None:
                self.link(v, m.inputs[i])
        return m.outputs[0]

    def link(self, a, b):
        self.nt.links.new(a, b)


def wrapped(g, u, v, radius, vscale, w_offset=0.0):
    """u(0..1, 가로 이음매 없이) → (cos, sin) 원, v 는 세로 좌표 × vscale → 노이즈용 벡터"""
    ang = g.math("MULTIPLY", u, math.tau)
    cx = g.math("MULTIPLY", g.math("COSINE", ang), radius)
    sy = g.math("MULTIPLY", g.math("SINE", ang), radius)
    vz = g.math("ADD", g.math("MULTIPLY", v, vscale), w_offset)
    comb = g.n("ShaderNodeCombineXYZ")
    g.link(cx, comb.inputs["X"])
    g.link(sy, comb.inputs["Y"])
    g.link(vz, comb.inputs["Z"])
    return comb.outputs[0]


def color_ramp(g, fac, stops):
    r = g.n("ShaderNodeValToRGB")
    els = r.color_ramp.elements
    while len(els) > 2:
        els.remove(els[-1])
    for i, (pos, col) in enumerate(stops):
        e = els[i] if i < 2 else els.new(pos)
        e.position = pos
        e.color = col
    g.link(fac, r.inputs["Fac"])
    return r.outputs["Color"]


WHITE = (1.0, 1.0, 1.0, 1)
GREEN_W = (0.75, 1.0, 0.8, 1)
GREEN = (0.15, 1.0, 0.35, 1)
TEAL = (0.05, 0.85, 0.8, 1)
VIOLET = (0.6, 0.35, 1.0, 1)


def finish(g, color, alpha):
    """발광 + 투명 섞기: 알파 = alpha, 색 = color"""
    emit = g.n("ShaderNodeEmission")
    emit.inputs["Strength"].default_value = 1.0
    g.link(color, emit.inputs["Color"])
    transp = g.n("ShaderNodeBsdfTransparent")
    mix = g.n("ShaderNodeMixShader")
    g.link(alpha, mix.inputs["Fac"])
    g.link(transp.outputs[0], mix.inputs[1])
    g.link(emit.outputs[0], mix.inputs[2])
    out = g.n("ShaderNodeOutputMaterial")
    g.link(mix.outputs[0], out.inputs["Surface"])


def curtain():
    sc, ob = scene("AuroraCurtain", 1024, 256)
    mat = bpy.data.materials.new("AuroraCurtainMat")
    g = G(mat)
    uvn = g.n("ShaderNodeUVMap")
    sep = g.n("ShaderNodeSeparateXYZ")
    g.link(uvn.outputs["UV"], sep.inputs[0])
    u, v = sep.outputs["X"], sep.outputs["Y"]
    # 커튼 물결: 아래 가장자리 높이가 가로로 출렁임
    wave_n = g.n("ShaderNodeTexNoise", Scale=1.2, Detail=2.0, Roughness=0.5)
    g.link(wrapped(g, u, 0.0, 1.0, 0.0), wave_n.inputs["Vector"])
    edge = g.math("ADD", g.math("MULTIPLY", g.math("SUBTRACT", wave_n.outputs["Fac"], 0.5), 0.35), 0.18)  # 아래 가장자리 v 위치
    h = g.math("SUBTRACT", v, edge)  # 가장자리 위로 얼마나 (음수 = 아래)
    # 세로 빛살: 가로로 촘촘, 세로로 길게 늘어난 노이즈
    rays = g.n("ShaderNodeTexNoise", Scale=1.0, Detail=6.0, Roughness=0.55)
    g.link(wrapped(g, u, v, 9.0, 0.6), rays.inputs["Vector"])
    ray_fac = g.n("ShaderNodeMapRange")
    ray_fac.inputs["From Min"].default_value = 0.35
    ray_fac.inputs["From Max"].default_value = 0.7
    ray_fac.inputs["To Min"].default_value = 0.15
    g.link(rays.outputs["Fac"], ray_fac.inputs["Value"])
    # 세로 밝기: 가장자리 바로 위가 가장 밝고 위로 옅어짐, 가장자리 아래는 짧게 사라짐
    up = g.n("ShaderNodeMapRange"); up.interpolation_type = "SMOOTHSTEP"
    up.inputs["From Min"].default_value = 0.0; up.inputs["From Max"].default_value = 0.78
    up.inputs["To Min"].default_value = 1.0; up.inputs["To Max"].default_value = 0.0
    g.link(h, up.inputs["Value"])
    below = g.n("ShaderNodeMapRange"); below.interpolation_type = "SMOOTHSTEP"
    below.inputs["From Min"].default_value = -0.06; below.inputs["From Max"].default_value = 0.0
    g.link(h, below.inputs["Value"])
    vert = g.math("MULTIPLY", up.outputs["Result"], below.outputs["Result"])
    inten = g.math("MULTIPLY", vert, ray_fac.outputs["Result"])
    # 가장자리 밝은 띠
    band = g.n("ShaderNodeMapRange"); band.interpolation_type = "SMOOTHSTEP"
    band.inputs["From Min"].default_value = 0.0; band.inputs["From Max"].default_value = 0.08
    band.inputs["To Min"].default_value = 1.0; band.inputs["To Max"].default_value = 0.0
    g.link(g.math("ABSOLUTE", h), band.inputs["Value"])
    inten2 = g.math("MINIMUM", g.math("ADD", inten, g.math("MULTIPLY", band.outputs["Result"], 0.8)), 1.0)
    # 색: 높이에 따라 흰초록 → 초록 → 청록 → 보라 (+ 빛살 노이즈로 조금 흔들어 섞음)
    cfac = g.math("ADD", g.math("MULTIPLY", h, 1.25), g.math("MULTIPLY", g.math("SUBTRACT", rays.outputs["Fac"], 0.5), 0.25))
    col = color_ramp(g, cfac, [(0.0, GREEN_W), (0.15, GREEN), (0.42, TEAL), (0.72, VIOLET)])
    finish(g, col, inten2)
    ob.data.materials.append(mat)
    sc.render.filepath = os.path.join(OUT, "AuroraCurtain.png")
    bpy.ops.render.render(write_still=True, scene=sc.name)
    print("rendered", sc.render.filepath)


def flow():
    sc, ob = scene("AuroraFlow", 1024, 128)
    mat = bpy.data.materials.new("AuroraFlowMat")
    g = G(mat)
    uvn = g.n("ShaderNodeUVMap")
    sep = g.n("ShaderNodeSeparateXYZ")
    g.link(uvn.outputs["UV"], sep.inputs[0])
    u, v = sep.outputs["X"], sep.outputs["Y"]
    # 가운데 선이 길이 방향으로 물결
    wave_n = g.n("ShaderNodeTexNoise", Scale=1.5, Detail=2.0)
    g.link(wrapped(g, u, 0.0, 1.0, 0.0), wave_n.inputs["Vector"])
    mid = g.math("ADD", 0.5, g.math("MULTIPLY", g.math("SUBTRACT", wave_n.outputs["Fac"], 0.5), 0.3))
    d = g.math("ABSOLUTE", g.math("SUBTRACT", v, mid))  # 가운데에서 거리 0..0.5
    core = g.n("ShaderNodeMapRange"); core.interpolation_type = "SMOOTHSTEP"
    core.inputs["From Min"].default_value = 0.0; core.inputs["From Max"].default_value = 0.45
    core.inputs["To Min"].default_value = 1.0; core.inputs["To Max"].default_value = 0.0
    g.link(d, core.inputs["Value"])
    # 길이 방향 결 (흐르는 빛 덩이)
    # 매끈한 비단 결 (v1 은 잔 노이즈라 흰 심이 회색 얼룩처럼 보였음)
    streak = g.n("ShaderNodeTexNoise", Scale=1.0, Detail=2.0, Roughness=0.4)
    g.link(wrapped(g, u, v, 3.0, 1.2), streak.inputs["Vector"])
    sf = g.n("ShaderNodeMapRange"); sf.interpolation_type = "SMOOTHSTEP"
    sf.inputs["From Min"].default_value = 0.35; sf.inputs["From Max"].default_value = 0.65
    sf.inputs["To Min"].default_value = 0.5
    g.link(streak.outputs["Fac"], sf.inputs["Value"])
    inten = g.math("MINIMUM", g.math("MULTIPLY", g.math("MULTIPLY", core.outputs["Result"], sf.outputs["Result"]), 1.8), 1.0)
    cfac = g.math("ADD", g.math("MULTIPLY", d, 2.0), g.math("MULTIPLY", g.math("SUBTRACT", streak.outputs["Fac"], 0.5), 0.3))
    col = color_ramp(g, cfac, [(0.0, WHITE), (0.2, GREEN_W), (0.42, GREEN), (0.68, TEAL), (0.95, VIOLET)])
    finish(g, col, inten)
    ob.data.materials.append(mat)
    sc.render.filepath = os.path.join(OUT, "AuroraFlow.png")
    bpy.ops.render.render(write_still=True, scene=sc.name)
    print("rendered", sc.render.filepath)


curtain()
flow()
