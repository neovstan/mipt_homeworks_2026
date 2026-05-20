from dataclasses import dataclass
from enum import StrEnum

from final_project.prompt_mentions.error import PromptFileError
from final_project.prompt_mentions.messages import PromptMessages, load_prompt_messages


class ChunkMode(StrEnum):
    PARAGRAPH = 'paragraph'
    LENGTH = 'len'


@dataclass(frozen=True)
class ChunkSettings:
    mode: ChunkMode
    size: int
    should_auto_confirm: bool = False


class ChunkCommandParser:
    def __init__(self, messages: PromptMessages | None = None) -> None:
        if messages is None:
            messages = load_prompt_messages()

        self._messages = messages

    def parse(self, command: str) -> ChunkSettings:
        tokens = command.split()

        if len(tokens) > 0:
            first_token = tokens[0]

            if self._is_option(first_token):
                message = self._messages.bad_chunk_command.format(
                    command=command,
                )
                raise PromptFileError(message)

        mode = ChunkMode.PARAGRAPH
        size = 1
        should_auto_confirm = False

        options = tokens[1:]

        for token in options:
            if token == '-y':
                should_auto_confirm = True
                continue

            name, separator, value = token.partition('=')

            if separator != '=':
                message = self._messages.bad_chunk_command.format(
                    command=command,
                )
                raise PromptFileError(message)

            if value == '':
                message = self._messages.bad_chunk_command.format(
                    command=command,
                )
                raise PromptFileError(message)

            if name == 'paragraph':
                size = self._read_size(value)
                mode = ChunkMode.PARAGRAPH
                continue

            if name == 'len':
                size = self._read_size(value)
                mode = ChunkMode.LENGTH
                continue

            message = self._messages.bad_chunk_command.format(
                command=command,
            )
            raise PromptFileError(message)

        return ChunkSettings(
            mode=mode,
            size=size,
            should_auto_confirm=should_auto_confirm,
        )

    def _is_option(self, token: str) -> bool:
        if token == '-y':
            return True

        if token.startswith('paragraph='):
            return True

        if token.startswith('len='):
            return True

        return False

    def _read_size(self, raw_size: str) -> int:
        try:
            size = int(raw_size)
        except ValueError as error:
            message = self._messages.bad_chunk_size.format(
                value=raw_size,
            )
            raise PromptFileError(message) from error

        if size <= 0:
            message = self._messages.bad_chunk_size.format(
                value=raw_size,
            )
            raise PromptFileError(message)

        return size


class ChunkSplitter:
    def split(self, text: str, settings: ChunkSettings) -> list[str]:
        if settings.mode == ChunkMode.PARAGRAPH:
            return self._split_by_paragraphs(text, settings.size)

        return self._split_by_length(text, settings.size)

    def _split_by_paragraphs(self, text: str, paragraph_count: int) -> list[str]:
        paragraphs = [paragraph for paragraph in text.split('\n\n') if paragraph.strip()]
        return [
            '\n\n'.join(paragraphs[i:i + paragraph_count])
            for i in range(0, len(paragraphs), paragraph_count)
        ]

    def _split_by_length(self, text: str, length: int) -> list[str]:
        if not text:
            return []

        return [text[i:i + length] for i in range(0, len(text), length)]


def parse_chunk_command(command: str) -> ChunkSettings:
    parser = ChunkCommandParser()
    return parser.parse(command)


def split_text(text: str, settings: ChunkSettings) -> list[str]:
    splitter = ChunkSplitter()
    return splitter.split(text, settings)
