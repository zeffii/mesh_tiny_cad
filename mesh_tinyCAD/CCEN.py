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


def generate_gp3d_stroke(r, center, v1, axis):

    # get grease pencil data
    # hella clunky for testing.
    grease_pencil_name = 'tc_circle_000'
    layer_name = "TinyCad Layer"

    grease_data = bpy.data.grease_pencil
    if grease_pencil_name not in grease_data:
        gp = grease_data.new(grease_pencil_name)
    else:
        gp = grease_data[grease_pencil_name]

    # get grease pencil layer
    if not (layer_name in gp.layers):
        layer = gp.layers.new(layer_name)
        layer.frames.new(1)
        layer.line_width = 1
    else:
        layer = gp.layers[layer_name]
        layer.frames[0].clear()

    layer.show_points = True
    layer.color = (0.2, 0.90, .2)
    s = layer.frames[0].strokes.new()
    s.draw_mode = '3DSPACE'

    chain = []
    num_verts = 14
    gamma = 2 * math.pi / num_verts
    for i in range(num_verts+1):
        theta = gamma * i
        mat_rot = mathutils.Matrix.Rotation(theta, 4, axis)
        world_point = (mat_rot * (v1 - center)) + center
        chain.append(world_point)

    s.points.add(len(chain))
    for idx, p in enumerate(chain):
        s.points[idx].co = p


def generate_3PT_mode_1(pts, obj):
    origin = obj.location
    transform_matrix = obj.matrix_local
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
        cp = transform_matrix * p1
        bpy.context.scene.cursor_location = cp

        radius = (transform_matrix * (p1-v1)).length
        generate_gp3d_stroke(radius, cp, transform_matrix*v1, axis)
    else:
        print('not on a circle')


def get_three_verts_from_selection(obj):
    me = obj.data
    bm = bmesh.from_edit_mesh(me)

    if hasattr(bm.verts, "ensure_lookup_table"):
        bm.verts.ensure_lookup_table()
        bm.edges.ensure_lookup_table()

    return [v.co[:] for v in bm.verts if v.select]


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
        pts = get_three_verts_from_selection(obj)
        generate_3PT_mode_1(pts, obj)
        return {'FINISHED'}
