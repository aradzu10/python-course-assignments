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

from converter import convert


def interactive_mode() -> None:
    print("Interactive converter")
    task = input("Task (temperature/length): ").strip()
    raw = input("Input value: ").strip()
    in_unit = input("Input unit (e.g. C, F, K, cm, in): ").strip()
    out_unit = input("Output unit: ").strip()
    try:
        val = float(raw)
    except Exception:
        print("Invalid numeric value")
        return
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
    args = parser.parse_args(argv)
    if not args.file:
        interactive_mode()
        return 0
    try:
        out = process_file(args.file)
        print(f"Wrote: {out}")
        return 0
    except Exception as e:
        print(f"Error processing file: {e}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
