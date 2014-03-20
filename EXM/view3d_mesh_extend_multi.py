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
    'version': (0, 0, 2),
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
    "projection": (0.9, 0.6, 0.5),
    "cursor": (0.9, 0.9, 0.2)
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


def get_prime(self, bm):
    edge_prime_idx = self.selected_edges[0]
    vp = bm.edges[edge_prime_idx].verts
    edge_prime = (vp[0].co, vp[1].co)
    return edge_prime


def intersection_edge(edge_prime, edge):
    p1, p2 = edge_prime
    p3, p4 = edge
    line = LineIntersect(p1, p2, p3, p4)
    return ((line[0] + line[1]) / 2)


def get_intersection(self, idx, bm):
    edge_prime = get_prime(self, bm)
    v = bm.edges[idx].verts
    edge = (v[0].co, v[1].co)
    return intersection_edge(edge_prime, edge)


def closest(p, e):
    '''p is a vector, e is a bmesh edge'''
    ev = e.verts
    v1 = ev[0].co
    v2 = ev[1].co
    distance_test = (v1 - p).length < (v2 - p).length
    return ev[0].index if distance_test else ev[1].index


def coords_from_idx(bm, idx):
    v = bm.edges[idx].verts
    return (v[0].co, v[1].co)


def get_projection_coords(self, bm):
    list2d = [val for key, val in self.xvectors.items()]
    list2d = [[p, bm.verts[pidx].co] for (p, pidx) in list2d]
    return list(itertools.chain.from_iterable(list2d))


def get_extender_coords(self, bm):
    coords = []
    for idx in self.selected_edges[1:]:
        c = coords_from_idx(bm, idx)
        coords.extend(c)
    return coords


def populate_vector_lists(self, bm):
    # this segment adds each new edge to the select_edges list
    for idx, e in enumerate(bm.edges):
        if e.hide:
            continue

        if e.select:
            if idx in self.selected_edges:
                continue

            # boom, edge_prime
            if len(self.selected_edges) == 0:
                self.selected_edges.append(idx)
                continue

            # now check if the newly selected edge intersects
            # (p will always be a vector, but it might not be an intersection)
            p = get_intersection(self, idx, bm)
            edge_prime = get_prime(self, bm)

            if not point_on_edge(p, edge_prime):
                e.select = False
                continue

            if point_on_edge(p, edge_prime):
                vert_idx_closest = closest(p, e)
                self.selected_edges.append(idx)
                self.xvectors[idx] = [p, vert_idx_closest]
                continue
            else:
                e.select = False

        else:
            if idx in self.selected_edges:
                self.selected_edges.remove(idx)

                if idx in self.xvectors:
                    del self.xvectors[idx]


def hid_states(self, event):

    if event.type in self.hid_state_dict:
        if self.hid_state_dict[event.type] == 0:
            if event.value == 'PRESS':
                self.hid_state_dict[event.type] = 1
        else:
            if event.value == 'RELEASE':
                self.hid_state_dict[event.type] = 0
                return True

    return False


def draw_callback_px(self, context, event):

    if context.mode != "EDIT_MESH":
        return

    self.state = hid_states(self, event)

    # get screen information
    region = context.region
    rv3d = context.space_data.region_3d
    this_object = context.active_object
    matrix_world = this_object.matrix_world

    scene = context.scene
    me = context.active_object.data
    bm = bmesh.from_edit_mesh(me)
    me.update()

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

    def do_single_draw_pass(self, bm):
        num_selected = len(self.selected_edges)

        # draw edge prime
        if num_selected > 0:
            idx = self.selected_edges[0]
            c = coords_from_idx(bm, idx)
            draw_edge(c, "prime", 3)

        # draw extender edges and projections.
        if num_selected > 1:

            # get and draw selected valid edges
            coords_ext = get_extender_coords(self, bm)
            draw_edge(coords_ext, "extend", 3)

            # get and draw extenders only
            coords_proj = get_projection_coords(self, bm)
            draw_edge(coords_proj, "projection", 3)

        restore_bgl_defaults()

    # only in the event of interaction, admittedly indiscriminate, shall
    # the vector list be updates.
    if self.state:
        populate_vector_lists(self, bm)

    # draw_cursor()
    do_single_draw_pass(self, bm)


class ExtendMultipleEdges(bpy.types.Operator):
    bl_idname = "view3d.extend_edges"
    bl_label = "extend all"
    bl_description = "Extends all edges towards a prime edge"

    selected_edges = []
    xvectors = {}
    handle = None
    state = True

    hid_state_dict = {
        'LEFTMOUSE': 0,
        'RIGHTMOUSE': 0,
        'LEFT_SHIFT': 0,
        'MIDDLEMOUSE': 0
    }

    # mx, my = None, None

    @classmethod
    def poll(cls, context):
        return context.mode == "EDIT_MESH"

    def unselect_all(self, context):
        me = context.active_object.data
        bm = bmesh.from_edit_mesh(me)
        me.update()
        for e in bm.edges:
            e.select = False

    def add_geometry(self, context):
        list2d = [val for key, val in self.xvectors.items()]
        me = context.active_object.data
        bm = bmesh.from_edit_mesh(me)
        vertex_count = len(bm.verts)

        for point, closest_idx in list2d:
            bm.verts.new((point))
            bm.edges.new((bm.verts[-1], bm.verts[closest_idx]))

        bmesh.update_edit_mesh(me)

    def modal(self, context, event):

        if event.type in ('PERIOD'):
            bpy.types.SpaceView3D.draw_handler_remove(self.handle, 'WINDOW')
            self.add_geometry(context)
            return {'FINISHED'}

        # if event.type == 'MOUSEMOVE':
        #     self.mx = event.mouse_region_x
        #     self.my = event.mouse_region_y

        if context.area and self.state:
            context.area.tag_redraw()

        return {'PASS_THROUGH'}

    def invoke(self, context, event):
        if context.area.type == "VIEW_3D":

            # scrub selections and storage
            self.selected_edges = []
            self.xvectors = {}
            self.unselect_all(context)

            fparams = (self, context, event)
            self.handle = bpy.types.SpaceView3D.draw_handler_add(
                draw_callback_px, fparams, 'WINDOW', 'POST_PIXEL')
            context.window_manager.modal_handler_add(self)
            return {'RUNNING_MODAL'}
        else:
            self.report({"WARNING"}, "View3D not found, can't run operator")
            return {'CANCELLED'}


def register():
    bpy.utils.register_class(ExtendMultipleEdges)


def unregister():
    bpy.utils.unregister_class(ExtendMultipleEdges)


if __name__ == "__main__":
    register()
