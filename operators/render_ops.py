import bpy
from bpy.types import Operator
from ..utils.naming import resolve_shot_name, build_output_path


class _BaseRenderOp:
    def _validate_shot(self, shot, index):
        if shot is None:
            return False, "No shot selected"
        if shot.camera is None or shot.camera.type != 'CAMERA':
            return False, f"Shot {index + 1}: missing camera"
        if shot.frame_start > shot.frame_end:
            return False, f"Shot {index + 1}: start frame is greater than end frame"
        return True, ""

    def _render_shot(self, context, shot, index):
        scene = context.scene
        valid, message = self._validate_shot(shot, index)
        if not valid:
            self.report({'WARNING'}, message)
            return False

        original_camera = scene.camera
        original_start = scene.frame_start
        original_end = scene.frame_end
        original_filepath = scene.render.filepath

        shot_name = resolve_shot_name(shot, index)

        try:
            scene.camera = shot.camera
            scene.frame_start = shot.frame_start
            scene.frame_end = shot.frame_end
            scene.render.filepath = build_output_path(original_filepath, shot_name)
            bpy.ops.render.render('EXEC_DEFAULT', animation=True)
        finally:
            scene.camera = original_camera
            scene.frame_start = original_start
            scene.frame_end = original_end
            scene.render.filepath = original_filepath
        return True


class BR_OT_render_all(Operator, _BaseRenderOp):
    bl_idname = "batch_renderer.render_all"
    bl_label = "Render Enabled Shots"
    bl_description = "Render all enabled shots in list order using Blender's current output settings"

    def execute(self, context):
        scene = context.scene
        any_rendered = False
        for i, shot in enumerate(scene.batch_renderer_shots):
            if not shot.enabled:
                continue
            if self._render_shot(context, shot, i):
                any_rendered = True
        if not any_rendered:
            self.report({'WARNING'}, "No enabled valid shots to render")
            return {'CANCELLED'}
        return {'FINISHED'}


classes = (
    BR_OT_render_all,
)


def register_render_ops():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister_render_ops():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
