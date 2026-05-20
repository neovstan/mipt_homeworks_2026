from final_project.settings.error import AppSettingsError
from final_project.settings.messages import AppSettingsMessages, load_settings_messages
from final_project.settings.model import AppSettings


class AppSettingsValidator:
    def __init__(self, messages: AppSettingsMessages | None = None) -> None:
        self._messages = messages or load_settings_messages()

    def validate(self, settings: AppSettings) -> None:
        self._validate_required_text(settings.api_key, self._messages.api_key_is_missing)
        self._validate_required_text(settings.api_host, self._messages.api_host_is_missing)
        self._validate_positive_limit(settings.limit_message, 'limit_message')
        self._validate_positive_limit(settings.limit_chars, 'limit_chars')
        self._validate_temperature(settings.temperature)

    def _validate_required_text(self, value: str, error_message: str) -> None:
        if not value:
            raise AppSettingsError(error_message)

    def _validate_positive_limit(self, value: int | None, name: str) -> None:
        if value is not None and value <= 0:
            message = self._messages.limit_should_be_positive.format(name=name)
            raise AppSettingsError(message)

    def _validate_temperature(self, temperature: float) -> None:
        if not 0 <= temperature <= 1:
            raise AppSettingsError(self._messages.temperature_out_of_range)
