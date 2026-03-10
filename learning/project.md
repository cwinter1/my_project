# project.md — Python-GStat Curriculum Status

Last updated: 2026-03-09

---

## Installation

A `requirements.txt` file is included in the root of the repo.

**Install all packages:**
```bash
pip install -r requirements.txt
```

**Install core only (for G-Lesson notebooks 1-8):**
```bash
pip install numpy pandas matplotlib seaborn openpyxl
```

| Group | Packages |
|-------|----------|
| Core | numpy, pandas, matplotlib, seaborn, openpyxl |
| Machine Learning | scikit-learn, joblib, mlflow |
| Database | sqlalchemy, pyodbc |
| Data Engineering | requests, boto3, pyspark, apache-airflow, pytest, pydantic |
| Web Scraping | selenium, webdriver-manager |

---

## Project Goal

Merge two curricula into one clean 12-week course:
- **python-gstat**: G-Stat notebooks (gstat visual style, beginner-friendly)
- **py_learn**: 40-day course (good topic breadth but unclear structure)

Output: `Curriculum/` folder — clean `.py` files for VS Code, gstat style,
interleaved concept → example → exercise structure.

---

## QA Tool

```bash
cd C:\Users\crist\Documents\GitHub\python-gstat\Curriculum
python verify_curriculum.py
```

Run this to get a PASS/FAIL report for every file. Fix all FAILs before considering a week complete.

**Last run result: 24/68 passing** (run again after current agents finish — expect 55+)

---

## File Status by Week

### COMPLETE and PASSING QA
| File | Status |
|------|--------|
| W1_D1 through W1_D5 | PASS |
| W1_D6 Project | PASS |
| W2_D1, W2_D2 | PASS |
| W2_D3 Error Handling | PASS |
| W2_D6 Classes/OOP | PASS |
| W2_D7 Project | PASS |
| W3_D6 Project | PASS |
| W4_D6 Project | PASS |
| W5_D1 Matplotlib | PASS |
| W5_D6 Project | PASS |
| W6_D6 Project | PASS |
| W7_D6 Project | PASS |
| W8_D6 Project | PASS |
| W8_D7 QA Verification lesson | PASS |
| W9_D1, W9_D2 | PASS |
| W9_D6 Project | PASS |
| W10_D6 Project | PASS |
| W12_D1 Docker/Kafka Setup | PASS |

---

### IN PROGRESS (agents running as of last check)

**Agent af52d42** — reformatting 32 files still in old `# ==` format:
- W2_D4, W2_D5
- W3_D1 through W3_D5
- W4_D1 through W4_D5
- W5_D5
- W6_D1 through W6_D5
- W7_D1 through W7_D5
- W8_D1 through W8_D5
- W9_D3, W9_D4, W9_D5
- W10_D1 through W10_D5
- W11_D1 through W11_D5

**Agent a59f3d9** — creating 5 missing files:
- `Week_11_Advanced_AI/W11_D6_Project_AI_Data_Assistant.py`
- `Week_12_Capstone/W12_D2_Extract_API_Producer.py`
- `Week_12_Capstone/W12_D3_Store_MinIO.py`
- `Week_12_Capstone/W12_D4_Transform_Load_PostgreSQL.py`
- `Week_12_Capstone/W12_D5_Pipeline_Final_Run.py`

---

### KNOWN ISSUES (fix after agents finish)

1. **W5_D2, W5_D3, W5_D4** — blank workspace check failing (only 3 blank lines, need 4).
   Fix: open each file, find the exercise areas, add one more blank line.

2. **W5_D1** — exercise area has code hints (lines 101-105 show np.arange example inside exercise).
   Fix: remove those code hint lines from inside the EXERCISE section.

3. **W12_OVERVIEW.py** — no exercises by design (it's a reference file). Already excluded from QA.

4. **W6_D5, W8_D2, W8_D5** — blank workspace missing (likely exercises have only 3 blank lines).
   Fix: same as W5 above — add blank lines.

---

### STILL MISSING (not yet created)

None known — all files either exist or are being created by current agents.
After agents finish, run `python verify_curriculum.py` to confirm.

---

## What To Do Next Session

### Step 1 — Check agent results
```bash
cd C:\Users\crist\Documents\GitHub\python-gstat\Curriculum
python verify_curriculum.py
```

### Step 2 — Fix blank workspace issues
Files that fail with "no blank workspace":
- Open the file in VS Code
- Find each EXERCISE/TASK section
- Make sure there are exactly 4-6 blank lines after the starting data variables
- Re-run verifier to confirm PASS

### Step 3 — Fix exercise code hints (W5_D1)
- Open `Week_5_Visualization/W5_D1_Matplotlib.py`
- Go to EXERCISE 1 (around line 94)
- Lines 101-105 contain code hints (`np.arange`, `plt.bar`, etc.) — DELETE these lines
- The exercise area should only have: instructions, expected output, starting data, then blank lines

### Step 4 — Update README.py
`Curriculum/README.py` was written before Week 12 was added. Update it to show:
- 12 weeks total
- Week 12 Capstone section with D1-D5 titles
- Career milestones: Junior DA (after W4), Junior DE (after W8), Junior AI Eng (after W11), Capstone (W12)

### Step 5 — Final QA target
Goal: **68/68 files passing** (or 67/68 if W12_OVERVIEW stays excluded).
Run `python verify_curriculum.py` and fix anything still showing FAIL.

---

## Curriculum Design Decisions (for reference)

| Decision | Choice | Reason |
|----------|--------|--------|
| File format | Interleaved concept→example→exercise | Student sees concept immediately followed by practice |
| Exercise area | Blank lines only, no code hints | Student must write from scratch, not uncomment |
| Starting data | Given as actual code above blank lines | Student knows what variables to use |
| Project files (D6/D7) | Use TASK not EXERCISE | Distinguishes project tasks from lesson exercises |
| Week 12 | SIMULATION + REAL MODE | Works without Docker, upgrades when services available |
| QA script | verify_curriculum.py | Permanent tool, run anytime, catches regressions |
| W8_D7 lesson | Automated QA / file verification | Turns the QA work itself into a learning lesson |

---

## Architecture of AI-Assisted Build (meta-notes)

This curriculum was built using Claude Code with:
- **Parallel background agents** for bulk file creation/reformatting
- **verify_curriculum.py** as the automated QA layer
- **Agent self-check** instructions: each agent re-reads files after writing and verifies format
- **Reviewer pattern**: after agents finish, main Claude runs QA and fixes failures

Lesson learned: agents often complete fewer files than assigned (context limits, turn limits).
Always verify file count with Glob after each agent completes.
