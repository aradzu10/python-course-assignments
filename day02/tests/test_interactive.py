import sys
from pathlib import Path

# ensure day02 is on sys.path so tests can import local modules
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import builtins
import pytest

from converter_cli import interactive_mode


def test_interactive_mode_monkeypatch(monkeypatch, capsys):
    # Simulate user input: task, value, in_unit, out_unit
    inputs = iter(["temperature", "32", "F", "C"])

    def fake_input(prompt=""):
        return next(inputs)

    monkeypatch.setattr(builtins, "input", fake_input)
    interactive_mode()
    captured = capsys.readouterr()
    # Should show the conversion line
    assert "32" in captured.out
    assert "0.0" in captured.out or "0" in captured.out
