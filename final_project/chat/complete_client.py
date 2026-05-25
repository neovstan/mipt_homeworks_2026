from collections.abc import Iterable, Iterator
from typing import Any, Optional, cast

from openai import OpenAI, OpenAIError

from final_project.chat.message import ChatMessage
from final_project.chat.messages import ChatMessages, load_chat_messages
from final_project.settings import AppSettings


class ChatCompletionError(Exception):
    pass


class ChatCompletionClient:
    def __init__(self, settings: AppSettings, messages: Optional[ChatMessages] = None) -> None:
        self._settings = settings

        if messages is None:
            messages = load_chat_messages()
        self._messages = messages

        self._openai_client = OpenAI(
            api_key=settings.api_key,
            base_url=settings.api_host,
        )

    def complete(self, messages: Iterable[ChatMessage]) -> str:
        api_messages = self._to_api_messages(messages)
        response = self._request_completion(api_messages)

        if not response.choices:
            raise ChatCompletionError(self._messages.llm_empty_answer)

        answer = response.choices[0].message.content

        if answer is None:
            return ''

        if isinstance(answer, str):
            return answer

        return str(answer)

    def stream_complete(self, messages: Iterable[ChatMessage]) -> Iterator[str]:
        api_messages = self._to_api_messages(messages)
        events = self._request_completion(api_messages, stream=True)

        for event in events:
            answer_part = self._get_stream_answer_part(event)

            if answer_part != '':
                yield answer_part

    def _request_completion(
        self,
        api_messages: list[dict[str, str]],
        stream: bool = False,
    ) -> Any:
        try:
            response = self._openai_client.chat.completions.create(
                model=self._settings.model,
                messages=cast(Any, api_messages),
                temperature=self._settings.temperature,
                stream=stream,
            )
        except OpenAIError as error:
            raise ChatCompletionError(str(error)) from error

        return response

    def _to_api_messages(self, messages: Iterable[ChatMessage]) -> list[dict[str, str]]:
        api_messages = []

        for message in messages:
            api_message = message.to_api_dict()
            api_messages.append(api_message)

        return api_messages

    def _get_stream_answer_part(self, completion_event: Any) -> str:
        if not completion_event.choices:
            return ''

        first_choice = completion_event.choices[0]
        content = first_choice.delta.content

        if content is None:
            return ''

        if isinstance(content, str):
            return content

        return str(content)
