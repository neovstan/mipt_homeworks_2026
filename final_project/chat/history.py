from collections import deque
from collections.abc import Iterator

from final_project.chat.message import ChatMessage, ChatRole
from final_project.chat.messages import ChatMessages, load_chat_messages


class ChatHistory:
    def __init__(
        self,
        limit_message: int | None = None,
        limit_chars: int | None = None,
        messages: ChatMessages | None = None,
    ) -> None:
        self._localized_messages = messages or load_chat_messages()
        self._validate_limits(limit_message, limit_chars)
        self._limit_message = limit_message
        self._limit_chars = limit_chars
        self._history: deque[ChatMessage] = deque()
        self._total_chars = 0

    def add_user_message(self, content: str) -> None:
        self._add_message(ChatRole.USER, content)

    def add_assistant_message(self, content: str) -> None:
        self._add_message(ChatRole.ASSISTANT, content)

    def clear(self) -> None:
        self._history.clear()
        self._total_chars = 0

    def __len__(self) -> int:
        return len(self._history)

    def __iter__(self) -> Iterator[ChatMessage]:
        return iter(self._history)

    @property
    def messages(self) -> tuple[ChatMessage, ...]:
        return tuple(self._history)

    @property
    def total_chars(self) -> int:
        return self._total_chars

    def _add_message(self, role: ChatRole, content: str) -> None:
        content = self._trim_message_content_if_needed(content)
        message = ChatMessage(role, content)
        self._history.append(message)
        self._total_chars += len(content)
        self._trim_history_if_needed()

    def _trim_message_content_if_needed(self, content: str) -> str:
        if self._limit_chars is None:
            return content

        if len(content) <= self._limit_chars:
            return content

        if self._limit_chars == 0:
            return ''

        return content[-self._limit_chars:]

    def _trim_history_if_needed(self) -> None:
        while self._is_over_limit():
            self._discard_oldest_message()

    def _discard_oldest_message(self) -> None:
        oldest_message = self._history.popleft()
        self._total_chars -= len(oldest_message.content)

    def _is_over_limit(self) -> bool:
        too_many_messages = (
            self._limit_message is not None
            and len(self._history) > self._limit_message
        )
        if too_many_messages:
            return True

        return self._limit_chars is not None and self._total_chars > self._limit_chars

    def _validate_limits(
        self,
        limit_message: int | None,
        limit_chars: int | None,
    ) -> None:
        if limit_message is not None and limit_message < 0:
            raise ValueError(self._localized_messages.message_limit_error)
        if limit_chars is not None and limit_chars < 0:
            raise ValueError(self._localized_messages.character_limit_error)
