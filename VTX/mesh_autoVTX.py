'''
BEGIN GPL LICENSE BLOCK

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.    See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software Foundation,
Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

END GPL LICENCE BLOCK
'''

bl_info = {
    "name": "autoVTX",
    "author": "zeffii (aka Dealga McArdle)",
    "version": (1, 0, 0),
    "blender": (2, 7, 0),
    "category": "Mesh",
    "location": "View3D > EditMode > (w) Specials",
    "wiki_url": "",
    "tracker_url": ""
}

"""
rewrite of the VTX addon, it automatically decides based on what
you've selected.

"""

import bpy
import sys
import bmesh
from mathutils import Vector, geometry
from mathutils.geometry import intersect_line_line as LineIntersect
from mathutils.geometry import intersect_point_line as PtLineIntersect


def point_on_edge(p, edge):
    '''
    > p:        vector
    > edge:     tuple of 2 vectors
    < returns:  True / False if a point happens to lie on an edge
    '''
    pt, _percent = PtLineIntersect(p, *edge)
    return (pt-p).length < AutoVTX.VTX_PRECISION


def get_intersection_points(edge1, edge2):
    [p1, p2], [p3, p4] = edge1, edge2
    return LineIntersect(p1, p2, p3, p4)


def intersection_edge(edge1, edge2):
    line = get_intersection_points(edge1, edge2)
    return ((line[0] + line[1]) / 2)


def test_coplanar(edge1, edge2):
    '''
    the line that describes the shortest line between the two edges
    would be short if the lines intersect mathematically. If this
    line is longer than the VTX_PRECISION then they are either
    coplanar or parallel.
    '''
    line = get_intersection_points(edge1, edge2)
    return (line[0]-line[1]).length < AutoVTX.VTX_PRECISION


def closest(p, e):
    '''
    > p:        vector
    > e:        bmesh edge
    < returns:  returns index of vertex closest to that point.
    '''
    ev = e.verts
    v1 = ev[0].co
    v2 = ev[1].co
    distance_test = (v1 - p).length < (v2 - p).length
    return ev[0].index if distance_test else ev[1].index


def coords_from_idx(self, idx):
    v = self.bm.edges[idx].verts
    return v[0].co, v[1].co


def find_intersection_vector(self):
    return intersection_edge(self.edge1, self.edge2)


def find_intersecting_edges(self):
    edges = [None, None]
    if point_on_edge(self.point, self.edge1):
        edges[0] = self.idx1
    if point_on_edge(self.point, self.edge2):
        edges[1] = self.idx2
    return edges


def selected_edges_share_vertices(self):
    ei = [self.bm.edges[i].verts for i in self.selected_edges]
    self.ii = [ei[a][b].index for a, b in [(0, 0), (0, 1), (1, 0), (1, 1)]]
    return len(set(self.ii)) < 4


def getVTX(self):
    self.idx1, self.idx2 = self.selected_edges
    self.edge1 = coords_from_idx(self, self.idx1)
    self.edge2 = coords_from_idx(self, self.idx2)
    self.point = find_intersection_vector(self)
    self.edges = find_intersecting_edges(self)


def vert_idxs_from_edge_idx(self, idx):
    edge = self.bm.edges[idx]
    return edge.verts[0].index, edge.verts[1].index


def add_edges(self, idxs):
    for e in idxs:
        v1 = self.bm.verts[-1]
        v2 = self.bm.verts[e]
        self.bm.edges.new((v1, v2))


def remove_earmarked_edges(self, earmarked):
    edges_select = [e for e in self.bm.edges if e.index in earmarked]
    bmesh.ops.delete(self.bm, geom=edges_select, context=2)


def checkVTX(self, context):
    '''
    - decides VTX automatically.
    - remembers edges attached to current selection, for later.
    '''

    # [x] if either of these edges share a vertex, return early.
    if selected_edges_share_vertices(self):
        msg = "edges share a vertex, degenerate case, returning early"
        self.report({"WARNING"}, msg)
        return False

    # [x] find which edges intersect
    getVTX(self)

    # [x] check coplanar, or parallel.
    if [None, None] == self.edges:
        coplanar = test_coplanar(self.edge1, self.edge2)
        if not coplanar:
            msg = "parallel or not coplanar! returning early"
            self.report({"WARNING"}, msg)
            return False

    return True


def doVTX(self):
    '''
    At this point we know that there is an intersection, and if it
    is V, T or X.
    - If both are None, then both edges are projected towards point. (V)
    - If only one is None, then it's a projection onto a real edge (T)
    - Else, then the intersection lies on both edges (X)
    '''
    print('point:', self.point)
    print('edges selected:', self.idx1, self.idx2)
    print('edges to use:', self.edges)

    self.bm.verts.new((self.point))
    earmarked = []

    # V (projection of both edges)
    if [None, None] == self.edges:
        cl_vert1 = closest(self.point, self.bm.edges[self.idx1])
        cl_vert2 = closest(self.point, self.bm.edges[self.idx2])
        add_edges(self, [cl_vert1, cl_vert2])

    # X (weld intersection)
    elif all(self.edges):
        add_edges(self, self.ii)
        earmarked = self.edges

    # T (extend towards)
    else:
        # this picks the non None member.
        to_edge_idx = [i for i in self.edges if i][0]
        from_edge_idx = self.idx1 if to_edge_idx == self.idx2 else self.idx2

        # make 3 new edges: 2 on the towards, 1 as extender
        cl_vert = closest(self.point, self.bm.edges[from_edge_idx])
        to_vert1, to_vert2 = vert_idxs_from_edge_idx(self, to_edge_idx)
        roto_indices = [cl_vert, to_vert1, to_vert2]
        add_edges(self, roto_indices)
        earmarked = [to_edge_idx]

    # final refresh before returning to user.
    if earmarked:
        remove_earmarked_edges(self, earmarked)
    bmesh.update_edit_mesh(self.me, True)


class AutoVTX(bpy.types.Operator):
    bl_idname = 'view3d.autovtx'
    bl_label = 'autoVTX'
    # bl_options = {'REGISTER', 'UNDO'}

    VTX_PRECISION = 1.0e-5  # or 1.0e-6 ..if you need

    @classmethod
    def poll(self, context):
        '''
        - only activate if two selected edges
        - and both are not hidden
        '''
        obj = context.active_object
        self.me = obj.data
        self.bm = bmesh.from_edit_mesh(self.me)
        self.me.update()

        if obj is not None and obj.type == 'MESH':
            edges = self.bm.edges
            ok = lambda v: v.select and not v.hide
            idxs = [v.index for v in edges if ok(v)]
            if len(idxs) is 2:
                self.selected_edges = idxs
                return True

    def execute(self, context):
        if checkVTX(self, context):
            doVTX(self)

        return {'FINISHED'}


def menu_func(self, context):
    nm = "Edges VTX Intersection"
    self.layout.operator(AutoVTX.bl_idname, text=nm)


def register():
    bpy.utils.register_class(AutoVTX)
    bpy.types.VIEW3D_MT_edit_mesh_specials.append(menu_func)


def unregister():
    bpy.utils.unregister_class(AutoVTX)
    bpy.types.VIEW3D_MT_edit_mesh_specials.remove(menu_func)


if __name__ == "__main__":
    register()
