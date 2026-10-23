import csv
import json
from collections.abc import Iterator


def parse_csv(file_names: list[str]) -> Iterator[tuple[int, int,dict[str,  str]]]:
    """Парсер, возвращающий итератор по строкам файлов csv"""
    file_number = 0
    for file_number, file_name in enumerate(file_names, start = 1):
        line_number = 0
        with open(file_name, encoding="utf-8") as file:
            dict_reader = csv.DictReader(file)
            for row in dict_reader:
                line_number += 1
                yield file_number, line_number, row


def parse_jsonl(file_names: list[str]) -> Iterator[tuple[int, int, dict[str, str]]]:
    """Парсер, возвращающий итератор по строкам файлов jsonl"""
    file_number = 0
    for file_number, file_name in enumerate(file_names, start = 1):
        line_number = 0
        with open(file_name, encoding="utf-8") as file:
            for row in file:
                line_number += 1
                yield file_number, line_number, json.loads(row)
