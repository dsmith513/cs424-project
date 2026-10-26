#!/usr/bin/env python3
"""Render four Assignment 1 sketch directions from the processed CSV data."""

from __future__ import annotations

import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "processed"
OUTPUT = ROOT / "figures" / "implemented"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.titlesize": 14,
    "axes.labelsize": 11,
})


def read_csv(filename: str) -> list[dict[str, str]]:
    with (DATA / filename).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def render_bars(stops: list[dict[str, str]]) -> None:
    selected_date = "2026-09-21"
    selected = [
        row for row in stops
        if row["date"] == selected_date
        and row["direction"] == "Inbound"
        and row["train_number"] == "640"
        and row["stop_status"] == "observed_stop"
    ]
    selected.sort(key=lambda row: int(row["stop_order"]))
    labels = [row["stop_name"] for row in selected]
    board = [int(row["boardings"]) for row in selected]
    exits = [int(row["exits"]) for row in selected]
    y = np.arange(len(labels))

    fig, ax = plt.subplots(figsize=(11, 7), constrained_layout=True)
    ax.barh(y + 0.18, board, height=0.34, label="Getting on", color="#3478B8")
    ax.barh(y - 0.18, exits, height=0.34, label="Getting off", color="#E4863A")
    ax.set_yticks(y, labels)
    ax.invert_yaxis()
    ax.set_xlabel("Passengers in observed car")
    ax.set_title("Inbound boarding and exiting by station\n"
                 f"{selected_date} · Train 640 · Cary to Chicago OTC · no bar means zero",
                 fontsize=13, pad=14)
    ax.grid(axis="x", alpha=0.22)
    ax.set_axisbelow(True)
    ax.legend(frameon=False, ncol=2, loc="lower right")
    fig.savefig(OUTPUT / "barsketch2.png", dpi=170, facecolor="white")
    plt.close(fig)


def render_lines(stops: list[dict[str, str]]) -> None:
    # One Monday from each of the five sampled weeks keeps the sketch's
    # multiple-date comparison while avoiding 15 overlapping trip lines.
    selected_dates = ["2026-09-21", "2026-09-28", "2026-10-05", "2026-10-12", "2026-10-19"]
    colors = ["#9CC7DF", "#72A9CC", "#4B8FB8", "#286E9A", "#174F75"]
    fig, ax = plt.subplots(figsize=(12, 6.5), constrained_layout=True)
    all_values: dict[str, list[int]] = {}

    for date, color in zip(selected_dates, colors):
        rows = [
            row for row in stops
            if row["date"] == date and row["direction"] == "Inbound"
            and row["train_number"] == "640"
        ]
        rows.sort(key=lambda row: int(row["stop_order"]))
        xs = list(range(len(rows)))
        ys = [int(row["passengers_after_stop"]) for row in rows]
        names = [row["stop_name"] for row in rows]
        ax.plot(xs, ys, marker="o", linewidth=1.8, markersize=4.5, color=color,
                label=date, alpha=0.9)
        for name, value in zip(names, ys):
            all_values.setdefault(name, []).append(value)

    # A heavier line summarizes these five comparable Monday trips.
    route_names = [row["stop_name"] for row in sorted(
        [r for r in stops if r["date"] == selected_dates[0] and r["direction"] == "Inbound"
         and r["train_number"] == "640"], key=lambda row: int(row["stop_order"]))]
    medians = [float(np.median(all_values[name])) for name in route_names]
    ax.plot(range(len(route_names)), medians, color="#172E42", linewidth=3.2,
            marker="D", markersize=5, label="Median of five Mondays")
    ax.set_xticks(range(len(route_names)), route_names, rotation=38, ha="right")
    ax.set_ylabel("Passengers in observed car after stop")
    ax.set_title("Inbound passenger load along the route\n"
                 "Train 640 · one Monday per sampled week",
                 fontsize=13, pad=14)
    ax.grid(axis="y", alpha=0.22)
    ax.set_axisbelow(True)
    ax.legend(frameon=False, ncol=3, loc="upper left")
    fig.savefig(OUTPUT / "linesketch.png", dpi=170, facecolor="white")
    plt.close(fig)


def render_pie(stops: list[dict[str, str]], trips: list[dict[str, str]]) -> None:
    selected_date = "2026-09-22"
    trip = next(row for row in trips if row["date"] == selected_date
                and row["direction"] == "Outbound" and row["train_number"] == "655")
    rows = [row for row in stops if row["date"] == selected_date
            and row["direction"] == "Outbound" and row["train_number"] == "655"
            and row["stop_status"] == "observed_stop"]
    slices = [(row["stop_name"], int(row["exits"])) for row in rows if int(row["exits"]) > 0]
    slices.append(("Remaining after Cary", int(trip["segment_end_passengers"])))
    labels, values = zip(*slices)
    colors = ["#3B82A0", "#67A88D", "#E4A64B", "#D56F55", "#B9C8D2"]

    fig, ax = plt.subplots(figsize=(10, 7), constrained_layout=True)
    wedges, _ = ax.pie(values, center=(0.35, 0.5), radius=0.77, startangle=90,
                       counterclock=False, colors=colors[:len(values)],
                       wedgeprops={"edgecolor": "white", "linewidth": 2})
    legend_labels = [f"{name}: {value}" for name, value in slices]
    ax.legend(wedges, legend_labels, title="Passengers", loc="center left",
              bbox_to_anchor=(0.70, 0.5), frameon=False, fontsize=10)
    ax.set_title("Where outbound express passengers leave\n"
                 f"{selected_date} · Train 655 · {trip['total_boardings']} passengers boarded at Chicago OTC",
                 fontsize=13, pad=14)
    fig.savefig(OUTPUT / "piesketch.png", dpi=170, facecolor="white")
    plt.close(fig)


def render_weekday_scatter(trips: list[dict[str, str]]) -> None:
    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    fig, ax = plt.subplots(figsize=(10, 6.5), constrained_layout=True)
    rng = np.random.default_rng(424)
    for direction, marker, face, label in [
        ("Inbound", "o", "#315E7D", "Inbound (filled)"),
        ("Outbound", "o", "white", "Outbound (hollow)"),
    ]:
        rows = [row for row in trips if row["direction"] == direction]
        xs = []
        ys = []
        for row in rows:
            base = weekdays.index(row["day_of_week"])
            direction_offset = -0.09 if direction == "Inbound" else 0.09
            xs.append(base + direction_offset + rng.uniform(-0.045, 0.045))
            ys.append(int(row["peak_passengers"]))
        ax.scatter(xs, ys, s=72, marker=marker, facecolors=face, edgecolors="#315E7D",
                   linewidths=1.6, alpha=0.82, label=label, zorder=3)
    ax.set_xticks(range(len(weekdays)), weekdays)
    ax.set_ylabel("Peak passengers in observed car")
    ax.set_xlabel("Weekday")
    ax.set_title("Peak passenger load by weekday and direction\n"
                 "Each point is one trip; jitter separates overlapping observations",
                 fontsize=13, pad=14)
    ax.grid(axis="y", alpha=0.22)
    ax.set_axisbelow(True)
    ax.legend(frameon=False, loc="upper right")
    fig.savefig(OUTPUT / "plotsketch.png", dpi=170, facecolor="white")
    plt.close(fig)


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    stops = read_csv("passenger-stops.csv")
    trips = read_csv("trip-summary.csv")
    render_bars(stops)
    render_lines(stops)
    render_pie(stops, trips)
    render_weekday_scatter(trips)
    print(f"Wrote four sketch implementations to {OUTPUT}")


if __name__ == "__main__":
    main()
