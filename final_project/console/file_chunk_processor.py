from collections.abc import Callable
from pathlib import Path

from final_project.console.view import ConsoleView
from final_project.prompt_mentions import (
    ChunkCommandParser,
    ChunkSplitter,
    FileReader,
    PromptFileError,
)


class FileChunkProcessor:
    def __init__(
        self,
        view: ConsoleView,
        sender: Callable[[str], None],
        file_reader: FileReader | None = None,
    ) -> None:
        self._view = view
        self._send_prompt = sender
        self._file_reader = file_reader or FileReader()
        self._command_parser = ChunkCommandParser()
        self._chunk_splitter = ChunkSplitter()
        self._exit_command = self._view.interface.commands.quit

    def process(self, command: str) -> None:
        try:
            chunk_settings = self._command_parser.parse(command)
            file_path_text = self._read_file_path()
            if file_path_text is None:
                return

            instruction = self._read_instruction()
            if instruction is None:
                return

            text = self._file_reader.read(Path(file_path_text))
            chunks = self._chunk_splitter.split(text, chunk_settings)
        except PromptFileError as error:
            self._view.print_file_error(error)
            return

        for chunk_number, chunk in enumerate(chunks, start=1):
            prompt = self._view.build_file_chunk_prompt(
                instruction=instruction,
                chunk=chunk,
                chunk_number=chunk_number,
                chunk_count=len(chunks),
            )
            self._send_prompt(prompt)

            if chunk_settings.should_auto_confirm:
                continue

            confirmation = self._view.read_file_chunk_confirmation()
            if self._should_exit(confirmation):
                return

        self._view.print_file_chunks_done()

    def _read_file_path(self) -> str | None:
        file_path = self._view.read_file_chunk_path()
        if self._should_exit(file_path):
            return None

        return file_path

    def _read_instruction(self) -> str | None:
        instruction = self._view.read_file_chunk_instruction()
        if self._should_exit(instruction):
            return None

        return instruction

    def _should_exit(self, user_input: str) -> bool:
        return user_input == self._exit_command
