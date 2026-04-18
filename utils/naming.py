import re


_INVALID = re.compile(r'[\\/:*?"<>|]+')


def sanitize_name(name: str) -> str:
    cleaned = _INVALID.sub("_", (name or "").strip())
    cleaned = cleaned.replace(" ", "_")
    while "__" in cleaned:
        cleaned = cleaned.replace("__", "_")
    return cleaned.strip("._")


def resolve_shot_name(shot, index: int) -> str:
    if shot.name.strip():
        base = shot.name.strip()
    elif shot.camera:
        base = shot.camera.name
    else:
        base = f"Shot_{index + 1:03d}"
    return sanitize_name(base) or f"Shot_{index + 1:03d}"


def build_output_path(base_path: str, shot_name: str) -> str:
    return f"{base_path}{shot_name}"
