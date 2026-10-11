"""Step 2: clean the trial data and run quality checks.

Plain-language note: this script turns the original study's file into a tidy
table (one row per student, with clear yes/no columns such as "passed with C or
better"), then checks that our counts match what the original authors reported.
It writes data/processed/students.csv and data/processed/qa_report.txt.
Open qa_report.txt if you want to see the checks; you do not need this file.
"""
import json
import pathlib

import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "kramer2023" / "anonymizedarchive.csv"
OUT = ROOT / "data" / "processed"
OUT.mkdir(parents=True, exist_ok=True)

PASS = {"A", "A-", "B+", "B", "B-", "C+", "C"}
DFW = {"D", "F", "DR", "OF"}
# Spot-check rows (the "Row" column in the original file) for the author to verify by hand.
SPOT_ROWS = [1, 2, 3, 500, 1019]


def build():
    raw = pd.read_csv(RAW)
    d = pd.DataFrame({
        "row": raw["Row"],
        "study_id": raw["studyID"],
        "arm": raw["Treatment"].map({"TR": "Active (MPC)", "CN": "Lecture"}),
        "active": (raw["Treatment"] == "TR").astype(int),
        "trial_status": raw["TrialStatus"],
        "stayed": (raw["TrialStatus"] == "Completer").astype(int),
        "section": raw["Section"].astype("Int64"),
        "slot": raw["SecPair"].astype("Int64"),
        "teacher": raw["TIDw"],
        "grade": raw["Grade"],
        "learning_measure": raw["LearningMeasure"],
        "prior_prep": raw["MBS"],
        "female": raw["Gender"].map({"F": 1, "M": 0}).astype("Int64"),
        "hispanic": raw["REHispanic"],
        "black": raw["REBlack"],
        "first_time_college": raw["Cohort"].map({"FTiC": 1, "Transfer": 0, "No Cohort": 0}).astype("Int64"),
        "major_group": raw["MajorGrp"],
    })
    has_grade = d["grade"].notna()
    d["pass_c_or_better"] = np.where(has_grade, d["grade"].isin(PASS).astype(float), np.nan)
    d["dfw"] = np.where(has_grade, d["grade"].isin(DFW).astype(float), np.nan)
    terc = pd.qcut(d["prior_prep"], 3, labels=["Lower third", "Middle third", "Upper third"])
    d["prior_prep_group"] = terc.astype(object)
    return raw, d


def qa(raw, d):
    lines, checks = [], {}

    def chk(name, got, want, note=""):
        ok = got == want
        checks[name] = {"got": got, "expected": want, "ok": bool(ok), "note": note}
        lines.append(f"[{'PASS' if ok else 'FLAG'}] {name}: got {got}, expected {want}. {note}".rstrip())

    lines.append("QUALITY CHECK REPORT. Plain-language summary: each line compares a count in our "
                 "cleaned data with what the original authors reported. PASS means it matches. "
                 "FLAG means it differs and is explained.\n")
    n_arm = d.groupby("active").size()
    chk("Students randomized", len(d), 1019, "Original README: 1,019.")
    chk("Randomized to active learning", int(n_arm[1]), 516)
    chk("Randomized to lecture", int(n_arm[0]), 503)
    st = d[d.stayed == 1].groupby("active").size()
    chk("Active students still in assigned section at drop/add", int(st[1]), 417)
    chk("Lecture students still in assigned section at drop/add", int(st[0]), 394)
    lm = d[(d.stayed == 1) & d.learning_measure.notna()].groupby("active").size()
    chk("Active stayers with an end-of-term learning score", int(lm[1]), 373,
        "Original README says 373. The file has 376. The 3-student gap is small and is noted "
        "as an open question in docs/LIMITATIONS.md; all analyses use what is in the file.")
    chk("Lecture stayers with an end-of-term learning score", int(lm[0]), 310, "Original README: 310.")
    chk("Course sections", int(d.section.nunique()), 32)
    chk("Time slots (randomization blocks)", int(d.slot.nunique()), 16)
    per_slot = d.dropna(subset=["section"]).groupby("slot").apply(
        lambda g: (g[g.active == 1].section.nunique(), g[g.active == 0].section.nunique()))
    chk("Time slots with exactly one active and one lecture section",
        int(sum(v == (1, 1) for v in per_slot)), 16)
    chk("Instructors", int(d.teacher.nunique()), 19)
    overlap = set(d[d.active == 1].teacher.dropna()) & set(d[d.active == 0].teacher.dropna())
    chk("Instructors who taught in both arms", len(overlap), 0,
        "Each instructor taught only one style, so instructor and teaching style cannot be "
        "fully separated. Analyses account for this by clustering on section.")
    ungraded_stayers = int(d[(d.stayed == 1) & d.grade.isna()].shape[0])
    chk("Stayers with no course grade", ungraded_stayers, 0)
    lm_ok = d.learning_measure.dropna().between(0, 100).all()
    chk("Learning scores all within 0 to 100", bool(lm_ok), True)
    pp_ok = d.prior_prep.dropna().between(0, 100).all()
    chk("Prior-preparation scores all within 0 to 100", bool(pp_ok), True)

    lines.append("\nMissing end-of-term learning scores among stayers, by arm "
                 "(different rates matter; see LIMITATIONS):")
    s = d[d.stayed == 1]
    miss = s.groupby("arm").learning_measure.apply(lambda x: x.isna().mean())
    for k, v in miss.items():
        lines.append(f"  {k}: {v:.1%} missing")

    lines.append("\nSPOT CHECKS. Open data/raw/kramer2023/anonymizedarchive.csv and "
                 "data/processed/students.csv, find each Row, and compare:")
    spot = []
    for r in SPOT_ROWS:
        a = raw[raw.Row == r].iloc[0]
        b = d[d.row == r].iloc[0]
        rec = {"row": r, "raw_Treatment": a.Treatment, "raw_Grade": None if pd.isna(a.Grade) else a.Grade,
               "raw_LearningMeasure": None if pd.isna(a.LearningMeasure) else float(a.LearningMeasure),
               "clean_arm": b.arm,
               "clean_pass": None if pd.isna(b.pass_c_or_better) else int(b.pass_c_or_better)}
        spot.append(rec)
        lines.append(f"  Row {r}: Treatment={rec['raw_Treatment']} -> arm '{rec['clean_arm']}'; "
                     f"Grade={rec['raw_Grade']} -> pass_c_or_better={rec['clean_pass']}; "
                     f"LearningMeasure={rec['raw_LearningMeasure']}")
    (OUT / "qa_report.txt").write_text("\n".join(lines) + "\n")
    (OUT / "qa.json").write_text(json.dumps({"checks": checks, "spot_checks": spot,
                                             "missing_lm_by_arm": miss.round(4).to_dict()}, indent=2))
    print("\n".join(lines))


if __name__ == "__main__":
    raw, d = build()
    d.to_csv(OUT / "students.csv", index=False)
    qa(raw, d)
