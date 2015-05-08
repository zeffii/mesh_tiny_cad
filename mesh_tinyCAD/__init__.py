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
    "blender": (2, 7, 4),
    "category": "Mesh",
    "location": "View3D > EditMode > (w) Specials",
    "wiki_url": "",
    "tracker_url": ""
}


if "bpy" in locals():
    import imp
    if 'VTX' in locals():
        try:
            print('tinyCAD detected reload event.')
            modules = "VTX V2X XALL BIX PERP CCEN EXM".split()
            for m in modules:
                exec('imp.reload({0})'.format(m))

            print("tinyCAD reloaded modules, all systems operational")
        except Exception as E:
            print('reload failed with error:')
            print(E)


import bpy
from .VTX import AutoVTX
from .V2X import Vert2Intersection
from .XALL import IntersectAllEdges
from .BIX import LineOnBisection
from .PERP import CutOnPerpendicular
from .CCEN import CircleCenter
from .CCEN import CircleMake
from .EXM import ExtendEdgesMulti


vtx_classes = (
    [AutoVTX, 'auto VTX'],
    [Vert2Intersection, 'V2X | Vertex at intersection'],
    [IntersectAllEdges, 'XALL | Intersect selected edges'],
    [LineOnBisection, 'BIX |  Bisector of 2 planar edges'],
    [CutOnPerpendicular, 'PERP | Cut face perpendicular'],
    [CircleCenter, 'CCEN | Resurrect circle center'],
    [ExtendEdgesMulti, 'EXM | Extend Multiple edges (experimenal)']
)


class VIEW3D_MT_edit_mesh_tinycad(bpy.types.Menu):
    bl_label = "TinyCAD"

    def draw(self, context):
        for i, text in vtx_classes:
            self.layout.operator(i.bl_idname, text=text)


def menu_func(self, context):
    self.layout.menu("VIEW3D_MT_edit_mesh_tinycad")
    self.layout.separator()


def register():
    # register scene properties first.
    ugly_green = (0.2, 0.90, .2)
    bpy.types.Scene.tc_gp_color = bpy.props.FloatVectorProperty(
        default=ugly_green,
        subtype='COLOR',
        min=0.0, max=1.0)
    bpy.types.Scene.tc_num_verts = bpy.props.IntProperty(
        min=3, max=60, default=12)

    # my classes
    for i, _ in vtx_classes:
        try:
            bpy.utils.register_class(i)
        except:
            print('failed:', i)

    # miscl registration not order dependant
    bpy.utils.register_class(VIEW3D_MT_edit_mesh_tinycad)
    bpy.types.VIEW3D_MT_edit_mesh_specials.prepend(menu_func)
    bpy.utils.register_class(CircleMake)


def unregister():
    for i, _ in vtx_classes:
        bpy.utils.unregister_class(i)

    bpy.utils.unregister_class(CircleMake)
    bpy.utils.unregister_class(VIEW3D_MT_edit_mesh_tinycad)
    bpy.types.VIEW3D_MT_edit_mesh_specials.remove(menu_func)
    del bpy.types.Scene.tc_num_verts
    del bpy.types.Scene.tc_gp_color
