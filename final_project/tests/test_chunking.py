import pytest

from final_project.prompt_mentions.chunking import ChunkCommandParser, ChunkMode
from final_project.prompt_mentions.messages import PromptMessages


@pytest.fixture
def mock_messages() -> PromptMessages:
    return PromptMessages(
        missing_file='',
        not_a_file='',
        file_is_too_big='',
        file_size_unavailable='',
        not_utf8_text='',
        file_read_failed='',
        bad_chunk_command='Некорректная команда: {command}',
        bad_chunk_size='Размер чанка должен быть положительным: {value}',
    )


def test_parse_default_paragraph(mock_messages: PromptMessages) -> None:
    parser = ChunkCommandParser(mock_messages)
    settings = parser.parse('/filechunk')
    assert settings.mode == ChunkMode.PARAGRAPH
    assert settings.size == 1
    assert settings.should_auto_confirm is False


def test_parse_paragraph_with_size(mock_messages: PromptMessages) -> None:
    settings = ChunkCommandParser(mock_messages).parse('/filechunk paragraph=3')
    assert settings.mode == ChunkMode.PARAGRAPH
    assert settings.size == 3
    assert settings.should_auto_confirm is False


def test_parse_length_mode(mock_messages: PromptMessages) -> None:
    settings = ChunkCommandParser(mock_messages).parse('/filechunk len=1488')
    assert settings.mode == ChunkMode.LENGTH
    assert settings.size == 1488


def test_parse_with_auto_confirm_flag(mock_messages: PromptMessages) -> None:
    settings = ChunkCommandParser(mock_messages).parse('/filechunk paragraph=2 -y')
    assert settings.mode == ChunkMode.PARAGRAPH
    assert settings.size == 2
    assert settings.should_auto_confirm is True
    settings = ChunkCommandParser(mock_messages).parse('/filechunk -y len=1337')
    assert settings.mode == ChunkMode.LENGTH
    assert settings.size == 1337
    assert settings.should_auto_confirm is True


def test_parse_multiple_options(mock_messages: PromptMessages) -> None:
    settings = ChunkCommandParser(mock_messages).parse('/filechunk paragraph=1 len=2026')
    assert settings.mode == ChunkMode.LENGTH
    assert settings.size == 2026
