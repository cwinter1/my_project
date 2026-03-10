"""
Convert a .py lesson file into a properly structured .ipynb notebook.

Splits on section borders (══) to keep indented blocks (functions, try/except,
loops) intact in a single code cell.  Adds empty workspace cells after
EXERCISE / TASK sections.

Usage:
    python convert_py_to_ipynb.py                     # convert ALL .py files
    python convert_py_to_ipynb.py W2_D1_Functions_Basics.py  # convert one file
"""

import json
import re
import os
import sys

CURRICULUM_DIR = os.path.dirname(os.path.abspath(__file__))
SKIP_FILES = {"convert_py_to_ipynb.py", "verify_curriculum.py", "README.py"}


def py_to_notebook(py_path):
    """Convert a single .py file to a notebook dict."""
    with open(py_path, encoding="utf-8") as f:
        source = f.read()

    # Split on ══ section borders
    sections = re.split(r"(?=^# ══)", source, flags=re.MULTILINE)

    cells = []
    for section in sections:
        if not section.strip():
            continue

        lines = section.split("\n")

        # Separate leading comment block from code
        md_lines = []
        code_lines = []
        in_code = False

        for line in lines:
            if not in_code:
                if line.strip() == "" or line.startswith("#"):
                    md_lines.append(line)
                else:
                    in_code = True
                    code_lines.append(line)
            else:
                code_lines.append(line)

        # --- markdown cell ---
        if md_lines:
            md_text = []
            for line in md_lines:
                if line.startswith("# "):
                    md_text.append(line[2:])
                elif line.startswith("#"):
                    md_text.append(line[1:])
                else:
                    md_text.append(line)
            while md_text and md_text[-1].strip() == "":
                md_text.pop()
            if md_text:
                cells.append({
                    "cell_type": "markdown",
                    "metadata": {},
                    "source": [l + "\n" for l in md_text[:-1]] + [md_text[-1]],
                })

        # Is this an exercise / task section?
        section_header = "\n".join(md_lines[:5])
        is_exercise = bool(re.search(r"EXERCISE|TASK", section_header))

        # --- code cell(s) ---
        if code_lines:
            # Strip trailing blank lines
            while code_lines and code_lines[-1].strip() == "":
                code_lines.pop()

            if code_lines:
                code_text = "\n".join(code_lines)
                workspace_match = re.search(r"\n{4,}", code_text)

                if workspace_match:
                    before = code_text[: workspace_match.start()].rstrip()
                    after = code_text[workspace_match.end() :].strip()

                    if before:
                        src = before.split("\n")
                        cells.append(_code_cell(src))

                    # Empty workspace cell
                    cells.append(_code_cell([]))

                    if after:
                        src = after.split("\n")
                        cells.append(_code_cell(src))
                else:
                    cells.append(_code_cell(code_lines))
                    if is_exercise:
                        cells.append(_code_cell([]))
            elif is_exercise:
                cells.append(_code_cell([]))
        elif is_exercise:
            cells.append(_code_cell([]))

    return {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {"name": "python", "version": "3.12.0"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


def _code_cell(lines):
    """Helper to build a code cell dict from a list of source lines."""
    if lines:
        source = [l + "\n" for l in lines[:-1]] + [lines[-1]]
    else:
        source = []
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": source,
    }


def convert_file(py_path):
    """Convert one .py file and write the .ipynb next to it."""
    nb = py_to_notebook(py_path)
    nb_path = py_path.rsplit(".", 1)[0] + ".ipynb"
    with open(nb_path, "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=2, ensure_ascii=False)
    return nb_path, len(nb["cells"])


if __name__ == "__main__":
    if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    targets = sys.argv[1:]

    if targets:
        for t in targets:
            path = t if os.path.isabs(t) else os.path.join(CURRICULUM_DIR, t)
            if os.path.isfile(path):
                nb_path, n = convert_file(path)
                print(f"  DONE  {os.path.basename(nb_path)} ({n} cells)")
            else:
                print(f"  SKIP  {t} (not found)")
    else:
        # Convert all .py lesson files
        for root, dirs, files in os.walk(CURRICULUM_DIR):
            dirs.sort()
            for fname in sorted(files):
                if not fname.endswith(".py"):
                    continue
                if fname in SKIP_FILES or fname.startswith("verify_"):
                    continue
                py_path = os.path.join(root, fname)
                nb_path, n = convert_file(py_path)
                print(f"  DONE  {os.path.relpath(nb_path, CURRICULUM_DIR)} ({n} cells)")
