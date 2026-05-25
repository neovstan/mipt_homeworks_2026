from dataclasses import dataclass
from pathlib import Path
from typing import Any

from final_project.yaml_loader import load_yaml


@dataclass(frozen=True)
class ConsoleCommands:
    quit: str
    show_help: str
    reset_chat: str
    chunk_by_paragraphs: str
    chunk_by_length: str


@dataclass(frozen=True)
class ConsoleMessages:
    hello: str
    input_prompt: str
    ask_file_path: str
    ask_chunk_task: str
    ask_to_continue_chunks: str
    goodbye: str
    cancelled_by_user: str
    llm_failed: str
    file_failed: str
    chat_was_reset: str
    help_text: str
    bad_settings: str
    chunk_prompt: str
    chunks_are_done: str


@dataclass(frozen=True)
class ConsoleScreen:
    clear_terminal: str


@dataclass(frozen=True)
class ConsoleInterface:
    commands: ConsoleCommands
    messages: ConsoleMessages
    screen: ConsoleScreen


def load_console_interface(path: Path | None = None) -> ConsoleInterface:
    path = path or _default_interface_path()
    values = load_yaml(path)

    commands = _read_section(values, 'terminal commands')
    messages = _read_section(values, 'terminal texts')
    screen = _read_section(values, 'terminal screen')

    return ConsoleInterface(
        commands=ConsoleCommands(
            quit=str(commands['quit']),
            show_help=str(commands['show help']),
            reset_chat=str(commands['reset chat']),
            chunk_by_paragraphs=str(commands['chunk by paragraphs']),
            chunk_by_length=str(commands['chunk by length']),
        ),
        messages=ConsoleMessages(
            hello=str(messages['hello']),
            input_prompt=str(messages['input prompt']),
            ask_file_path=str(messages['ask file path']),
            ask_chunk_task=str(messages['ask chunk task']),
            ask_to_continue_chunks=str(messages['ask to continue chunks']),
            goodbye=str(messages['goodbye']),
            cancelled_by_user=str(messages['cancelled by user']),
            llm_failed=str(messages['llm failed']),
            file_failed=str(messages['file failed']),
            chat_was_reset=str(messages['chat was reset']),
            help_text=str(messages['help text']),
            bad_settings=str(messages['bad settings']),
            chunk_prompt=str(messages['chunk prompt']),
            chunks_are_done=str(messages['chunks are done']),
        ),
        screen=ConsoleScreen(
            clear_terminal=str(screen['clear terminal']),
        ),
    )


def _default_interface_path() -> Path:
    return Path(__file__).with_name('resources') / 'interface.yaml'


def _read_section(values: dict[str, Any], name: str) -> dict[str, Any]:
    section = values[name]
    if not isinstance(section, dict):
        raise ValueError(f'console interface section {name} is not mapping')

    return section
