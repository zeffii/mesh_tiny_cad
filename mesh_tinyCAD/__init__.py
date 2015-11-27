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

bl_info = {
    "name": "tinyCAD Mesh tools",
    "author": "zeffii (aka Dealga McArdle)",
    "version": (1, 2, 0),
    "blender": (2, 7, 6),
    "category": "Mesh",
    "location": "View3D > EditMode > (w) Specials",
    "wiki_url": "",
    "tracker_url": ""
}


if "bpy" in locals():
    if 'VTX' in locals():
        import imp
        print('tinyCAD: detected reload event.')
        try:
            modules = "VTX V2X XALL BIX CCEN".split()
            for m in modules:
                exec('imp.reload({0})'.format(m))
            print("tinyCAD: reloaded modules, all systems operational")

        except Exception as E:
            print('reload failed with error:')
            print(E)


import os
import bpy
from .VTX import AutoVTX
from .V2X import Vert2Intersection
from .XALL import IntersectAllEdges
from .BIX import LineOnBisection
from .CCEN import CircleCenter
from .CCEN import CircleMake


vtx_classes = [
    AutoVTX, Vert2Intersection, IntersectAllEdges, LineOnBisection, CircleCenter
]


class VIEW3D_MT_edit_mesh_tinycad(bpy.types.Menu):
    bl_label = "TinyCAD"

    @classmethod
    def poll(cls, context):
        return (context.object is not None)

    def draw(self, context):
        self.layout.operator('mesh.autovtx', text='VTX | AUTO')
        self.layout.operator('mesh.vertintersect', text='V2X | Vertex at intersection')
        self.layout.operator('mesh.intersectall', text='XALL | Intersect selected edges')
        self.layout.operator('mesh.linetobisect', text='BIX |  Bisector of 2 planar edges')
        self.layout.operator('mesh.circlecenter', text='CCEN | Resurrect circle center')


def menu_func(self, context):
    self.layout.menu("VIEW3D_MT_edit_mesh_tinycad")
    self.layout.separator()


def register():
    scn = bpy.types.Scene

    # register scene properties first.
    ugly_green = (0.2, 0.90, .2)
    scn.tc_gp_color = bpy.props.FloatVectorProperty(
        default=ugly_green,
        subtype='COLOR',
        min=0.0, max=1.0)
    scn.tc_num_verts = bpy.props.IntProperty(
        min=3, max=60, default=12)

    for i in vtx_classes:
        bpy.utils.register_class(i)

    # miscl registration not order dependant
    bpy.utils.register_class(VIEW3D_MT_edit_mesh_tinycad)
    bpy.types.VIEW3D_MT_edit_mesh_specials.prepend(menu_func)
    bpy.utils.register_class(CircleMake)


def unregister():
    scn = bpy.types.Scene

    for i in vtx_classes:
        bpy.utils.unregister_class(i)

    bpy.utils.unregister_class(CircleMake)
    bpy.utils.unregister_class(VIEW3D_MT_edit_mesh_tinycad)
    bpy.types.VIEW3D_MT_edit_mesh_specials.remove(menu_func)
    del scn.tc_num_verts
    del scn.tc_gp_color
