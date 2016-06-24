import bpy
import sys
import bmesh
from mathutils import Vector
from mathutils.geometry import intersect_line_line as LineIntersect
from mathutils.geometry import intersect_point_line as PtLineIntersect

from . import cad_module as cm


def get_vert_indices_from_bmedges(bm, edges):
    temp_edges = []
    for e in [e for e in bm.edges if e.select]:
        for v in e.verts[:]:
            temp_edges.extend(v.index)
    return temp_edges


def do_vtx_if_appropriate(bm, edges):
    vertex_indices = get_vert_indices_from_bmedges(bn, edges)
    
    # test 1 , are there shared vers? if so return non-viable
    if not len(set(vertex_indices)) == 4:
        return

    # test 2 , are any of the vertex coordintes within epsilon ?
    # [   not implement, overkill?  ]

    


    edge_indices = [e.index for e in edges]

    return bm


class TCAutoVTX(bpy.types.Operator):
    bl_idname = 'tinycad.autovtx'
    bl_label = 'VTX autoVTX'

    VTX_PRECISION = 1.0e-5

    @classmethod
    def poll(self, context):
        obj = context.active_object
        return bool(obj) and obj.type == 'MESH'

    def cancel_message(self, msg):
        print(msg)
        self.report({"WARNING"}, msg)
        return {'CANCELLED'}

    def execute(self, context):
        obj = context.active_object
        me = obj.data
        bm = bmesh.from_edit_mesh(me)
        bm.verts.ensure_lookup_table()
        bm.edges.ensure_lookup_table()

        edges = [e for e in bm.edges if e.select and not e.hide]

        if len(edges) == 2:
            bm = do_vtx_if_appropriate(bm, edges)
            if not bm:
                msg = 'edges parallel or non-planar, no intersection possible'
                return self.cancel_message(msg)
        else:
            return self.cancel_message('select two edges!')

        bmesh.update_edit_mesh(me, True)
        return {'FINISHED'}


def register():
    bpy.utils.register_module(__name__)


def unregister():
    bpy.utils.unregister_module(__name__)
