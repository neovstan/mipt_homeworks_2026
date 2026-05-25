from dataclasses import dataclass
from pathlib import Path

from final_project.yaml_loader import load_yaml


@dataclass(frozen=True)
class PromptMessages:
    missing_file: str
    not_a_file: str
    file_is_too_big: str
    file_size_unavailable: str
    not_utf8_text: str
    file_read_failed: str
    bad_chunk_command: str
    bad_chunk_size: str


def load_prompt_messages(path: Path | None = None) -> PromptMessages:
    path = path or Path(__file__).with_name('resources').joinpath('messages.yaml')
    values = load_yaml(path)
    return PromptMessages(
        missing_file=str(values['missing file']),
        not_a_file=str(values['not a file']),
        file_is_too_big=str(values['file is too big']),
        file_size_unavailable=str(values['file size unavailable']),
        not_utf8_text=str(values['not utf8 text']),
        file_read_failed=str(values['file read failed']),
        bad_chunk_command=str(values['bad chunk command']),
        bad_chunk_size=str(values['bad chunk size']),
    )
