# Passenger Data Dictionary

Each row represents one observed commute. Passenger counts describe the observed train car, rather than the entire train. The workbook uses separate `Inbound` and `Outbound` sheets to indicate travel direction.

Types: **Temporal** denotes dates or times; **Categorical** denotes labels or identifiers; **Quantitative** denotes nonnegative integer passenger counts. Train numbers are categorical identifiers even though they contain digits.

A blank station count indicates a skipped stop; `0` means the train stopped but no passengers performed that action. 

## Inbound

| Attribute | Type | Description | Example |
| --- | --- | --- | --- |
| `Date` | Temporal | Calendar date of the commute. | `2026-09-21` |
| `Day of Week` | Categorical | Weekday on which the commute occurred. | `Monday` |
| `Train Number` | Categorical | Identifier of the train service observed. | `640` |
| `Departure Time - Cary` | Temporal | Departure time from Cary, expressed in local time. | `08:24` |
| `Existing Passengers` | Quantitative | Passengers already in the observed car before boarding and exiting at Cary. | `7` |
| `Cary - Getting On` | Quantitative | Passengers boarding the observed car at Cary. | `2` |
| `Cary - Getting Off` | Quantitative | Passengers exiting the observed car at Cary. | `0` |
| `Fox River Grove - Getting On` | Quantitative | Passengers boarding the observed car at Fox River Grove. | `2` |
| `Fox River Grove - Getting Off` | Quantitative | Passengers exiting the observed car at Fox River Grove. | `0` |
| `Barrington - Getting On` | Quantitative | Passengers boarding the observed car at Barrington. | `3` |
| `Barrington - Getting Off` | Quantitative | Passengers exiting the observed car at Barrington. | `0` |
| `Palatine - Getting On` | Quantitative | Passengers boarding the observed car at Palatine. | `7` |
| `Palatine - Getting Off` | Quantitative | Passengers exiting the observed car at Palatine. | `0` |
| `Arlington Park - Getting On` | Quantitative | Passengers boarding the observed car at Arlington Park. | `3` |
| `Arlington Park - Getting Off` | Quantitative | Passengers exiting the observed car at Arlington Park. | `1` |
| `Arlington Heights - Getting On` | Quantitative | Passengers boarding the observed car at Arlington Heights. | `6` |
| `Arlington Heights - Getting Off` | Quantitative | Passengers exiting the observed car at Arlington Heights. | `0` |
| `Mt. Prospect - Getting On` | Quantitative | Passengers boarding the observed car at Mt. Prospect. | `3` |
| `Mt. Prospect - Getting Off` | Quantitative | Passengers exiting the observed car at Mt. Prospect. | `0` |
| `Cumberland - Getting On` | Quantitative | Passengers boarding the observed car at Cumberland. | `1` |
| `Cumberland - Getting Off` | Quantitative | Passengers exiting the observed car at Cumberland. | `0` |
| `Des Plaines - Getting On` | Quantitative | Passengers boarding the observed car at Des Plaines. | `4` |
| `Des Plaines - Getting Off` | Quantitative | Passengers exiting the observed car at Des Plaines. | `0` |
| `Dee Road - Getting On` | Quantitative | Passengers boarding the observed car at Dee Road. | `0` |
| `Dee Road - Getting Off` | Quantitative | Passengers exiting the observed car at Dee Road. | `0` |
| `Park Ridge - Getting On` | Quantitative | Passengers boarding the observed car at Park Ridge. | `0` |
| `Park Ridge - Getting Off` | Quantitative | Passengers exiting the observed car at Park Ridge. | `0` |
| `Edison Park - Getting On` | Quantitative | Passengers boarding the observed car at Edison Park. | `0` |
| `Edison Park - Getting Off` | Quantitative | Passengers exiting the observed car at Edison Park. | `0` |
| `Norwood Park - Getting On` | Quantitative | Passengers boarding the observed car at Norwood Park. | `0` |
| `Norwood Park - Getting Off` | Quantitative | Passengers exiting the observed car at Norwood Park. | `0` |
| `Gladstone Park - Getting On` | Quantitative | Passengers boarding the observed car at Gladstone Park. | `0` |
| `Gladstone Park - Getting Off` | Quantitative | Passengers exiting the observed car at Gladstone Park. | `0` |
| `Jefferson Park - Getting On` | Quantitative | Passengers boarding the observed car at Jefferson Park. | `2` |
| `Jefferson Park - Getting Off` | Quantitative | Passengers exiting the observed car at Jefferson Park. | `1` |
| `Irving Park - Getting On` | Quantitative | Passengers boarding the observed car at Irving Park. | `0` |
| `Irving Park - Getting Off` | Quantitative | Passengers exiting the observed car at Irving Park. | `0` |
| `Clybourn - Getting On` | Quantitative | Passengers boarding the observed car at Clybourn. | `1` |
| `Clybourn - Getting Off` | Quantitative | Passengers exiting the observed car at Clybourn. | `2` |
| `Chicago OTC - Total` | Quantitative | Calculated passengers arriving at Chicago OTC and exiting at this terminal: existing passengers plus all boardings minus all exits before Chicago OTC. | `37` |

## Outbound

| Attribute | Type | Description | Example |
| --- | --- | --- | --- |
| `Date` | Temporal | Calendar date of the commute. | `2026-09-21` |
| `Day of Week` | Categorical | Weekday on which the commute occurred. | `Monday` |
| `Train Number` | Categorical | Identifier of the train service observed. | `627` |
| `Departure Time - Chicago OTC` | Temporal | Departure time from Chicago OTC, expressed in local time. | `12:35` |
| `Chicago OTC - Getting On` | Quantitative | Calculated passengers boarding the observed car at the starting station: remaining passengers after Cary plus later exits minus later boardings. | `23` |
| `Clybourn - Getting On` | Quantitative | Passengers boarding the observed car at Clybourn. | `1` |
| `Clybourn - Getting Off` | Quantitative | Passengers exiting the observed car at Clybourn. | `0` |
| `Irving Park - Getting On` | Quantitative | Passengers boarding the observed car at Irving Park. | `1` |
| `Irving Park - Getting Off` | Quantitative | Passengers exiting the observed car at Irving Park. | `1` |
| `Jefferson Park - Getting On` | Quantitative | Passengers boarding the observed car at Jefferson Park. | `2` |
| `Jefferson Park - Getting Off` | Quantitative | Passengers exiting the observed car at Jefferson Park. | `1` |
| `Gladstone Park - Getting On` | Quantitative | Passengers boarding the observed car at Gladstone Park. | `0` |
| `Gladstone Park - Getting Off` | Quantitative | Passengers exiting the observed car at Gladstone Park. | `0` |
| `Norwood Park - Getting On` | Quantitative | Passengers boarding the observed car at Norwood Park. | `0` |
| `Norwood Park - Getting Off` | Quantitative | Passengers exiting the observed car at Norwood Park. | `1` |
| `Edison Park - Getting On` | Quantitative | Passengers boarding the observed car at Edison Park. | `0` |
| `Edison Park - Getting Off` | Quantitative | Passengers exiting the observed car at Edison Park. | `0` |
| `Park Ridge - Getting On` | Quantitative | Passengers boarding the observed car at Park Ridge. | `0` |
| `Park Ridge - Getting Off` | Quantitative | Passengers exiting the observed car at Park Ridge. | `0` |
| `Dee Road - Getting On` | Quantitative | Passengers boarding the observed car at Dee Road. | `0` |
| `Dee Road - Getting Off` | Quantitative | Passengers exiting the observed car at Dee Road. | `0` |
| `Des Plaines - Getting On` | Quantitative | Passengers boarding the observed car at Des Plaines. | `0` |
| `Des Plaines - Getting Off` | Quantitative | Passengers exiting the observed car at Des Plaines. | `2` |
| `Cumberland - Getting On` | Quantitative | Passengers boarding the observed car at Cumberland. | `0` |
| `Cumberland - Getting Off` | Quantitative | Passengers exiting the observed car at Cumberland. | `0` |
| `Mt. Prospect - Getting On` | Quantitative | Passengers boarding the observed car at Mt. Prospect. | `1` |
| `Mt. Prospect - Getting Off` | Quantitative | Passengers exiting the observed car at Mt. Prospect. | `3` |
| `Arlington Heights - Getting On` | Quantitative | Passengers boarding the observed car at Arlington Heights. | `0` |
| `Arlington Heights - Getting Off` | Quantitative | Passengers exiting the observed car at Arlington Heights. | `2` |
| `Arlington Park - Getting On` | Quantitative | Passengers boarding the observed car at Arlington Park. | `0` |
| `Arlington Park - Getting Off` | Quantitative | Passengers exiting the observed car at Arlington Park. | `5` |
| `Palatine - Getting On` | Quantitative | Passengers boarding the observed car at Palatine. | `0` |
| `Palatine - Getting Off` | Quantitative | Passengers exiting the observed car at Palatine. | `7` |
| `Barrington - Getting On` | Quantitative | Passengers boarding the observed car at Barrington. | `0` |
| `Barrington - Getting Off` | Quantitative | Passengers exiting the observed car at Barrington. | `0` |
| `Fox River Grove - Getting On` | Quantitative | Passengers boarding the observed car at Fox River Grove. | `0` |
| `Fox River Grove - Getting Off` | Quantitative | Passengers exiting the observed car at Fox River Grove. | `0` |
| `Cary - Getting On` | Quantitative | Passengers boarding the observed car at Cary. | `0` |
| `Cary - Getting Off` | Quantitative | Passengers exiting the observed car at Cary. | `4` |
| `Remaining Passengers` | Quantitative | Passengers still in the observed car after boarding and exiting at Cary; these passengers continue beyond the observed commute. | `2` |

## Count calculations

Inbound: `Chicago OTC - Total = Existing Passengers + sum(Getting On) - sum(Getting Off)` across the observed stops before Chicago OTC.

Outbound: `Chicago OTC - Getting On = Remaining Passengers + sum(later Getting Off) - sum(later Getting On)` across the observed stops from Clybourn through Cary.

Example values illustrate valid entries; a `0` example for a station skipped in the sample row does not replace that row's blank cell.
