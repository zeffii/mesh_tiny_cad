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

import bpy
import bmesh
from mathutils import geometry
from mesh_tinyCAD import cad_module as cm


def add_line_to_bisection(self):

    obj = bpy.context.object
    me = obj.data
    bm = bmesh.from_edit_mesh(me)

    edges = [e for e in bm.edges if (e.select and not e.hide)]

    if not len(edges) == 2:
        msg = "select two coplanar non parallel edges"
        self.report({"WARNING"}, msg)
        return

    [[v1, v2], [v3, v4]] = [[v.co for v in e.verts] for e in edges]
    print(v1, '\n', v2, '\n', v3, '\n', v4, '\n\n')

    dist1 = (v1-v2).length
    dist2 = (v2-v3).length
    bdist = min([dist1, dist2])
    edge1 = (v1, v2)
    edge2 = (v3, v4)

    if not cm.test_coplanar(edge1, edge2):
        msg = "edges must be coplanar non parallel edges"
        self.report({"WARNING"}, msg)
        return

    pt = cm.get_intersection(edge1, edge2)

    # pick fartest vertex from (projected) intersections
    far1 = v2 if (pt-v1).length < (pt-v2).length else v1
    far2 = v4 if (pt-v3).length < (pt-v4).length else v3
    dex1 = far1 - pt
    dex2 = far2 - pt
    dex1 = dex1 * (bdist / dex1.length)
    dex2 = dex2 * (bdist / dex2.length)
    pt2 = (pt+dex1).lerp((pt+dex2), 0.5)

    bm.verts.new(pt)
    bm.verts.new(pt2)
    bm.edges.new((bm.verts[-2], bm.verts[-1]))
    bmesh.update_edit_mesh(me)
    print("awesome")


class LineOnBisection(bpy.types.Operator):

    bl_idname = 'mesh.linetobisect'
    bl_label = 'bix line to bisector'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(self, context):
        obj = context.active_object
        return all([obj is not None, obj.type == 'MESH', obj.mode == 'EDIT'])

    def execute(self, context):
        add_line_to_bisection(self)
        return {'FINISHED'}
