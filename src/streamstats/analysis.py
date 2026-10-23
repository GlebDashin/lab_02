import logging
from collections.abc import Iterator
from datetime import datetime

from .errors import InvalidEventError, InvalidTimePointError, StreamStatsError

logger = logging.getLogger(__name__)


def validate(row: dict[str,str]):
    """Валидация словаря(строки события)"""
    if "source" not in row:
        raise InvalidEventError("Не задан source")
    if not isinstance(row["source"], str) or row["source"] == "":
        raise InvalidEventError("Некорректно задан source")

    if "level" not in row:
        raise InvalidEventError("Не задан level")
    if not isinstance(row["level"], str) or (row["level"] != "DEBUG" and row["level"] != "INFO" and row["level"] != "WARNING" and row["level"] != "ERROR" and row["level"] != "CRITICAL") :
        raise InvalidEventError("Некорректно задан level")

    if "timestamp" not in row:
        raise InvalidEventError("Не задан timestamp")
    try:
        datetime.fromisoformat(row["timestamp"])
    except ValueError:
        raise InvalidTimePointError("Некорректная временная метка")

    if "message" not in row:
        raise InvalidEventError("Не задан message")
    if not isinstance(row["message"], str):
        raise InvalidEventError("Некорректно задан message")



def analys(rows: Iterator[tuple[int, int, dict[str, str]]], skip: bool) -> tuple[int, int, dict[str, int], dict[str, int], list[str], datetime | None, datetime | None]:
    """Главная функция обработки строк через итератор по ним"""
    skipped = 0
    events_count = 0
    levels = {
        "DEBUG":  0,
        "INFO": 0,
        "WARNING": 0,
        "ERROR": 0,
        "CRITICAL": 0
    }
    sources = {}
    errors_sources = {}
    earliest = None
    latest = None

    while True:
        try:
            file, line, row = next(rows)
            validate(row)
        except StopIteration:
            break
        except (InvalidEventError, InvalidTimePointError) as error:
            if skip:
                logger.warning("Файл %d, строка %d: %s", file, line, error)
                skipped+=1
                continue
            else:
                raise StreamStatsError(f"Файл {file}, строка {line}: {error}")
        events_count += 1
        levels[row["level"]] += 1
        if row["source"] not in sources:
            sources[row["source"]]=1
        else:
            sources[row["source"]]+=1
        if row["level"] == "CRITICAL" or row["level"] == "ERROR" :
            if row["source"] not in errors_sources:
                errors_sources[row["source"]] = 1
            else:
                errors_sources[row["source"]] += 1

        if latest is None or datetime.fromisoformat(row["timestamp"]) > latest:
            latest = datetime.fromisoformat(row["timestamp"])
        if earliest is None or datetime.fromisoformat(row["timestamp"]) < earliest:
            earliest = datetime.fromisoformat(row["timestamp"])


    top = sorted(errors_sources, key=lambda x: errors_sources[x], reverse=True)[:5]

    return skipped, events_count, levels, sources, top, earliest, latest
