#!/usr/bin/env python3
"""Render evidence images for the two passenger-load line-chart iterations."""

from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "processed" / "passenger-stops.csv"
OUTPUT = ROOT / "figures" / "iterations"
SELECTED_DATE = "2026-09-21"


def main() -> None:
    with DATA.open(newline="", encoding="utf-8") as handle:
        rows = [r for r in csv.DictReader(handle)
                if r["direction"] == "Inbound" and r["train_number"] == "640"]
    groups: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        groups[row["observation_id"]].append(row)
    for trip_rows in groups.values():
        trip_rows.sort(key=lambda r: int(r["stop_order"]))
    dates = sorted(groups)
    stations = [r["stop_name"] for r in groups[dates[0]]]
    matrix = np.array([[int(r["passengers_after_stop"]) for r in groups[trip]] for trip in dates])
    x = np.arange(len(stations))
    median = np.median(matrix, axis=0)
    q1, q3 = np.quantile(matrix, [0.25, 0.75], axis=0)
    selected_id = next(trip for trip in dates if trip.startswith(SELECTED_DATE))
    selected = np.array([int(r["passengers_after_stop"]) for r in groups[selected_id]])
    OUTPUT.mkdir(parents=True, exist_ok=True)

    def frame(title: str, subtitle: str):
        fig, ax = plt.subplots(figsize=(12, 6.5), constrained_layout=True)
        ax.fill_between(x, q1, q3, color="#85b5c5", alpha=0.35, label="25th–75th percentile")
        ax.plot(x, median, color="#183247", linewidth=3, marker="D", markersize=5, label="Median")
        ax.set_xticks(x, stations, rotation=38, ha="right")
        ax.set_ylabel("Passengers in observed car after stop")
        ax.set_title(f"{title}\n{subtitle}", fontsize=14, pad=14)
        ax.grid(axis="y", alpha=0.22)
        ax.set_axisbelow(True)
        return fig, ax

    fig, ax = frame("Iteration 1 · Summarize trip variation",
                    "Inbound train 640 · all 15 observed trips · median and interquartile range")
    ax.legend(frameon=False, loc="upper left")
    fig.savefig(OUTPUT / "line-iteration-1.png", dpi=170, facecolor="white")
    plt.close(fig)

    fig, ax = frame("Iteration 2 · Highlight a selected trip",
                    f"Train 640 · orange is {SELECTED_DATE}; band and median summarize all 15 trips")
    ax.plot(x, selected, color="#df853e", linewidth=2.8, marker="o", markersize=5,
            label=f"Selected trip · {SELECTED_DATE}")
    peak = int(np.argmax(selected))
    ax.annotate(f"Peak: {selected[peak]} at {stations[peak]}", (x[peak], selected[peak]),
                xytext=(10, 16), textcoords="offset points", color="#a34f23",
                arrowprops={"arrowstyle": "->", "color": "#a34f23"})
    ax.legend(frameon=False, loc="upper left")
    fig.savefig(OUTPUT / "line-iteration-2.png", dpi=170, facecolor="white")
    plt.close(fig)
    print(f"Wrote two line-chart iteration figures to {OUTPUT}")


if __name__ == "__main__":
    main()
