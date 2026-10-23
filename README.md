# Потоковый анализатор файлов

Лабораторная работа №2. Консольное приложение на Python для анализа событий из CSV и JSONL файлов и формирования статистического отчёта.

## Возможности

### Чтение файлов

- Поддерживаются форматы CSV и JSONL.
- Файлы читаются построчно, без полной загрузки в память.
- CSV содержит заголовок с названиями полей.
- Поддерживается обработка нескольких файлов.
- Используется кодировка UTF-8.

### События

Обязательные поля:

- `timestamp` — временная метка ISO 8601.
- `level` — `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`.
- `source` — непустая строка.
- `message` — строка.

### Анализ

Программа подсчитывает:

- Общее количество событий.
- Количество событий каждого уровня.
- Количество событий каждого источника.
- Топ-5 источников ошибок уровня `ERROR` и `CRITICAL`.
- Первую и последнюю временную метку.
- Количество пропущенных строк.

Статистика нескольких файлов объединяется в один отчёт, который сохраняется в формате JSON.

## Поддерживаемые команды

```powershell
python -m streamstats analyze INPUT [INPUT ...] --format csv|jsonl --output REPORT.json
python -m streamstats analyze INPUT --format jsonl --skip-invalid
python -m streamstats --help
```

## Примеры использования

Анализ CSV:

```powershell
python -m streamstats analyze test.csv --format csv --output report.json
```

Анализ JSONL:

```powershell
python -m streamstats analyze test.jsonl --format jsonl --output report.json
```

Анализ нескольких файлов:

```powershell
python -m streamstats analyze file1.csv file2.csv --format csv --output report.json
```

Пропуск некорректных строк:

```powershell
python -m streamstats analyze test.csv --format csv --output report.json --skip-invalid
```

## Обработка ошибок

Программа проверяет:

- Наличие обязательных полей.
- Корректность временной метки.
- Допустимость уровня события.
- Непустое значение `source`.
- Корректность входных данных.
- Поддерживаемый формат файла.

По умолчанию при некорректной строке обработка прекращается с указанием номера файла и строки.

С флагом `--skip-invalid` некорректные строки пропускаются, записывается предупреждение `WARNING`, а их количество добавляется в отчёт.

Для обработки ошибок используется базовое исключение `StreamStatsError` и отдельные классы исключений.

Коды завершения:

- `0` — успешное выполнение.
- `2` — ошибка обработки, сообщение выводится в `stderr`.

## Структура проекта

```text
lab_02/
     src/
        streamstats/
            __init__.py
            __main__.py
            parsers.py
            analysis.py
            report.py
            constants.py
            errors.py
    tests/
    .gitignore
    .pre-commit-config.yaml
    pyproject.toml
    requirements.txt
    uv.lock
    README.md
```

Назначение основных файлов:

- `__main__.py` — разбор аргументов CLI и запуск программы.
- `parsers.py` — чтение CSV и JSONL.
- `analysis.py` — проверка событий и подсчёт статистики.
- `report.py` — формирование JSON-отчёта.
- `constants.py` — константы.
- `errors.py` — классы исключений.

## Команды проверки

### Тесты

Предусмотрены тесты парсеров CSV и JSONL, пустого файла, некорректных строк, нескольких файлов, Unicode и CLI.

Запуск тестов:

```powershell
python -m pytest
```

### Ruff

Проверка кода:

```powershell
ruff check .
```

### CLI

```powershell
python -m streamstats --help
```
