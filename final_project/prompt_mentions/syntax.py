from dataclasses import dataclass


@dataclass(frozen=True)
class MentionSyntax:
    starts_with: str
    ends_with: str
    eat_spaces_before_it: bool = False
