import sys
from pathlib import Path

import pytest

from converter import convert


def test_temp_c_to_f():
    assert pytest.approx(convert("temperature", 0, "C", "F"), rel=1e-9) == 32.0


def test_temp_f_to_c():
    assert pytest.approx(convert("temp", 212, "f", "c"), rel=1e-9) == 100.0


def test_temp_k_to_c():
    assert pytest.approx(convert("temperature", 273.15, "k", "c"), rel=1e-9) == 0.0


def test_length_cm_to_in():
    assert pytest.approx(convert("length", 2.54, "cm", "in"), rel=1e-9) == 1.0


def test_length_in_to_cm():
    assert pytest.approx(convert("len", 1.0, "in", "cm"), rel=1e-9) == 2.54


def test_invalid_unit():
    with pytest.raises(ValueError):
        convert("temperature", 10, "m", "c")
