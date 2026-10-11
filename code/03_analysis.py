"""Step 3: the analysis. Writes paper/stats.json, the single source of every number.

Plain-language note: this script compares students randomly placed in active-learning
calculus sections with students placed in lecture sections. It asks three questions:
(1) Did active-learning students score higher on the end-of-term learning test?
(2) Did more of them pass with a C or better?
(3) Was the benefit similar for different groups of students?
Every number that appears in the paper is written to paper/stats.json by this script,
so the paper and the data cannot disagree. You do not need to open this file.

Methods (technical):
- Unit of randomization: students, randomly allocated to one active (MPC) or one
  lecture section within each of 16 registration time slots ("slots").
- Primary estimates: OLS with slot fixed effects; cluster-robust (CR1) standard
  errors by section (32 clusters), t reference with G-1 = 31 df.
- Section-level check: 16 slot pairs, difference in section means, paired t-test and
  exact sign-flip randomization test (2^16 = 65,536 sign patterns).
- Effect size: Hedges' g with pooled SD among students with a learning score.
- Differential missingness: Lee (2009) trimming bounds on the learning measure.
- Subgroups: arm-by-subgroup interaction in the slot-fixed-effects model, clustered SEs.
  Subgroup results are exploratory.
"""
import itertools
import json
import pathlib

import numpy as np
import pandas as pd
from scipy import stats

ROOT = pathlib.Path(__file__).resolve().parents[1]
D = pd.read_csv(ROOT / "data" / "processed" / "students.csv")
OUT = ROOT / "paper"
OUT.mkdir(exist_ok=True)


def ols_cluster(y, X, cl):
    """OLS with CR1 cluster-robust covariance. Returns beta, se, df."""
    y, X = np.asarray(y, float), np.asarray(X, float)
    n, k = X.shape
    XtX_inv = np.linalg.pinv(X.T @ X)
    b = XtX_inv @ X.T @ y
    e = y - X @ b
    groups = pd.Series(cl).astype(str).values
    G = len(np.unique(groups))
    meat = np.zeros((k, k))
    for g in np.unique(groups):
        m = groups == g
        s = X[m].T @ e[m]
        meat += np.outer(s, s)
    c = (G / (G - 1)) * ((n - 1) / (n - k))
    V = c * XtX_inv @ meat @ XtX_inv
    return b, np.sqrt(np.diag(V)), G - 1


def design(df, extra=None, adjust=False):
    """Columns: active, [extra...], slot dummies (no intercept; slots absorb it)."""
    cols = [df["active"].astype(float)]
    names = ["active"]
    for e in extra or []:
        cols.append(df[e].astype(float)); names.append(e)
    if adjust:
        pp = df["prior_prep"]
        cols.append(pp.fillna(pp.mean()) - pp.mean()); names.append("prior_prep_c")
        cols.append(pp.isna().astype(float)); names.append("prior_prep_missing")
    slots = pd.get_dummies(df["slot"].astype(int), prefix="slot", dtype=float)
    X = pd.concat([pd.concat(cols, axis=1, keys=names), slots], axis=1)
    return X


def effect(df, y, adjust=False):
    sub = df[df[y].notna()].copy()
    X = design(sub, adjust=adjust)
    b, se, dof = ols_cluster(sub[y], X.values, sub["section"])
    t = b[0] / se[0]
    crit = stats.t.ppf(0.975, dof)
    return {"est": b[0], "se": se[0], "lo": b[0] - crit * se[0], "hi": b[0] + crit * se[0],
            "p": 2 * stats.t.sf(abs(t), dof), "n": len(sub), "clusters": dof + 1}


def interaction(df, y, g):
    sub = df[df[y].notna() & df[g].notna()].copy()
    sub["inter"] = sub["active"] * sub[g]
    X = design(sub, extra=[g, "inter"])
    b, se, dof = ols_cluster(sub[y], X.values, sub["section"])
    t = b[2] / se[2]
    return {"diff_in_effect": b[2], "se": se[2], "p": 2 * stats.t.sf(abs(t), dof), "n": len(sub)}


def hedges_g(a, b):
    a, b = np.asarray(a), np.asarray(b)
    na, nb = len(a), len(b)
    sp = np.sqrt(((na - 1) * a.var(ddof=1) + (nb - 1) * b.var(ddof=1)) / (na + nb - 2))
    d = (a.mean() - b.mean()) / sp
    J = 1 - 3 / (4 * (na + nb) - 9)
    g = J * d
    se = np.sqrt((na + nb) / (na * nb) + g ** 2 / (2 * (na + nb)))
    return {"g": g, "lo": g - 1.96 * se, "hi": g + 1.96 * se, "sd_pooled": sp}


def section_pairs(df, y):
    m = df[df[y].notna()].groupby(["slot", "active"])[y].mean().unstack()
    cnt = df[df[y].notna()].groupby(["slot", "active"])[y].size().unstack()
    diffs = (m[1] - m[0]).values
    t = stats.ttest_1samp(diffs, 0)
    obs = diffs.mean()
    flips = np.array(list(itertools.product([1, -1], repeat=len(diffs))))
    null = (flips * np.abs(diffs)).mean(axis=1)
    p_exact = np.mean(np.abs(null) >= abs(obs) - 1e-12)
    return {"mean_diff": obs, "pairs": len(diffs), "pairs_favoring_active": int((diffs > 0).sum()),
            "p_paired_t": t.pvalue, "p_exact": p_exact,
            "min_diff": diffs.min(), "max_diff": diffs.max(), "diffs": diffs.tolist(),
            "by_slot": [{"slot": int(k), "mean_active": float(m.loc[k, 1]), "mean_lecture": float(m.loc[k, 0]),
                         "n_active": int(cnt.loc[k, 1]), "n_lecture": int(cnt.loc[k, 0])} for k in m.index]}


def lee_bounds(df, y):
    """Lee (2009) bounds: trim the arm with more observed outcomes."""
    p = df.groupby("active")[y].apply(lambda s: s.notna().mean())
    hi_arm = int(p.idxmax()); lo_arm = 1 - hi_arm
    q = (p[hi_arm] - p[lo_arm]) / p[hi_arm]
    yh = np.sort(df[(df.active == hi_arm)][y].dropna().values)
    yl = df[(df.active == lo_arm)][y].dropna().values
    k = int(round(q * len(yh)))
    lower_trim = yh[: len(yh) - k]  # drop top k -> smallest mean
    upper_trim = yh[k:]             # drop bottom k -> largest mean
    sign = 1 if hi_arm == 1 else -1
    a = sign * (lower_trim.mean() - yl.mean())
    b = sign * (upper_trim.mean() - yl.mean())
    sp = hedges_g(yh, yl)["sd_pooled"]
    return {"observed_share_active": p[1], "observed_share_lecture": p[0], "trim_share": q,
            "trimmed_n": k, "lower": min(a, b), "upper": max(a, b),
            "lower_g": min(a, b) / sp, "upper_g": max(a, b) / sp}


def main():
    s = D[D.stayed == 1].copy()       # in assigned section at drop/add (n = 811)
    S = {}

    # Flow
    n_arm = D.groupby("active").size()
    stay = D.groupby("active").stayed.mean()
    S["flow"] = {
        "randomized": len(D), "randomized_active": int(n_arm[1]), "randomized_lecture": int(n_arm[0]),
        "stayed_active": int(D[(D.active == 1)].stayed.sum()), "stayed_lecture": int(D[(D.active == 0)].stayed.sum()),
        "stay_rate_active": stay[1], "stay_rate_lecture": stay[0],
        "stayers": len(s), "sections": int(D.section.nunique()), "slots": int(D.slot.nunique()),
        "instructors": int(D.teacher.nunique()),
        "instructors_active": int(D[D.active == 1].teacher.nunique()),
        "instructors_lecture": int(D[D.active == 0].teacher.nunique()),
        "lm_n_active": int(s[s.active == 1].learning_measure.notna().sum()),
        "lm_n_lecture": int(s[s.active == 0].learning_measure.notna().sum()),
    }
    # Not every randomized student has a recorded slot/section (68 left before placement
    # was recorded), so the stay-rate and balance checks use simple unclustered tests.
    x1, n1 = D[D.active == 1].stayed.sum(), (D.active == 1).sum()
    x0, n0 = D[D.active == 0].stayed.sum(), (D.active == 0).sum()
    pp_ = (x1 + x0) / (n1 + n0)
    z = (x1 / n1 - x0 / n0) / np.sqrt(pp_ * (1 - pp_) * (1 / n1 + 1 / n0))
    S["stay_effect"] = {"est": x1 / n1 - x0 / n0, "p": 2 * stats.norm.sf(abs(z))}

    # Balance on prior preparation (randomization check)
    pp = D.groupby("active").prior_prep.agg(["mean", "std", "count"])
    S["balance"] = {"prior_prep_mean_active": pp.loc[1, "mean"], "prior_prep_mean_lecture": pp.loc[0, "mean"],
                    "prior_prep_sd_active": pp.loc[1, "std"], "prior_prep_sd_lecture": pp.loc[0, "std"],
                    "prior_prep_p": stats.ttest_ind(D[D.active == 1].prior_prep.dropna(),
                                                     D[D.active == 0].prior_prep.dropna(), equal_var=False).pvalue}
    ppl = s.groupby("active").prior_prep.mean()
    S["balance"]["stayers_with_score_prior_prep_active"] = s[(s.active == 1) & s.learning_measure.notna()].prior_prep.mean()
    S["balance"]["stayers_with_score_prior_prep_lecture"] = s[(s.active == 0) & s.learning_measure.notna()].prior_prep.mean()
    S["balance"]["stayers_without_score_prior_prep_lecture"] = s[(s.active == 0) & s.learning_measure.isna()].prior_prep.mean()
    S["balance"]["stayers_without_score_prior_prep_active"] = s[(s.active == 1) & s.learning_measure.isna()].prior_prep.mean()

    # Learning measure
    lm = s[s.learning_measure.notna()]
    S["lm"] = {
        "mean_active": lm[lm.active == 1].learning_measure.mean(),
        "mean_lecture": lm[lm.active == 0].learning_measure.mean(),
        "sd_active": lm[lm.active == 1].learning_measure.std(),
        "sd_lecture": lm[lm.active == 0].learning_measure.std(),
        "raw_diff": lm[lm.active == 1].learning_measure.mean() - lm[lm.active == 0].learning_measure.mean(),
        "fe": effect(s, "learning_measure"),
        "fe_adj": effect(s, "learning_measure", adjust=True),
        "g": hedges_g(lm[lm.active == 1].learning_measure, lm[lm.active == 0].learning_measure),
        "pairs": section_pairs(s, "learning_measure"),
        "lee": lee_bounds(s, "learning_measure"),
    }

    # Pass rate (C or better) and DFW among stayers
    S["pass"] = {
        "rate_active": s[s.active == 1].pass_c_or_better.mean(),
        "rate_lecture": s[s.active == 0].pass_c_or_better.mean(),
        "fe": effect(s, "pass_c_or_better"),
        "fe_adj": effect(s, "pass_c_or_better", adjust=True),
        "pairs": section_pairs(s, "pass_c_or_better"),
        "dfw_active": s[s.active == 1].dfw.mean(), "dfw_lecture": s[s.active == 0].dfw.mean(),
    }
    S["pass"]["relative_dfw_reduction"] = 1 - S["pass"]["dfw_active"] / S["pass"]["dfw_lecture"]

    # Subgroups (exploratory)
    groups = {
        "Women": ("female", 1), "Men": ("female", 0),
        "Hispanic or Latino/a": ("hispanic", 1), "Not Hispanic or Latino/a": ("hispanic", 0),
        "Black or African American": ("black", 1),
        "First time in college": ("first_time_college", 1), "Transfer or other": ("first_time_college", 0),
    }
    sub = []
    for label, (col, val) in groups.items():
        part = s[s[col] == val]
        lmr = effect(part, "learning_measure")
        pr = effect(part, "pass_c_or_better")
        sub.append({"group": label, "var": col, "n": len(part),
                    "n_active": int((part.active == 1).sum()), "n_lecture": int((part.active == 0).sum()),
                    "lm": lmr, "pass": pr,
                    "pass_active": part[part.active == 1].pass_c_or_better.mean(),
                    "pass_lecture": part[part.active == 0].pass_c_or_better.mean()})
    for g3 in ["Lower third", "Middle third", "Upper third"]:
        part = s[s.prior_prep_group == g3]
        sub.append({"group": f"Prior preparation: {g3.lower()}", "var": "prior_prep_group", "n": len(part),
                    "n_active": int((part.active == 1).sum()), "n_lecture": int((part.active == 0).sum()),
                    "lm": effect(part, "learning_measure"), "pass": effect(part, "pass_c_or_better"),
                    "pass_active": part[part.active == 1].pass_c_or_better.mean(),
                    "pass_lecture": part[part.active == 0].pass_c_or_better.mean()})
    S["subgroups"] = sub
    s["prep_z"] = (s.prior_prep - s.prior_prep.mean()) / s.prior_prep.std()
    S["interactions"] = {
        "female": {"lm": interaction(s, "learning_measure", "female"), "pass": interaction(s, "pass_c_or_better", "female")},
        "hispanic": {"lm": interaction(s, "learning_measure", "hispanic"), "pass": interaction(s, "pass_c_or_better", "hispanic")},
        "black": {"lm": interaction(s, "learning_measure", "black"), "pass": interaction(s, "pass_c_or_better", "black")},
        "first_time_college": {"lm": interaction(s, "learning_measure", "first_time_college"),
                               "pass": interaction(s, "pass_c_or_better", "first_time_college")},
        "prior_prep_per_sd": {"lm": interaction(s, "learning_measure", "prep_z"),
                              "pass": interaction(s, "pass_c_or_better", "prep_z")},
    }
    S["sample"] = {
        "share_hispanic": D.hispanic.mean(), "share_female_known": D.female.dropna().mean(),
        "share_black": D.black.mean(),
    }

    def clean(o):
        if isinstance(o, dict):
            return {k: clean(v) for k, v in o.items()}
        if isinstance(o, list):
            return [clean(v) for v in o]
        if isinstance(o, (np.floating, float)):
            return round(float(o), 6)
        if isinstance(o, (np.integer,)):
            return int(o)
        return o

    (OUT / "stats.json").write_text(json.dumps(clean(S), indent=2))
    print(json.dumps(clean({k: S[k] for k in ["flow", "stay_effect", "balance", "lm", "pass", "interactions"]}), indent=1))
    for r in sub:
        print(f"{r['group']:42s} n={r['n']:4d} LM {r['lm']['est']:6.2f} [{r['lm']['lo']:.1f},{r['lm']['hi']:.1f}]  "
              f"pass {r['pass_active']:.2f} vs {r['pass_lecture']:.2f} diff {r['pass']['est']:.3f} p={r['pass']['p']:.3f}")


if __name__ == "__main__":
    main()
