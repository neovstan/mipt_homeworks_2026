from pathlib import Path

from final_project.prompt_mentions.defaults import (
    MentionDefaults,
    load_mention_defaults,
)
from final_project.prompt_mentions.file_reader import FileReader
from final_project.prompt_mentions.mention_expand import MentionExpander


class FileMentionExpander:
    def __init__(
        self,
        mention_expander: MentionExpander | None = None,
        file_reader: FileReader | None = None,
        defaults: MentionDefaults | None = None,
    ) -> None:
        self._defaults = defaults or load_mention_defaults()
        syntax = self._defaults.file_mention
        self._mention_expander = mention_expander or MentionExpander(syntax)
        self._file_reader = file_reader or FileReader()

    def expand(self, text: str) -> str:
        return self._mention_expander.expand(
            text=text,
            replace_mention_body=self._replace_with_file_content,
        )

    def _replace_with_file_content(self, mention_body: str) -> str:
        file_path = Path(mention_body)
        content = self._file_reader.read(
            file_path,
            self._defaults.max_file_size_bytes,
        )
        return f'\n{content}'
