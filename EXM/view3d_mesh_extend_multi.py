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
    'version': (0, 0, 1),
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
    # restore opengl defaults
    bgl.glLineWidth(1)
    bgl.glDisable(bgl.GL_BLEND)
    bgl.glColor4f(0.0, 0.0, 0.0, 1.0)


#   returns distance between two given points
def mDist(A, B):
    return (A-B).length


#   returns True / False if a point happens to lie on an edge
def point_on_edge(point, edge):
    A, B = edge
    eps = ((mDist(A, B) - mDist(point, B)) - mDist(A, point))
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
    ev = e.verts
    v1 = ev[0].co
    v2 = ev[1].co
    distance_test = mDist(v1, p) < mDist(v2, p)
    return ev[0].index if distance_test else ev[1].index


# calculate locations and store them as ID property in the mesh
def draw_callback_px(self, context):

    if context.mode != "EDIT_MESH":
        return

    # get screen information
    region = context.region
    rv3d = context.space_data.region_3d
    this_object = context.active_object
    matrix_world = this_object.matrix_world

    def draw_gl_strip(coords, line_thickness):
        bgl.glLineWidth(line_thickness)
        bgl.glBegin(bgl.GL_LINES)
        for coord in coords:
            vector3d = matrix_world * coord
            vector2d = loc3d2d(region, rv3d, vector3d)
            bgl.glVertex2f(*vector2d)
        bgl.glEnd()

    def draw_edge(coords, mode):
        bgl.glColor3f(*line_colors[mode])
        draw_gl_strip(coords, 3)

    scene = context.scene
    me = context.active_object.data
    bm = bmesh.from_edit_mesh(me)
    me.update()

    # this segment adds each new edge to the select_edges storage
    # suboptimal..
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
                del self.xvectors[idx]

    num_selected = len(self.selected_edges)
    print(self.selected_edges)

    # draw edge prime
    if num_selected > 0:
        idx = self.selected_edges[0]
        v = bm.edges[idx].verts
        coords = (v[0].co, v[1].co)
        draw_edge(coords, "prime")

    # draw extender edges and projections.
    if num_selected > 1:
        print('wiips')
        # get and draw selected valid edges
        coords = []
        for idx in self.selected_edges[1:]:
            v = bm.edges[idx].verts
            c = (v[0].co, v[1].co)
            coords.extend(c)

        draw_edge(coords, "extend")

        # get and draw extenders only
        list2d = [val for key, val in self.xvectors.items()]
        list2d = [[p, bm.verts[pidx].co] for (p, pidx) in list2d]
        coordinates = list(itertools.chain.from_iterable(list2d))
        draw_edge(coordinates, "projection")

    restore_bgl_defaults()


# operator
class EdgeHover(bpy.types.Operator):
    bl_idname = "view3d.edge_visualiser"
    bl_label = "_extend all"
    bl_description = "Toggle the visualisation of indices"

    # [0] will contain edge_prime
    # [1:] will contain the extender edges, (edges that really intersect)
    selected_edges = []
    xvectors = {}
    handle = None

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
            return {"CANCELLED"}

        if context.area:
            context.area.tag_redraw()

        return {"PASS_THROUGH"}

    def invoke(self, context, event):
        if context.area.type == "VIEW_3D":
            self.unselect_all(context)
            self.handle = bpy.types.SpaceView3D.draw_handler_add(
                draw_callback_px, (self, context), 'WINDOW', 'POST_PIXEL')
            context.window_manager.modal_handler_add(self)
            return {"RUNNING_MODAL"}
        else:
            self.report({"WARNING"}, "View3D not found, can't run operator")
            return {"CANCELLED"}


def register():
    bpy.utils.register_class(EdgeHover)


def unregister():
    bpy.utils.unregister_class(EdgeHover)


if __name__ == "__main__":
    register()
