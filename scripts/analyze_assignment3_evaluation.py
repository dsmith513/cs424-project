"""Summarize Task 3 evaluation records and generate Task 4 figures."""
import csv
from collections import defaultdict
from pathlib import Path
import statistics

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "evaluation" / "evaluation-results.csv"
OUT = ROOT / "figures" / "evaluation"
OUT.mkdir(parents=True, exist_ok=True)

with DATA.open(newline="", encoding="utf-8-sig") as f:
    rows = list(csv.DictReader(f))

def num(row, key):
    return int(row[key])

conditions = ["Static", "Interactive"]
variants = [("Task 1", "A"), ("Task 1", "B"), ("Task 2", "A"), ("Task 2", "B")]
colors = {"Static": "#5470a8", "Interactive": "#e07a35"}

# Accuracy by task variant: each bar is a count out of five participants.
fig, ax = plt.subplots(figsize=(9, 5.2))
x = np.arange(len(variants))
width = 0.34
for j, condition in enumerate(conditions):
    vals = []
    for task, variant in variants:
        subset = [r for r in rows if r["condition"] == condition and r["task_type"] == task and r["variant"] == variant]
        vals.append(sum(num(r, "fully_correct") for r in subset))
    bars = ax.bar(x + (j - 0.5) * width, np.array(vals) / 5, width, label=condition,
                  color=colors[condition])
    for bar, value in zip(bars, vals):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + .025, f"{value}/5",
                ha="center", va="bottom", fontsize=9)
ax.set_xticks(x, [f"{t} {v}" for t, v in variants])
ax.set_ylim(0, 1.12)
ax.set_ylabel("Fully correct participants")
ax.set_yticks(np.arange(0, 1.01, .2), [f"{int(v*100)}%" for v in np.arange(0, 1.01, .2)])
ax.set_title("Task accuracy by variant")
ax.legend(frameon=False, ncol=2, loc="upper right")
ax.grid(axis="y", alpha=.2)
fig.tight_layout()
fig.savefig(OUT / "accuracy-by-variant.png", dpi=180)
plt.close(fig)

# Completion time: show individual participant/task observations and means with SD.
fig, ax = plt.subplots(figsize=(8.5, 5.2))
groups = [("Task 1", "Static"), ("Task 1", "Interactive"),
          ("Task 2", "Static"), ("Task 2", "Interactive")]
positions = np.arange(len(groups))
rng = np.random.default_rng(4242)
for pos, (task, condition) in zip(positions, groups):
    subset = [r for r in rows if r["task_type"] == task and r["condition"] == condition]
    times = [num(r, "time_seconds") for r in subset]
    jitter = rng.uniform(-.09, .09, len(times))
    ax.scatter(pos + jitter, times, color=colors[condition], alpha=.55, s=27,
               edgecolor="white", linewidth=.4, zorder=2)
    mean = statistics.mean(times)
    sd = statistics.stdev(times)
    ax.errorbar(pos, mean, yerr=sd, fmt="D", color="#222222", capsize=4,
                markersize=5, linewidth=1.4, zorder=3)
ax.set_xticks(positions, [f"{t}\n{c}" for t, c in groups])
ax.set_ylabel("Completion time (seconds)")
ax.set_title("Completion time by task type and condition")
ax.text(.99, .98, "Dots: individual records; diamond and whisker: mean ± SD",
        transform=ax.transAxes, ha="right", va="top", fontsize=8, color="#444444")
ax.grid(axis="y", alpha=.2)
fig.tight_layout()
fig.savefig(OUT / "completion-time-by-task.png", dpi=180)
plt.close(fig)

for condition in conditions:
    subset = [r for r in rows if r["condition"] == condition]
    times = [num(r, "time_seconds") for r in subset]
    correct = sum(num(r, "fully_correct") for r in subset)
    print(f"{condition}: full accuracy {correct}/{len(subset)}; time mean={statistics.mean(times):.1f}, "
          f"median={statistics.median(times):.1f}, SD={statistics.stdev(times):.1f}, "
          f"range={min(times)}-{max(times)}")
for task, variant in variants:
    for condition in conditions:
        subset = [r for r in rows if r["condition"] == condition and r["task_type"] == task and r["variant"] == variant]
        times = [num(r, "time_seconds") for r in subset]
        correct = sum(num(r, "fully_correct") for r in subset)
        print(f"{task} {variant} {condition}: {correct}/5; mean={statistics.mean(times):.1f}, "
              f"median={statistics.median(times):.1f}, SD={statistics.stdev(times):.1f}")
