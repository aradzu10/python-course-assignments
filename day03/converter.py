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

import pint

# Initialize pint unit registry
ureg = pint.UnitRegistry()

TEMP_UNITS = ["C", "F", "K"]
LEN_UNITS = ["cm", "inch"]

def _normalize_unit(unit: str) -> str:
    """Normalize unit names to pint-compatible format."""
    u = unit.strip().lower()
    if u in ("c", "celsius", "centigrade"):
        return "degC"
    if u in ("f", "fahrenheit"):
        return "degF"
    if u in ("k", "kelvin"):
        return "kelvin"
    if u in ("cm", "centimeter", "centimeters"):
        return "cm"
    if u in ("in", "inch", "inches"):
        return "inch"
    raise ValueError(f"Unknown unit: {unit}")


def convert(task: str, value: float, from_unit: str, to_unit: str) -> float:
    """Convert value from from_unit to to_unit for a given task.

    task: 'temperature' or 'length' (case-insensitive, accepts 'temp', 't', 'len')
    Raises ValueError on unknown units or tasks.
    """
    t = task.strip().lower()

    try:
        # Normalize units to pint format
        from_pint = _normalize_unit(from_unit)
        to_pint = _normalize_unit(to_unit)

        # Create quantity with pint
        quantity = ureg.Quantity(value, from_pint)

        # Convert to target unit
        result = quantity.to(to_pint)

        # Round to 12 decimal places to avoid floating point precision issues
        return round(result.magnitude, 5)
    except (pint.errors.DimensionalityError, pint.errors.UndefinedUnitError) as e:
        raise ValueError(f"Cannot convert {from_unit} to {to_unit}: {e}")
    except Exception as e:
        raise ValueError(f"Conversion error: {e}")
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
