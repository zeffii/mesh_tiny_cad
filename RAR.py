import bpy
import mathutils
from mathutils import Euler

import time
import math
from math import radians

def get_orthographic_view(context):
    return 'TOP'

def add_empty(loc, name):
    scene = bpy.context.scene
    objects = bpy.data.objects
    mt = objects.new(name, None)
    mt.location = loc
    mt.empty_draw_size = 2
    scene.objects.link(mt)
    scene.update()
    return mt

def main(self, context):
	
    active_object = bpy.context.active_object
    loc = active_object.location
    mts = [o for o in bpy.data.objects if o.type == 'EMPTY' and o['UID'] == self.UID]
    if mts:
        mt = mts[-1] 
    else:
        mt = add_empty(loc, name="empty_name")
        mt['UID'] = self.UID

    modifiers = active_object.modifiers
    array = modifiers.get('radial_array')
    if not array:
        array = modifiers.new(name='radial_array', type='ARRAY')
    array.use_relative_offset = False
    array.use_object_offset = True
    array.offset_object = mt

    # depending on view, must be ortographic.
    view_kind = get_orthographic_view(context)
    if self.count == 0:
        rotation = 0
        array.count = 1
    else:
        array.count = abs(self.count)
        rotation = radians(360 / self.count)

    comp = 'XYZ'.index(self.orientation)
    vec = [0, 0, 0]
    vec[comp] = rotation
    mt.rotation_euler = Euler(vec, 'XYZ')




class TCRadialArray(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "tinycad.radial_array"
    bl_label = "Radial Array"
    bl_options = {'REGISTER', 'UNDO'}
    
    count = bpy.props.IntProperty(min=0, default=3)
    orientation = bpy.props.EnumProperty(
        default='X',
        items=[('X','X', '', 0), ('Y','Y', '', 1), ('Z','Z', '', 2)]
    )


    @classmethod
    def poll(cls, context):
        return bool(context.active_object)

    def execute(self, context):
        main(self, context)
		return {'FINISHED'}
	
	def invoke(self, context, event):
	    self.UID = str(hash(self) ^ hash(time.monotonic()))
        return self.execute(context)
		

def register():
    bpy.utils.register_module(__name__)


def unregister():
    bpy.utils.unregister_module(__name__)
