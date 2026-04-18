import bpy
from bpy.types import Panel


class BR_PT_main(Panel):
    bl_label = "Multi-Cam Batch Renderer"
    bl_idname = "BR_PT_main"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Multi-Cam Batch Renderer'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        shots = scene.batch_renderer_shots
        idx = scene.batch_renderer_active_index

        box = layout.box()
        box.label(text="Shot List")

        row = box.row()
        row.template_list(
            "BR_UL_shots",
            "",
            scene,
            "batch_renderer_shots",
            scene,
            "batch_renderer_active_index",
            rows=7,
        )

        col = row.column(align=True)
        col.operator("batch_renderer.add_shot", text="", icon='ADD')
        col.operator("batch_renderer.remove_shot", text="", icon='REMOVE')
        col.separator()
        col.operator("batch_renderer.duplicate_shot", text="", icon='DUPLICATE')
        col.separator()
        up = col.operator("batch_renderer.move_shot", text="", icon='TRIA_UP')
        up.direction = 'UP'
        down = col.operator("batch_renderer.move_shot", text="", icon='TRIA_DOWN')
        down.direction = 'DOWN'

        if 0 <= idx < len(shots):
            shot = shots[idx]
            box = layout.box()
            box.label(text="Selected Shot")
            box.prop(shot, "enabled")
            box.prop(shot, "name")
            box.prop(shot, "camera")
            row = box.row(align=True)
            row.prop(shot, "frame_start")
            row.prop(shot, "frame_end")

        box = layout.box()
        box.label(text="Render")
        box.label(text="Uses Blender's existing output settings", icon='INFO')
        box.label(text="Blender might freeze momentarily while rendering", icon='INFO')
        box.operator("batch_renderer.render_all", text="Render Enabled Shots", icon='RENDER_ANIMATION')


classes = (BR_PT_main,)


def register_panel():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister_panel():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
