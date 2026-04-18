import bpy
from bpy.props import BoolProperty, StringProperty, IntProperty, PointerProperty, CollectionProperty, IntProperty
from bpy.types import PropertyGroup


class BR_PG_shot(PropertyGroup):
    enabled: BoolProperty(
        name="Enabled",
        description="Render this shot when running the batch",
        default=True,
    )
    name: StringProperty(
        name="Shot Name",
        description="Name used for the output suffix. Falls back to camera name if empty",
        default="",
    )
    camera: PointerProperty(
        name="Camera",
        description="Camera used for this shot",
        type=bpy.types.Object,
        poll=lambda self, obj: obj and obj.type == 'CAMERA',
    )
    frame_start: IntProperty(
        name="Start",
        description="First frame of the shot",
        default=1,
    )
    frame_end: IntProperty(
        name="End",
        description="Last frame of the shot",
        default=250,
    )


classes = (
    BR_PG_shot,
)


def register_properties():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.batch_renderer_shots = CollectionProperty(type=BR_PG_shot)
    bpy.types.Scene.batch_renderer_active_index = IntProperty(
        name="Active Shot",
        default=0,
        min=0,
    )



def unregister_properties():
    del bpy.types.Scene.batch_renderer_active_index
    del bpy.types.Scene.batch_renderer_shots

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
