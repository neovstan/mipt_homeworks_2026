from dataclasses import dataclass
from pathlib import Path

from final_project.yaml_loader import load_yaml


@dataclass(frozen=True)
class ChatMessages:
    llm_empty_answer: str
    message_limit_error: str
    character_limit_error: str


def load_chat_messages(path: Path | None = None) -> ChatMessages:
    if path is None:
        current_file = Path(__file__)
        resources_dir = current_file.with_name('resources')
        path = resources_dir / 'messages.yaml'

    values = load_yaml(path)

    return ChatMessages(
        llm_empty_answer=str(values['llm empty answer']),
        message_limit_error=str(values['message limit error']),
        character_limit_error=str(values['character limit error']),
    )
