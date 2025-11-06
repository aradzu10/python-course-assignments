"""Tkinter GUI for the unit converter (temperatures and lengths).

Run with:

    python -m day02.gui

The GUI lets the user pick a task (temperature/length), enter a numeric value,
choose input and output units, and see the converted result.
"""

from __future__ import annotations

import sys
import tkinter as tk
from tkinter import ttk, messagebox

from converter import convert


TEMP_UNITS = ["C", "F", "K"]
LEN_UNITS = ["cm", "in"]


class ConverterGUI(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Unit Converter")
        self.resizable(False, False)

        frm = ttk.Frame(self, padding=12)
        frm.grid(row=0, column=0, sticky="nsew")

        # Task
        ttk.Label(frm, text="Task:").grid(row=0, column=0, sticky="w")
        self.task_var = tk.StringVar(value="temperature")
        task_combo = ttk.Combobox(
            frm,
            textvariable=self.task_var,
            values=["temperature", "length"],
            state="readonly",
        )
        task_combo.grid(row=0, column=1, sticky="ew")
        task_combo.bind("<<ComboboxSelected>>", lambda e: self._update_units())

        # Input value
        ttk.Label(frm, text="Value:").grid(row=1, column=0, sticky="w")
        self.value_var = tk.StringVar()
        ttk.Entry(frm, textvariable=self.value_var).grid(row=1, column=1, sticky="ew")

        # Input unit
        ttk.Label(frm, text="From:").grid(row=2, column=0, sticky="w")
        self.from_var = tk.StringVar()
        self.from_combo = ttk.Combobox(
            frm, textvariable=self.from_var, state="readonly"
        )
        self.from_combo.grid(row=2, column=1, sticky="ew")

        # Output unit
        ttk.Label(frm, text="To:").grid(row=3, column=0, sticky="w")
        self.to_var = tk.StringVar()
        self.to_combo = ttk.Combobox(frm, textvariable=self.to_var, state="readonly")
        self.to_combo.grid(row=3, column=1, sticky="ew")

        # Convert button
        convert_btn = ttk.Button(frm, text="Convert", command=self._on_convert)
        convert_btn.grid(row=4, column=0, columnspan=2, pady=(8, 0))

        # Result
        self.result_var = tk.StringVar(value="")
        ttk.Label(frm, textvariable=self.result_var, font=(None, 11, "bold")).grid(
            row=5, column=0, columnspan=2, pady=(8, 0)
        )

        for i in range(2):
            frm.columnconfigure(i, weight=1)

        self._update_units()

    def _update_units(self) -> None:
        task = self.task_var.get().strip().lower()
        if task.startswith("t"):
            units = TEMP_UNITS
        else:
            units = LEN_UNITS
        # keep selections if possible
        cur_from = self.from_var.get()
        cur_to = self.to_var.get()
        self.from_combo.config(values=units)
        self.to_combo.config(values=units)
        if cur_from not in units:
            self.from_var.set(units[0])
        if cur_to not in units:
            self.to_var.set(units[1] if len(units) > 1 else units[0])

    def _on_convert(self) -> None:
        task = self.task_var.get()
        raw = self.value_var.get().strip()
        from_u = self.from_var.get()
        to_u = self.to_var.get()
        try:
            v = float(raw)
        except Exception:
            messagebox.showerror("Invalid input", "Please enter a numeric value.")
            return
        try:
            out = convert(task, v, from_u, to_u)
        except Exception as e:
            messagebox.showerror("Conversion error", str(e))
            return
        # Format result cleanly
        if abs(out) < 1e-6:
            out_str = f"{out:.6g}"
        else:
            out_str = f"{out:.6f}".rstrip("0").rstrip(".")
        self.result_var.set(f"{v} {from_u} → {out_str} {to_u}")


def main() -> int:
    # If script is run directly from project root, ensure package imports resolve
    try:
        app = ConverterGUI()
        app.mainloop()
        return 0
    except Exception as e:
        print("Error running GUI:", e, file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
