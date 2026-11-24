# 명령줄 Blender 용: 지정한 씬의 몇 프레임을 렌더해 검은 바탕 한 줄 미리보기로 합침
# 사용: blender -b <blend> --python-expr "SCENE='VFX_SmokeWisp'; FRAMES=[4,12,24,40,56]; SIZE=192; OUT=r'...png'; exec(open(r'D:\god\scripts\vfx_preview_frames.py', encoding='utf-8').read())"
import bpy, os
import numpy as np

sc = bpy.data.scenes[SCENE]
sc.render.resolution_x = SIZE
sc.render.resolution_y = SIZE
sc.render.resolution_percentage = 100
tiles = []
tmp = OUT + "_tmp.png"
for f in FRAMES:
    sc.frame_set(f)
    sc.render.filepath = tmp
    bpy.ops.render.render(write_still=True, scene=sc.name)
    img = bpy.data.images.load(tmp, check_existing=False)
    px = np.array(img.pixels[:], dtype=np.float32).reshape(SIZE, SIZE, 4)
    bpy.data.images.remove(img)
    rgb = px[:, :, :3] * px[:, :, 3:4]  # 검은 바탕 위 합성
    tile = np.concatenate([rgb, np.ones((SIZE, SIZE, 1), np.float32)], axis=2)
    tiles.append(tile)
strip = np.concatenate(tiles, axis=1)
out = bpy.data.images.new("preview", strip.shape[1], SIZE, alpha=True)
out.pixels[:] = strip.ravel()
out.filepath_raw = OUT
out.file_format = "PNG"
out.save()
os.remove(tmp)
print("preview", OUT)
