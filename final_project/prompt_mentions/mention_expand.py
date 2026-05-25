from collections.abc import Callable, Iterator

from final_project.prompt_mentions.syntax import MentionSyntax


class MentionExpander:
    def __init__(self, syntax: MentionSyntax) -> None:
        self._syntax = syntax

    def expand(self, text: str, replace_mention_body: Callable[[str], str]) -> str:
        fragments = self._iter_expanded_parts(text, replace_mention_body)
        return ''.join(fragments)

    def _iter_expanded_parts(
        self,
        text: str,
        replace_mention_body: Callable[[str], str],
    ) -> Iterator[str]:
        start_marker = self._syntax.starts_with
        finish_marker = self._syntax.ends_with
        cursor = 0

        while True:
            start = text.find(start_marker, cursor)
            if start == -1:
                yield text[cursor:]
                break

            body_start = start + len(start_marker)
            finish = text.find(finish_marker, body_start)
            if finish == -1:
                yield text[cursor:]
                break

            prefix = text[cursor:start]
            if self._syntax.eat_spaces_before_it:
                prefix = prefix.rstrip(' \t')

            body = text[body_start:finish]
            yield prefix
            yield replace_mention_body(body)
            cursor = finish + len(finish_marker)
