# 노점 컨테이너 몸체 타일 텍스처 StallSteel (tex_kit 먼저 exec 할 것)
# U = 길이 24 스터드 (이음매 없이 반복), V = 높이 0..12 스터드 (아래 때·위 녹 번짐, 반복 안 함).
# 메쉬 UV: u = 길이/24 (+칸별 오프셋), v = 높이/12. 지붕은 v = 0.62 + 폭/40.
import bpy, math

STALL_PAINTS = {
    "RustRed": (0.205, 0.045, 0.026),
    "FadedBlue": (0.040, 0.082, 0.125),
    "Olive": (0.085, 0.095, 0.045),
    "DirtyWhite": (0.40, 0.38, 0.33),
}


def ring_u(nt, sep, kv, seed):
    """U 만 이어지는 좌표: (cos2πu, sin2πu, v*kv), W = seed. kv = π 면 가로·세로 같은 비율."""
    mu = mathn(nt, "MULTIPLY", None, TAU); L(nt, sep, 0, mu, 0)
    cu = mathn(nt, "COSINE"); su = mathn(nt, "SINE"); L(nt, mu, 0, cu, 0); L(nt, mu, 0, su, 0)
    mv = mathn(nt, "MULTIPLY", None, kv); L(nt, sep, 1, mv, 0)
    comb = N(nt, "ShaderNodeCombineXYZ")
    L(nt, cu, 0, comb, 0); L(nt, su, 0, comb, 1); L(nt, mv, 0, comb, 2)
    w = mathn(nt, "ADD", seed, 0.0)
    return comb, w


def mx(nt, a, ao, b, bo):
    n = mathn(nt, "MAXIMUM"); L(nt, a, ao, n, 0); L(nt, b, bo, n, 1); return n


def stall_mat(name, paint, seed=31.0):
    m, nt, sep = new_mat(name)
    P, W = ring_u(nt, sep, math.pi, seed)
    Ps, Ws = ring_u(nt, sep, math.pi * 0.07, seed + 3.0)      # 세로로 늘어진 좌표 (녹물 줄)
    v = sep  # output 1 = v
    tone = noise4(nt, P, W, 1.1, 3, 0.5)
    rbig = noise4(nt, P, W, 1.8, 6, 0.6)
    rmed = noise4(nt, P, W, 4.5, 8, 0.6)
    fine = noise4(nt, P, W, 22.0, 6, 0.6)
    chipn = noise4(nt, P, W, 9.0, 12, 0.72)
    streakn = noise4(nt, Ps, Ws, 7.0, 4, 0.55)
    grimen = noise4(nt, P, W, 2.6, 5, 0.6)

    top = mrange(nt, v, 1, 0.86, 0.985, 0.0, 1.0)
    bot = mrange(nt, v, 1, 0.0, 0.11, 1.0, 0.0)
    edge_band = mathn(nt, "ADD"); L(nt, top, 0, edge_band, 0); L(nt, bot, 0, edge_band, 1)
    edge_rust = mul(nt, edge_band, 0, mrange(nt, rmed, "Fac", 0.40, 0.58, 0.0, 1.0), 0)
    rust_patch = mul(nt, mrange(nt, rbig, "Fac", 0.585, 0.635, 0.0, 1.0), 0, mrange(nt, fine, "Fac", 0.30, 0.55, 0.55, 1.0), 0)
    rustm = mx(nt, rust_patch, 0, edge_rust, 0)
    streak = mul(nt, mrange(nt, streakn, "Fac", 0.52, 0.66, 0.0, 0.9), 0, mrange(nt, v, 1, 0.08, 0.95, 0.15, 1.0), 0)
    chip = mrange(nt, chipn, "Fac", 0.625, 0.64, 0.0, 1.0)
    grime = mul(nt, mrange(nt, v, 1, 0.0, 0.30, 1.0, 0.0), 0, mrange(nt, grimen, "Fac", 0.35, 0.65, 0.35, 1.0), 0)
    sunf = mul(nt, mrange(nt, v, 1, 0.45, 1.0, 0.0, 0.30), 0, mrange(nt, tone, "Fac", 0.3, 0.7, 0.4, 1.0), 0)

    pr, pg, pb = paint
    c_paint = rgb(nt, paint)
    c_dark = rgb(nt, (pr * 0.62, pg * 0.62, pb * 0.62))
    c_bleach = rgb(nt, (min(1, pr * 1.45 + 0.05), min(1, pg * 1.45 + 0.05), min(1, pb * 1.45 + 0.05)))
    c0 = mix(nt, mrange(nt, tone, "Fac", 0.3, 0.7, 0.0, 1.0), 0, c_dark, c_paint)
    c1 = mix(nt, sunf, 0, c0, c_bleach)
    c2 = mix(nt, streak, 0, c1, rgb(nt, (0.10, 0.042, 0.02)))
    r_col = mix(nt, mrange(nt, rmed, "Fac", 0.35, 0.65, 0.0, 1.0), 0, rgb(nt, (0.24, 0.085, 0.032)), rgb(nt, (0.09, 0.04, 0.02)))
    r_col2 = mix(nt, mrange(nt, fine, "Fac", 0.45, 0.62, 0.0, 0.6), 0, r_col, rgb(nt, (0.04, 0.025, 0.018)))
    c3 = mix(nt, rustm, 0, c2, r_col2)
    c4 = mix(nt, chip, 0, c3, rgb(nt, (0.085, 0.075, 0.068)))
    c5 = mix(nt, mul(nt, grime, 0, mathn(nt, "ADD", 0.8, 0.0), 0), 0, c4, rgb(nt, (0.075, 0.066, 0.052)))
    out_emit(nt, "Color", c5, 2)

    rough = mix(nt, streak, 0, rgb(nt, (0.58, 0.58, 0.58)), rgb(nt, (0.78, 0.78, 0.78)))
    rough = mix(nt, rustm, 0, rough, rgb(nt, (0.93, 0.93, 0.93)))
    rough = mix(nt, chip, 0, rough, rgb(nt, (0.48, 0.48, 0.48)))
    rough = mix(nt, grime, 0, rough, rgb(nt, (0.9, 0.9, 0.9)))
    out_emit(nt, "Rough", rough, 2)
    metal = mix(nt, chip, 0, rgb(nt, (0.0, 0.0, 0.0)), rgb(nt, (0.55, 0.55, 0.55)))
    metal = mix(nt, rustm, 0, metal, rgb(nt, (0.04, 0.04, 0.04)))
    out_emit(nt, "Metal", metal, 2)

    h = madd(nt, chip, 0, -0.35, mul(nt, rustm, 0, rmed, "Fac"), 0)     # 페인트 벗겨진 곳은 낮게
    h = madd(nt, fine, "Fac", 0.25, h, 0)
    h = madd(nt, rustm, 0, 0.2, h, 0)
    out_normal(nt, h, 0, 0.55, 0.02)
    return m


def build_mats():
    names = []
    for k, col in STALL_PAINTS.items():
        stall_mat("TX_Stall_" + k, col)
        names.append("TX_Stall_" + k)
    return names
