import bpy
from bpy.types import UIList


class BR_UL_shots(UIList):
    """Scrollable shot list for Batch Renderer"""

    bl_idname = "BR_UL_shots"

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        shot = item
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            row = layout.row(align=True)
            row.prop(shot, "enabled", text="")
            row.prop(shot, "name", text="", emboss=False, icon='RENDER_STILL')
            row.prop(shot, "camera", text="")
            row.prop(shot, "frame_start", text="S")
            row.prop(shot, "frame_end", text="E")
        elif self.layout_type == 'GRID':
            layout.alignment = 'CENTER'
            layout.label(text="", icon='RENDER_STILL')


classes = (BR_UL_shots,)


def register_uilist():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister_uilist():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
