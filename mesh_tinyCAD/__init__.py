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
    if 'VTX' in locals():
        import imp
        print('tinyCAD: detected reload event.')
        try:
            modules = "VTX V2X XALL BIX PERP CCEN EXM".split()
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
from .PERP import CutOnPerpendicular
from .CCEN import CircleCenter
from .CCEN import CircleMake
from .EXM import ExtendEdgesMulti

Scene = bpy.types.Scene

vtx_classes = (
    # class, shortname ui, icon
    [AutoVTX, 'auto VTX', 'VTX.png'],
    [Vert2Intersection, 'V2X | Vertex at intersection', 'V2X.png'],
    [IntersectAllEdges, 'XALL | Intersect selected edges', 'XALL.png'],
    [LineOnBisection, 'BIX |  Bisector of 2 planar edges', 'BIX.png'],
    [CutOnPerpendicular, 'PERP | Cut face perpendicular', 'PERP.png'],
    [CircleCenter, 'CCEN | Resurrect circle center', 'CCEN.png'],
    [ExtendEdgesMulti, 'EXM | Extend Multiple edges (experimenal)', 'EXM.png']
)

preview_collections = {}


class VIEW3D_MT_edit_mesh_tinycad(bpy.types.Menu):
    bl_label = "TinyCAD"

    @classmethod
    def poll(cls, context):
        return (context.object is not None)

    def draw(self, context):
        try:
            pcoll = preview_collections["main"]
            for i, text, ico_info in vtx_classes:
                icon_name = ico_info[:-4]
                my_icon = pcoll[icon_name]
                self.layout.operator(i.bl_idname, icon_value=my_icon.icon_id, text=text)
        except:
            print('blender not ready.. try again')


def menu_func(self, context):
    self.layout.menu("VIEW3D_MT_edit_mesh_tinycad")
    self.layout.separator()


def register():
    # icons!
    import bpy.utils.previews
    pcoll = bpy.utils.previews.new()
    my_icons_dir = os.path.join(os.path.dirname(__file__), "icons")

    for classinfo in vtx_classes:
        icon_file = classinfo[2]
        icon_name = icon_file[:-4]
        pcoll.load(icon_name, os.path.join(my_icons_dir, icon_file), 'IMAGE')

    preview_collections["main"] = pcoll

    # register scene properties first.
    ugly_green = (0.2, 0.90, .2)
    Scene.tc_gp_color = bpy.props.FloatVectorProperty(
        default=ugly_green,
        subtype='COLOR',
        min=0.0, max=1.0)
    Scene.tc_num_verts = bpy.props.IntProperty(
        min=3, max=60, default=12)

    # my classes
    for i, _, _ in vtx_classes:
        bpy.utils.register_class(i)

    # miscl registration not order dependant
    bpy.utils.register_class(VIEW3D_MT_edit_mesh_tinycad)
    bpy.types.VIEW3D_MT_edit_mesh_specials.prepend(menu_func)
    bpy.utils.register_class(CircleMake)


def unregister():
    for i, _, _ in vtx_classes:
        bpy.utils.unregister_class(i)

    bpy.utils.unregister_class(CircleMake)
    bpy.utils.unregister_class(VIEW3D_MT_edit_mesh_tinycad)
    bpy.types.VIEW3D_MT_edit_mesh_specials.remove(menu_func)
    del Scene.tc_num_verts
    del Scene.tc_gp_color

    for pcoll in preview_collections.values():
        bpy.utils.previews.remove(pcoll)
    preview_collections.clear()
