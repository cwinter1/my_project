# ══════════════════════════════════════════════════════════════
#  CURRICULUM QA VERIFIER
#  Run this from the Curriculum/ folder:  python verify_curriculum.py
#
#  Checks every lesson file for:
#    1. ══ border format present
#    2. No input() calls
#    3. No emojis
#    4. At least 3 EXERCISE or TASK markers
#    5. At least 3 EXAMPLE or PART markers (non-project files only)
#    6. Blank workspace (4+ blank lines after an EXERCISE/TASK section)
#    7. Python syntax validity (ast.parse — .py files only)
#    8. ARCHITECTURE DECISION block present (W8-W12 files only)
# ══════════════════════════════════════════════════════════════

import os
import ast
import re
import sys
import json

# Force UTF-8 output on Windows so box-drawing characters print correctly
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

CURRICULUM_DIR = os.path.dirname(os.path.abspath(__file__))

SKIP_FILES = {
    "verify_curriculum.py", "verify_execution.py", "README.py", "W12_OVERVIEW.py",
    "convert_py_to_ipynb.py",
    "README.ipynb", "W12_OVERVIEW.ipynb", "qa.ipynb",
}

# Subfolders to skip entirely (not lesson content)
SKIP_DIRS = {"datasets", "__pycache__", "nl_sql_app", "tests"}

# Emoji range: U+1F000 and above (excludes box-drawing chars like ══ ─── │)
EMOJI_PATTERN = re.compile(r"[\U0001F000-\U0010FFFF]")


def extract_notebook_source(filepath):
    """
    Read a .ipynb file and return all cell sources concatenated as one string.
    Returns None on error.
    """
    try:
        with open(filepath, encoding="utf-8") as f:
            nb = json.load(f)
        parts = []
        for cell in nb.get("cells", []):
            src = cell.get("source", [])
            if isinstance(src, list):
                parts.append("".join(src))
            else:
                parts.append(src)
            parts.append("\n\n")
        return "".join(parts)
    except Exception as e:
        return None


def check_file(filepath):
    """
    Read a single lesson file (.py or .ipynb) and return a list of issues found.
    Empty list means the file passes all checks.
    """
    issues = []

    if filepath.endswith(".ipynb"):
        source = extract_notebook_source(filepath)
        if source is None:
            return [f"could not read notebook file"]
        # Skip Python syntax check for notebooks (cells may not be valid standalone)
        skip_syntax = True
    else:
        try:
            with open(filepath, encoding="utf-8") as f:
                source = f.read()
        except Exception as e:
            return [f"could not read file: {e}"]
        skip_syntax = False

    # 1. New ══ border format
    if "══" not in source:
        issues.append("missing ══ border — file may still use old == format")

    # 2. No input() — use word boundary so guard_input() etc. are not flagged
    if re.search(r"\binput\(", source):
        issues.append("contains input() — not allowed in lesson files")

    # 3. No emojis
    if EMOJI_PATTERN.search(source):
        issues.append("contains emoji characters — remove them")

    # 4. At least 3 EXERCISE or TASK markers (project files use TASK)
    exercise_count = source.count("EXERCISE") + source.count("TASK")
    if exercise_count < 3:
        issues.append(
            f"only {exercise_count} EXERCISE/TASK section(s) found — need at least 3"
        )

    # 5. At least 3 EXAMPLE or PART markers
    #    Skip this check for project/overview files — they use TASK sections only
    is_project_file = re.search(r"(_D6_|_D7_|OVERVIEW|_Project_|_project_)", filepath)
    if not is_project_file:
        example_count = source.count("EXAMPLE") + source.count("PART")
        if example_count < 3:
            issues.append(
                f"only {example_count} EXAMPLE/PART block(s) found — need at least 3"
            )

    # 6. Student workspace (4+ consecutive blank lines somewhere after an EXERCISE or TASK marker)
    #    Search window is 2000 chars (handles long exercise descriptions with starting data)
    exercise_positions = [m.start() for m in re.finditer(r"EXERCISE|TASK", source)]
    workspace_found = False
    for pos in exercise_positions:
        section_after = source[pos: pos + 2000]
        if re.search(r"\n{4,}", section_after):
            workspace_found = True
            break
    if not workspace_found and exercise_count >= 1:
        issues.append("no blank workspace (4+ blank lines) found after any EXERCISE/TASK section")

    # 7. Python syntax (only for .py files)
    if not skip_syntax:
        try:
            ast.parse(source)
        except SyntaxError as e:
            issues.append(f"SYNTAX ERROR line {e.lineno}: {e.msg}")

    # 8. ARCHITECTURE DECISION block present (W8-W12 files only)
    is_w8_to_w12 = re.search(r"Week_(8|9|10|11|12)_", filepath)
    if is_w8_to_w12 and "ARCHITECTURE DECISION" not in source:
        issues.append("missing ARCHITECTURE DECISION block in W8-W12 file header")

    return issues


def collect_lesson_files():
    """
    Walk the Curriculum directory and return sorted list of lesson file paths.
    Checks both .py and .ipynb files.
    Skips files listed in SKIP_FILES, verify_*.py files, and SKIP_DIRS folders.
    """
    lesson_files = []
    for root, dirs, files in os.walk(CURRICULUM_DIR):
        # Skip excluded subdirectories in-place so os.walk doesn't descend into them
        dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS)
        for filename in sorted(files):
            if not (filename.endswith(".py") or filename.endswith(".ipynb")):
                continue
            if filename in SKIP_FILES:
                continue
            if filename.startswith("verify_"):
                continue
            filepath = os.path.join(root, filename)
            lesson_files.append(filepath)
    return lesson_files


def run_qa():
    lesson_files = collect_lesson_files()
    results = {}

    for filepath in lesson_files:
        rel = os.path.relpath(filepath, CURRICULUM_DIR)
        results[rel] = check_file(filepath)

    total_files = len(results)
    total_issues = sum(len(v) for v in results.values())
    files_passing = sum(1 for v in results.values() if not v)
    files_failing = total_files - files_passing

    print()
    print("=" * 64)
    print("  CURRICULUM QA REPORT")
    print(f"  Files checked : {total_files}")
    print(f"  Passing       : {files_passing}")
    print(f"  Failing       : {files_failing}")
    print(f"  Total issues  : {total_issues}")
    print("=" * 64)
    print()

    current_week = None
    for rel_path, issues in results.items():
        week_folder = rel_path.split(os.sep)[0] if os.sep in rel_path else ""
        if week_folder != current_week:
            current_week = week_folder
            print(f"  {week_folder}")
            print(f"  {'─' * 50}")

        filename = os.path.basename(rel_path)
        status = "PASS" if not issues else "FAIL"
        print(f"    {status}  {filename}")
        for issue in issues:
            print(f"          - {issue}")

    print()
    print("=" * 64)
    if files_failing == 0:
        print("  All files pass. Curriculum QA clean.")
    else:
        print(f"  {files_failing} file(s) need attention. Fix issues above and re-run.")
    print("=" * 64)
    print()


if __name__ == "__main__":
    run_qa()
