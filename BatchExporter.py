import bpy
from bpy.props import (StringProperty, PointerProperty)
from bpy.types import (Panel, Operator, AddonPreferences, PropertyGroup)

bl_info = \
    {
        "name": "Quick Export",
        "author": "",
        "version": (1, 0, 0),
        "blender": (2, 7, 9),
        "location": "View 3D > Object Mode > Batch Exporter",
        "description":
            "Quick and dirty exporter",
        "warning": "",
        "wiki_url": "",
        "tracker_url": "",
        "category": "Add Mesh",
    }


class MySettings(PropertyGroup):

    path = StringProperty(
        name="",
        description="Path to Directory",
        default="",
        maxlen=1024,
        subtype='DIR_PATH')


class ToolPanel(Panel):
    bl_idname = "ToolPanel"
    bl_label = "Export Selected"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "Batch Exporter"
    bl_context = "objectmode"

    def draw(self, context):
        layout = self.layout
        scn = context.scene
        layout.prop(scn.my_tool, "path", text="")
        layout.operator("myops.batch_exporter",
                        text='Export Selected', icon='TRIA_RIGHT')

        # print the path to the console
        print(scn.my_tool.path)


class BatchExporter(bpy.types.Operator):
    bl_idname = "myops.batch_exporter"
    bl_label = "Export Selected"
    bl_options = {"UNDO"}

    def execute(self, context):
        self.report({'INFO'}, 'Printing report to Info window.')
        return {'FINISHED'}

    def invoke(self, context, event):
        exportAll(context.scene.my_tool.path + '\\')
        return {'FINISHED'}


def exportAll(exportFolder):
    objects = bpy.context.selected_objects
    for object in objects:
        bpy.ops.object.select_all(action='DESELECT')
        object.select = True
        # check to make sure only exporting meshes
        if object.type not in ['MESH']:
            continue
        exportName = exportFolder + object.name + '.fbx'
        print('Exported ' + object.name)
        bpy.ops.export_scene.fbx(filepath=exportName, use_selection=True)


def register():
    bpy.utils.register_class(ToolPanel)
    bpy.utils.register_class(BatchExporter)
    bpy.utils.register_module(__name__)
    bpy.types.Scene.my_tool = PointerProperty(type=MySettings)


def unregister():
    bpy.utils.unregister_class(ToolPanel)
    bpy.utils.unregister_class(BatchExporter)
    bpy.utils.unregister_module(__name__)
    del bpy.types.Scene.my_tool


if __name__ == "__main__":
    register()
