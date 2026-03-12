import os
from dataclasses import dataclass
from functools import lru_cache


@dataclass(frozen=True, slots=True)
class Settings:
    app_name: str
    app_version: str
    default_model_alias: str
    max_upload_bytes: int
    custom_model_map_file: str | None


def _env_int(name: str, default: int) -> int:
    raw = os.getenv(name, "").strip()
    if not raw:
        return default
    try:
        return int(raw)
    except ValueError:
        return default


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings(
        app_name=os.getenv("NEUROROUTER_APP_NAME", "NeuroRouter Demo"),
        app_version=os.getenv("NEUROROUTER_APP_VERSION", "0.1.0"),
        default_model_alias=os.getenv("NEUROROUTER_DEFAULT_MODEL_ALIAS", "resnet18"),
        max_upload_bytes=_env_int("NEUROROUTER_MAX_UPLOAD_BYTES", 10 * 1024 * 1024),
        custom_model_map_file=os.getenv("NEUROROUTER_CUSTOM_MODEL_MAP_FILE", None),
    )

