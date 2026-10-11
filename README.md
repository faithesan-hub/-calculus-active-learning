# Active Learning in First-Semester Calculus: An Open Re-analysis

**Status:** Released · version 0.1.0 · Faith Oluwafunmitan Esan (Independent Researcher, Laramie, Wyoming, USA) · ORCID [0009-0001-3694-157X](https://orcid.org/0009-0001-3694-157X)

## In plain language

College calculus decides who stays in science and engineering. This project re-checks, in the open, one of the strongest experiments on how to teach it. In a randomized trial of 1,019 students at a large Hispanic-Serving university, students placed in active-learning sections (working problems in class, in small groups) scored **15.8 points higher** on a common 0 to 100 end-of-term test and **passed with a C or better more often (80.3% vs 68.5%)** than students in lecture sections. The benefit held under a worst-case treatment of missing test scores and was similar for women and men, Hispanic and Black students, first-time and transfer students, and students with weaker and stronger preparation. Everything here, data and code, can be rerun by anyone.

New to this project? Start with [docs/START_HERE.md](docs/START_HERE.md). Unfamiliar words are in [docs/GLOSSARY.md](docs/GLOSSARY.md).

## Headline results

| Outcome | Active learning | Lecture | Effect [95% CI] |
|---|---|---|---|
| End-of-term learning score (0 to 100) | 63.5 | 47.7 | +15.8 points [11.8, 19.8]; Hedges' g = 0.77 |
| Worst-case bound for missing scores | | | at least +11.7 points |
| Passed with C or better | 80.3% | 68.5% | +11.7 percentage points [6.4, 17.1] |
| D, F, or withdrawal | 19.7% | 31.5% | 37.5% fewer |
| Time slots where active section scored higher | | | 14 of 16 |

Students who stayed in their randomly assigned section (n = 811). Effects use time-slot fixed effects with standard errors clustered by section. Details: [paper/manuscript.pdf](paper/manuscript.pdf).

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

Maintainer: Faith Oluwafunmitan Esan, faithesan14@gmail.com
