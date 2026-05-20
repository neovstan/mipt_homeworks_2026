from dataclasses import dataclass
from pathlib import Path

from final_project.prompt_mentions.syntax import MentionSyntax
from final_project.yaml_loader import load_yaml


@dataclass(frozen=True)
class MentionDefaults:
    file_mention: MentionSyntax
    max_file_size_bytes: int


def load_mention_defaults(path: Path | None = None) -> MentionDefaults:
    path = path or Path(__file__).with_name('resources').joinpath('defaults.yaml')
    values = load_yaml(path)
    file_mention = values['file mention']
    if not isinstance(file_mention, dict):
        raise ValueError('file mention section is not mapping')

    return MentionDefaults(
        file_mention=MentionSyntax(
            starts_with=str(file_mention['starts with']),
            ends_with=str(file_mention['ends with']),
            eat_spaces_before_it=bool(file_mention['eat spaces before it']),
        ),
        max_file_size_bytes=int(file_mention['max file size bytes']),
    )
