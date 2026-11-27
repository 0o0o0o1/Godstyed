# 컬렉션 안 메시 겹침 전수 검사 (Blender, exec → check_overlaps(["Chapel", ...]))
# 오브젝트를 떨어진 덩어리(loose part) 단위로 나눠, 덩어리마다 안쪽으로 shrink(기본 0.03) 줄인 BVH 끼리 겹침 검사.
# 닿기만 하는 면은 줄이면 떨어지므로 걸리지 않고, 실제로 파고든 것만 나옴.
import bpy, bmesh
from mathutils import Vector
from mathutils.bvhtree import BVHTree


def _islands(ob):
    bm = bmesh.new(); bm.from_mesh(ob.data); bm.transform(ob.matrix_world)
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-4)   # 면마다 따로 만든 꼭짓점 합치기
    bm.verts.ensure_lookup_table(); bm.faces.ensure_lookup_table()
    bm.verts.index_update(); bm.faces.index_update()
    seen, out = set(), []
    for f in bm.faces:
        if f.index in seen:
            continue
        stack, comp = [f], []
        seen.add(f.index)
        while stack:
            g = stack.pop(); comp.append(g)
            for e in g.edges:
                for h in e.link_faces:
                    if h.index not in seen:
                        seen.add(h.index); stack.append(h)
        out.append(comp)
    res = []
    for comp in out:
        vids = sorted({v.index for f in comp for v in f.verts})
        remap = {vi: k for k, vi in enumerate(vids)}
        nb = bmesh.new()
        nv = [nb.verts.new(bm.verts[vi].co.copy()) for vi in vids]
        for f in comp:
            try:
                nb.faces.new([nv[remap[v.index]] for v in f.verts])
            except ValueError:
                pass
        res.append(nb)
    bm.free()
    return res


def check_overlaps(colls, shrink=0.03, limit=80):
    lines = []
    for cn in colls:
        col = bpy.data.collections[cn]
        items = []
        for ob in col.all_objects:
            if ob.type != 'MESH' or ob.name.endswith(("_IvyLeaves", "_IvyStems", "_Moss")):
                continue   # 잎·이끼는 판 수천 장이라 따로 (생성할 때 표면 거리 검사로 보장)
            for i, nb in enumerate(_islands(ob)):
                bmesh.ops.recalc_face_normals(nb, faces=nb.faces)
                nb.normal_update()
                mn = Vector((1e9, 1e9, 1e9)); mx = Vector((-1e9, -1e9, -1e9))
                for v in nb.verts:
                    mn = Vector(map(min, mn, v.co)); mx = Vector(map(max, mx, v.co))
                for v in nb.verts:
                    v.co = v.co - v.normal * shrink
                items.append((ob.name, i, mn, mx, BVHTree.FromBMesh(nb), (mn + mx) / 2))
                nb.free()
        hits = []
        for a in range(len(items)):
            na, ia, mna, mxa, ta, ca = items[a]
            for b in range(a + 1, len(items)):
                nb_, ib, mnb, mxb, tb, cb = items[b]
                if any(mxa[k] < mnb[k] or mxb[k] < mna[k] for k in range(3)):
                    continue
                n = len(ta.overlap(tb))
                if n:
                    hits.append((na, ia, nb_, ib, n, ca, cb))
        lines.append("%s: %d parts, %d overlapping pairs" % (cn, len(items), len(hits)))
        for h in hits[:limit]:
            # Roblox 좌표로 위치 표시 (-x, z, y)
            lines.append("  %s#%d x %s#%d (%d)  at R(%.1f,%.1f,%.1f) / R(%.1f,%.1f,%.1f)" % (
                h[0], h[1], h[2], h[3], h[4], -h[5].x, h[5].z, h[5].y, -h[6].x, h[6].z, h[6].y))
    return "\n".join(lines)
