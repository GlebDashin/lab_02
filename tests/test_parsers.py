import json
import os
import subprocess
import sys

from streamstats.analysis import analys
from streamstats.parsers import parse_csv, parse_jsonl
from streamstats.report import write_report


def test_csv_parser():
    with open("testpy.csv", "w", encoding="utf-8") as file:
        file.write("timestamp,level,source,message\n2026-10-15T11:07:00+03:00,DEBUG,api,message\n")

    rows = [
        (1, 1, {
            "timestamp": "2026-10-15T11:07:00+03:00",
            "level": "DEBUG",
            "source": "api",
            "message": "message"
        })
    ]
    try:
        assert list(parse_csv(["testpy.csv"])) == rows
    finally:
        os.remove("testpy.csv")

def test_jsonl_parser():
    with open("testpy.jsonl", "w", encoding="utf-8") as file:
        file.write('{"timestamp": "2026-10-15T11:07:00+03:00", "level": "DEBUG", "source": "api", "message": "message"}')

    rows = [
        (1, 1, {
            "timestamp": "2026-10-15T11:07:00+03:00",
            "level": "DEBUG",
            "source": "api",
            "message": "message"
        })
    ]
    try:
        assert list(parse_jsonl(["testpy.jsonl"])) == rows
    finally:
        os.remove("testpy.jsonl")

def test_empty_file():
    with open("testpy.jsonl", "w", encoding="utf-8") as file:
        pass
    try:
        res = analys(parse_jsonl(["testpy.jsonl"]), True)
        write_report (res, "testpy1.json")

        with open("testpy1.json", "r", encoding="utf-8") as file:
            report = json.load(file)
        assert report == {
            "event_count": 0,
            "skipped": 0,
            "levels": {
            "DEBUG": 0,
            "INFO": 0,
            "WARNING": 0,
            "ERROR": 0,
            "CRITICAL": 0
            },
            "source": {},
            "top": [],
            "earliest": "None",
            "latest": "None"
        }
    finally:
        if os.path.exists("testpy1.json"):
            os.remove("testpy1.json")
        if os.path.exists("testpy.jsonl"):
         os.remove("testpy.jsonl")

def test_many_files():
    with open("testpy1.jsonl", "w", encoding="utf-8") as file:
            file.write('{"timestamp": "2026-10-15T11:07:00+03:00", "level": "DEBUG", "source": "api", "message": "message"}')
    with open("testpy2.jsonl", "w", encoding="utf-8") as file:
            file.write('{"timestamp": "2026-10-15T11:08:00+03:00", "level": "CRITICAL", "source": "database", "message": "message1"}')
    try:
        res = analys(parse_jsonl(["testpy1.jsonl", "testpy2.jsonl"]), True)
        write_report (res, "testpy1.json")

        with open("testpy1.json", "r", encoding="utf-8") as file:
            report = json.load(file)
        assert report == {
            "event_count": 2,
            "skipped": 0,
            "levels": {
            "DEBUG": 1,
            "INFO": 0,
            "WARNING": 0,
            "ERROR": 0,
            "CRITICAL": 1
            },
            "source": {"api": 1, "database": 1},
            "top": ["database"],
            "earliest": "2026-10-15T11:07:00+03:00",
            "latest": "2026-10-15T11:08:00+03:00"            }
    finally:
        if os.path.exists("testpy1.json"):
            os.remove("testpy1.json")
        if os.path.exists("testpy1.jsonl"):
            os.remove("testpy1.jsonl")
        if os.path.exists("testpy2.jsonl"):
            os.remove("testpy2.jsonl")

def test_unicode():
    with open("testpy.jsonl", "w", encoding="utf-8") as file:
        file.write('{"timestamp": "2026-10-15T11:07:00+03:00", "level": "DEBUG", "source": "api", "message": "русский месадж"}')

    rows = [
        (1, 1, {
            "timestamp": "2026-10-15T11:07:00+03:00",
            "level": "DEBUG",
            "source": "api",
            "message": "русский месадж"
        })
    ]
    try:
        assert list(parse_jsonl(["testpy.jsonl"])) == rows
    finally:
        os.remove("testpy.jsonl")

def test_cli(tmp_path):
    input_file = tmp_path / "test.jsonl"

    with open(input_file, "w", encoding="utf-8") as file:
        file.write('{"timestamp": "2026-10-15T11:07:00+03:00", "level": "DEBUG", "source": "api", "message": "message"}')

    res = subprocess.run([
        sys.executable,
        "-m", "streamstats",
        "analyze",
        str(input_file),
        "--format", "jsonl",
        "--output", str(tmp_path / "report.json")
    ], check=False)

    assert res.returncode == 0
