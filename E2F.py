'''
BEGIN GPL LICENSE BLOCK

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software Foundation,
Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

END GPL LICENCE BLOCK
'''

import bpy
import bmesh
import mathutils
from mathutils.geometry import intersect_line_plane


def extend_vertex():

    obj = bpy.context.edit_object
    me = obj.data
    bm = bmesh.from_edit_mesh(me)
    verts = bm.verts
    faces = bm.faces

    plane = [f for f in faces if f.select][0]
    plane_vert_indices = [v for v in plane.verts[:]]
    all_selected_vert_indices = [v for v in verts if v.select]

    M = set(plane_vert_indices)
    N = set(all_selected_vert_indices)
    O = N.difference(M)
    O = list(O)
    (v1_ref, v1_idx, v1), (v2_ref, v2_idx, v2) = [(i, i.index, i.co) for i in O]

    plane_co = plane.calc_center_median()
    plane_no = plane.normal

    new_co = intersect_line_plane(v1, v2, plane_co, plane_no, False)
    new_vertex = verts.new(new_co)

    A_len = (v1 - new_co).length
    B_len = (v2 - new_co).length

    vertex_reference = v1_ref if (A_len < B_len) else v2_ref
    bm.edges.new([vertex_reference, new_vertex])

    bmesh.update_edit_mesh(me, True)


class TCEdgeToFace(bpy.types.Operator):

    bl_idname = 'tinycad.edge_to_face'
    bl_label = 'E2F edge to face'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(self, context):
        ob = context.object
        return all([bool(ob), ob.type == 'MESH', ob.mode == 'EDIT'])

    def execute(self, context):
        extend_vertex()
        return {'FINISHED'}


def register():
    bpy.utils.register_module(__name__)


def unregister():
    bpy.utils.unregister_module(__name__)
