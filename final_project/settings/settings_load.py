import os
from collections.abc import Mapping
from pathlib import Path

from final_project.settings.defaults import DefaultAppSettings, load_default_set
from final_project.settings.error import AppSettingsError
from final_project.settings.messages import AppSettingsMessages, load_settings_messages
from final_project.settings.model import AppSettings
from final_project.settings.validator import AppSettingsValidator
from final_project.settings.yaml_reader import SettingsFileRead


class SettingsLoad:
    def __init__(
        self,
        reader: SettingsFileRead | None = None,
        validator: AppSettingsValidator | None = None,
        defaults: DefaultAppSettings | None = None,
        messages: AppSettingsMessages | None = None,
    ) -> None:
        if messages is None:
            messages = load_settings_messages()

        if reader is None:
            reader = SettingsFileRead(messages)

        if validator is None:
            validator = AppSettingsValidator(messages)

        if defaults is None:
            defaults = load_default_set()

        self._messages = messages
        self._reader = reader
        self._validator = validator
        self._defaults = defaults

    def load_setting(
        self,
        path: Path | None = None,
        environment_variables: Mapping[str, str] | None = None,
    ) -> AppSettings:
        if path is None:
            path = Path(self._defaults.config_file)

        if environment_variables is None:
            environment_variables = os.environ

        yaml_values = self._reader.read(path)

        self._ensure_source_present(yaml_values, environment_variables)

        settings = self._build_settings(
            yaml_values,
            environment_variables,
        )

        self._validator.validate(settings)

        return settings

    def _build_settings(
        self,
        yaml_values: Mapping[str, object],
        env: Mapping[str, str],
    ) -> AppSettings:
        api_key_value = self._read_value(env, yaml_values, 'API_KEY', 'api_key', '')
        api_key = str(api_key_value).strip()

        api_host_value = self._read_value(env, yaml_values, 'API_HOST', 'api_host', '')
        api_host = str(api_host_value).strip()

        model_value = self._read_value(
            env,
            yaml_values,
            'MODEL',
            'model',
            self._defaults.model,
        )
        model = str(model_value).strip()

        limit_message_value = self._read_optional_value(
            env,
            yaml_values,
            'LIMIT_MESSAGE',
            'limit_message',
        )
        limit_message = self._parse_optional_int(
            limit_message_value,
            'limit_message',
        )

        limit_chars_value = self._read_optional_value(
            env,
            yaml_values,
            'LIMIT_CHARS',
            'limit_chars',
        )
        limit_chars = self._parse_optional_int(
            limit_chars_value,
            'limit_chars',
        )

        temperature_value = self._read_value(
            env,
            yaml_values,
            'TEMPERATURE',
            'temperature',
            self._defaults.temperature,
        )
        temperature = self._parse_float(
            temperature_value,
            'temperature',
        )

        system_prompt_value = yaml_values.get(
            'system_prompt',
            self._defaults.system_prompt,
        )
        system_prompt = str(system_prompt_value)

        stream_value = self._read_value(env, yaml_values, 'STREAM', 'stream', False)
        stream = self._parse_bool(
            stream_value,
            'stream',
        )

        return AppSettings(
            api_key=api_key,
            api_host=api_host,
            model=model,
            limit_message=limit_message,
            limit_chars=limit_chars,
            temperature=temperature,
            system_prompt=system_prompt,
            stream=stream,
        )

    def _read_value(
        self,
        env: Mapping[str, str],
        yaml_values: Mapping[str, object],
        env_key: str,
        yaml_key: str,
        default: object,
    ) -> object:
        if env_key in env:
            return env[env_key]

        return yaml_values.get(yaml_key, default)

    def _read_optional_value(
        self,
        env: Mapping[str, str],
        yaml_values: Mapping[str, object],
        env_key: str,
        yaml_key: str,
    ) -> object | None:
        if env_key in env:
            return env[env_key]

        return yaml_values.get(yaml_key)

    def _parse_optional_int(self, value: object, name: str) -> int | None:
        if value is None:
            return None

        value_as_string = str(value).strip()

        if value_as_string == '':
            return None

        try:
            parsed_value = int(value_as_string)
        except (TypeError, ValueError) as error:
            message = self._messages.should_be_integer.format(name=name)
            raise AppSettingsError(message) from error

        return parsed_value

    def _parse_float(self, value: object, name: str) -> float:
        try:
            if isinstance(value, int | float):
                parsed_value = float(value)
            else:
                parsed_value = float(str(value).strip())
        except (TypeError, ValueError) as error:
            message = self._messages.should_be_float.format(name=name)
            raise AppSettingsError(message) from error

        return parsed_value

    def _parse_bool(self, value: object, name: str) -> bool:
        if isinstance(value, bool):
            return value

        value_as_string = str(value).strip().lower()

        true_values = ('1', 'true', 'yes', 'y', 'on')
        false_values = ('0', 'false', 'no', 'n', 'off')

        if value_as_string in true_values:
            return True

        if value_as_string in false_values:
            return False

        message = self._messages.should_be_boolean.format(name=name)
        raise AppSettingsError(message)

    def _ensure_source_present(
        self,
        yaml_values: Mapping[str, object],
        environment_variables: Mapping[str, str],
    ) -> None:
        if yaml_values:
            return

        has_env_values = self._has_required_env_values(environment_variables)

        if has_env_values:
            return

        raise AppSettingsError(self._messages.no_settings_found)

    def _has_required_env_values(self, environment_variables: Mapping[str, str]) -> bool:
        for key in self._defaults.required_env_vars:
            if key in environment_variables:
                return True

        return False
