#!/usr/bin/env python3
"""Transform passenger-data.xlsx into tidy stop-level and trip-level CSV files.

Uses only Python's standard library. Run from any directory with:
    python scripts/prepare_passenger_data.py
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import posixpath
import re
import sys
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "passenger-data.xlsx"
DEFAULT_OUTPUT_DIR = ROOT / "data" / "processed"
NS = {
    "main": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
    "rel": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "pkg": "http://schemas.openxmlformats.org/package/2006/relationships",
}

# The observed schedules identify these train services as express or local.
# Keep this mapping explicit so a new train cannot be silently misclassified.
SERVICE_TYPE = {
    "638": "Non-express",
    "640": "Express",
    "627": "Non-express",
    "655": "Express",
}

STOP_FIELDS = [
    "observation_id",
    "date",
    "day_of_week",
    "direction",
    "train_number",
    "service_type",
    "departure_time",
    "stop_order",
    "stop_name",
    "stop_status",
    "boardings",
    "exits",
    "passengers_after_stop",
    "initial_passengers",
]
TRIP_FIELDS = [
    "observation_id",
    "date",
    "day_of_week",
    "direction",
    "train_number",
    "service_type",
    "departure_time",
    "initial_passengers",
    "total_boardings",
    "total_observed_exits",
    "peak_passengers",
    "peak_at_stop",
    "segment_end_passengers",
]


def column_number(cell_ref: str) -> int:
    letters = re.match(r"[A-Z]+", cell_ref)
    if not letters:
        raise ValueError(f"Invalid cell reference: {cell_ref}")
    number = 0
    for char in letters.group():
        number = number * 26 + ord(char) - ord("A") + 1
    return number


def load_workbook(path: Path) -> dict[str, list[dict[str, str]]]:
    """Read worksheet cell values, including shared and inline strings."""
    with zipfile.ZipFile(path) as archive:
        shared_strings: list[str] = []
        if "xl/sharedStrings.xml" in archive.namelist():
            root = ET.fromstring(archive.read("xl/sharedStrings.xml"))
            shared_strings = [
                "".join(node.text or "" for node in item.findall(".//main:t", NS))
                for item in root.findall("main:si", NS)
            ]

        workbook = ET.fromstring(archive.read("xl/workbook.xml"))
        relationships = ET.fromstring(archive.read("xl/_rels/workbook.xml.rels"))
        targets = {
            relationship.attrib["Id"]: relationship.attrib["Target"]
            for relationship in relationships.findall("pkg:Relationship", NS)
        }
        sheets: dict[str, list[dict[str, str]]] = {}

        for sheet in workbook.findall("main:sheets/main:sheet", NS):
            name = sheet.attrib["name"]
            rel_id = sheet.attrib[f"{{{NS['rel']}}}id"]
            target = targets[rel_id]
            sheet_path = (
                target.lstrip("/")
                if target.startswith("/")
                else posixpath.normpath(posixpath.join("xl", target))
            )
            root = ET.fromstring(archive.read(sheet_path))
            rows: list[dict[str, str]] = []
            for row in root.findall(".//main:sheetData/main:row", NS):
                cells: dict[int, str] = {}
                for cell in row.findall("main:c", NS):
                    value = cell.find("main:v", NS)
                    inline = cell.find(".//main:t", NS)
                    kind = cell.attrib.get("t")
                    if kind == "inlineStr":
                        text = "" if inline is None or inline.text is None else inline.text
                    elif value is None or value.text is None:
                        text = ""
                    elif kind == "s":
                        text = shared_strings[int(value.text)]
                    else:
                        text = value.text
                    cells[column_number(cell.attrib["r"])] = text
                if cells:
                    rows.append({str(k): v for k, v in cells.items()})

            if not rows:
                raise ValueError(f"Worksheet {name!r} has no data")
            headers = rows[0]
            if set(headers) != {str(k) for k in range(1, len(headers) + 1)}:
                raise ValueError(f"Worksheet {name!r} has missing or noncontiguous headers")
            header_names = [headers[str(k)] for k in range(1, len(headers) + 1)]
            records = []
            for cells in rows[1:]:
                records.append(
                    {header_names[k - 1]: cells.get(str(k), "") for k in range(1, len(header_names) + 1)}
                )
            sheets[name] = records
        return sheets


def excel_date(value: str) -> dt.date:
    return (dt.datetime(1899, 12, 30) + dt.timedelta(days=float(value))).date()


def excel_time(value: str) -> str:
    seconds = round(float(value) * 24 * 60 * 60)
    seconds %= 24 * 60 * 60
    return f"{seconds // 3600:02d}:{(seconds % 3600) // 60:02d}"


def count_value(value: str, field: str, observation_id: str) -> int:
    try:
        number = float(value)
    except ValueError as exc:
        raise ValueError(f"{observation_id}: {field} is not numeric: {value!r}") from exc
    if number < 0 or not number.is_integer():
        raise ValueError(f"{observation_id}: {field} must be a nonnegative whole number")
    return int(number)


def station_pairs(record: dict[str, str]) -> list[tuple[str, str, str]]:
    pairs = []
    for field in record:
        suffix = " - Getting On"
        if field.endswith(suffix):
            station = field[: -len(suffix)]
            off_field = f"{station} - Getting Off"
            # Outbound Chicago OTC is the trip's calculated starting count,
            # not a stop pair in the sheet's downstream movement columns.
            if station == "Chicago OTC" and off_field not in record:
                continue
            if off_field not in record:
                raise ValueError(f"Missing matching field {off_field!r}")
            pairs.append((station, field, off_field))
    return pairs


def rows_for_sheet(
    sheet_name: str, records: list[dict[str, str]]
) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    direction = sheet_name
    if direction not in {"Inbound", "Outbound"}:
        raise ValueError(f"Unexpected worksheet {sheet_name!r}; expected Inbound and Outbound")

    stop_rows: list[dict[str, object]] = []
    trip_rows: list[dict[str, object]] = []
    for record in records:
        date = excel_date(record["Date"])
        weekday = record["Day of Week"]
        if weekday != date.strftime("%A"):
            raise ValueError(f"{date}: weekday {weekday!r} does not match the date")
        train = str(int(float(record["Train Number"])))
        if train not in SERVICE_TYPE:
            raise ValueError(f"No service type configured for train {train}")
        observation_id = f"{date.isoformat()}_{direction.lower()}_{train}"
        departure_field = "Departure Time - Cary" if direction == "Inbound" else "Departure Time - Chicago OTC"
        departure = excel_time(record[departure_field])
        pairs = station_pairs(record)
        initial_field = "Existing Passengers" if direction == "Inbound" else "Chicago OTC - Getting On"

        if direction == "Inbound":
            initial = count_value(record[initial_field], initial_field, observation_id)
            occupancy = initial
            stops = []
            total_boardings = total_exits = 0
            for station, on_field, off_field in pairs:
                on_raw, off_raw = record[on_field], record[off_field]
                if (on_raw == "") != (off_raw == ""):
                    raise ValueError(f"{observation_id}: only one count is blank at {station}")
                if on_raw == "":  # Both blank means this service skipped the stop.
                    continue
                boardings = count_value(on_raw, on_field, observation_id)
                exits = count_value(off_raw, off_field, observation_id)
                occupancy += boardings - exits
                if occupancy < 0:
                    raise ValueError(f"{observation_id}: occupancy becomes negative at {station}")
                stops.append((station, boardings, exits, occupancy, "observed_stop"))
                total_boardings += boardings
                total_exits += exits
            segment_end = count_value(record["Chicago OTC - Total"], "Chicago OTC - Total", observation_id)
            if occupancy != segment_end:
                raise ValueError(
                    f"{observation_id}: calculated arrival count {occupancy} does not match {segment_end}"
                )
            stops.append(("Chicago OTC", None, None, segment_end, "terminal_checkpoint"))
        else:
            # The workbook's Chicago OTC boarding count is calculated from the
            # observed downstream exits, boardings, and remaining passengers.
            initial = count_value(record[initial_field], initial_field, observation_id)
            occupancy = initial
            stops = [("Chicago OTC", initial, 0, occupancy, "observed_stop")]
            total_boardings, total_exits = initial, 0
            for station, on_field, off_field in pairs:
                if station == "Chicago OTC":
                    continue
                on_raw, off_raw = record[on_field], record[off_field]
                if (on_raw == "") != (off_raw == ""):
                    raise ValueError(f"{observation_id}: only one count is blank at {station}")
                if on_raw == "":
                    continue
                boardings = count_value(on_raw, on_field, observation_id)
                exits = count_value(off_raw, off_field, observation_id)
                occupancy += boardings - exits
                if occupancy < 0:
                    raise ValueError(f"{observation_id}: occupancy becomes negative at {station}")
                stops.append((station, boardings, exits, occupancy, "observed_stop"))
                total_boardings += boardings
                total_exits += exits
            segment_end = count_value(record["Remaining Passengers"], "Remaining Passengers", observation_id)
            if occupancy != segment_end:
                raise ValueError(
                    f"{observation_id}: calculated remaining count {occupancy} does not match {segment_end}"
                )

        peak = max(row[3] for row in stops)
        peak_stop = next(row[0] for row in stops if row[3] == peak)
        context = {
            "observation_id": observation_id,
            "date": date.isoformat(),
            "day_of_week": weekday,
            "direction": direction,
            "train_number": train,
            "service_type": SERVICE_TYPE[train],
            "departure_time": departure,
        }
        for order, (station, boardings, exits, passengers, status) in enumerate(stops, start=1):
            stop_rows.append(
                {
                    **context,
                    "stop_order": order,
                    "stop_name": station,
                    "stop_status": status,
                    "boardings": "" if boardings is None else boardings,
                    "exits": "" if exits is None else exits,
                    "passengers_after_stop": passengers,
                    "initial_passengers": initial,
                }
            )
        trip_rows.append(
            {
                **context,
                "initial_passengers": initial,
                "total_boardings": total_boardings,
                "total_observed_exits": total_exits,
                "peak_passengers": peak,
                "peak_at_stop": peak_stop,
                "segment_end_passengers": segment_end,
            }
        )
    return stop_rows, trip_rows


def write_csv(path: Path, fields: list[str], rows: list[dict[str, object]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as output:
        writer = csv.DictWriter(output, fieldnames=fields, extrasaction="raise")
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT, help="Original .xlsx workbook")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR, help="Directory for generated CSV files")
    args = parser.parse_args()

    try:
        sheets = load_workbook(args.input)
        if set(sheets) != {"Inbound", "Outbound"}:
            raise ValueError(f"Expected Inbound and Outbound sheets, found {sorted(sheets)}")
        stop_rows: list[dict[str, object]] = []
        trip_rows: list[dict[str, object]] = []
        for sheet_name in ("Inbound", "Outbound"):
            stops, trips = rows_for_sheet(sheet_name, sheets[sheet_name])
            stop_rows.extend(stops)
            trip_rows.extend(trips)
        args.output_dir.mkdir(parents=True, exist_ok=True)
        write_csv(args.output_dir / "passenger-stops.csv", STOP_FIELDS, stop_rows)
        write_csv(args.output_dir / "trip-summary.csv", TRIP_FIELDS, trip_rows)
    except (OSError, KeyError, ValueError, zipfile.BadZipFile, ET.ParseError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    print(f"Wrote {len(stop_rows)} stop/checkpoint rows and {len(trip_rows)} trip rows to {args.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
