#!/usr/bin/env python3
"""habit-tracker-cli: a tiny command-line habit tracker.

Data is stored in a JSON file (default: ~/.habits.json, override with HABITS_FILE).
"""
import argparse
import json
import os
import sys
from datetime import date, timedelta
from pathlib import Path

DATA_FILE = Path(os.environ.get("HABITS_FILE", Path.home() / ".habits.json"))


def load():
    if DATA_FILE.exists():
        try:
            return json.loads(DATA_FILE.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            sys.exit(f"Error: {DATA_FILE} is not valid JSON.")
    return {}


def save(data):
    DATA_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def streak(days, today=None):
    """Return the current consecutive-day streak ending today (or yesterday)."""
    today = today or date.today()
    done = {date.fromisoformat(d) for d in days}
    cursor = today if today in done else today - timedelta(days=1)
    count = 0
    while cursor in done:
        count += 1
        cursor -= timedelta(days=1)
    return count


def cmd_add(args, data):
    if args.name in data:
        sys.exit(f"Habit '{args.name}' already exists.")
    data[args.name] = []
    save(data)
    print(f"Added habit '{args.name}'.")


def cmd_done(args, data):
    if args.name not in data:
        sys.exit(f"Habit '{args.name}' not found. Use 'add' first.")
    today = date.today().isoformat()
    if today in data[args.name]:
        print(f"'{args.name}' is already marked done today.")
        return
    data[args.name].append(today)
    save(data)
    print(f"Nice! '{args.name}' done. Current streak: {streak(data[args.name])} day(s).")


def cmd_list(args, data):
    if not data:
        print("No habits yet. Add one with: habit.py add <name>")
        return
    today = date.today().isoformat()
    for name, days in sorted(data.items()):
        mark = "[x]" if today in days else "[ ]"
        print(f"{mark} {name:<25} streak: {streak(days):>3}  total: {len(days)}")


def cmd_remove(args, data):
    if data.pop(args.name, None) is None:
        sys.exit(f"Habit '{args.name}' not found.")
    save(data)
    print(f"Removed habit '{args.name}'.")


def build_parser():
    parser = argparse.ArgumentParser(description="A tiny command-line habit tracker.")
    sub = parser.add_subparsers(dest="command", required=True)
    for name, func, help_ in [
        ("add", cmd_add, "add a new habit"),
        ("done", cmd_done, "mark a habit as done today"),
        ("remove", cmd_remove, "delete a habit"),
    ]:
        p = sub.add_parser(name, help=help_)
        p.add_argument("name")
        p.set_defaults(func=func)
    p = sub.add_parser("list", help="show all habits")
    p.set_defaults(func=cmd_list)
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    args.func(args, load())


if __name__ == "__main__":
    main()
