# 스킬 이펙트 프레임 시트 키트 (Blender 5.3)
# exec(open(r"D:\god\scripts\vfx_sheet_kit.py", encoding="utf-8").read()) 로 불러온 뒤 함수를 쓴다.
# - vfx_scene(name): 이펙트 전용 씬(투명 배경, Cycles, 정사영 카메라)을 새로 만들어 활성화
# - render_sheet(name, frames, cell, grid, out_dir): 현재 씬의 프레임 1..frames를 cell 크기로 렌더해
#   grid×grid 시트 PNG 하나로 합친다 (왼쪽 위부터 가로 순서 = Roblox ParticleEmitter Flipbook 순서)
import bpy, os, math
import numpy as np

EXPORT_DIR = r"D:\god\exports\vfx"


def vfx_scene(name, ortho_scale=2.4, cam_dir=(0.0, -1.0, 0.0), cam_dist=10.0, cam_target=(0, 0, 0)):
    """이펙트 렌더용 빈 씬. cam_dir: 대상에서 카메라 쪽 방향 (기본 정면, (0,0,1)이면 위에서 내려다봄)"""
    if name in bpy.data.scenes:
        bpy.data.scenes.remove(bpy.data.scenes[name])
    sc = bpy.data.scenes.new(name)
    bpy.context.window.scene = sc
    try:
        sc.render.engine = "CYCLES"
    except TypeError as e:
        print("engine:", e)
    sc.cycles.samples = 64
    sc.cycles.use_denoising = True
    try:
        sc.cycles.device = "GPU"
    except Exception:
        pass
    sc.render.film_transparent = True
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGBA"
    sc.view_settings.view_transform = "Standard"
    # 월드: 아주 어두운 주변광 (연기 그늘이 새까맣지 않게)
    world = bpy.data.worlds.new(name + "_World")
    world.use_nodes = True
    bg = next(n for n in world.node_tree.nodes if n.type == "BACKGROUND")
    bg.inputs[0].default_value = (0.35, 0.37, 0.4, 1)
    bg.inputs[1].default_value = 0.35
    sc.world = world
    cam_data = bpy.data.cameras.new(name + "_Cam")
    cam_data.type = "ORTHO"
    cam_data.ortho_scale = ortho_scale
    cam = bpy.data.objects.new(name + "_Cam", cam_data)
    sc.collection.objects.link(cam)
    d = np.array(cam_dir, dtype=float)
    d = d / np.linalg.norm(d)
    cam.location = tuple(np.array(cam_target) + d * cam_dist)
    direction = -d
    from mathutils import Vector
    cam.rotation_euler = Vector(direction).to_track_quat("-Z", "Z" if abs(d[2]) < 0.99 else "Y").to_euler()
    sc.camera = cam
    return sc


def pack_sheet(frame_dir, out_path, grid=8, cell=128, premultiply_dark=False):
    """frame_dir 의 PNG(이름순) 를 grid×grid 시트로 합침 (왼쪽 위부터 가로 순서).
    명령줄 Blender 로 렌더한 프레임을 합칠 때 쓴다."""
    files = sorted(f for f in os.listdir(frame_dir) if f.lower().endswith(".png"))[: grid * grid]
    sheet = np.zeros((grid * cell, grid * cell, 4), dtype=np.float32)
    for i, f in enumerate(files):
        img = bpy.data.images.load(os.path.join(frame_dir, f), check_existing=False)
        if img.size[0] != cell:
            img.scale(cell, cell)
        px = np.array(img.pixels[:], dtype=np.float32).reshape(cell, cell, 4)
        bpy.data.images.remove(img)
        row, col = divmod(i, grid)
        y0 = (grid - 1 - row) * cell
        sheet[y0:y0 + cell, col * cell:(col + 1) * cell] = px
    out = bpy.data.images.new(os.path.basename(out_path), grid * cell, grid * cell, alpha=True)
    out.pixels[:] = sheet.ravel()
    out.filepath_raw = out_path
    out.file_format = "PNG"
    out.save()
    bpy.data.images.remove(out)
    print("packed %d frames -> %s" % (len(files), out_path))
    return out_path


def render_sheet(name, frames=64, cell=128, grid=8, out_dir=EXPORT_DIR, keep_frames=False):
    sc = bpy.context.scene
    sc.render.resolution_x = cell
    sc.render.resolution_y = cell
    sc.render.resolution_percentage = 100
    frame_dir = os.path.join(out_dir, "_frames", name)
    os.makedirs(frame_dir, exist_ok=True)
    sheet = np.zeros((grid * cell, grid * cell, 4), dtype=np.float32)
    for i in range(frames):
        sc.frame_set(i + 1)
        path = os.path.join(frame_dir, "f%03d.png" % i)
        sc.render.filepath = path
        bpy.ops.render.render(write_still=True)
        img = bpy.data.images.load(path, check_existing=False)
        px = np.array(img.pixels[:], dtype=np.float32).reshape(cell, cell, 4)  # 아래에서 위로
        bpy.data.images.remove(img)
        row, col = divmod(i, grid)
        # 시트 배열도 Blender 규칙(아래쪽 행이 0)이라 맨 위 행 = grid-1
        y0 = (grid - 1 - row) * cell
        sheet[y0:y0 + cell, col * cell:(col + 1) * cell] = px
    out = bpy.data.images.new(name + "_Sheet", grid * cell, grid * cell, alpha=True)
    out.pixels[:] = sheet.ravel()
    out.filepath_raw = os.path.join(out_dir, name + ".png")
    out.file_format = "PNG"
    out.save()
    bpy.data.images.remove(out)
    if not keep_frames:
        for f in os.listdir(frame_dir):
            os.remove(os.path.join(frame_dir, f))
    print("sheet saved:", os.path.join(out_dir, name + ".png"))
    return os.path.join(out_dir, name + ".png")
