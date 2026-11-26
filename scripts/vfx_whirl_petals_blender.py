# 칼날 회오리 마무리 — 꽃잎 플립북 (Blender 5.3 렌더판, 2026-11-26). Python 판(vfx_whirl_petals.py)과 비교용.
# 실행 (Blender MCP): exec(open(r"D:\god\scripts\vfx_whirl_petals_blender.py", encoding="utf-8").read())
# 결과: exports/vfx/blade_whirl/petal_bl_<a|b>.png → vfx_whirl_petals.py finish() 가 빛 번짐을 더해 petal_<a|b>.png (최종) (4x4, 칸 256, 16칸 = 기울어진 축으로 한 바퀴, 투명 배경 RGBA)
# 꽃잎: 밑동 좁고 끝 둥근 잎(a, 끝 가운데 살짝 파임) / 가늘고 뾰족한 잎(b). 오목하게 휘고 끝이 말림.
# 재질: UV 로 밑동 진보라 → 보라 → 가장자리·끝 흰 라일락, 잎맥, 반투명(뒤에서 비치는 빛) + 약한 발광. 조명: 위앞 키 + 뒤 역광.
import bpy, bmesh, math, os
import numpy as np
from mathutils import Quaternion, Vector

exec(open(r"D:\god\scripts\vfx_sheet_kit.py", encoding="utf-8").read())
OUT_DIR = r"D:\god\exports\vfx\blade_whirl"
os.makedirs(OUT_DIR, exist_ok=True)
FRAMES = 16


def petal_shape(shape, u, v):
    if shape == "a":
        grow = 0.42 * (min(u / 0.68, 1.0) ** 0.75)
        rt = 0.42 * math.sqrt(max(1 - ((u - 0.68) / 0.32) ** 2, 0.0))
        width = grow if u < 0.68 else rt
        notch = 0.09 * math.exp(-(v / 0.2) ** 2)
        cup, curl = 0.55, 0.22
    else:
        width = 0.30 * math.sin(math.pi * u ** 0.62) ** 1.1
        notch = 0.0
        cup, curl = 0.45, 0.32
    uu = u * (1 - notch)
    x = v * width
    y = uu - 0.5
    z = cup * x * x * 2.2 - curl * uu ** 2.2 + 0.04 * math.sin(v * 3.1 + uu * 4.0)
    return Vector((x, z, y)), uu  # Blender: 위 = Z, 카메라는 -Y 쪽에서 봄 → 꽃잎 길이 = Z, 오목 = Y


def make_petal(shape, nu=70, nv=34):
    me = bpy.data.meshes.new("Petal_" + shape)
    bm = bmesh.new()
    uv_layer = bm.loops.layers.uv.new("UVMap")
    verts = []
    uvs = []
    for i in range(nu):
        u = i / (nu - 1)
        row = []
        for j in range(nv):
            v = -1 + 2 * j / (nv - 1)
            p, uu = petal_shape(shape, u, v)
            row.append(bm.verts.new(p))
            uvs.append(None)
        verts.append(row)
    for i in range(nu - 1):
        for j in range(nv - 1):
            f = bm.faces.new((verts[i][j], verts[i][j + 1], verts[i + 1][j + 1], verts[i + 1][j]))
            for loop in f.loops:
                vi = None
                for ii in range(i, i + 2):
                    for jj in range(j, j + 2):
                        if verts[ii][jj] == loop.vert:
                            vi = (ii, jj)
                loop[uv_layer].uv = (vi[0] / (nu - 1), vi[1] / (nv - 1))  # U = 길이, V = 폭 (0..1)
    bm.to_mesh(me)
    bm.free()
    for p in me.polygons:
        p.use_smooth = True
    ob = bpy.data.objects.new("Petal_" + shape, me)
    bpy.context.scene.collection.objects.link(ob)
    ob.data.materials.append(petal_material())
    return ob


def petal_material():
    if "PetalMat" in bpy.data.materials:
        return bpy.data.materials["PetalMat"]
    m = bpy.data.materials.new("PetalMat")
    m.use_nodes = True
    nt = m.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    tc = nt.nodes.new("ShaderNodeTexCoord")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    nt.links.new(tc.outputs["UV"], sep.inputs[0])
    # 길이(U) 색: 밑동 진보라 → 보라
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    cr = ramp.color_ramp
    cr.elements[0].position = 0.0
    cr.elements[0].color = (0.045, 0.002, 0.22, 1)
    cr.elements[1].position = 0.55
    cr.elements[1].color = (0.24, 0.02, 1.0, 1)
    nt.links.new(sep.outputs[0], ramp.inputs[0])
    # 흰 끝: 가장자리(|V-0.5|) 와 끝(U)
    sub = nt.nodes.new("ShaderNodeMath"); sub.operation = "SUBTRACT"; sub.inputs[1].default_value = 0.5
    nt.links.new(sep.outputs[1], sub.inputs[0])
    ab = nt.nodes.new("ShaderNodeMath"); ab.operation = "ABSOLUTE"
    nt.links.new(sub.outputs[0], ab.inputs[0])
    m2 = nt.nodes.new("ShaderNodeMath"); m2.operation = "MULTIPLY"; m2.inputs[1].default_value = 2.0
    nt.links.new(ab.outputs[0], m2.inputs[0])
    pe = nt.nodes.new("ShaderNodeMath"); pe.operation = "POWER"; pe.inputs[1].default_value = 4.0
    nt.links.new(m2.outputs[0], pe.inputs[0])
    pt = nt.nodes.new("ShaderNodeMath"); pt.operation = "POWER"; pt.inputs[1].default_value = 3.0
    nt.links.new(sep.outputs[0], pt.inputs[0])
    add = nt.nodes.new("ShaderNodeMath"); add.operation = "ADD"; add.use_clamp = True
    nt.links.new(pe.outputs[0], add.inputs[0])
    mt = nt.nodes.new("ShaderNodeMath"); mt.operation = "MULTIPLY"; mt.inputs[1].default_value = 0.85
    nt.links.new(pt.outputs[0], mt.inputs[0])
    nt.links.new(mt.outputs[0], add.inputs[1])
    mix = nt.nodes.new("ShaderNodeMix"); mix.data_type = "RGBA"
    nt.links.new(add.outputs[0], mix.inputs["Factor"])
    nt.links.new(ramp.outputs["Color"], mix.inputs["A"])
    mix.inputs["B"].default_value = (0.92, 0.82, 1.0, 1)
    # 잎맥: 폭 방향 파동 노이즈로 가는 줄 (밑동 쪽만)
    wave = nt.nodes.new("ShaderNodeTexWave")
    wave.wave_type = "BANDS"
    wave.bands_direction = "Y"
    wave.inputs["Scale"].default_value = 2.4
    wave.inputs["Distortion"].default_value = 3.0
    wave.inputs["Detail"].default_value = 1.0
    nt.links.new(tc.outputs["UV"], wave.inputs["Vector"])
    vr = nt.nodes.new("ShaderNodeValToRGB")
    vr.color_ramp.elements[0].position = 0.85
    vr.color_ramp.elements[0].color = (1, 1, 1, 1)
    vr.color_ramp.elements[1].position = 1.0
    vr.color_ramp.elements[1].color = (0.8, 0.8, 0.8, 1)
    nt.links.new(wave.outputs["Fac"], vr.inputs[0])
    # 잎맥은 밑동 쪽만 옅게 (첫 렌더는 끝까지 같은 굵기 줄이라 기계로 그은 듯했음)
    vf = nt.nodes.new("ShaderNodeMath"); vf.operation = "SUBTRACT"; vf.use_clamp = True
    vf.inputs[0].default_value = 0.75
    nt.links.new(sep.outputs[0], vf.inputs[1])
    veinmix = nt.nodes.new("ShaderNodeMix"); veinmix.data_type = "RGBA"; veinmix.blend_type = "MULTIPLY"
    nt.links.new(vf.outputs[0], veinmix.inputs["Factor"])
    nt.links.new(mix.outputs["Result"], veinmix.inputs["A"])
    nt.links.new(vr.outputs["Color"], veinmix.inputs["B"])
    col = veinmix.outputs["Result"]
    bsdf = nt.nodes.new("ShaderNodeBsdfPrincipled")
    nt.links.new(col, bsdf.inputs["Base Color"])
    bsdf.inputs["Roughness"].default_value = 0.42
    for name, val in (("Sheen Weight", 0.6), ("Sheen Roughness", 0.3), ("Coat Weight", 0.15)):
        if name in bsdf.inputs:
            bsdf.inputs[name].default_value = val
    if "Emission Color" in bsdf.inputs:
        nt.links.new(col, bsdf.inputs["Emission Color"])
        bsdf.inputs["Emission Strength"].default_value = 0.35
    trans = nt.nodes.new("ShaderNodeBsdfTranslucent")
    nt.links.new(col, trans.inputs["Color"])
    mixs = nt.nodes.new("ShaderNodeMixShader")
    mixs.inputs["Fac"].default_value = 0.4
    nt.links.new(bsdf.outputs[0], mixs.inputs[1])
    nt.links.new(trans.outputs[0], mixs.inputs[2])
    nt.links.new(mixs.outputs[0], out.inputs["Surface"])
    return m


def axis_rot(axis, ang):
    a = Vector(axis).normalized()
    return Quaternion(a, ang)


def animate(ob, shape):
    ob.rotation_mode = "QUATERNION"
    ax = (0.55, 0.75, 0.35) if shape == "a" else (0.25, 0.7, 0.6)  # Python 판과 같은 축 (Y·Z 바뀜)
    for k in range(FRAMES):
        ang = 2 * math.pi * k / FRAMES
        q = axis_rot(ax, ang) @ axis_rot((1, 0, 0), 0.35 * math.sin(2 * ang))
        ob.rotation_quaternion = q
        ob.keyframe_insert("rotation_quaternion", frame=k + 1)


def lights(sc):
    key = bpy.data.lights.new("PetalKey", "SUN")
    key.energy = 3.2
    k = bpy.data.objects.new("PetalKey", key)
    k.rotation_euler = (math.radians(50), 0, math.radians(25))
    sc.collection.objects.link(k)
    back = bpy.data.lights.new("PetalBack", "SUN")
    back.energy = 4.5
    back.color = (0.85, 0.75, 1.0)
    b = bpy.data.objects.new("PetalBack", back)
    b.rotation_euler = (math.radians(-60), 0, math.radians(180))  # 뒤에서 앞으로 (반투명 빛)
    sc.collection.objects.link(b)


def build_and_render(shape):
    if "PetalMat" in bpy.data.materials:
        bpy.data.materials.remove(bpy.data.materials["PetalMat"])
    sc = vfx_scene("WhirlPetal_" + shape, ortho_scale=1.28)
    sc.cycles.samples = 48
    sc.frame_start, sc.frame_end = 1, FRAMES
    lights(sc)
    ob = make_petal(shape)
    animate(ob, shape)
    path = render_sheet("petal_bl_" + shape, frames=FRAMES, cell=256, grid=4, out_dir=OUT_DIR)
    return path


for s in ("a", "b"):
    print(build_and_render(s))
