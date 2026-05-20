from pathlib import Path

import yaml


def load_yaml(path: Path) -> dict[str, object]:
    with path.open(encoding='utf-8') as file:
        data = yaml.safe_load(file)

    if data is None:
        return {}

    if not isinstance(data, dict):
        raise ValueError(
            f'YAML root is not mapping for file {path}, got {type(data).__name__}',
        )

    return {str(key): value for key, value in data.items()}
