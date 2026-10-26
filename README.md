# cs424-project

## Data and processing

- `passenger-data.xlsx` is the original collected workbook. Keep it as the source data.
- `scripts/prepare_passenger_data.py` contains the reproducible transformation from the workbook to analysis-ready CSV files.
- `scripts/explore_passenger_data.py` recreates the exploratory figures from those processed files.
- `data/processed/passenger-stops.csv` is the tidy station-level dataset for visualizations.
- `data/processed/trip-summary.csv` contains derived, trip-level measures for service and weekday comparisons.
- `figures/exploratory/` contains the generated exploratory figures.

Recreate the processed files from the repository root with:

```text
python scripts/prepare_passenger_data.py
```

See Task 2 in `Assignment-2.md` for the transformation details and interpretation of the output fields.

Install the plotting dependencies listed in `requirements.txt`, then recreate the exploratory figures with:

```text
python scripts/explore_passenger_data.py
```

See Task 3 in `Assignment-2.md` for the plots and exploratory observations.
