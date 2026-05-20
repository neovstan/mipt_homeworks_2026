from final_project.chat import (
    ChatCompletionClient,
    ChatCompletionError,
    ChatHistory,
    ChatMessage,
    ChatRole,
)
from final_project.settings import AppSettings

from final_project.prompt_mentions import (
    PromptFileError,
    FileMentionExpander,
)
from final_project.console.file_chunk_processor import FileChunkProcessor
from final_project.console.view import ConsoleView


class ConsoleApp:
    def __init__(
        self,
        settings: AppSettings,
        chat_completion_client: ChatCompletionClient | None = None,
        chat_history: ChatHistory | None = None,
        mention_expander: FileMentionExpander | None = None,
        view: ConsoleView | None = None,
    ) -> None:
        self._settings = settings
        self._chat_completion_client = chat_completion_client or ChatCompletionClient(settings)
        self._mention_expander = mention_expander or FileMentionExpander()
        self._view = view or ConsoleView()
        self._commands = self._view.interface.commands

        self._file_chunk_processor = FileChunkProcessor(
            view=self._view,
            sender=self._send_direct_prompt,
        )

        if chat_history is None:
            chat_history = ChatHistory(
                limit_message=settings.limit_message,
                limit_chars=settings.limit_chars,
            )
        self._chat_history = chat_history

    def run(self) -> None:
        self._view.print_startup()

        while True:
            user_input = self._view.read_user_input()

            if user_input == self._commands.quit:
                self._view.print_finish()
                return

            if user_input == '':
                continue

            self._handle_input(user_input)

    def _handle_input(self, user_input: str) -> None:
        if user_input == self._commands.show_help:
            self._view.print_help()
            return

        if user_input == self._commands.reset_chat:
            self._chat_history.clear()
            self._view.clear_screen()
            self._view.print_history_cleared()
            return

        if self._is_file_chunk_command(user_input):
            self._file_chunk_processor.process(user_input)
            return

        self._send_user_message(user_input)

    def _is_file_chunk_command(self, user_input: str) -> bool:
        first_word = user_input.split(maxsplit=1)[0]
        return first_word in (
            self._commands.chunk_by_paragraphs,
            self._commands.chunk_by_length,
        )

    def _send_user_message(self, user_message: str) -> None:
        message = self._expand_user_message(user_message)
        if message is None:
            return

        self._chat_history.add_user_message(message)
        dialog = self._build_messages_for_model()

        try:
            model_answer = self._ask_model(dialog, save_to_history=True)
        except KeyboardInterrupt:
            self._view.print_cancelled()
            return
        except ChatCompletionError as error:
            self._view.print_model_error(error)
            return

        if self._settings.stream:
            return

        self._view.print_model_answer(model_answer)
        self._chat_history.add_assistant_message(model_answer)

    def _expand_user_message(self, user_message: str) -> str | None:
        try:
            return self._mention_expander.expand(user_message)
        except PromptFileError as error:
            self._view.print_file_error(error)
            return None

    def _send_direct_prompt(self, user_message: str) -> None:
        prompt_messages = [
            ChatMessage(ChatRole.SYSTEM, self._settings.system_prompt),
            ChatMessage(ChatRole.USER, user_message),
        ]

        try:
            model_answer = self._ask_model(prompt_messages, save_to_history=False)
        except KeyboardInterrupt:
            self._view.print_cancelled()
            return
        except ChatCompletionError as error:
            self._view.print_model_error(error)
            return

        if not self._settings.stream:
            self._view.print_model_answer(model_answer)

    def _ask_model(self, messages: list[ChatMessage], save_to_history: bool) -> str:
        if self._settings.stream:
            return self._get_streamed_model_answer(
                messages,
                save_to_history=save_to_history,
            )

        return self._chat_completion_client.complete(messages)

    def _get_streamed_model_answer(
        self,
        dialog: list[ChatMessage],
        save_to_history: bool,
    ) -> str:
        answer_parts: list[str] = []

        for piece in self._chat_completion_client.stream_complete(dialog):
            self._view.print_stream_part(piece)
            answer_parts.append(piece)

        self._view.finish_stream_line()

        answer = ''.join(answer_parts)
        if save_to_history:
            self._chat_history.add_assistant_message(answer)

        return answer

    def _build_messages_for_model(self) -> list[ChatMessage]:
        return [
            ChatMessage(ChatRole.SYSTEM, self._settings.system_prompt),
            *self._chat_history.messages,
        ]
