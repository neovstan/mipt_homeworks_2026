from pathlib import Path

import yaml

from final_project.settings.error import AppSettingsError
from final_project.settings.messages import AppSettingsMessages, load_settings_messages


class SettingsFileRead:
    def __init__(self, messages: AppSettingsMessages | None = None) -> None:
        self._messages = messages or load_settings_messages()

    def read(self, path: Path) -> dict[str, object]:
        if not path.exists():
            return {}

        try:
            with path.open(encoding='utf-8') as file:
                loaded_data = yaml.safe_load(file)
        except OSError as error:
            raise AppSettingsError(
                self._messages.config_cannot_be_opened.format(path=path),
            ) from error
        except yaml.YAMLError as error:
            raise AppSettingsError(
                self._messages.config_is_broken_yaml.format(path=path),
            ) from error

        if loaded_data is None:
            return {}

        if not isinstance(loaded_data, dict):
            raise AppSettingsError(self._messages.config_should_be_a_map)

        return loaded_data
