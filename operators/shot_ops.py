import bpy
from bpy.types import Operator


def _active_scene(context):
    return context.scene


class BR_OT_add_shot(Operator):
    bl_idname = "batch_renderer.add_shot"
    bl_label = "Add Shot"
    bl_description = "Add a new shot entry"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = _active_scene(context)
        shot = scene.batch_renderer_shots.add()
        shot.frame_start = scene.frame_start
        shot.frame_end = scene.frame_end
        if scene.camera and scene.camera.type == 'CAMERA':
            shot.camera = scene.camera
            shot.name = scene.camera.name
        scene.batch_renderer_active_index = len(scene.batch_renderer_shots) - 1
        return {'FINISHED'}


class BR_OT_remove_shot(Operator):
    bl_idname = "batch_renderer.remove_shot"
    bl_label = "Remove Shot"
    bl_description = "Remove the selected shot"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = _active_scene(context)
        idx = scene.batch_renderer_active_index
        if 0 <= idx < len(scene.batch_renderer_shots):
            scene.batch_renderer_shots.remove(idx)
            if scene.batch_renderer_shots:
                scene.batch_renderer_active_index = min(idx, len(scene.batch_renderer_shots) - 1)
            else:
                scene.batch_renderer_active_index = 0
            return {'FINISHED'}
        self.report({'WARNING'}, "No shot selected")
        return {'CANCELLED'}


class BR_OT_duplicate_shot(Operator):
    bl_idname = "batch_renderer.duplicate_shot"
    bl_label = "Duplicate Shot"
    bl_description = "Duplicate the selected shot"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = _active_scene(context)
        idx = scene.batch_renderer_active_index
        if not (0 <= idx < len(scene.batch_renderer_shots)):
            self.report({'WARNING'}, "No shot selected")
            return {'CANCELLED'}

        src = scene.batch_renderer_shots[idx]
        dst = scene.batch_renderer_shots.add()
        dst.enabled = src.enabled
        dst.name = src.name + "_copy" if src.name else "Shot_copy"
        dst.camera = src.camera
        dst.frame_start = src.frame_start
        dst.frame_end = src.frame_end
        new_idx = len(scene.batch_renderer_shots) - 1
        scene.batch_renderer_shots.move(new_idx, idx + 1)
        scene.batch_renderer_active_index = idx + 1
        return {'FINISHED'}


class BR_OT_move_shot(Operator):
    bl_idname = "batch_renderer.move_shot"
    bl_label = "Move Shot"
    bl_description = "Move the selected shot up or down"
    bl_options = {'REGISTER', 'UNDO'}

    direction: bpy.props.EnumProperty(
        items=[('UP', 'Up', 'Move the shot up'), ('DOWN', 'Down', 'Move the shot down')],
        name="Direction",
    )

    def execute(self, context):
        scene = _active_scene(context)
        idx = scene.batch_renderer_active_index
        count = len(scene.batch_renderer_shots)
        if not (0 <= idx < count):
            self.report({'WARNING'}, "No shot selected")
            return {'CANCELLED'}

        if self.direction == 'UP' and idx > 0:
            scene.batch_renderer_shots.move(idx, idx - 1)
            scene.batch_renderer_active_index = idx - 1
        elif self.direction == 'DOWN' and idx < count - 1:
            scene.batch_renderer_shots.move(idx, idx + 1)
            scene.batch_renderer_active_index = idx + 1
        else:
            return {'CANCELLED'}
        return {'FINISHED'}


classes = (
    BR_OT_add_shot,
    BR_OT_remove_shot,
    BR_OT_duplicate_shot,
    BR_OT_move_shot,
)


def register_shot_ops():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister_shot_ops():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
