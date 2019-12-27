import bpy
from bpy.props import (StringProperty, PointerProperty)
from bpy.types import (Panel, Operator, AddonPreferences, PropertyGroup)

bl_info = \
    {
        "name": "Quick Export",
        "author": "",
        "version": (1, 0, 0),
        "blender": (2, 80, 0),
        "location": "View 3D > Object Mode > Batch Exporter",
        "description":
            "Quick and dirty exporter",
        "warning": "",
        "wiki_url": "",
        "tracker_url": "",
        "category": "Add Mesh",
    }


class MySettings(PropertyGroup):

    path : StringProperty(
        name="",
        description="Path to Directory",
        default="",
        maxlen=1024,
        subtype='DIR_PATH')


class VIEW3D_PT_PanelExportAll(bpy.types.Panel):
    bl_label = "Export Selected"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Export"
    bl_context = "objectmode"

    def draw(self, context):
        layout = self.layout
        scn = context.scene
        layout.label(text="Do not forget to UNCHECK relative pathes!")
        layout.prop(scn.my_tool, "path", text="")
        layout.operator("myops.batch_exporter",
                        text='Export Selected', icon='TRIA_RIGHT')

        # print the path to the console
        print(scn.my_tool.path)


class OBJECT_OT_BatchExport(bpy.types.Operator):
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
        object.select_set(True)
        # check to make sure only exporting meshes
        if object.type not in ['MESH']:
            continue
        exportName = exportFolder + object.name + '.fbx'
        print('Exported ' + object.name)
        bpy.ops.export_scene.fbx(filepath=exportName, use_selection=True)


classes = (
    VIEW3D_PT_PanelExportAll,
    OBJECT_OT_BatchExport,
    MySettings
)


def register():
    for c in classes:
        bpy.utils.register_class(c)
    bpy.types.Scene.my_tool = bpy.props.PointerProperty(type=MySettings)


def unregister():
    for c in reversed(classes):
        bpy.utils.unregister_class(c)
    del bpy.types.Scene.my_tool


if __name__ == "__main__":
    register()
