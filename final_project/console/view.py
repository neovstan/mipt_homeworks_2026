from final_project.console.interface import ConsoleInterface, load_console_interface


class ConsoleView:
    def __init__(self, interface: ConsoleInterface | None = None) -> None:
        self._interface = interface or load_console_interface()
        self._messages = self._interface.messages

    @property
    def interface(self) -> ConsoleInterface:
        return self._interface

    def print_startup(self) -> None:
        print(self._messages.hello)

    def read_user_input(self) -> str:
        return self._read(self._messages.input_prompt)

    def read_file_chunk_path(self) -> str:
        return self._read(self._messages.ask_file_path)

    def read_file_chunk_instruction(self) -> str:
        return self._read(self._messages.ask_chunk_task)

    def read_file_chunk_confirmation(self) -> str:
        return self._read(self._messages.ask_to_continue_chunks)

    def print_finish(self) -> None:
        print(self._messages.goodbye)

    def print_cancelled(self) -> None:
        print(self._messages.cancelled_by_user)

    def print_model_error(self, error: Exception) -> None:
        self._print_with_error(self._messages.llm_failed, error)

    def print_file_error(self, error: Exception) -> None:
        self._print_with_error(self._messages.file_failed, error)

    def print_model_answer(self, answer: str) -> None:
        print(answer)

    def print_stream_part(self, answer_part: str) -> None:
        print(answer_part, end='', flush=True)

    def finish_stream_line(self) -> None:
        print()

    def clear_screen(self) -> None:
        print(self._interface.screen.clear_terminal, end='')

    def print_history_cleared(self) -> None:
        print(self._messages.chat_was_reset)

    def print_help(self) -> None:
        print(self._messages.help_text)

    def print_invalid_settings(self, error: Exception) -> None:
        self._print_with_error(self._messages.bad_settings, error)

    def print_file_chunks_done(self) -> None:
        print(self._messages.chunks_are_done)

    def build_file_chunk_prompt(
        self,
        instruction: str,
        chunk: str,
        chunk_number: int,
        chunk_count: int,
    ) -> str:
        return self._messages.chunk_prompt.format(
            instruction=instruction,
            chunk=chunk,
            chunk_number=chunk_number,
            chunk_count=chunk_count,
        )

    def _read(self, prompt: str) -> str:
        return input(prompt).strip()

    def _print_with_error(self, template: str, error: Exception) -> None:
        print(template.format(error=error))
