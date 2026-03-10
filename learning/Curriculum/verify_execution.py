# ══════════════════════════════════════════════════════════════
#  EXECUTION QA VERIFIER
#  Run from Curriculum/ folder:  python verify_execution.py
#
#  Actually executes every lesson notebook and reports cell errors.
#  Uses nbformat + nbconvert (ships with Jupyter — no extra install).
#
#  Automatically injects a __file__ workaround so notebooks that use
#  os.path.dirname(__file__) work even though notebooks don't define __file__.
#
#  Options:
#    python verify_execution.py            -- runs W1-W9 only
#    python verify_execution.py --all      -- includes W10-W12 (need API keys)
#    python verify_execution.py --week 3   -- runs a single week
# ══════════════════════════════════════════════════════════════

import os
import sys
import re
import copy
import argparse

# Matches print() or display() at the start of a line (top-level call, not inside a function/class body)
_TOP_LEVEL_PRINT = re.compile(r"^(?:print|display)\(", re.MULTILINE)

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

CURRICULUM_DIR = os.path.dirname(os.path.abspath(__file__))

SKIP_FILES = {
    "verify_curriculum.py", "verify_execution.py", "README.py", "W12_OVERVIEW.py",
    "convert_py_to_ipynb.py", "README.ipynb", "W12_OVERVIEW.ipynb",
    "qa.ipynb", "verify_curriculum.ipynb",
}

SKIP_DIRS = {"datasets", "__pycache__", "temp_output"}

# Weeks that require live API keys or external services (OpenAI, LangChain, etc.)
API_KEY_WEEKS = {10, 11, 12}


def collect_notebooks(include_api_weeks=False, single_week=None):
    notebooks = []
    for root, dirs, files in os.walk(CURRICULUM_DIR):
        dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS)
        for filename in sorted(files):
            if not filename.endswith(".ipynb"):
                continue
            if filename in SKIP_FILES:
                continue
            filepath = os.path.join(root, filename)
            week_match = re.search(r"Week_(\d+)_", filepath)
            week_num = int(week_match.group(1)) if week_match else None
            if single_week is not None and week_num != single_week:
                continue
            if not include_api_weeks and week_num in API_KEY_WEEKS:
                continue
            notebooks.append(filepath)
    return notebooks


def check_example_outputs(nb_copy):
    """
    After execution, check that each EXAMPLE code cell produced non-empty output.
    Returns list of warning strings.
    An EXAMPLE cell is a code cell that immediately follows a markdown cell
    whose source contains the word EXAMPLE.
    """
    warnings = []
    prev_is_example_markdown = False

    for cell in nb_copy.cells:
        if cell.cell_type == "markdown":
            src = "".join(cell.get("source", []))
            prev_is_example_markdown = "EXAMPLE" in src
        elif cell.cell_type == "code":
            if prev_is_example_markdown:
                src = "".join(cell.get("source", []))
                # Only check cells with a top-level print() or display() call.
                # Cells that define classes/functions with print() in method bodies
                # are intentionally silent until the student calls them.
                if src.strip() and _TOP_LEVEL_PRINT.search(src):
                    outputs = cell.get("outputs", [])
                    has_visible = any(
                        o.get("output_type") in ("stream", "execute_result", "display_data")
                        for o in outputs
                    )
                    if not has_visible:
                        first_line = src.strip().split("\n")[0][:70]
                        warnings.append(f"EXAMPLE cell has print() but produced no output: {first_line}")
            prev_is_example_markdown = False
    return warnings


def run_notebook(filepath):
    """
    Execute a notebook in-memory (no changes saved to disk).
    Injects a __file__ definition so notebooks behave like .py scripts.
    Returns (success, error_list, warning_list).
    """
    try:
        import nbformat
        from nbconvert.preprocessors import ExecutePreprocessor, CellExecutionError
    except ImportError:
        return None, ["nbformat/nbconvert not installed — run: pip install nbformat nbconvert"], []

    try:
        with open(filepath, encoding="utf-8") as f:
            nb = nbformat.read(f, as_version=4)
    except Exception as e:
        return False, [f"Could not read notebook: {e}"], []

    # Inject __file__ workaround as the very first cell.
    # This makes os.path.dirname(__file__) work correctly in all lesson notebooks.
    notebook_dir = os.path.dirname(os.path.abspath(filepath))
    injection_source = (
        f"import os\n"
        f"__file__ = {repr(filepath)}\n"
        f"# injected by verify_execution.py — not part of the lesson"
    )
    nb_copy = copy.deepcopy(nb)
    nb_copy.cells.insert(0, nbformat.v4.new_code_cell(source=injection_source))

    ep = ExecutePreprocessor(timeout=60, kernel_name="python3")

    try:
        ep.preprocess(nb_copy, {"metadata": {"path": notebook_dir}})
        return True, [], check_example_outputs(nb_copy)
    except CellExecutionError as e:
        return False, [f"  {e.ename}: {e.evalue}"], []
    except Exception as e:
        return False, [f"  {type(e).__name__}: {e}"], []


def run_qa(include_api_weeks=False, single_week=None):
    notebooks = collect_notebooks(include_api_weeks, single_week)

    if not notebooks:
        print("No notebooks matched the filter.")
        return

    results = {}
    for filepath in notebooks:
        rel = os.path.relpath(filepath, CURRICULUM_DIR)
        print(f"  Running {rel} ...", end="", flush=True)
        success, errors, warnings = run_notebook(filepath)
        results[rel] = (success, errors, warnings)
        if success is None:
            print(" SKIP")
        elif success:
            print(" PASS" if not warnings else f" PASS ({len(warnings)} warn)")
        else:
            print(" FAIL")

    total = len(results)
    passing = sum(1 for s, _, _w in results.values() if s is True)
    failing = sum(1 for s, _, _w in results.values() if s is False)
    skipped = sum(1 for s, _, _w in results.values() if s is None)
    total_warnings = sum(len(w) for _, _, w in results.values())

    print()
    print("=" * 64)
    print("  EXECUTION QA REPORT")
    print(f"  Notebooks run : {total}")
    print(f"  Passing       : {passing}")
    print(f"  Failing       : {failing}")
    if total_warnings:
        print(f"  Warnings      : {total_warnings} (EXAMPLE cells with no output)")
    if skipped:
        print(f"  Skipped       : {skipped} (missing nbformat/nbconvert)")
    if not include_api_weeks and single_week is None:
        print("  W10-W12 skipped (need API keys) -- use --all to include")
    print("=" * 64)
    print()

    current_week = None
    for rel_path, (success, errors, warnings) in results.items():
        week_folder = rel_path.split(os.sep)[0] if os.sep in rel_path else ""
        if week_folder != current_week:
            current_week = week_folder
            print(f"  {week_folder}")
            print(f"  {'─' * 50}")
        status = "PASS" if success else ("SKIP" if success is None else "FAIL")
        print(f"    {status}  {os.path.basename(rel_path)}")
        for err in errors:
            for line in err.strip().splitlines()[:5]:
                print(f"          {line}")
        for w in warnings:
            print(f"          WARN: {w}")

    print()
    print("=" * 64)
    if failing == 0 and total_warnings == 0:
        print("  All notebooks executed without errors. All EXAMPLE cells produce output.")
    elif failing == 0:
        print(f"  All notebooks executed without errors. {total_warnings} EXAMPLE cell(s) produce no output — see WARN above.")
    else:
        print(f"  {failing} notebook(s) failed. See errors above.")
    print("=" * 64)
    print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Execute all lesson notebooks and report cell errors."
    )
    parser.add_argument(
        "--all", action="store_true",
        help="Include W10-W12 (require API keys)"
    )
    parser.add_argument(
        "--week", type=int, metavar="N",
        help="Only run a single week (e.g. --week 3)"
    )
    args = parser.parse_args()
    run_qa(include_api_weeks=args.all, single_week=args.week)
