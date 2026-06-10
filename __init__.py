bl_info = {
    "name": "Multi-Cam Batch Renderer",
    "author": "Dk",
    "version": (0, 1, 0),
    "blender": (5, 0, 0),
    "location": "View3D > Sidebar > Multi-Cam Batch Renderer",
    "description": "Queue and render multiple camera frame-range shots from one scene",
    "category": "Render",
}

from .properties.shot_props import register_properties, unregister_properties
from .ui.uilist import register_uilist, unregister_uilist
from .ui.panel import register_panel, unregister_panel
from .operators.shot_ops import register_shot_ops, unregister_shot_ops
from .operators.render_ops import register_render_ops, unregister_render_ops


def register():
    register_properties()
    register_uilist()
    register_shot_ops()
    register_render_ops()
    register_panel()


def unregister():
    unregister_panel()
    unregister_render_ops()
    unregister_shot_ops()
    unregister_uilist()
    unregister_properties()
