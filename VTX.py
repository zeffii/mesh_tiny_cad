import bpy
import bmesh
from mathutils import Vector
from mathutils.geometry import intersect_line_line as LineIntersect
from mathutils.geometry import intersect_point_line as PtLineIntersect

from . import cad_module as cm

messages = {
    'SHARED_VERTEX': 'Shared Vertex, no intersection possible',
    'PARALLEL_EDGES': 'Edges Parallel, no intersection possible',
    'NON_PLANAR_EDGES': 'Non Planar Edges, no clean intersection point'
}

def get_vert_indices_from_bmedges(edges):
    temp_edges = []
    for e in edges:
        for v in e.verts[:]:
            temp_edges.extend(v.index)
    return temp_edges

def perform_vtx(bm=bm, pt=point, edges=edges, pts=(p1, p2, p3, p4)):
    '''
    csx
    '''

    return bm


def do_vtx_if_appropriate(bm, edges):
    vertex_indices = get_vert_indices_from_bmedges(edges)
    
    # test 1 , are there shared vers? if so return non-viable
    if not len(set(vertex_indices)) == 4:
        return {'SHARED_VERTEX'}

    # test 2 , is parallel? 
    p1, p2, p3, p4 = [bm.verts[i].co for i in vertex_indices]
    point = cm.get_intersection([p1, p2], [p3, p4])
    if not point:
        return {'PARALLEL_EDGES'}

    # test 3 , coplanar edges?
    coplanar = cm.test_coplanar([p1, p2], [p3, p4])
    if not coplanar:
        return {'NON_PLANAR_EDGES'}

    # point must lie on an edge or the virtual extention of an edge
    bm = perform_vtx(bm=bm, pt=point, edges=edges, pts=(p1, p2, p3, p4))
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
            if isinstance(bm, set):
                msg = messages.get(bm.pop())
                return self.cancel_message(msg)
        else:
            return self.cancel_message('select two edges!')

        bmesh.update_edit_mesh(me, True)
        return {'FINISHED'}


def register():
    bpy.utils.register_module(__name__)


def unregister():
    bpy.utils.unregister_module(__name__)
