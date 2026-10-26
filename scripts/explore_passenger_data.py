#!/usr/bin/env python3
"""Create simple exploratory figures from the processed passenger CSV files."""

from __future__ import annotations

import csv
import statistics
from collections import Counter, defaultdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"
FIGURES = ROOT / "figures" / "exploratory"
WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
INBOUND_ORDER = [
    "Cary", "Fox River Grove", "Barrington", "Palatine", "Arlington Park",
    "Arlington Heights", "Mt. Prospect", "Cumberland", "Des Plaines", "Dee Road",
    "Park Ridge", "Edison Park", "Norwood Park", "Gladstone Park", "Jefferson Park",
    "Irving Park", "Clybourn", "Chicago OTC",
]
OUTBOUND_ORDER = list(reversed(INBOUND_ORDER))
COLORS = {"Boardings": "#2878B5", "Exits": "#E07A25"}
TRAIN_COLORS = {"638": "#3D8B5B", "640": "#7656A6", "627": "#3D8B5B", "655": "#7656A6"}


def read_csv(name: str) -> list[dict[str, str]]:
    with (PROCESSED / name).open(newline="", encoding="utf-8") as source:
        return list(csv.DictReader(source))


def quantile(values: list[int], probability: float) -> float:
    return float(np.quantile(values, probability))


def save_station_counts(stops: list[dict[str, str]]) -> None:
    groups = [("Inbound", "638", "Non-express"), ("Inbound", "640", "Express"),
              ("Outbound", "627", "Non-express"), ("Outbound", "655", "Express")]
    observed = [row for row in stops if row["stop_status"] == "observed_stop"]
    fig, axes = plt.subplots(2, 2, figsize=(14, 12), constrained_layout=True)

    for ax, (direction, train, service) in zip(axes.flat, groups):
        rows = [row for row in observed if row["direction"] == direction and row["train_number"] == train]
        station_order = list(dict.fromkeys(row["stop_name"] for row in rows))
        station_order.reverse()
        positions = np.arange(len(station_order))
        board_medians, exit_medians = [], []
        for station in station_order:
            at_station = [row for row in rows if row["stop_name"] == station]
            board_medians.append(statistics.median(int(row["boardings"]) for row in at_station))
            exit_medians.append(statistics.median(int(row["exits"]) for row in at_station))
        height = 0.36
        ax.barh(positions - height / 2, board_medians, height, color=COLORS["Boardings"], label="Boardings")
        ax.barh(positions + height / 2, exit_medians, height, color=COLORS["Exits"], label="Exits")
        ax.set_yticks(positions, station_order)
        ax.set_title(f"{direction}: train {train} ({service})")
        ax.set_xlabel("Median passengers per observed trip")
        ax.grid(axis="x", alpha=0.25)
        ax.set_axisbelow(True)
    axes[0, 0].legend(frameon=False)
    fig.suptitle("Typical station activity by observed service\n(medians; skipped stops omitted)", fontsize=14)
    fig.savefig(FIGURES / "station-counts.png", dpi=160)
    plt.close(fig)


def save_occupancy_profiles(stops: list[dict[str, str]]) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(16, 6), constrained_layout=True)
    direction_trains = {"Inbound": ["638", "640"], "Outbound": ["627", "655"]}
    direction_labels = {"Inbound": "Cary to Chicago OTC", "Outbound": "Chicago OTC to Cary"}

    for ax, direction in zip(axes, ["Inbound", "Outbound"]):
        rows = [row for row in stops if row["direction"] == direction]
        station_order = INBOUND_ORDER if direction == "Inbound" else OUTBOUND_ORDER
        x_by_station = {station: i for i, station in enumerate(station_order)}
        for offset, train in zip([-0.13, 0.13], direction_trains[direction]):
            train_rows = [row for row in rows if row["train_number"] == train]
            grouped: dict[str, list[int]] = defaultdict(list)
            for row in train_rows:
                grouped[row["stop_name"]].append(int(row["passengers_after_stop"]))
            xs, medians, lower, upper = [], [], [], []
            for station in station_order:
                values = grouped.get(station)
                if not values:
                    continue
                median = statistics.median(values)
                xs.append(x_by_station[station] + offset)
                medians.append(median)
                lower.append(median - quantile(values, 0.25))
                upper.append(quantile(values, 0.75) - median)
            service = "Express" if train in {"640", "655"} else "Non-express"
            ax.errorbar(xs, medians, yerr=[lower, upper], fmt="o", capsize=3,
                        color=TRAIN_COLORS[train], label=f"Train {train} ({service})")
        ax.set_xticks(range(len(station_order)), station_order, rotation=55, ha="right")
        ax.set_ylabel("Passengers in observed car")
        ax.set_title(direction_labels[direction])
        ax.grid(axis="y", alpha=0.25)
        ax.set_axisbelow(True)
        ax.legend(frameon=False)
    fig.suptitle("Passenger load at observed stops\n(median and interquartile range; points only, no interpolation)", fontsize=14)
    fig.savefig(FIGURES / "occupancy-by-stop.png", dpi=160)
    plt.close(fig)


def save_trip_distributions(trips: list[dict[str, str]]) -> None:
    panels = [
        ("Inbound", "total_boardings", "Total boardings"),
        ("Inbound", "peak_passengers", "Peak passengers"),
        ("Outbound", "total_boardings", "Total boardings"),
        ("Outbound", "peak_passengers", "Peak passengers"),
    ]
    fig, axes = plt.subplots(2, 2, figsize=(11, 8), constrained_layout=True)
    rng = np.random.default_rng(424)
    for ax, (direction, field, title) in zip(axes.flat, panels):
        direction_rows = [row for row in trips if row["direction"] == direction]
        trains = sorted({row["train_number"] for row in direction_rows})
        for position, train in enumerate(trains):
            values = [int(row[field]) for row in direction_rows if row["train_number"] == train]
            jitter = rng.uniform(-0.08, 0.08, len(values))
            ax.scatter(position + jitter, values, s=28, alpha=0.68, color=TRAIN_COLORS[train], edgecolors="none")
            median = statistics.median(values)
            ax.hlines(median, position - 0.2, position + 0.2, color="black", linewidth=2)
            ax.text(position, max(values) + 1, f"n={len(values)}", ha="center", fontsize=8)
        ax.set_xticks(range(len(trains)), [f"Train {train}" for train in trains])
        ax.set_ylabel("Passengers per trip")
        ax.set_title(f"{direction}: {title}")
        ax.grid(axis="y", alpha=0.25)
        ax.set_axisbelow(True)
    fig.suptitle("Trip-level distributions by observed train\n(points are individual trips; black marks are medians)", fontsize=14)
    fig.savefig(FIGURES / "trip-distributions.png", dpi=160)
    plt.close(fig)


def save_sampling_design(trips: list[dict[str, str]]) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.5), constrained_layout=True)
    for ax, direction, trains in zip(axes, ["Inbound", "Outbound"], [["638", "640"], ["627", "655"]]):
        counts = np.zeros((len(WEEKDAYS), len(trains)), dtype=int)
        for row in trips:
            if row["direction"] == direction:
                counts[WEEKDAYS.index(row["day_of_week"]), trains.index(row["train_number"])] += 1
        ax.imshow(counts, cmap="Blues", vmin=0, vmax=max(1, counts.max()), aspect="auto")
        ax.set_xticks(range(len(trains)), [f"Train {train}" for train in trains])
        ax.set_yticks(range(len(WEEKDAYS)), WEEKDAYS)
        ax.set_title(direction)
        for y in range(counts.shape[0]):
            for x in range(counts.shape[1]):
                ax.text(x, y, str(counts[y, x]), ha="center", va="center",
                        color="white" if counts[y, x] >= max(1, counts.max() * 0.6) else "black")
    fig.suptitle("Observed trips by weekday and train\n(cell values are trip counts)", fontsize=14)
    fig.savefig(FIGURES / "sampling-design.png", dpi=160)
    plt.close(fig)


def main() -> None:
    FIGURES.mkdir(parents=True, exist_ok=True)
    stops = read_csv("passenger-stops.csv")
    trips = read_csv("trip-summary.csv")
    save_station_counts(stops)
    save_occupancy_profiles(stops)
    save_trip_distributions(trips)
    save_sampling_design(trips)
    print(f"Wrote four exploratory figures to {FIGURES}")


if __name__ == "__main__":
    main()
