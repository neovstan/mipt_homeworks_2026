from dataclasses import dataclass


@dataclass(frozen=True)
class AppSettings:
    api_key: str
    api_host: str
    model: str = ''
    temperature: float = 0.0
    system_prompt: str = ''
    stream: bool = False
    limit_message: int | None = None
    limit_chars: int | None = None
