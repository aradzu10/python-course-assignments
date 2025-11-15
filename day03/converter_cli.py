"""Command-line interface for the unit converter.

Usage:
- Interactive: run without arguments and answer prompts
- File mode: pass a path to a file where each line is:
  task,input_value,input_unit,output_unit
  e.g. temperature,32,f,c
  The program will write a new file next to the input with `_converted` suffix.
"""

from __future__ import annotations

import argparse
import os
import sys
import csv
from typing import List

from converter import convert, TEMP_UNITS, LEN_UNITS


def interactive_mode() -> None:
    print("Interactive converter")
    task = input("Task (temperature/length): ").strip()

    # choose allowed units based on task
    t_low = task.strip().lower()
    if t_low.startswith("t"):
        allowed = TEMP_UNITS
    else:
        allowed = LEN_UNITS

    raw = input("Input value: ").strip()
    try:
        val = float(raw)
    except Exception:
        print("Invalid numeric value")
        return

    def ask_unit(prompt: str, choices: list[str]) -> str:
        choices_str = ", ".join(choices)
        while True:
            u = input(f"{prompt} ({choices_str}): ").strip()
            if any(u.lower() == c.lower() for c in choices):
                return u
            print(f"Invalid unit. Choose one of: {choices_str}")

    in_unit = ask_unit("Input unit", allowed)
    out_unit = ask_unit("Output unit", allowed)

    try:
        result = convert(task, val, in_unit, out_unit)
    except Exception as e:
        print(f"Error: {e}")
        return
    print(f"{val} {in_unit} -> {result} {out_unit}")


def _output_path_for(path: str) -> str:
    base, ext = os.path.splitext(path)
    if ext:
        return f"{base}_converted{ext}"
    return f"{path}_converted"


def process_file(path: str) -> str:
    """Read input file lines and write converted output file next to it.

    Returns the output file path.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(path)
    out_path = _output_path_for(path)
    results: List[str] = []
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.reader(
            line for line in f if line.strip() and not line.lstrip().startswith("#")
        )
        for lineno, parts in enumerate(reader, start=1):
            try:
                if len(parts) < 4:
                    raise ValueError("need 4 fields")
                task = parts[0].strip()
                val = float(parts[1].strip())
                in_unit = parts[2].strip()
                out_unit = parts[3].strip()
                out_val = convert(task, val, in_unit, out_unit)
                results.append(f"{task},{val},{in_unit},{out_val},{out_unit}")
            except Exception as e:
                results.append(f"ERROR,line {lineno},{','.join(parts)},{e}")
    with open(out_path, "w", encoding="utf-8") as of:
        of.write("# task,input_value,input_unit,output_value,output_unit\n")
        for r in results:
            of.write(r + "\n")
    return out_path


def main(argv: List[str] | None = None) -> int:
    if argv is None:
        argv = sys.argv[1:]
    parser = argparse.ArgumentParser(description="Simple converter")
    parser.add_argument(
        "file", nargs="?", help="Input file with conversion instructions"
    )
    # allow single-shot conversions via CLI args
    parser.add_argument(
        "-t",
        "--task",
        choices=["temperature", "length"],
        help="Task: temperature or length",
    )
    parser.add_argument("-v", "--value", type=float, help="Input numeric value")
    parser.add_argument(
        "-f", "--from-unit", dest="from_unit", help="Input unit (C,F,K,cm,in)"
    )
    parser.add_argument(
        "-o", "--to-unit", dest="to_unit", help="Output unit (C,F,K,cm,in)"
    )
    args = parser.parse_args(argv)

    # If user supplied a file and also supplied task/value flags, that's ambiguous
    if args.file and args.task:
        print("Error: provide either a file OR task/value arguments, not both.")
        return 2

    # If file provided, run file processing
    if args.file:
        out = process_file(args.file)
        print(f"Wrote: {out}")
        return 0

    # If task provided, require value and units
    if args.task:
        if args.value is None or not args.from_unit or not args.to_unit:
            print(
                "Error: when using --task you must also provide --value, --from-unit and --to-unit"
            )
            return 2
        result = convert(args.task, args.value, args.from_unit, args.to_unit)
        # print concise result
        print(f"{args.value} {args.from_unit} -> {result} {args.to_unit}")
        return 0

    # No file and no task flags -> interactive mode
    interactive_mode()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
