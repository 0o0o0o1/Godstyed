# M키 미니맵 이미지: Studio 위에서 내려다본 캡처 7장(높이 1500, FOV 16, 위 = -Z, 오른쪽 = +X)을 이어 붙임
# 캡처 1장 = 1913×670 px, 0.62925 스터드/px (세로 시야 421.6). 결과: 월드 X -1252..52, Z 323..1588 → 1024×993
# exec(open(r"D:\god\scripts\steelworks_minimap.py", encoding="utf-8").read()); build_minimap()
import bpy, numpy as np, os

TILE_DIR = r"D:\god\exports\minimap_tiles"
TILES = [("r1c1", -648, 533), ("r1c2", -150, 533), ("r2c1", -648, 885), ("r2c2", -150, 885),
         ("r3c1", -648, 1237), ("r3c2", -150, 1237), ("r4c1", -648, 1378)]
S = 421.6 / 670.0
XMIN, XMAX, ZMIN, ZMAX = -1252.0, 52.0, 323.0, 1588.0
OW = 1024; OH = int(round(OW * (ZMAX - ZMIN) / (XMAX - XMIN)))


def load(path):
    img = bpy.data.images.load(path, check_existing=False)
    w, h = img.size
    a = np.array(img.pixels[:], np.float32).reshape(h, w, 4)[::-1].copy()
    bpy.data.images.remove(img)
    return a


def build_minimap(ss=2):
    tiles = [(load(os.path.join(TILE_DIR, n + ".jpg")), cx, cz) for n, cx, cz in TILES]
    W2, H2 = OW * ss, OH * ss
    xs = XMIN + (np.arange(W2) + 0.5) * (XMAX - XMIN) / W2
    zs = ZMIN + (np.arange(H2) + 0.5) * (ZMAX - ZMIN) / H2
    X, Z = np.meshgrid(xs, zs)
    out = np.zeros((H2, W2, 4), np.float32); best = np.full((H2, W2), np.inf, np.float32)
    for img, cx, cz in tiles:
        h, w = img.shape[:2]
        u = (w / 2 - 0.5) + (X - cx) / S; v = (h / 2 - 0.5) + (Z - cz) / S
        ok = (u >= 0) & (u <= w - 1) & (v >= 0) & (v <= h - 1)
        score = np.maximum(np.abs(X - cx) / 602.0, np.abs(Z - cz) / 210.8)   # 가운데에 가까운 캡처 우선 (기울어짐 최소)
        take = ok & (score < best)
        ui = np.clip(u, 0, w - 1.001); vi = np.clip(v, 0, h - 1.001)
        u0 = ui.astype(int); v0 = vi.astype(int); fu = (ui - u0)[..., None]; fv = (vi - v0)[..., None]
        samp = (img[v0, u0] * (1 - fu) * (1 - fv) + img[v0, u0 + 1] * fu * (1 - fv) + img[v0 + 1, u0] * (1 - fu) * fv + img[v0 + 1, u0 + 1] * fu * fv)
        out[take] = samp[take]; best[take] = score[take]
    out[np.isinf(best)] = (0.27, 0.27, 0.26, 1.0)    # 캡처가 안 덮은 곳 = 맵 밖 빈 땅 색
    out = out.reshape(OH, ss, OW, ss, 4).mean(axis=(1, 3))
    out[..., 3] = 1.0
    img = bpy.data.images.get("SteelworksMinimap") or bpy.data.images.new("SteelworksMinimap", OW, OH, alpha=True)
    img.scale(OW, OH)
    img.pixels.foreach_set(np.ascontiguousarray(out[::-1]).ravel())
    img.filepath_raw = r"D:\god\exports\steelworks_zone\SteelworksMinimap.png"; img.file_format = 'PNG'; img.save()
    return img.filepath_raw, OW, OH
