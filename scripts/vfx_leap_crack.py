# 도약 찌르기: 바닥 균열 이미지 (위에서 내려다봄) — 선을 실제 도형(리본 메시)으로 그려 렌더
# 주 균열 8개가 중심에서 바깥으로 랜덤워크로 꺾이며 뻗고(끝으로 갈수록 가늘게), 가다가 갈래가 갈라지고,
# 이웃한 주 균열 사이에 짧은 동심 균열, 중심 둘레는 잘게 부서짐.
# 결과: 1024x512 = 왼쪽 512 선(날카로움, 흰색+알파) / 오른쪽 512 빛(굵게 + 흐림). Roblox 에서 ImageRectOffset 으로 나눠 씀.
# 먼저 vfx_sheet_kit.py 를 exec 한 뒤 실행.
import bpy, bmesh, os, math, random
import numpy as np
from mathutils import Vector

random.seed(23)
sc = vfx_scene("VFX_LeapCrack", ortho_scale=2.0, cam_dir=(0, 0, 1))
sc.cycles.samples = 16
sc.render.resolution_x = sc.render.resolution_y = 512

polylines = []  # [(점들, 시작굵기, 끝굵기)]


def walk(start, ang, length, w0, w1, step=0.05, wiggle=0.1, branch_p=0.05, depth=0, kink=0.22):
    pts = [start]
    p = Vector(start)
    a = ang
    n = max(int(length / step), 2)
    for i in range(n):
        a += random.uniform(-wiggle, wiggle)
        if random.random() < kink:  # 돌이 깨질 때처럼 가끔 꺾임
            a += random.choice((-1, 1)) * random.uniform(0.35, 0.7)
        # 바깥(반지름 방향)으로 조금 끌어당김
        out = math.atan2(p.y, p.x)
        da = (out - a + math.pi) % math.tau - math.pi
        a += da * 0.18
        p = p + Vector((math.cos(a), math.sin(a), 0)) * step * random.uniform(0.7, 1.3)
        pts.append(p.copy())
        if depth < 2 and i > 2 and random.random() < branch_p:
            t = i / n
            bw = w0 + (w1 - w0) * t
            walk(p.copy(), a + random.choice((-1, 1)) * random.uniform(0.45, 0.9),
                 length * (1 - t) * random.uniform(0.35, 0.65), bw * 0.7, w1 * 0.6,
                 step, wiggle, branch_p * 0.5, depth + 1, kink)
    polylines.append((pts, w0, w1))
    return pts


mains = []
K = 8
for k in range(K):
    ang = k / K * math.tau + random.uniform(-0.25, 0.25)
    r0 = random.uniform(0.06, 0.1)
    start = Vector((math.cos(ang) * r0, math.sin(ang) * r0, 0))
    mains.append(walk(start, ang, random.uniform(0.62, 0.9), 0.03, 0.005))
# 동심 균열: 이웃 주 균열의 비슷한 반지름 점을 휘게 이음 (일부만)
for k in range(K):
    if random.random() < 0.2:
        continue
    A, B = mains[k], mains[(k + 1) % K]
    t = random.uniform(0.3, 0.6)
    pa = A[int(len(A) * t)]
    pb = B[int(len(B) * t)]
    ra = (pa.length + pb.length) / 2
    aa, ab = math.atan2(pa.y, pa.x), math.atan2(pb.y, pb.x)
    if ab < aa: ab += math.tau
    pts = []
    seg = 10
    for i in range(seg + 1):
        u = i / seg
        a = aa + (ab - aa) * u
        rr = ra * (1 + random.uniform(-0.04, 0.04)) + math.sin(u * math.pi) * 0.02
        pts.append(Vector((math.cos(a) * rr, math.sin(a) * rr, 0)))
    # 끝까지 다 잇지 않고 70~100% 만
    cut = int(len(pts) * random.uniform(0.7, 1.0))
    polylines.append((pts[:cut], 0.014, 0.007))
# 중심 둘레 잔 균열: 짧은 조각들
for k in range(26):
    ang = random.uniform(0, math.tau)
    r0 = random.uniform(0.05, 0.2)
    s = Vector((math.cos(ang) * r0, math.sin(ang) * r0, 0))
    walk(s, ang + random.uniform(-1.2, 1.2), random.uniform(0.05, 0.13), 0.013, 0.004, step=0.025, wiggle=0.2, branch_p=0, depth=2, kink=0.35)


def ribbon_mesh(name, widen=1.0):
    bm = bmesh.new()
    for pts, w0, w1 in polylines:
        if len(pts) < 2:
            continue
        left, right = [], []
        n = len(pts)
        for i, p in enumerate(pts):
            d = (pts[min(i + 1, n - 1)] - pts[max(i - 1, 0)])
            if d.length < 1e-6:
                d = Vector((1, 0, 0))
            d.normalize()
            nrm = Vector((-d.y, d.x, 0))
            w = (w0 + (w1 - w0) * (i / (n - 1))) * widen * random.uniform(0.75, 1.2)
            left.append(bm.verts.new(p + nrm * w / 2))
            right.append(bm.verts.new(p - nrm * w / 2))
        for i in range(n - 1):
            try:
                bm.faces.new((left[i], right[i], right[i + 1], left[i + 1]))
            except ValueError:
                pass
    # 중심 구덩이 (작은 원판)
    c = bm.verts.new((0, 0, 0))
    ring = [bm.verts.new((math.cos(a) * 0.055 * widen ** 0.5 * random.uniform(0.85, 1.15), math.sin(a) * 0.055 * widen ** 0.5 * random.uniform(0.85, 1.15), 0)) for a in np.linspace(0, math.tau, 14, endpoint=False)]
    for i in range(len(ring)):
        bm.faces.new((c, ring[i], ring[(i + 1) % len(ring)]))
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    o = bpy.data.objects.new(name, me)
    sc.collection.objects.link(o)
    return o


mat = bpy.data.materials.new("CrackWhite")
mat.use_nodes = True
nt = mat.node_tree
for n in list(nt.nodes):
    nt.nodes.remove(n)
em = nt.nodes.new("ShaderNodeEmission"); em.inputs["Color"].default_value = (1, 1, 1, 1)
out = nt.nodes.new("ShaderNodeOutputMaterial")
nt.links.new(em.outputs[0], out.inputs["Surface"])

d = r"D:\god\exports\vfx\_frames"
os.makedirs(d, exist_ok=True)
tiles = []
for name, widen in [("crack_lines", 1.0), ("crack_glow", 3.0)]:
    random.seed(99)  # 굵기 흔들림을 두 장 같게
    o = ribbon_mesh(name, widen)
    o.data.materials.append(mat)
    p = os.path.join(d, name + ".png")
    sc.render.filepath = p
    bpy.ops.render.render(write_still=True)
    bpy.data.objects.remove(o)
    img = bpy.data.images.load(p, check_existing=False)
    px = np.array(img.pixels[:], dtype=np.float32).reshape(512, 512, 4)
    bpy.data.images.remove(img)
    if widen > 1:
        # 빛: 알파를 흐리게 (상자 흐림 3번 ≈ 가우시안)
        a = px[..., 3]
        for _ in range(3):
            k = 7
            a = np.cumsum(np.pad(a, ((0, 0), (k, k)), mode="edge"), axis=1)
            a = (a[:, 2 * k:] - a[:, :-2 * k]) / (2 * k)
            a = np.cumsum(np.pad(a, ((k, k), (0, 0)), mode="edge"), axis=0)
            a = (a[2 * k:, :] - a[:-2 * k, :]) / (2 * k)
        a = np.clip(a * 1.6, 0, 1)
        px = np.dstack([np.ones_like(a), np.ones_like(a), np.ones_like(a), a]).astype(np.float32)
    tiles.append(px)
sheet = np.concatenate(tiles, axis=1)
img = bpy.data.images.new("LeapCrack", 1024, 512, alpha=True)
img.pixels[:] = sheet.ravel(); img.filepath_raw = r"D:\god\exports\vfx\LeapCrack.png"; img.file_format = "PNG"; img.save(); bpy.data.images.remove(img)
print("crack saved", len(polylines), "lines")
