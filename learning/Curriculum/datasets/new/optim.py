import json
from pathlib import Path

ROOT_FOLDER = r"C:\Users\crist\Documents\GitHub\python-gstat\Curriculum"  # ← change this


def split_to_cells(code_text):
    lines = code_text.splitlines()
    cells = []
    buffer = []
    current_type = None

    def flush():
        nonlocal buffer, current_type, cells
        if not buffer:
            return

        if current_type == "markdown":
            md_lines = []
            for l in buffer:
                if l.startswith("# "):
                    md_lines.append(l[2:])
                elif l.startswith("#"):
                    md_lines.append(l[1:])
                else:
                    md_lines.append(l)

            cells.append({
                "cell_type": "markdown",
                "metadata": {},
                "source": [line + "\n" for line in md_lines],
            })
        else:
            cells.append({
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [line + "\n" for line in buffer],
            })

        buffer = []
        current_type = None

    for line in lines:
        is_comment = line.strip().startswith("#")
        new_type = "markdown" if is_comment else "code"

        if current_type is None:
            current_type = new_type
            buffer.append(line)
        elif new_type == current_type:
            buffer.append(line)
        else:
            flush()
            current_type = new_type
            buffer.append(line)

    flush()
    return cells


root = Path(ROOT_FOLDER)

for py_file in root.rglob("*.py"):
    code = py_file.read_text(encoding="utf-8")
    cells = split_to_cells(code)

    nb = {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {"name": "python", "version": "3.x"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }

    ipynb_path = py_file.with_suffix(".ipynb")
    ipynb_path.write_text(json.dumps(nb, indent=2), encoding="utf-8")

print("✅ Conversion complete")
