# Итоговый проект "GigaVibeMiptCode"

Суть - консольный ИИ-ассистент на OpenAI-совместимом API, который умеет сохранять историю сообщений, выполняет chunking, поддерживает ссылки на файлы

# Команды
```
@::filepath:: - вставить содержимое файла
/filechunk [pararaph=N, len=M, -y] - анализ файла с промптом для каждого чанка
/reset - сбросить историю
\q - выйти
```

# Установка
```
cd path_to_repos
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

# Настройка модели
Нужен OpenAI-совместимый сервер
Пример для Ollama:
```
olamma pull gemma3:270m
olamma serve
```

# Конфигурация через config.yaml
```
api_key: ollama
api_host: http://localhost/...
model: gemma3:270m
temperature: 0.3
limit_message: 20
limit_chars: 2000
system_prompt: Мяу
stream: false
```

# Запуск
```
.venv/bin/python -m final_project
```

# Покрытие тестами
```
19 passed
coverage: 54%
```

# Архитектура
```
chat - история и OpenAI-клиент
settings - загрузка и валидация настроек
prompt_mentions - @::file:: и чанки
console - CLI-интерфейс
resources/*.yaml - тексты и дефолты
```