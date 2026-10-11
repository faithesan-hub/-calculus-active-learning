"""Step 6: write the documents that quote numbers (README, limitations, checklist, talk track).

Plain-language note: like the paper, these documents take every number from
paper/stats.json, so they always agree with the data. Run with --final after you
have checked the work to remove the DRAFT markers. You do not need this file.
"""
import json
import pathlib
import sys

import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parents[1]
S = json.loads((ROOT / "paper" / "stats.json").read_text())
Q = json.loads((ROOT / "data" / "processed" / "qa.json").read_text())
A = json.loads((ROOT / "AUTHORS.json").read_text())["authors"][0]
D = pd.read_csv(ROOT / "data" / "processed" / "students.csv")
FINAL = "--final" in sys.argv
fl, lm, ps = S["flow"], S["lm"], S["pass"]
f1 = lambda x: f"{x:.1f}"
pc = lambda x: f"{100 * x:.1f}%"
pp = lambda x: f"{100 * x:.1f}"
status = "Released" if FINAL else "DRAFT, awaiting author verification"
REPO = f"https://github.com/{A['github']}/calculus-active-learning"
sub = {r["group"]: r for r in S["subgroups"]}

# ---------------------------------------------------------------- README
readme = f"""# Active Learning in First-Semester Calculus: An Open Re-analysis

**Status:** {status} · version 0.1.0 · {A['name']} ({A['affiliation']}) · ORCID [{A['orcid']}](https://orcid.org/{A['orcid']})

## In plain language

{"" if FINAL else "[VERIFY: rewrite this summary in your own words.] "}College calculus decides who stays in science and engineering. This project re-checks, in the open, one of the strongest experiments on how to teach it. In a randomized trial of {fl['randomized']:,} students at a large Hispanic-Serving university, students placed in active-learning sections (working problems in class, in small groups) scored **{f1(lm['fe']['est'])} points higher** on a common 0 to 100 end-of-term test and **passed with a C or better more often ({pc(ps['rate_active'])} vs {pc(ps['rate_lecture'])})** than students in lecture sections. The benefit held under a worst-case treatment of missing test scores and was similar for women and men, Hispanic and Black students, first-time and transfer students, and students with weaker and stronger preparation. Everything here, data and code, can be rerun by anyone.

New to this project? Start with [docs/START_HERE.md](docs/START_HERE.md). Unfamiliar words are in [docs/GLOSSARY.md](docs/GLOSSARY.md).

## Headline results

| Outcome | Active learning | Lecture | Effect [95% CI] |
|---|---|---|---|
| End-of-term learning score (0 to 100) | {f1(lm['mean_active'])} | {f1(lm['mean_lecture'])} | +{f1(lm['fe']['est'])} points [{f1(lm['fe']['lo'])}, {f1(lm['fe']['hi'])}]; Hedges' g = {lm['g']['g']:.2f} |
| Worst-case bound for missing scores | | | at least +{f1(lm['lee']['lower'])} points |
| Passed with C or better | {pc(ps['rate_active'])} | {pc(ps['rate_lecture'])} | +{pp(ps['fe']['est'])} percentage points [{pp(ps['fe']['lo'])}, {pp(ps['fe']['hi'])}] |
| D, F, or withdrawal | {pc(ps['dfw_active'])} | {pc(ps['dfw_lecture'])} | {pc(ps['relative_dfw_reduction'])} fewer |
| Time slots where active section scored higher | | | {lm['pairs']['pairs_favoring_active']} of {lm['pairs']['pairs']} |

Students who stayed in their randomly assigned section (n = {fl['stayers']}). Effects use time-slot fixed effects with standard errors clustered by section. Details: [paper/manuscript.pdf](paper/manuscript.pdf).

## How to rerun it

You need Python 3.10 or newer and a LaTeX installation with `pdflatex` (TeX Live or MiKTeX).

```bash
pip install -r requirements.txt
bash run_all.sh --final
```

The last lines should show `figures written` and `wrote paper/manuscript.pdf`, and `paper/stats.json` should match the committed copy. If the original data files are missing, `code/01_fetch.py` downloads them from Zenodo and checks their fingerprints.

| Step | Script | What it does |
|---|---|---|
| 1 | `code/01_fetch.py` | Gets the original data and confirms it is unchanged (SHA-256) |
| 2 | `code/02_build.py` | Cleans the data, writes `data/processed/students.csv` and `qa_report.txt` |
| 3 | `code/03_analysis.py` | Runs every analysis, writes `paper/stats.json` |
| 4 | `code/04_figures.py` | Draws the three figures from `stats.json` |
| 5 | `code/05_manuscript.py` | Writes `paper/numbers.tex` and tables from `stats.json`, then compiles `paper/manuscript.tex` to PDF |
| 6 | `code/06_docs.py` | Builds this README and other documents from `stats.json` |

## Source data

Kramer, L., Fuller, E., Watson, C., Castillo, A., Duran Oliva, P., & Potvin, G. (2023). *Establishing a new standard of care for calculus using trials with randomized student allocation* [Dataset]. Dryad/Zenodo. https://doi.org/10.5061/dryad.kkwh70s95. Released under CC0 1.0; the data README asks that it be used for research purposes. Accessed 2026-10-10; fingerprints in `data/raw/PROVENANCE.txt`. The original study: Kramer et al. (2023), *Science*, https://doi.org/10.1126/science.ade9803.

## Limitations

See [docs/LIMITATIONS.md](docs/LIMITATIONS.md). The most important: this is one trial at one institution, and each instructor taught only one style.

## License and citation

Code: MIT ([LICENSE](LICENSE)). Derived data, figures, and text: CC BY 4.0. Please cite using [CITATION.cff](CITATION.cff).

Maintainer: {A['name']}, {A['email']}
"""
(ROOT / "README.md").write_text(readme)

# ---------------------------------------------------------------- LIMITATIONS
lim = f"""# Limitations

*Plain-language note: every study has limits. These are this project's, stated plainly so that no one, including you, claims more than the data support. The paper's limitations section is written from this list. {"" if FINAL else "Status: DRAFT."}*

1. **One trial, one institution.** All {fl['randomized']:,} students attended one large Hispanic-Serving university over three semesters. Results may differ elsewhere. This project does not yet measure national effects; that is version 2 (see NEXT_STEPS.md).
2. **Instructors are tied to teaching style.** {fl['instructors_active']} instructors taught only active sections and {fl['instructors_lecture']} taught only lecture sections. Some of the measured difference could reflect who taught rather than how. Clustering by section widens the uncertainty to reflect this but cannot remove it.
3. **Unequal missing test scores.** {pc(1 - lm['lee']['observed_share_lecture'])} of lecture students and {pc(1 - lm['lee']['observed_share_active'])} of active-learning students who stayed have no end-of-term score. Lee bounds show the gain is at least {f1(lm['lee']['lower'])} points under the least favorable assumption, but those bounds assume active learning did not cause any student to skip the test who otherwise would have taken it.
4. **Grades are not blind.** Course grades were assigned by instructors who knew which style they taught. The common learning measure is more standardized than grades.
5. **Students who switched sections have no outcomes.** {fl['randomized'] - fl['stayers']} allocated students did not remain in their assigned section. Results describe students who stayed. Stay rates were similar in both groups ({pc(fl['stay_rate_active'])} and {pc(fl['stay_rate_lecture'])}).
6. **Subgroup results are exploratory.** Some groups are small (for example, {sub['Black or African American']['n']} Black or African American students), and many comparisons were made. No group showed a reliably different effect.
7. **Small count discrepancy.** The data README reports 373 active-learning students with a learning score; the file contains {fl['lm_n_active']}. All analyses use the file as released.
8. **Reuse terms.** The Zenodo record is CC0, but the data README says the data "may be used for research purposes only." This project is research and honors that request.
"""
(ROOT / "docs" / "LIMITATIONS.md").write_text(lim)

# ---------------------------------------------------------------- VERIFY CHECKLIST
lmrows = D[D.stayed == 1].dropna(subset=["learning_measure"])
hi = lmrows.loc[lmrows.learning_measure.idxmax()]
lo = lmrows.loc[lmrows.learning_measure.idxmin()]
rnd = D.sample(5, random_state=2026).sort_values("row")
RAWF = "data/raw/kramer2023/anonymizedarchive.csv"


def rowline(r):
    g = "blank" if pd.isna(r.grade) else r.grade
    m = "blank" if pd.isna(r.learning_measure) else f"{r.learning_measure:g}"
    p = "blank" if pd.isna(r.pass_c_or_better) else int(r.pass_c_or_better)
    return (f"- [ ] Row {int(r.row)}: in `{RAWF}` Treatment = {'TR' if r.active else 'CN'}, Grade = {g}, "
            f"LearningMeasure = {m}. In `data/processed/students.csv` the same row shows arm = {r.arm} and "
            f"pass_c_or_better = {p}. ___")


spot = "\n".join(rowline(D[D.row == s["row"]].iloc[0]) for s in Q["spot_checks"])
ext = "\n".join(rowline(r) for r in [hi, lo])
rand = "\n".join(rowline(r) for _, r in rnd.iterrows())
check = f"""# Your verification checklist

*Plain-language version: before anything goes public under your name, you check it. Total time: about 1 to 2 hours. Tick each box and add the date. {"" if FINAL else "Status: DRAFT."}*

*The publish gate (`scripts/publish_gate.py`) checks the mechanical items automatically. These are yours.*

## Part 1: Make sure the results can be rebuilt (15 to 30 min)

Pick one:
- [ ] **Option A, run it yourself.** In a terminal in the project folder, paste:
  `pip install -r requirements.txt && bash run_all.sh --final`
  The screen should end with `wrote README.md, ...`.
- [ ] **Option B, ask Claude.** In a new chat with Opus 5.5 or Fable 5, upload the project folder and say: "Re-run this pipeline from scratch and give me the headline numbers." They should match these:
  - Learning score: active {f1(lm['mean_active'])}, lecture {f1(lm['mean_lecture'])}, effect +{f1(lm['fe']['est'])} points
  - Pass rate: active {pc(ps['rate_active'])}, lecture {pc(ps['rate_lecture'])}, effect +{pp(ps['fe']['est'])} points
  - Lee lower bound: +{f1(lm['lee']['lower'])} points

Then:
- [ ] Open `data/processed/qa_report.txt`. Every line says PASS except the one FLAG about 376 vs 373, which is explained there.
- [ ] Spot-check five numbers in `paper/manuscript.pdf` against `paper/stats.json` (search the file for the number). For example, the abstract's "{f1(lm['fe']['est'])} points" is `lm.fe.est` = {lm['fe']['est']:.4f}.

## Part 2: Check the sources (15 min)

- [ ] Open https://zenodo.org/records/8306160. It loads, the files are free, and the license says CC0 1.0.
- [ ] Open https://doi.org/10.1126/science.ade9803 (the original paper). Confirm the title and authors match our reference list. If you can read the paper (try https://par.nsf.gov and search "Kramer calculus randomized"), note whether its reported effect sizes are close to ours (g = {lm['g']['g']:.2f}). Small differences are expected because methods differ.
- [ ] Click every DOI in the paper's reference list. Each should open the correct article. Tick here when all ten work: ___

## Part 3: Check rows by hand (20 to 30 min)

Open both files in Excel or Google Sheets. The `Row` column in the original and the `row` column in the cleaned file are the same student.

**Five named spot checks:**
{spot}

**The two extreme learning scores:**
{ext}

**Five random rows (chosen by computer, seed 2026):**
{rand}

## Part 4: Your decisions (10 min)

The build made these choices provisionally. Agree or change each one.
- [ ] **Who counts in the main analysis?** A: students who stayed in their assigned section ({fl['stayers']}), because students who switched have no grades in the file. B: all {fl['randomized']:,} allocated students, counting anyone without a grade as not passing; this would understate both groups and mix in switching. Recommended: A. Your choice: ___
- [ ] **Do withdrawals count as not passing?** A: yes, a withdrawal (DR) or other no-credit outcome (OF) counts as D/F/W. B: leave them out, which raises both pass rates. Recommended: A, the standard DFW definition. Your choice: ___
- [ ] **Title.** Current: "Active Learning in First-Semester Calculus: An Open Re-analysis of a Randomized Trial at a Hispanic-Serving Institution." Keep, or suggest your own: ___
- [ ] **Your 2016 project.** The introduction says this work continues your undergraduate research on cooperative and active learning in calculus, begun in 2016, and uses no data from it. Correct? ___

## Part 5: Before it goes public (15 to 30 min)

- [ ] The README summary and the paper abstract are rewritten in your own words. Nothing remains that you could not explain or defend. (Claude can do this with you line by line.)
- [ ] Your name, ORCID, affiliation, and email are correct in `AUTHORS.json`: {A['name']}, {A['orcid']}, {A['affiliation']}, {A['email']}.
- [ ] You confirm the competing-interests statement (none).
- [ ] You have read `docs/LIMITATIONS.md` and agree with it.
- [ ] Draft stamps removed (Claude rebuilds with `--final`) and `publish_gate.py` passes.
- [ ] Evidence log row written on release day.

**When every box is ticked, reply to Claude in your own words that you have checked the package and approve publishing.**
"""
(ROOT / "docs" / "VERIFY_CHECKLIST.md").write_text(check)

# ---------------------------------------------------------------- TALK TRACK
talk = f"""# Talking about this project
{"" if FINAL else chr(10) + "*DRAFT: numbers become final after your verification.*" + chr(10)}
## 60-second version

**The problem:** First-semester calculus is where many students leave science and engineering. Departments are told to switch to active learning, but most of the evidence comes from studies whose data nobody else can check.

**What I did:** I took the largest openly shared randomized experiment on calculus teaching, {fl['randomized']:,} students at a Hispanic-Serving university, and re-analyzed it independently with my own code, which is public.

**What it shows:** Students randomly placed in active-learning sections scored about {round(lm['fe']['est'])} points higher out of 100 on a common final assessment, and {pc(ps['rate_active'])} passed with a C or better compared with {pc(ps['rate_lecture'])} in lecture. That is about {round(100 * ps['fe']['est'])} more passing students per hundred. The result holds even under worst-case assumptions about missing test scores, and the benefit was similar across gender, ethnicity, and preparation levels.

**Who can use it:** Math departments deciding how to teach calculus, researchers who want to check or extend the analysis, and institutions that want to run the same code on their own course records.

**Where it is:** {REPO}, archived with a permanent DOI on Zenodo (listed in the README), with the paper posted as a preprint on EdArXiv.

## Two-sentence version

{A['name']} re-analyzed the largest open randomized trial of calculus teaching and found that active learning raised pass rates from {pc(ps['rate_lecture'])} to {pc(ps['rate_active'])} and end-of-term scores by about {round(lm['fe']['est'])} points, with similar benefits across student groups. All data and code are public so anyone can reproduce and extend the work.

## Questions you may be asked

1. **Where does the data come from?** From Kramer and colleagues at Florida International University, who ran the trial and shared the anonymized data publicly in 2023. I did not collect it; I re-analyzed it independently and added new checks.
2. **What are its limits?** It is one university, and each instructor taught only one style, so part of the difference could be the instructors. Grades were not blind. I state these openly in the paper.
3. **Why does this matter for the United States?** The country needs more STEM graduates, and calculus is a major point where students drop out, especially at Hispanic-Serving Institutions, which enroll a large share of Hispanic undergraduates. Open, checkable evidence helps departments make changes with confidence.
"""
(ROOT / "docs" / "TALK_TRACK.md").write_text(talk)
print("wrote README.md, docs/LIMITATIONS.md, docs/VERIFY_CHECKLIST.md, docs/TALK_TRACK.md")
