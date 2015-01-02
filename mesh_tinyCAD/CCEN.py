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

import math

import bpy
import bmesh
import mathutils
from mathutils import geometry
from mathutils import Vector


def generate_gp3d_stroke(p1, axis, v1, radius=1.0):

    # get grease pencil data
    # hella clunky for testing.
    # grease_pencil_name = 'tc_circle_000'
    # layer_name = "TinyCad Layer"

    # if grease_pencil_name not in bpy.data.grease_pencil:
    #     gp = bpy.data.grease_pencil.new(grease_pencil_name)
    # else:
    #     gp = bpy.data.grease_pencil[grease_pencil_name]

    # # get grease pencil layer
    # if not (layer_name in gp.layers):
    #     layer = gp.layers.new(layer_name)
    #     layer.frames.new(1)
    #     layer.line_width = 1
    # else:
    #     layer = gp.layers[layer_name]
    #     layer.frames[0].clear()

    #     s = layer.frames[0].strokes.new()
    #     s.draw_mode = '3DSPACE'

    #     num_verts = 20
    #     chain = []
    #     for i in range(num_verts+1):
    #         mat_rot = mathutils.Matrix.Rotation(((360 / num_verts) * i), 4, axis)
    #         chain.append(((v1 - p1) * mat_rot) + p1)

    #     s.points.add(len(chain))
    #     for idx, p in enumerate(chain):
    #         s.points[idx].co = p

    num_verts = 20
    chain = []
    for i in range(num_verts+1):
        mat_rot = mathutils.Matrix.Rotation(((360 / num_verts) * i), 4, axis)
        point = ((v1 - p1) * mat_rot) + p1
        chain.append(point)
        # bpy.ops.object.add(type='EMPTY', location=point, rotation=(0, 0, 0))

    print(chain)


def generate_3PT_mode_1(pts=[], origin=(0, 0, 0)):
    V = Vector

    # construction
    v1, v2, v3, v4 = V(pts[0]), V(pts[1]), V(pts[1]), V(pts[2])
    edge1_mid = v1.lerp(v2, 0.5)
    edge2_mid = v3.lerp(v4, 0.5)
    axis = geometry.normal(v1, v2, v4)
    mat_rot = mathutils.Matrix.Rotation(math.radians(90.0), 4, axis)

    # triangle edges
    v1_ = ((v1 - edge1_mid) * mat_rot) + edge1_mid
    v2_ = ((v2 - edge1_mid) * mat_rot) + edge1_mid
    v3_ = ((v3 - edge2_mid) * mat_rot) + edge2_mid
    v4_ = ((v4 - edge2_mid) * mat_rot) + edge2_mid

    r = geometry.intersect_line_line(v1_, v2_, v3_, v4_)
    if r:
        p1, _ = r
        bpy.context.scene.cursor_location = p1 + origin
        generate_gp3d_stroke(p1 + origin, axis, v1_ + origin, radius=(v1_-p1).length)
    else:
        print('not on a circle')


def get_three_verts_from_selection(obj):
    me = obj.data
    bm = bmesh.from_edit_mesh(me)

    if hasattr(bm.verts, "ensure_lookup_table"):
        bm.verts.ensure_lookup_table()
        bm.edges.ensure_lookup_table()

    return [v.co[:] for v in bm.verts if v.select], obj.location


class CircleCenter(bpy.types.Operator):

    bl_idname = 'mesh.circlecenter'
    bl_label = 'circle center from selected'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(self, context):
        obj = context.active_object
        return obj is not None and obj.type == 'MESH' and obj.mode == 'EDIT'

    def execute(self, context):
        obj = bpy.context.object
        pts, origin = get_three_verts_from_selection(obj)
        generate_3PT_mode_1(pts, origin)
        return {'FINISHED'}
