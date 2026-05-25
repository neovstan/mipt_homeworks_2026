from unittest.mock import Mock

import pytest

from final_project.chat.history import ChatHistory
from final_project.chat.message import ChatRole
from final_project.chat.messages import ChatMessages


@pytest.fixture
def mock_chat_messages() -> Mock:
    messages = Mock(spec=ChatMessages)
    messages.message_limit_error = 'limit_message должен быть неотрицательным'
    messages.character_limit_error = 'limit_chars должен быть неотрицательным'
    return messages


def test_add_user_and_assistant(mock_chat_messages: ChatMessages) -> None:
    history = ChatHistory(messages=mock_chat_messages)
    history.add_user_message('Здарова')
    history.add_assistant_message('Нет')
    assert len(history) == 2
    assert history.total_chars == len('Здарова') + len('Нет')
    assert history.messages[0].role == ChatRole.USER
    assert history.messages[1].role == ChatRole.ASSISTANT


def test_limit_by_message_count(mock_chat_messages: ChatMessages) -> None:
    history = ChatHistory(limit_message=2, messages=mock_chat_messages)
    history.add_user_message('1')
    history.add_assistant_message('2')
    history.add_user_message('3')
    assert len(history) == 2
    assert history.messages[0].content == '2'
    assert history.messages[1].content == '3'
    assert history.total_chars == len('2') + len('3')


def test_limit_by_total_chars(mock_chat_messages: ChatMessages) -> None:
    history = ChatHistory(limit_chars=10, messages=mock_chat_messages)
    history.add_user_message('12345')
    history.add_assistant_message('67890')
    assert len(history) == 2
    history.add_user_message('abc')
    assert len(history) == 2
    assert history.messages[0].content == '67890'
    assert history.messages[1].content == 'abc'
    assert history.total_chars == 8


def test_trim_new_message_content(mock_chat_messages: ChatMessages) -> None:
    history = ChatHistory(limit_chars=5, messages=mock_chat_messages)
    history.add_user_message('1234567890')
    assert history.messages[0].content == '67890'
    assert history.total_chars == 5


def test_zero_limit_chars(mock_chat_messages: ChatMessages) -> None:
    history = ChatHistory(limit_chars=0, messages=mock_chat_messages)
    history.add_user_message('hello')
    assert history.messages[0].content == ''
    assert history.total_chars == 0


def test_mixed_limits_both_active(mock_chat_messages: ChatMessages) -> None:
    history = ChatHistory(limit_message=3, limit_chars=20, messages=mock_chat_messages)
    history.add_user_message('a')
    history.add_assistant_message('bb')
    history.add_user_message('ccc')
    assert len(history) == 3
    assert history.total_chars == 6
    history.add_user_message('dddd')
    assert len(history) == 3
    assert history.messages[0].content == 'bb'
    assert history.total_chars == 9


def test_clear(mock_chat_messages: ChatMessages) -> None:
    history = ChatHistory(messages=mock_chat_messages)
    history.add_user_message('test')
    history.clear()
    assert len(history) == 0
    assert history.total_chars == 0


def test_validation_negative_message_limit(mock_chat_messages: ChatMessages) -> None:
    with pytest.raises(ValueError, match='limit_message должен быть неотрицательным'):
        ChatHistory(limit_message=-1, messages=mock_chat_messages)


def test_validation_negative_chars_limit(mock_chat_messages: ChatMessages) -> None:
    with pytest.raises(ValueError, match='limit_chars должен быть неотрицательным'):
        ChatHistory(limit_chars=-5, messages=mock_chat_messages)


def test_iteration(mock_chat_messages: ChatMessages) -> None:
    history = ChatHistory(messages=mock_chat_messages)
    history.add_user_message('A')
    history.add_assistant_message('B')
    contents = [msg.content for msg in history]
    assert contents == ['A', 'B']
