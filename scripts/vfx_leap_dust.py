# 도약 찌르기: 흙먼지 덩이 프레임 시트 (8x8 = 64칸, 칸 128px)
# 덩이 하나가 뭉게뭉게 커지면서 흩어진다. Roblox 에서 ParticleEmitter Flipbook(OneShot)로 여러 개를 사방으로 뿌림.
# 모양: 구 중심 기울기(spherical gradient) + 큰 노이즈로 울퉁불퉁한 덩이(콜리플라워), 작은 노이즈로 가는 결.
# 시간이 갈수록 문턱을 올려 바깥부터 흩어짐. 먼저 vfx_sheet_kit.py 를 exec 한 뒤 실행.
import bpy, bmesh

FRAMES = 64

sc = vfx_scene("VFX_LeapDust", ortho_scale=2.5, cam_dir=(0, -1, 0.15))
sc.frame_start, sc.frame_end = 1, FRAMES
sc.cycles.samples = 48
try:
    sc.cycles.volume_step_rate = 1.0
    sc.cycles.volume_max_steps = 256
except Exception:
    pass
# 주변광 밝게 (그늘이 진흙색이 되도록)
bg = next(n for n in sc.world.node_tree.nodes if n.type == "BACKGROUND")
bg.inputs[0].default_value = (0.55, 0.55, 0.58, 1)
bg.inputs[1].default_value = 0.9

sun = bpy.data.lights.new("DustSun", "SUN")
sun.energy = 7.0
sun.color = (1.0, 0.96, 0.9)
sun.angle = 0.4
o = bpy.data.objects.new("DustSun", sun)
o.rotation_euler = (0.7, -0.6, 0.35)
sc.collection.objects.link(o)

mesh = bpy.data.meshes.new("DustBallMesh")
bm = bmesh.new()
bmesh.ops.create_icosphere(bm, subdivisions=3, radius=1.0)
bm.to_mesh(mesh)
bm.free()
ball = bpy.data.objects.new("DustBall", mesh)
sc.collection.objects.link(ball)

mat = bpy.data.materials.new("DustVolume")
mat.use_nodes = True
nt = mat.node_tree
for n in list(nt.nodes):
    nt.nodes.remove(n)
N = nt.nodes.new
L = nt.links.new
out = N("ShaderNodeOutputMaterial")
vol = N("ShaderNodeVolumePrincipled")
tc = N("ShaderNodeTexCoord")
big = N("ShaderNodeTexNoise")
big.noise_dimensions = "4D"
big.inputs["Scale"].default_value = 1.5
big.inputs["Detail"].default_value = 3.0
big.inputs["Roughness"].default_value = 0.5
fine = N("ShaderNodeTexNoise")
fine.noise_dimensions = "4D"
fine.inputs["Scale"].default_value = 6.0
fine.inputs["Detail"].default_value = 8.0
fine.inputs["Roughness"].default_value = 0.65
grad = N("ShaderNodeTexGradient")
grad.gradient_type = "SPHERICAL"
# field = gradient + (big - 0.5) * 1.1
sub = N("ShaderNodeMath"); sub.operation = "SUBTRACT"; sub.inputs[1].default_value = 0.5
amp = N("ShaderNodeMath"); amp.operation = "MULTIPLY"; amp.inputs[1].default_value = 1.1
add = N("ShaderNodeMath"); add.operation = "ADD"
shape = N("ShaderNodeMapRange")  # 문턱: 시간 따라 올림
shape.inputs["From Min"].default_value = 0.05
shape.inputs["From Max"].default_value = 0.22
wisp = N("ShaderNodeMapRange")  # 가는 결: 0.4..1
wisp.inputs["From Min"].default_value = 0.35
wisp.inputs["From Max"].default_value = 0.7
wisp.inputs["To Min"].default_value = 0.35
wisp.inputs["To Max"].default_value = 1.0
m1 = N("ShaderNodeMath"); m1.operation = "MULTIPLY"
dens = N("ShaderNodeMath"); dens.operation = "MULTIPLY"; dens.inputs[1].default_value = 40.0
vol.inputs["Color"].default_value = (0.72, 0.65, 0.55, 1)
vol.inputs["Anisotropy"].default_value = 0.15
L(tc.outputs["Object"], big.inputs["Vector"])
L(tc.outputs["Object"], fine.inputs["Vector"])
L(tc.outputs["Object"], grad.inputs["Vector"])
L(big.outputs["Fac"], sub.inputs[0])
L(sub.outputs[0], amp.inputs[0])
L(grad.outputs["Fac"], add.inputs[0])
L(amp.outputs[0], add.inputs[1])
L(add.outputs[0], shape.inputs["Value"])
L(fine.outputs["Fac"], wisp.inputs["Value"])
L(shape.outputs["Result"], m1.inputs[0])
L(wisp.outputs["Result"], m1.inputs[1])
L(m1.outputs[0], dens.inputs[0])
L(dens.outputs[0], vol.inputs["Density"])
L(vol.outputs["Volume"], out.inputs["Volume"])
mesh.materials.append(mat)


def key(sock, frame, value):
    sock.default_value = value
    sock.keyframe_insert("default_value", frame=frame)


# 빠르게 부풀었다가(앞 1/4) 천천히 퍼지며 옅어짐
for f, s, t0, d, w in [
    (1, 0.30, 0.02, 45.0, 0.0),
    (8, 0.66, 0.04, 40.0, 0.3),
    (20, 0.86, 0.10, 30.0, 0.75),
    (40, 0.96, 0.22, 20.0, 1.3),
    (56, 1.00, 0.34, 12.0, 1.7),
    (64, 1.02, 0.46, 6.0, 1.95),
]:
    ball.scale = (s, s, s * 0.9)
    ball.keyframe_insert("scale", frame=f)
    key(shape.inputs["From Min"], f, t0)
    key(shape.inputs["From Max"], f, t0 + 0.2)
    key(dens.inputs[1], f, d)
    key(big.inputs["W"], f, w)
    key(fine.inputs["W"], f, w * 1.6)
ball.location = (0, 0, -0.15)
ball.keyframe_insert("location", frame=1)
ball.location = (0, 0, 0.15)
ball.keyframe_insert("location", frame=64)
print("dust scene ready")
