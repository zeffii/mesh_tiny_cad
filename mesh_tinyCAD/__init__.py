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
            modules = "VTX V2X XALL BIX CCEN E2F".split()
            for m in modules:
                exec('imp.reload({0})'.format(m))
            print("tinyCAD: reloaded modules, all systems operational")

        except Exception as E:
            print('reload failed with error:')
            print(E)


import os
import bpy
from .VTX import TCAutoVTX
from .V2X import TCVert2Intersection
from .XALL import TCIntersectAllEdges
from .BIX import TCLineOnBisection
from .CCEN import TCCircleCenter
from .CCEN import TCCircleMake
from .E2F import TCEdgeToFace


vtx_classes = [
    TCAutoVTX,
    TCVert2Intersection,
    TCIntersectAllEdges,
    TCLineOnBisection,
    TCCircleCenter,
    TCEdgeToFace
]


class TinyCADProperties(bpy.types.PropertyGroup):

    gp_color = bpy.props.FloatVectorProperty(
        default=(0.2, 0.90, .2),
        subtype='COLOR',
        min=0.0, max=1.0)

    num_verts = bpy.props.IntProperty(
        min=3, max=60, default=12)


class VIEW3D_MT_edit_mesh_tinycad(bpy.types.Menu):
    bl_label = "TinyCAD"

    @classmethod
    def poll(cls, context):
        return bool(context.object)

    def draw(self, context):
        operator = self.layout.operator
        operator('tinycad.autovtx', text='VTX | AUTO')
        operator('tinycad.vertintersect', text='V2X | Vertex at intersection')
        operator('tinycad.intersectall', text='XALL | Intersect selected edges')
        operator('tinycad.linetobisect', text='BIX |  Bisector of 2 planar edges')
        operator('tinycad.circlecenter', text='CCEN | Resurrect circle center')
        operator('tinycad.edge_to_face', text='E2F | Extend Edge to Face')


def menu_func(self, context):
    self.layout.menu("VIEW3D_MT_edit_mesh_tinycad")
    self.layout.separator()


def register():

    bpy.utils.register_class(TinyCADProperties)
    bpy.types.Scene.tinycad_props = bpy.props.PointerProperty(name="TinyCAD props", type=TinyCADProperties)

    for i in vtx_classes:
        bpy.utils.register_class(i)

    # miscl registration not order dependant
    bpy.utils.register_class(VIEW3D_MT_edit_mesh_tinycad)
    bpy.types.VIEW3D_MT_edit_mesh_specials.prepend(menu_func)
    bpy.utils.register_class(TCCircleMake)


def unregister():

    bpy.utils.unregister_class(TinyCADProperties)
    del bpy.types.Scene.tinycad_props

    for i in vtx_classes:
        bpy.utils.unregister_class(i)

    bpy.utils.unregister_class(TCCircleMake)
    bpy.utils.unregister_class(VIEW3D_MT_edit_mesh_tinycad)
    bpy.types.VIEW3D_MT_edit_mesh_specials.remove(menu_func)
