from pathlib import Path

from converter_cli import process_file


def test_golden_conversion(tmp_path: Path):
    repo_day02 = Path(__file__).resolve().parents[1]
    golden_in = repo_day02 / "testdata" / "golden_input.txt"
    expected_path = repo_day02 / "testdata" / "expected_output.txt"

    # copy golden input into tmp dir (process_file writes next to input)
    inp = tmp_path / "input.txt"
    inp.write_text(golden_in.read_text(encoding="utf-8"), encoding="utf-8")

    out_path = process_file(str(inp))
    out_text = Path(out_path).read_text(encoding="utf-8").strip().splitlines()
    expected_lines = expected_path.read_text(encoding="utf-8").strip().splitlines()

    assert out_text == expected_lines
