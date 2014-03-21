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


bl_info = {
    'name': 'extend multi edges (BMesh, bgl)',
    'author': 'zeffii',
    'version': (0, 0, 3),
    'blender': (2, 7, 0),
    'location': '',
    'warning': '',
    'description': '',
    'wiki_url': '',
    'tracker_url': '',
    'category': '3D View'
}


import math
import itertools

import bpy
import bgl
import mathutils
import bmesh

from bpy_extras.view3d_utils import location_3d_to_region_2d as loc3d2d
from mathutils.geometry import intersect_line_line as LineIntersect


VTX_PRECISION = 1.0e-5  # or 1.0e-6 ..if you need

line_colors = {
    "prime": (0.2, 0.8, 0.9),
    "extend": (0.9, 0.8, 0.2),
    "projection": (0.9, 0.6, 0.5)
}


def restore_bgl_defaults():
    bgl.glLineWidth(1)
    bgl.glDisable(bgl.GL_BLEND)
    bgl.glColor4f(0.0, 0.0, 0.0, 1.0)


#   returns True / False if a point happens to lie on an edge
def point_on_edge(point, edge):
    A, B = edge
    eps = (((A - B).length - (point - B).length) - (A - point).length)
    return abs(eps) < VTX_PRECISION


def get_prime(self):
    vp = self.bm.edges[self.edge_prime_idx].verts
    return vp[0].co, vp[1].co


def intersection_edge(edge_prime, edge):
    p1, p2 = edge_prime
    p3, p4 = edge
    line = LineIntersect(p1, p2, p3, p4)
    return ((line[0] + line[1]) / 2)


def get_intersection(self, idx):
    edge_prime = get_prime(self)
    v = self.bm.edges[idx].verts
    edge = (v[0].co, v[1].co)
    return intersection_edge(edge_prime, edge)


def closest(p, e):
    '''p is a vector, e is a bmesh edge'''
    ev = e.verts
    v1 = ev[0].co
    v2 = ev[1].co
    distance_test = (v1 - p).length < (v2 - p).length
    return ev[0].index if distance_test else ev[1].index


def coords_from_idx(self, idx):
    v = self.bm.edges[idx].verts
    return (v[0].co, v[1].co)


def get_projection_coords(self):
    list2d = [val for key, val in self.xvectors.items()]
    list2d = [[p, self.bm.verts[pidx].co] for (p, pidx) in list2d]
    return list(itertools.chain.from_iterable(list2d))


def get_extender_coords(self):
    coords = []
    for idx in self.selected_edges:
        c = coords_from_idx(self, idx)
        coords.extend(c)
    return coords


def add_or_remove_new_edge(self, idx):
    '''
        - only add idx if not edge_prime
        - and not currently present in selected_edges
    '''
    if idx == self.edge_prime_idx:
        print(idx, 'is edge prime, not adding')
        return

    present = (idx in self.selected_edges)
    if present:
        self.selected_edges.remove(idx)
        del self.xvectors[idx]
    else:

        p = get_intersection(self, idx)
        edge_prime = get_prime(self)

        if not point_on_edge(p, edge_prime):
            return

        vert_idx_closest = closest(p, self.bm.edges[idx])
        self.xvectors[idx] = [p, vert_idx_closest]
        self.selected_edges.append(idx)


def set_mesh_data(self):
    history = self.bm.select_history
    if not (len(history) > 0):
        return

    a = history[-1]
    if not isinstance(a, bmesh.types.BMEdge):
        return

    add_or_remove_new_edge(self, a.index)
    a.select = False


def draw_callback_px(self, context, event):

    if context.mode != "EDIT_MESH":
        return

    # get screen information
    region = context.region
    rv3d = context.space_data.region_3d
    this_object = context.active_object
    matrix_world = this_object.matrix_world
    # scene = context.scene

    def draw_gl_strip(coords, line_thickness):
        bgl.glLineWidth(line_thickness)
        bgl.glBegin(bgl.GL_LINES)
        for coord in coords:
            vector3d = matrix_world * coord
            vector2d = loc3d2d(region, rv3d, vector3d)
            bgl.glVertex2f(*vector2d)
        bgl.glEnd()

    def draw_edge(coords, mode, lt):
        bgl.glColor3f(*line_colors[mode])
        draw_gl_strip(coords, lt)

    # def draw_cursor():
    #     hsize = 2
    #     cmx, cmy = self.mx, self.my
    #     p1 = cmx - hsize, cmy - hsize
    #     p2 = cmx + hsize, cmy - hsize
    #     p3 = cmx + hsize, cmy + hsize
    #     p4 = cmx - hsize, cmy + hsize
    #     coords = [p1, p2, p3, p4, p1]
    #     print(coords)

    #     bgl.glColor3f(*line_colors["cursor"])
    #     bgl.glLineWidth(1)
    #     bgl.glBegin(bgl.GL_LINE_LOOP)
    #     for coord in coords:
    #         bgl.glVertex2f(*coord)
    #     bgl.glEnd()

    def do_single_draw_pass(self):

        # draw edge prime
        c = coords_from_idx(self, self.edge_prime_idx)
        draw_edge(c, "prime", 3)

        # draw extender edges and projections.
        if len(self.selected_edges) > 0:

            # get and draw selected valid edges
            coords_ext = get_extender_coords(self)
            draw_edge(coords_ext, "extend", 3)

            # get and draw extenders only
            coords_proj = get_projection_coords(self)
            draw_edge(coords_proj, "projection", 3)

        restore_bgl_defaults()

    # draw_cursor()
    do_single_draw_pass(self)


class ExtendEdgesMulti(bpy.types.Operator):
    bl_idname = "view3d.extend_eges"
    bl_label = "extend_edges"
    bl_description = "extend edge"

    @classmethod
    def poll(cls, context):
        return context.mode == "EDIT_MESH"

    def add_geometry(self, context):
        list2d = [val for key, val in self.xvectors.items()]
        vertex_count = len(self.bm.verts)

        for point, closest_idx in list2d:
            self.bm.verts.new((point))
            v1 = self.bm.verts[-1]
            v2 = self.bm.verts[closest_idx]
            self.bm.edges.new((v1, v2))

        bmesh.update_edit_mesh(self.me)

    def modal(self, context, event):

        if event.type in ('PERIOD'):
            bpy.types.SpaceView3D.draw_handler_remove(self.handle, 'WINDOW')
            bpy.context.space_data.show_manipulator = True
            self.add_geometry(context)
            del self.selected_edges
            del self.xvectors
            return {'FINISHED'}

        if (event.type, event.value) == ("RIGHTMOUSE", "RELEASE"):
            set_mesh_data(self)

        if context.area:
            context.area.tag_redraw()

        return {'PASS_THROUGH'}

    def invoke(self, context, event):
        if context.area.type == "VIEW_3D":

            self.selected_edges = []
            self.xvectors = {}
            self.me = context.active_object.data
            self.bm = bmesh.from_edit_mesh(self.me)
            self.me.update()

            # enforce singular edge selection first then assign to edge_prime
            m = [e.index for e in self.bm.edges if e.select]
            if not len(m) is 1:
                self.report({"WARNING"}, "Please select 1 edge only")
                return {'CANCELLED'}

            # switch off axial manipulator, set important variables.
            self.edge_prime_idx = m[0]
            bpy.context.space_data.show_manipulator = False

            # configure draw handler
            fparams = self, context, event
            handler_config = draw_callback_px, fparams, 'WINDOW', 'POST_PIXEL'
            draw_handler_add = bpy.types.SpaceView3D.draw_handler_add
            self.handle = draw_handler_add(*handler_config)

            context.window_manager.modal_handler_add(self)
            return {'RUNNING_MODAL'}
        else:
            self.report({"WARNING"}, "Please run operator from within 3d view")
            return {'CANCELLED'}


def register():
    bpy.utils.register_class(ExtendEdgesMulti)


def unregister():
    bpy.utils.unregister_class(ExtendEdgesMulti)


if __name__ == "__main__":
    register()
