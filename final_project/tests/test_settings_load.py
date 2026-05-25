from unittest.mock import Mock

import pytest

from final_project.settings import AppSettingsError, SettingsLoad
from final_project.settings.defaults import DefaultAppSettings


@pytest.fixture
def mock_defaults() -> Mock:
    defaults = Mock()
    defaults.model = 'gemma'
    defaults.system_prompt = 'prompt'
    defaults.temperature = 0.3
    defaults.config_file = 'config.yaml'
    defaults.required_env_vars = ('API_KEY', 'API_HOST')
    return defaults


def test_env_overrides_yaml(mock_defaults: DefaultAppSettings) -> None:
    loader = SettingsLoad(defaults=mock_defaults)
    yaml_values = {'api_key': 'from_yaml', 'api_host': 'host_yaml', 'model': 'yolo'}
    env = {'API_KEY': 'from_env', 'LIMIT_MESSAGE': '42'}

    settings = loader._build_settings(yaml_values, env)

    assert settings.api_key == 'from_env'
    assert settings.api_host == 'host_yaml'
    assert settings.model == 'yolo'
    assert settings.limit_message == 42


def test_required_env_any_one_is_enough(mock_defaults: DefaultAppSettings) -> None:
    loader = SettingsLoad(defaults=mock_defaults)

    env = {'API_HOST': 'anton zuev'}
    assert loader._has_required_env_values(env) is True

    env = {'API_KEY': 'vasily ilichev'}
    assert loader._has_required_env_values(env) is True

    env = {'SOMETHING': '403 kitchen'}
    assert loader._has_required_env_values(env) is False


def test_missing_both_source_raises(mock_defaults: DefaultAppSettings) -> None:
    loader = SettingsLoad(defaults=mock_defaults)
    with pytest.raises(AppSettingsError, match='Конфигурация отсутствует'):
        loader._ensure_source_present({}, {})


def test_parse_bool_variants(mock_defaults: DefaultAppSettings) -> None:
    loader = SettingsLoad(defaults=mock_defaults)
    assert loader._parse_bool('yes', 'stream') is True
    assert loader._parse_bool('1', 'stream') is True
    assert loader._parse_bool('off', 'stream') is False
    assert loader._parse_bool('false', 'stream') is False
    with pytest.raises(AppSettingsError):
        loader._parse_bool('maybe', 'stream')
