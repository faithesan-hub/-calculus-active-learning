# Your verification checklist

*Plain-language version: before anything goes public under your name, you check it. Total time: about 1 to 2 hours. Tick each box and add the date. *

*The publish gate (`scripts/publish_gate.py`) checks the mechanical items automatically. These are yours.*

## Part 1: Make sure the results can be rebuilt (15 to 30 min)

Pick one:
- [ ] **Option A, run it yourself.** In a terminal in the project folder, paste:
  `pip install -r requirements.txt && bash run_all.sh --final`
  The screen should end with `wrote README.md, ...`.
- [ ] **Option B, ask Claude.** In a new chat with Opus 5.5 or Fable 5, upload the project folder and say: "Re-run this pipeline from scratch and give me the headline numbers." They should match these:
  - Learning score: active 63.5, lecture 47.7, effect +15.8 points
  - Pass rate: active 80.3%, lecture 68.5%, effect +11.7 points
  - Lee lower bound: +11.7 points

Then:
- [ ] Open `data/processed/qa_report.txt`. Every line says PASS except the one FLAG about 376 vs 373, which is explained there.
- [ ] Spot-check five numbers in `paper/manuscript.pdf` against `paper/stats.json` (search the file for the number). For example, the abstract's "15.8 points" is `lm.fe.est` = 15.8118.

## Part 2: Check the sources (15 min)

- [ ] Open https://zenodo.org/records/8306160. It loads, the files are free, and the license says CC0 1.0.
- [ ] Open https://doi.org/10.1126/science.ade9803 (the original paper). Confirm the title and authors match our reference list. If you can read the paper (try https://par.nsf.gov and search "Kramer calculus randomized"), note whether its reported effect sizes are close to ours (g = 0.77). Small differences are expected because methods differ.
- [ ] Click every DOI in the paper's reference list. Each should open the correct article. Tick here when all ten work: ___

## Part 3: Check rows by hand (20 to 30 min)

Open both files in Excel or Google Sheets. The `Row` column in the original and the `row` column in the cleaned file are the same student.

**Five named spot checks:**
- [ ] Row 1: in `data/raw/kramer2023/anonymizedarchive.csv` Treatment = CN, Grade = DR, LearningMeasure = blank. In `data/processed/students.csv` the same row shows arm = Lecture and pass_c_or_better = 0. ___
- [ ] Row 2: in `data/raw/kramer2023/anonymizedarchive.csv` Treatment = TR, Grade = A, LearningMeasure = 83.75. In `data/processed/students.csv` the same row shows arm = Active (MPC) and pass_c_or_better = 1. ___
- [ ] Row 3: in `data/raw/kramer2023/anonymizedarchive.csv` Treatment = TR, Grade = blank, LearningMeasure = blank. In `data/processed/students.csv` the same row shows arm = Active (MPC) and pass_c_or_better = blank. ___
- [ ] Row 500: in `data/raw/kramer2023/anonymizedarchive.csv` Treatment = CN, Grade = A, LearningMeasure = 60.5. In `data/processed/students.csv` the same row shows arm = Lecture and pass_c_or_better = 1. ___
- [ ] Row 1019: in `data/raw/kramer2023/anonymizedarchive.csv` Treatment = TR, Grade = D, LearningMeasure = 33.5. In `data/processed/students.csv` the same row shows arm = Active (MPC) and pass_c_or_better = 0. ___

**The two extreme learning scores:**
- [ ] Row 920: in `data/raw/kramer2023/anonymizedarchive.csv` Treatment = TR, Grade = A, LearningMeasure = 98.5. In `data/processed/students.csv` the same row shows arm = Active (MPC) and pass_c_or_better = 1. ___
- [ ] Row 326: in `data/raw/kramer2023/anonymizedarchive.csv` Treatment = CN, Grade = D, LearningMeasure = 4.25. In `data/processed/students.csv` the same row shows arm = Lecture and pass_c_or_better = 0. ___

**Five random rows (chosen by computer, seed 2026):**
- [ ] Row 339: in `data/raw/kramer2023/anonymizedarchive.csv` Treatment = CN, Grade = D, LearningMeasure = blank. In `data/processed/students.csv` the same row shows arm = Lecture and pass_c_or_better = 0. ___
- [ ] Row 423: in `data/raw/kramer2023/anonymizedarchive.csv` Treatment = TR, Grade = blank, LearningMeasure = 41. In `data/processed/students.csv` the same row shows arm = Active (MPC) and pass_c_or_better = blank. ___
- [ ] Row 441: in `data/raw/kramer2023/anonymizedarchive.csv` Treatment = TR, Grade = A, LearningMeasure = 86. In `data/processed/students.csv` the same row shows arm = Active (MPC) and pass_c_or_better = 1. ___
- [ ] Row 938: in `data/raw/kramer2023/anonymizedarchive.csv` Treatment = TR, Grade = blank, LearningMeasure = blank. In `data/processed/students.csv` the same row shows arm = Active (MPC) and pass_c_or_better = blank. ___
- [ ] Row 949: in `data/raw/kramer2023/anonymizedarchive.csv` Treatment = CN, Grade = A, LearningMeasure = 80. In `data/processed/students.csv` the same row shows arm = Lecture and pass_c_or_better = 1. ___

## Part 4: Your decisions (10 min)

The build made these choices provisionally. Agree or change each one.
- [ ] **Who counts in the main analysis?** A: students who stayed in their assigned section (811), because students who switched have no grades in the file. B: all 1,019 allocated students, counting anyone without a grade as not passing; this would understate both groups and mix in switching. Recommended: A. Your choice: ___
- [ ] **Do withdrawals count as not passing?** A: yes, a withdrawal (DR) or other no-credit outcome (OF) counts as D/F/W. B: leave them out, which raises both pass rates. Recommended: A, the standard DFW definition. Your choice: ___
- [ ] **Title.** Current: "Active Learning in First-Semester Calculus: An Open Re-analysis of a Randomized Trial at a Hispanic-Serving Institution." Keep, or suggest your own: ___
- [ ] **Your 2016 project.** The introduction says this work continues your undergraduate research on cooperative and active learning in calculus, begun in 2016, and uses no data from it. Correct? ___

## Part 5: Before it goes public (15 to 30 min)

- [ ] The README summary and the paper abstract are rewritten in your own words. Nothing remains that you could not explain or defend. (Claude can do this with you line by line.)
- [ ] Your name, ORCID, affiliation, and email are correct in `AUTHORS.json`: Faith Oluwafunmitan Esan, 0009-0001-3694-157X, Independent Researcher, Laramie, Wyoming, USA, faithesan14@gmail.com.
- [ ] You confirm the competing-interests statement (none).
- [ ] You have read `docs/LIMITATIONS.md` and agree with it.
- [ ] Draft stamps removed (Claude rebuilds with `--final`) and `publish_gate.py` passes.
- [ ] Evidence log row written on release day.

**When every box is ticked, reply to Claude in your own words that you have checked the package and approve publishing.**
