from dataclasses import dataclass
from enum import StrEnum


class ChatRole(StrEnum):
    USER = 'user'
    ASSISTANT = 'assistant'
    SYSTEM = 'system'


@dataclass
class ChatMessage:
    role: ChatRole
    content: str

    def to_api_dict(self) -> dict[str, str]:
        return {
            'role': self.role.value,
            'content': self.content,
        }
