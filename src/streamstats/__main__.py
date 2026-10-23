import argparse
import sys

from .analysis import analys
from .errors import StreamStatsError
from .parsers import parse_csv, parse_jsonl
from .report import write_report


def create_parser() -> argparse.ArgumentParser:
    """Создание парсерса команд строки"""
    parser = argparse.ArgumentParser()
    commands = parser.add_subparsers(required=True)

    analyze = commands.add_parser("analyze")
    analyze.add_argument("inputs", nargs="+")
    analyze.add_argument("--format", choices=["csv", "jsonl"], required=True)
    analyze.add_argument("--output")
    analyze.add_argument("--skip-invalid", dest = "skip", action="store_true")
    return parser



def main() -> None:

    parser = create_parser()
    args = parser.parse_args()

    if args.format=="csv":
        rows = parse_csv(args.inputs)
    else:
        rows = parse_jsonl(args.inputs)

    try:
        res = analys(rows, args.skip)
    except StreamStatsError as error:
        print(f"{error}", file=sys.stderr)
        sys.exit(2)

    write_report(res, args.output)

if __name__ == "__main__":
    main()
