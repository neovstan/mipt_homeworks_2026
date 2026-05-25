from dataclasses import dataclass
from pathlib import Path

from final_project.yaml_loader import load_yaml


@dataclass(frozen=True)
class DefaultAppSettings:
    model: str
    system_prompt: str
    temperature: float
    config_file: str
    required_env_vars: tuple[str, ...]


def load_default_set(path: Path | None = None) -> DefaultAppSettings:
    if path is None:
        current_file = Path(__file__)
        resources_dir = current_file.with_name('resources')
        path = resources_dir / 'defaults.yaml'

    values = load_yaml(path)

    return DefaultAppSettings(
        model=str(values['model']),
        system_prompt=str(values['system prompt']),
        temperature=_parse_float(values['temperature']),
        config_file=str(values['config file']),
        required_env_vars=_read_string_tuple(values['required env vars']),
    )


def _parse_float(value: object) -> float:
    if isinstance(value, int | float):
        return float(value)

    return float(str(value).strip())


def _read_string_tuple(value: object) -> tuple[str, ...]:
    if not isinstance(value, list | tuple):
        raise ValueError('required env vars is not list')

    return tuple(str(item) for item in value)
