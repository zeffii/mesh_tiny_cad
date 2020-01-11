# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# <pep8 compliant>


import bpy
import bmesh
from mathutils import geometry


def add_vertex_to_intersection():
    objs = bpy.context.selected_objects
    fobj = bpy.context.active_object
    #making sure the active object is the last object in the "objs"-list
    #Important as it makes sure the new vertex is added
    #in the mesh of the object of which the edge was selected first
    objs.remove(fobj)
    objs.append(fobj)
    
    #working with one object
    if len(objs)==1:
        me = objs[0].data
        #matrix needed for global coordinates
        wm = objs[0].matrix_world
        bme = bmesh.from_edit_mesh(me)
        edges = [e for e in bme.edges if e.select]

        if len(edges) == 2:
            [[v1, v2], [v3, v4]] = [[wm @ v.co for v in e.verts] for e in edges]

    #working with 2 objects
    if len(objs)==2:
        me = objs[0].data
        wm = objs[0].matrix_world
        he = objs[1].data
        wm1 = objs[1].matrix_world
        bme = bmesh.from_edit_mesh(me)
        bhe = bmesh.from_edit_mesh(he)

        edgesme = [e for e in bme.edges if e.select]
        edgeshe = [e for e in bhe.edges if e.select]

        if len(edgesme) == 1 and len(edgeshe) == 1:
            [v1, v2] = [wm @ v.co for v in edgesme[0].verts]
            [v3, v4] = [wm1 @ v.co for v in edgeshe[0].verts]

        bhe.free()

    iv = geometry.intersect_line_line(v1, v2, v3, v4)

    if iv:
        iv = (iv[0] + iv[1]) / 2
        bme.verts.new(iv)
        bme.verts.ensure_lookup_table()
        bme.verts[-1].select = True
        bmesh.update_edit_mesh(me)

class TCVert2Intersection(bpy.types.Operator):
    '''Add a vertex at the intersection (projected or real) of two selected edges of up to 2 objects'''
    bl_idname = 'tinycad.vertintersect'
    bl_label = 'V2X vertex to intersection'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        objs = context.selected_objects
        if len(objs) >2 or len(objs)==0:
            return 0
        for obj in objs:
            if obj is None or obj.type != 'MESH' or obj.mode != 'EDIT':
                return 0
        return 1

    def execute(self, context):
        add_vertex_to_intersection()
        return {'FINISHED'}
