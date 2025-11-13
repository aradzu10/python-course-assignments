"""Simple unit converter for temperatures and lengths.

Supported:
- Temperatures: Celsius (C), Fahrenheit (F), Kelvin (K)
- Lengths: centimeters (cm) and inches (in)

Functions:
- convert(task, value, from_unit, to_unit) -> float

Unit names are case-insensitive and common synonyms are accepted.
"""
from __future__ import annotations

from typing import Tuple


def _normalize_unit(unit: str) -> str:
    u = unit.strip().lower()
    if u in ("c", "celsius", "centigrade"):
        return "c"
    if u in ("f", "fahrenheit"):
        return "f"
    if u in ("k", "kelvin"):
        return "k"
    if u in ("cm", "centimeter", "centimeters"):
        return "cm"
    if u in ("in", "inch", "inches"):
        return "in"
    raise ValueError(f"Unknown unit: {unit}")


def _to_celsius(value: float, unit: str) -> float:
    u = _normalize_unit(unit)
    if u == "c":
        return value
    if u == "f":
        return (value - 32.0) * 5.0 / 9.0
    if u == "k":
        return value - 273.15
    raise ValueError(f"Cannot convert {unit} to celsius")


def _from_celsius(c: float, unit: str) -> float:
    u = _normalize_unit(unit)
    if u == "c":
        return c
    if u == "f":
        return c * 9.0 / 5.0 + 32.0
    if u == "k":
        return c + 273.15
    raise ValueError(f"Cannot convert celsius to {unit}")


def _to_cm(value: float, unit: str) -> float:
    u = _normalize_unit(unit)
    if u == "cm":
        return value
    if u == "in":
        return value * 2.54
    raise ValueError(f"Cannot convert {unit} to cm")


def _from_cm(cm: float, unit: str) -> float:
    u = _normalize_unit(unit)
    if u == "cm":
        return cm
    if u == "in":
        return cm / 2.54
    raise ValueError(f"Cannot convert cm to {unit}")


def convert(task: str, value: float, from_unit: str, to_unit: str) -> float:
    """Convert value from from_unit to to_unit for a given task.

    task: 'temperature' or 'length' (case-insensitive, accepts 'temp', 't', 'len')
    Raises ValueError on unknown units or tasks.
    """
    t = task.strip().lower()
    if t in ("temperature", "temp", "t"):
        # use Celsius as intermediate
        c = _to_celsius(value, from_unit)
        return _from_celsius(c, to_unit)
    if t in ("length", "len", "l"):
        cm = _to_cm(value, from_unit)
        return _from_cm(cm, to_unit)
    raise ValueError(f"Unknown task: {task}")


def parse_line(line: str) -> Tuple[str, float, str, str]:
    """Parse a CSV-ish line: task,input_value,input_unit,output_unit

    Returns (task, value, input_unit, output_unit)
    Raises ValueError on malformed lines.
    """
    parts = [p.strip() for p in line.strip().split(",")]
    if len(parts) < 4:
        raise ValueError("Each line must have 4 comma-separated fields: task,input_value,input_unit,output_unit")
    task, raw_val, in_unit, out_unit = parts[:4]
    try:
        val = float(raw_val)
    except Exception:
        raise ValueError(f"Invalid numeric value: {raw_val}")
    return task, val, in_unit, out_unit


if __name__ == "__main__":
    # quick demo when run directly
    print(convert("temperature", 0, "c", "f"))
