"""Step 4: figures, built only from paper/stats.json.

Plain-language note: this makes the three charts in the paper and saves them in
paper/figures/. Each chart says DRAFT until you have checked the work; running
`python code/04_figures.py --final` removes the stamp. You do not need this file.
"""
import json
import pathlib
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = pathlib.Path(__file__).resolve().parents[1]
S = json.loads((ROOT / "paper" / "stats.json").read_text())
FIG = ROOT / "paper" / "figures"
FIG.mkdir(parents=True, exist_ok=True)
FINAL = "--final" in sys.argv

ACTIVE, LECTURE = "#2a78d6", "#eb6834"      # categorical slots 1 and 2 (validated palette)
INK, INK2, GRID, SURF = "#0b0b0b", "#52514e", "#e4e3df", "#ffffff"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10, "axes.edgecolor": INK2,
                     "axes.labelcolor": INK, "xtick.color": INK2, "ytick.color": INK2,
                     "figure.facecolor": SURF, "axes.facecolor": SURF, "savefig.facecolor": SURF})


def stamp(fig):
    if not FINAL:
        fig.text(0.99, 0.01, "DRAFT", ha="right", va="bottom", fontsize=9, color="#a8a7a1", weight="bold")


def tidy(ax):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.grid(axis="x", color=GRID, lw=0.8)
    ax.set_axisbelow(True)


# Figure 1: headline outcomes by arm
lm, ps = S["lm"], S["pass"]
fig, axes = plt.subplots(1, 2, figsize=(8, 2.8))
rows = [("Lecture", LECTURE, lm["mean_lecture"], lm["sd_lecture"], S["flow"]["lm_n_lecture"],
         ps["rate_lecture"], S["flow"]["stayed_lecture"]),
        ("Active learning", ACTIVE, lm["mean_active"], lm["sd_active"], S["flow"]["lm_n_active"],
         ps["rate_active"], S["flow"]["stayed_active"])]
for i, (lab, col, m, sd, n, p, n2) in enumerate(rows):
    se = sd / n ** 0.5
    axes[0].errorbar(m, i, xerr=1.96 * se, fmt="o", ms=8, color=col, ecolor=col, elinewidth=2, capsize=0)
    axes[0].text(m, i + 0.22, f"{m:.1f}", ha="center", va="bottom", color=INK, fontsize=10)
    pse = (p * (1 - p) / n2) ** 0.5
    axes[1].errorbar(100 * p, i, xerr=196 * pse, fmt="o", ms=8, color=col, ecolor=col, elinewidth=2, capsize=0)
    axes[1].text(100 * p, i + 0.22, f"{100 * p:.1f}%", ha="center", va="bottom", color=INK, fontsize=10)
for ax, title, lim in [(axes[0], "End-of-term learning score (0 to 100)", (40, 70)),
                       (axes[1], "Passed with C or better (%)", (60, 90))]:
    ax.set_yticks([0, 1], ["Lecture", "Active learning"])
    ax.set_ylim(-0.6, 1.7); ax.set_xlim(*lim); ax.set_title(title, loc="left", fontsize=10, color=INK)
    tidy(ax)
stamp(fig); fig.tight_layout()
fig.savefig(FIG / "fig1_outcomes.png", dpi=200, bbox_inches="tight"); plt.close(fig)

# Figure 2: section-pair differences across the 16 time slots
fig, axes = plt.subplots(1, 2, figsize=(8, 3.2))
for ax, key, scale, unit, title in [(axes[0], "lm", 1, "points", "Learning score gap (active minus lecture)"),
                                   (axes[1], "pass", 100, "percentage points", "Pass-rate gap (active minus lecture)")]:
    diffs = sorted(v * scale for v in S[key]["pairs"]["diffs"])
    cols = [ACTIVE if v > 0 else LECTURE for v in diffs]
    ax.scatter(diffs, range(len(diffs)), s=36, c=cols, edgecolors=SURF, linewidths=1.5, zorder=3)
    ax.axvline(0, color=INK2, lw=1)
    mean = S[key]["pairs"]["mean_diff"] * scale
    ax.axvline(mean, color=ACTIVE, lw=2, ls=(0, (4, 3)))
    ax.text(mean, len(diffs) - 0.2, f" average {mean:+.1f}", color=INK, fontsize=9, va="bottom")
    ax.set_yticks([]); ax.set_xlabel(unit, color=INK2)
    ax.set_title(title, loc="left", fontsize=10, color=INK); ax.set_ylim(-1, len(diffs) + 1)
    tidy(ax)
stamp(fig); fig.tight_layout()
fig.savefig(FIG / "fig2_section_pairs.png", dpi=200, bbox_inches="tight"); plt.close(fig)

# Figure 3: subgroup estimates (exploratory)
sub = S["subgroups"]
fig, axes = plt.subplots(1, 2, figsize=(8.5, 4.2), sharey=True)
labels = [r["group"] for r in sub][::-1]
for ax, key, scale, title, ref in [(axes[0], "lm", 1, "Learning score gain (points)", S["lm"]["fe"]["est"]),
                                   (axes[1], "pass", 100, "Pass-rate gain (percentage points)", 100 * S["pass"]["fe"]["est"])]:
    for i, r in enumerate(sub[::-1]):
        e = r[key]
        ax.plot([scale * e["lo"], scale * e["hi"]], [i, i], color=ACTIVE, lw=2, solid_capstyle="round")
        ax.scatter(scale * e["est"], i, s=40, color=ACTIVE, edgecolors=SURF, linewidths=1.5, zorder=3)
    ax.axvline(0, color=INK2, lw=1)
    ax.axvline(ref, color=INK2, lw=1, ls=(0, (2, 3)))
    ax.set_title(title, loc="left", fontsize=10, color=INK)
    ax.set_yticks(range(len(labels)), [f"{l} (n={r['n']})" for l, r in zip(labels, sub[::-1])], fontsize=8.5)
    tidy(ax)
stamp(fig); fig.tight_layout()
fig.savefig(FIG / "fig3_subgroups.png", dpi=200, bbox_inches="tight"); plt.close(fig)
print("figures written:", sorted(p.name for p in FIG.glob("*.png")))
