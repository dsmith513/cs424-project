#### Task 1: Implementing interaction

I selected the passenger-load line visualization from Assignment 2. It answers revised domain question 2: how passenger load changes along the observed segment and where it peaks. The data describes one observed train car on the Cary–Chicago OTC segment. Each mark is a recorded passenger count after an observed stop or terminal checkpoint. A connecting line guides the eye along the route and does not represent measurements between stops.

I implemented two versions from the same `data/processed/passenger-stops.csv` and `data/processed/trip-summary.csv` files:

[Static passenger-load overview](visualizations/assignment3-static.html) shows four small multiples, one for each direction and train. Every observed trip profile is drawn in gray, with the median and interquartile range summarized for its service group. The common passenger-count scale supports comparison across the panels. A table lists each trip's date, weekday, peak count, and peak stop. This lets a participant compare all service profiles and inspect trip-level peaks without filtering.

[Interactive passenger-load explorer](visualizations/assignment3-interactive.html) has direction, train, and weekday filters plus a trip selector. Filtering recalculates the median and interquartile range for the displayed subset. Selecting a trip highlights its full route profile in orange and marks its peak. When a weekday is selected, a dashed line preserves the all-weekday median for that train as context. A checkbox reveals the other individual trip profiles.

The weekday filter supports a comparison of observed weekday-service patterns, while the date selector helps locate a trip's peak and compare its path with other trips. The static panels expose those groups and trips together. The interactive version lets a participant focus on a subset and a particular date. Both versions therefore provide the information for the same analytical tasks, with the static version giving an all-at-once overview and the interactive version reducing visual clutter during focused comparisons.

The interaction is available using native keyboard-accessible select controls and a checkbox. The pages are self-contained and can be opened directly in a browser, including from a local copy of the project. Rebuild them from the repository root with:

```text
python scripts/build_assignment3_visualizations.py
```

The sample pairs each train with a fixed set of weekdays and departure time. The weekday comparison is descriptive and cannot establish an independent weekday or service-type effect. The band summarizes the observed trips only, and the profiles represent the sampled car rather than the entire train.

#### Task 2: Evaluation design

##### Evaluation question and hypothesis

**Evaluation question:** 
Does filtering to a weekday/service subset and highlighting a trip help people compare passenger-load patterns more quickly and accurately than reading the static overview?

**Hypothesis:** 
Participants will complete the interactive tasks in less time, with accuracy at least as high as in the static condition. The weekday filter should be most useful for comparing the spread of trip peaks. The train filter should help focus attention on the route profile being compared.

##### Analytical tasks and answer key

Each task has two variants. A participant sees one variant of each task in each condition, never the same variant twice. Both tasks require comparing several observations. Task 1 compares the spread of five trip peaks for each of two weekdays. Task 2 compares median passenger counts at two route locations. Task 1 relates to Assignment 2's weekday-service question, and Task 2 relates to its passenger-load-along-the-route question.

| Task | Variant A | Variant B |
| --- | --- | --- |
| 1. Compare weekday variability in peak load | **Inbound train 638:** For Tuesday and Thursday trips, calculate each weekday's range of trip peak passenger counts (highest minus lowest). Which weekday has the wider range, and by how many passengers? | **Outbound train 655:** For Tuesday and Thursday trips, calculate each weekday's range of trip peak passenger counts (highest minus lowest). Which weekday has the wider range, and by how many passengers? |
| 2. Compare passenger load by location | **Inbound train 640:** Using the all-weekday median profile, compare passengers after Palatine with passengers after Jefferson Park. Which stop has the higher median, and by about how many passengers? | **Inbound train 638:** Using the all-weekday median profile, compare passengers after Palatine with passengers after Jefferson Park. Which stop has the higher median, and by about how many passengers? |

**Researcher answer key (do not show participants before the session):**

- **Task 1A:** Train 638 inbound peaks are Tuesday 50, 52, 38, 45, 46 (range 14) and Thursday 44, 46, 46, 48, 51 (range 7). Tuesday is wider by **7 passengers**.
- **Task 1B:** Train 655 outbound peaks are Tuesday 42, 41, 39, 40, 44 (range 5) and Thursday 44, 40, 36, 43, 48 (range 12). Thursday is wider by **7 passengers**.
- **Task 2A:** Train 640 inbound median counts after Palatine and Jefferson Park are 21 and 38. Jefferson Park is higher by **17 passengers**.
- **Task 2B:** Train 638 inbound median counts after Palatine and Jefferson Park are 13.5 and 44.5. Jefferson Park is higher by **31 passengers**.

For Task 1, score the weekday choice and the difference separately. Accept a difference within 1 passenger of 7. For Task 2, score the higher stop and the reported difference separately. Accept a difference within 2 passengers of the answer key because values must be read from the plotted median. A task is fully correct only when both parts are correct. Keep the component scores to distinguish a comparison error from a chart-reading estimate.

##### Participants, counterbalancing, and procedure

Recruit **10 participants** who are not involved in building the visualization. Use participant IDs P01–P10 and randomly assign two participants to each sequence below. If the available sample is larger, add participants in balanced blocks of four. Each person uses both versions and answers two questions per version, for four timed tasks total.

| Sequence (2 participants each) | First condition and task set | Second condition and task set |
| --- | --- | --- |
| 1 | Static, set A (Tasks 1A and 2A) | Interactive, set B (Tasks 1B and 2B) |
| 2 | Static, set B (Tasks 1B and 2B) | Interactive, set A (Tasks 1A and 2A) |
| 3 | Interactive, set A (Tasks 1A and 2A) | Static, set B (Tasks 1B and 2B) |
| 4 | Interactive, set B (Tasks 1B and 2B) | Static, set A (Tasks 1A and 2A) |

This gives five participants each condition order, and each task variant is assigned to each condition equally often. Within each two-person sequence, give one participant Task 1 then Task 2 in the first condition and Task 2 then Task 1 in the second. Give the other participant the reverse task order. This balances task order as well.

1. Use the same computer, browser, window size, and zoom for everyone. Open the two local HTML pages from Task 1. Both use the same passenger-count axis range. Reset the interactive page before each task. Begin with all weekdays selected, and let participants change controls as needed.
2. Read the participant instructions below. Give a 60-second untimed orientation to the legends and controls using train 627, which does not appear in the scored variants. Do not reveal answers or give correctness feedback. Give the same amount of orientation time for both versions.
3. Present the first condition's two tasks in the assigned order. Start a stopwatch when the task prompt and visualization are visible. Stop when the participant commits to an answer. Allow up to 180 seconds per task. Record an unanswered timeout as 180 seconds and incorrect.
4. Give a one-minute break, switch to the other version, and present its two tasks in the assigned order. Do not revisit or discuss earlier answers.
5. After each answer, ask for confidence on a 1–5 scale (1 = not confident, 5 = very confident). Record the response verbatim and, in the interactive condition, tally filter, date-selection, and checkbox changes.

**Participant instructions:** “The visualization shows passenger counts in one observed train car along the Cary–Chicago OTC segment. Counts are recorded after observed stops. The lines guide the eye between observations. The dark line is the median and the shaded band shows the middle half of the trips. Use the visualization to answer each question. You may use any available controls. Please give your best answer and tell me when you are done.”

##### Pilot and measurements

Before the main sessions, pilot the procedure with two people who will not join the main sample. Use opposite condition orders. Ask them afterward which question or chart element was unclear. Revise wording or orientation if either participant interprets a task differently, cannot locate the required values, or reaches the time limit. Also check that neither task is answered immediately without comparing the requested observations. Keep the answer key and scoring tolerances fixed after piloting begins. If a task needs substantive revision, rerun the pilot with new participants.

Record one row per participant-task in [the results template](evaluation/task2-results-template.csv). The required quantitative measures are **task accuracy** (full correctness and the component scores) and **completion time in seconds**. Confidence and number of interactive control changes are secondary measures. Compare static and interactive results within participant and task type, and report task variants separately as well as pooled by condition. With eight participants, summarize paired differences and individual results. Treat the outcome as a small class evaluation rather than a broad claim about all users.

#### Task 3: Conducting the evaluation

#### Task 4: Quantitative analysis

#### Task 5: Reflection and recommendations
