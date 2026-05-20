from pathlib import Path

from final_project.prompt_mentions.chunking import (
    ChunkCommandParser,
    ChunkMode,
    ChunkSettings,
    ChunkSplitter,
    parse_chunk_command,
    split_text,
)
from final_project.prompt_mentions.error import PromptFileError
from final_project.prompt_mentions.file_mention_expand import FileMentionExpander
from final_project.prompt_mentions.file_reader import FileReader


__all__ = [
    'ChunkCommandParser',
    'ChunkMode',
    'ChunkSettings',
    'ChunkSplitter',
    'FileMentionExpander',
    'FileReader',
    'PromptFileError',
    'expand_file_mentions',
    'parse_chunk_command',
    'read_text_file',
    'split_text',
]


def read_text_file(path: Path, maximum_size: int | None = None) -> str:
    return FileReader().read(path, maximum_size)


def expand_file_mentions(text: str) -> str:
    return FileMentionExpander().expand(text)
