import sys
from pathlib import Path

import os
import pytest

from converter_cli import process_file


def test_process_file_creates_output(tmp_path: Path):
    content = """
temperature,32,F,C
length,2.54,cm,in
""".strip()
    in_path = tmp_path / "input.txt"
    in_path.write_text(content + "\n", encoding="utf-8")
    out_path = process_file(str(in_path))
    assert os.path.exists(out_path)
    data = Path(out_path).read_text(encoding="utf-8")
    assert "# task,input_value,input_unit,output_value,output_unit" in data
    assert "temperature,32.0,F,0.0,C" in data
    assert "length,2.54,cm,1.0,in" in data
