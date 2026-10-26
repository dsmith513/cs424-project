# cs424-project

- `passenger-data.xlsx` is the original collected workbook. Keep it as the source data.
- `scripts/prepare_passenger_data.py` contains the reproducible transformation from the workbook to analysis-ready CSV files.
- `scripts/explore_passenger_data.py` recreates the exploratory figures from those processed files.
- `scripts/implement_visualizations.py` renders the Assignment 1 sketch implementations.
- `scripts/build_interactive_visualization.py` builds a self-contained coordinated HTML explorer.
- `scripts/build_refined_visualization.py` builds a separate explorer that includes the Task 6 line-chart refinements.
- `scripts/render_line_refinement.py` recreates the two line-chart iteration evidence figures.
- `data/processed/passenger-stops.csv` is the tidy station-level dataset for visualizations.
- `data/processed/trip-summary.csv` contains derived, trip-level measures for service and weekday comparisons.
- `figures/exploratory/` contains the generated exploratory figures.
- `figures/implemented/` contains the four implemented sketch figures.
- `figures/iterations/` contains evidence for the line-chart refinements.
- `visualizations/passenger-explorer.html` is the interactive version with linked trip selection.
- `visualizations/passenger-explorer-refined.html` is the refined interactive version used in Task 7.

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

Recreate the implemented sketch figures with:

```text
python scripts/implement_visualizations.py
```

See Task 4 in `Assignment-2.md` for the design choices and limitations of each direction.

Recreate the interactive explorer after preparing the processed CSV files with:

```text
python scripts/build_interactive_visualization.py
```

Open `visualizations/passenger-explorer.html` in a browser. See Task 5 in `Assignment-2.md` for how the views coordinate.

Build the separate refined explorer with:

```text
python scripts/build_refined_visualization.py
```

Open `visualizations/passenger-explorer-refined.html` in a browser. This page adds the median and interquartile band, selected-trip highlight, and peak marker while preserving the Task 5 explorer unchanged. See Task 7 in `Assignment-2.md` for the current design.

After preparing the processed CSV files and installing the plotting dependencies from `requirements.txt`, run:

```text
python scripts/render_line_refinement.py
```

This recreates the two refinement figures in `figures/iterations/`: `line-iteration-1.png` (median and interquartile range across the observed train 640 trips) and `line-iteration-2.png` (the same profile with the September 21 trip highlighted). Task 6 in `Assignment-2.md` explains the design changes.
