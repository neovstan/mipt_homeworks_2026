from dataclasses import dataclass
from pathlib import Path

from final_project.yaml_loader import load_yaml


@dataclass(frozen=True)
class AppSettingsMessages:
    no_settings_found: str
    config_cannot_be_opened: str
    config_is_broken_yaml: str
    config_should_be_a_map: str
    should_be_integer: str
    should_be_float: str
    should_be_boolean: str
    api_key_is_missing: str
    api_host_is_missing: str
    limit_should_be_positive: str
    temperature_out_of_range: str


def load_settings_messages(path: Path | None = None) -> AppSettingsMessages:
    if path is None:
        current_file = Path(__file__)
        resources_dir = current_file.with_name('resources')
        path = resources_dir / 'messages.yaml'

    values = load_yaml(path)

    return AppSettingsMessages(
        no_settings_found=str(values['no settings found']),
        config_cannot_be_opened=str(values['config cannot be opened']),
        config_is_broken_yaml=str(values['config is broken yaml']),
        config_should_be_a_map=str(values['config should be a map']),
        should_be_integer=str(values['should be integer']),
        should_be_float=str(values['should be float']),
        should_be_boolean=str(values['should be boolean']),
        api_key_is_missing=str(values['api key is missing']),
        api_host_is_missing=str(values['api host is missing']),
        limit_should_be_positive=str(values['limit should be positive']),
        temperature_out_of_range=str(values['temperature out of range']),
    )
