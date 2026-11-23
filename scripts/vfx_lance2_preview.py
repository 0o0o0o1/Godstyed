# 빛의 창 v2 미리보기 렌더 (하늘빛 환경 + 해 2개, 투명 배경을 밝은 회색에 합성)
# vfx_leap_lance2.py, vfx_leap_lance2_mat.py 다음에 실행. 결과: exports/vfx/preview_Lance2*.png
import bpy, numpy as np
from mathutils import Vector

sc = bpy.data.scenes["VFX_LeapLance2"]
sc.render.engine = "CYCLES"; sc.cycles.samples = 24; sc.cycles.device = "CPU"
sc.view_settings.view_transform = "AgX"
w = bpy.data.worlds.get("_Lance2World")
if w is None:
    w = bpy.data.worlds.new("_Lance2World"); w.use_nodes = True
    nt = w.node_tree; bg = next(n for n in nt.nodes if n.type == "BACKGROUND")
    sky = nt.nodes.new("ShaderNodeTexSky"); nt.links.new(sky.outputs[0], bg.inputs[0]); bg.inputs[1].default_value = 0.3
sc.world = w
sc.render.film_transparent = True
for name, rot, e in [("_K2", (0.9, 0.3, 0.8), 3.0), ("_R2", (1.3, -0.3, -2.3), 5.0)]:
    if name in sc.objects:
        continue
    ld = bpy.data.lights.get(name) or bpy.data.lights.new(name, "SUN"); ld.energy = e
    l = bpy.data.objects.new(name, ld); l.rotation_euler = rot; sc.collection.objects.link(l)
cd = bpy.data.cameras.get("_C2") or bpy.data.cameras.new("_C2")
cam = sc.objects.get("_C2") or bpy.data.objects.new("_C2", cd)
if cam.name not in sc.objects:
    sc.collection.objects.link(cam)
sc.camera = cam


def shot(path, target, offset, lens, rx, ry):
    sc.render.resolution_x, sc.render.resolution_y = rx, ry
    cam.data.lens = lens
    t = Vector(target); cam.location = t + Vector(offset)
    cam.rotation_euler = (t - cam.location).to_track_quat("-Z", "Y").to_euler()
    sc.render.filepath = path
    bpy.ops.render.render(write_still=True)
    img = bpy.data.images.load(path, check_existing=False)
    px = np.array(img.pixels[:], dtype=np.float32).reshape(img.size[1], img.size[0], 4); bpy.data.images.remove(img)
    a = px[..., 3:4]; bgc = np.array([0.86, 0.87, 0.88])
    o = bpy.data.images.new("p", px.shape[1], px.shape[0])
    o.pixels[:] = np.concatenate([np.clip(px[..., :3] + bgc * (1 - a), 0, 1), np.ones_like(a)], axis=2).astype(np.float32).ravel()
    o.filepath_raw = path; o.file_format = "PNG"; o.save(); bpy.data.images.remove(o)
