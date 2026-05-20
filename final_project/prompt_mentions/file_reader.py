from pathlib import Path

from final_project.prompt_mentions.error import PromptFileError
from final_project.prompt_mentions.messages import PromptMessages, load_prompt_messages


class FileReader:
    def __init__(self, messages: PromptMessages | None = None) -> None:
        self._messages = messages or load_prompt_messages()

    def read(self, path: Path, maximum_size: int | None = None) -> str:
        self._validate_file(path, maximum_size)
        return self._read_text(path)

    def _validate_file(self, path: Path, maximum_size: int | None = None) -> None:
        if not path.exists():
            raise PromptFileError(self._messages.missing_file.format(path=path))

        if not path.is_file():
            raise PromptFileError(self._messages.not_a_file.format(path=path))

        if maximum_size is None:
            return

        if self._file_size(path) > maximum_size:
            raise PromptFileError(self._messages.file_is_too_big.format(path=path))

    def _file_size(self, path: Path) -> int:
        try:
            return path.stat().st_size
        except OSError as error:
            raise PromptFileError(
                self._messages.file_size_unavailable.format(path=path),
            ) from error

    def _read_text(self, path: Path) -> str:
        try:
            return path.read_text(encoding='utf-8')
        except UnicodeDecodeError as error:
            raise PromptFileError(
                self._messages.not_utf8_text.format(path=path),
            ) from error
        except OSError as error:
            raise PromptFileError(
                self._messages.file_read_failed.format(path=path),
            ) from error
