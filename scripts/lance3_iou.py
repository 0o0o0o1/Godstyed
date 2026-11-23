# 빛의 창 v3 — 정면(XZ) 실루엣 IoU 검사. references/lance_mask.png 와 같은 픽셀 격자로 렌더해 비교.
# 마스크 격자: 폭 260, 높이 1514, 1 스터드 = 49.15 px, 아래 여백 20 px (z=0 = 아래에서 20 px).
# 결과: IoU 전체 + 구간별(머리 0~10.5, 목 10.5~15, 자루 15~23.3, 꼬리 23.3~30), 차이 그림 references/lance_iou_diff.png
#   (초록 = 겹침, 빨강 = 모델만 있음(넘침), 파랑 = 참고만 있음(모자람))
# 실행: lance3 씬이 있는 상태에서 exec(open(r"D:\god\scripts\lance3_iou.py", encoding="utf-8").read())
import bpy, numpy as np

PPU, M, WOUT, HOUT = 49.15, 20, 260, 1514
sc = bpy.data.scenes["VFX_Lance3"]
if bpy.context.window is not None:
    bpy.context.window.scene = sc
try:
    sc.render.engine = "CYCLES"
except TypeError:
    pass
sc.cycles.samples = 1
sc.cycles.use_denoising = False
sc.cycles.device = "CPU"
sc.render.film_transparent = True
sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = WOUT, HOUT, 100
cam = sc.objects.get("_IoUCam")
if cam is None:
    cam = bpy.data.objects.new("_IoUCam", bpy.data.cameras.new("_IoUCam"))
    sc.collection.objects.link(cam)
cam.data.type = "ORTHO"
cam.data.ortho_scale = HOUT / PPU  # 세로가 더 김 → ortho_scale 은 긴 쪽
zc = ((HOUT - 1) / 2 - M) / PPU     # 이미지 가운데 행의 z
cam.location = (0, -50, zc)
cam.rotation_euler = (np.pi / 2, 0, 0)
cam.data.clip_end = 200
sc.camera = cam
sc.render.filepath = r"D:\god\references\_iou_render.png"
bpy.ops.render.render(write_still=True)
im = bpy.data.images.load(sc.render.filepath, check_existing=False)
rend = np.array(im.pixels[:], dtype=np.float32).reshape(HOUT, WOUT, 4)[..., 3] > 0.5
bpy.data.images.remove(im)
mk = bpy.data.images.load(r"D:\god\references\lance_mask.png", check_existing=False)
ref = np.array(mk.pixels[:], dtype=np.float32).reshape(HOUT, WOUT, 4)[..., 0] < 0.5
bpy.data.images.remove(mk)
# pixels 배열은 아래→위: 행 i 의 z = (i - M) / PPU


def iou(a, b):
    u = (a | b).sum()
    return (a & b).sum() / u if u else 1.0


report = {"all": round(float(iou(rend, ref)), 3)}
for name, z0, z1 in [("head", 0, 10.5), ("neck", 10.5, 15), ("shaft", 15, 23.3), ("butt", 23.3, 30.2)]:
    r0, r1 = int(M + z0 * PPU), int(M + z1 * PPU)
    report[name] = round(float(iou(rend[r0:r1], ref[r0:r1])), 3)
over = rend & ~ref
under = ref & ~rend
diff = np.ones((HOUT, WOUT, 4), np.float32)
diff[..., :3] = 0.95
diff[rend & ref] = [0.3, 0.8, 0.3, 1]
diff[over] = [0.9, 0.2, 0.2, 1]
diff[under] = [0.2, 0.35, 0.95, 1]
o = bpy.data.images.new("diff", WOUT, HOUT, alpha=True); o.pixels[:] = diff.ravel()
o.filepath_raw = r"D:\god\references\lance_iou_diff.png"; o.file_format = "PNG"; o.save(); bpy.data.images.remove(o)
# 구간별 넘침/모자람 (1 스터드 단위로 가장 큰 곳)
rows = []
for z in range(0, 30):
    r0, r1 = int(M + z * PPU), int(M + (z + 1) * PPU)
    ov, un = over[r0:r1].sum() / PPU ** 2, under[r0:r1].sum() / PPU ** 2
    if ov > 0.08 or un > 0.08:
        rows.append("z %2d-%2d: 넘침 %.2f / 모자람 %.2f (스터드²)" % (z, z + 1, ov, un))
print("IoU", report)
print("\n".join(rows))
