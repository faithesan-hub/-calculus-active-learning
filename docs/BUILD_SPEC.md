# Build spec

*Plain-language note: this one-page plan is what the build followed. You only need it if you want to see the decisions in one place.*

```
PROJECT:        Open re-analysis of active learning in first-semester calculus (analysis paper + replication package)
QUESTION:       Do students randomly placed in active-learning calculus sections learn more and pass more often than students in lecture sections, and for whom?
SOURCES:        Kramer et al. (2023) trial data, Dryad/Zenodo doi:10.5061/dryad.kkwh70s95, CC0 1.0, v1 (2023-08-31), accessed 2026-10-10
UNIT:           Student (1,019 allocated; 811 remained in assigned section)
MEASURES:       Learning measure (0-100); pass = C or better; DFW = D, F, withdrawal, other no-credit
METHODS:        OLS with time-slot fixed effects, section-clustered SEs (CR1); section-pair paired and exact sign-flip tests; Hedges' g; Lee bounds; exploratory subgroup interactions
OUTPUTS:        data/processed/students.csv, qa_report.txt, paper/stats.json, 3 figures, paper/manuscript.tex and manuscript.pdf (two-column journal layout), README, docs
VENUES:         GitHub + Zenodo DOI; EdArXiv preprint; then a mathematics-education journal (e.g., International Journal of Research in Undergraduate Mathematics Education)
VERIFY POINTS:  analytic sample; DFW definition; title; 2016 background sentence; abstract and README in author's words
LICENSE:        Code MIT; derived data and text CC BY 4.0
ASSUMPTIONS:    Pass rate is headline; subgroups included as exploratory; 2016 undergraduate project is background only (no data)
```
