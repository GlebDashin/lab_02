import json
from datetime import datetime


def write_report(res: tuple[int, int, dict[str, int], dict[str, int], list[str], datetime | None, datetime | None], output: str) -> None:
    """Формирование отчета и запись его в файл"""
    skipped, event_count, levels, source, top, earliest, latest = res
    if earliest is None and latest is None:
        earliest_str = "None"
        latest_str = "None"
    elif earliest is not None and latest is not None:
        earliest_str = earliest.isoformat()
        latest_str = latest.isoformat()
    report = {
                "event_count": event_count,
                "skipped": skipped,
                "levels": levels,
                "source": source,
                "top": top,
                "earliest": earliest_str,
                "latest": latest_str
            }
    with open(output, "w", encoding="utf-8") as file:
        json.dump(report, file, indent = 2)
