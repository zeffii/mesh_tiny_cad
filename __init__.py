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

# 2023

bl_info = {
    "name": "tinyCAD Mesh tools",
    "author": "zeffii (aka Dealga McArdle)",
    "version": (1, 3, 3),
    "blender": (2, 80, 0),
    "category": "Mesh",
    "location": "View3D > EditMode Context Menu",
    "wiki_url": "http://zeffii.github.io/mesh_tiny_cad/",
    "tracker_url": "https://github.com/zeffii/mesh_tiny_cad/issues"
}


if "bpy" in locals():
    if 'VTX' in locals():

        print('tinyCAD: detected reload event.')
        import importlib

        try:
            modules = (CFG, VTX, V2X, XALL, BIX, CCEN, E2F)
            for m in modules:
                importlib.reload(m)
            print("tinyCAD: reloaded modules, all systems operational")

        except Exception as E:
            print('reload failed with error:')
            print(E)


import bpy

from .CFG import TinyCADProperties, VIEW3D_MT_edit_mesh_tinycad
from .CFG import register_icons, unregister_icons
from . import VTX, V2X, XALL, BIX, CCEN, E2F


def menu_func(self, context):
    self.layout.menu("VIEW3D_MT_edit_mesh_tinycad")
    self.layout.separator()

classes = [
    TinyCADProperties, VIEW3D_MT_edit_mesh_tinycad,
    VTX.TCAutoVTX,
    XALL.TCIntersectAllEdges,
    V2X.TCVert2Intersection,
    E2F.TCEdgeToFace,
    CCEN.TCCallBackCCEN, CCEN.TCCircleCenter,
    BIX.TCLineOnBisection
]

def register():
    register_icons()
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.tinycad_props = bpy.props.PointerProperty(
        name="TinyCAD props", type=TinyCADProperties)
    bpy.types.VIEW3D_MT_edit_mesh_context_menu.prepend(menu_func)


def unregister():
    bpy.types.VIEW3D_MT_edit_mesh_context_menu.remove(menu_func)
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.tinycad_props
    unregister_icons()
