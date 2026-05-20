from pathlib import Path
from collections.abc import Mapping

from final_project.settings.error import AppSettingsError
from final_project.settings.defaults import (
    DefaultAppSettings,
    load_default_set,
)
from final_project.settings.settings_load import SettingsLoad
from final_project.settings.messages import (
    AppSettingsMessages,
    load_settings_messages,
)
from final_project.settings.model import AppSettings


__all__ = [
    'AppSettings',
    'SettingsLoad',
    'AppSettingsError',
    'AppSettingsMessages',
    'DefaultAppSettings',
    'load_default_set',
    'load_settings_messages',
    'load_app_settings',
]


def load_app_settings(
    path: Path | None = None,
    environment_variables: Mapping[str, str] | None = None,
) -> AppSettings:
    return SettingsLoad().load_setting(
        path=path,
        environment_variables=environment_variables,
    )
