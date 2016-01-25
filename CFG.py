import bpy


class TinyCADProperties(bpy.types.PropertyGroup):

    gp_color = bpy.props.FloatVectorProperty(
        default=(0.2, 0.90, .2),
        subtype='COLOR',
        min=0.0, max=1.0)

    num_verts = bpy.props.IntProperty(
        min=3, max=60, default=12)

    rescale = bpy.props.FloatProperty(
        default=1.0,
        precision=4,
        min=0.0001)


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


def register():
    bpy.utils.register_module(__name__)


def unregister():
    bpy.utils.unregister_module(__name__)
