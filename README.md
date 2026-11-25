# Class Size Forecasting

Capstone project — forecasting per-course enrollment demand for the UNO CS degree plan using Markov chain and discrete event simulation models.

## Quick start

```bash
pip install -r requirements.txt
streamlit run app/main.py
```

The Streamlit application provides three forecasting models developed across the project milestones.

**Milestone 1 — Four-State Baseline:** Users can enter initial enrollment counts for CS1, CS2, CS3, and Done, select a forecast horizon of 1–12 semesters, and view projected enrollment in a table and chart. The model uses fixed transition probabilities: 20% remain in the current state and 80% advance to the next state, while students in Done remain there.

**Milestone 2 — Eleven-Course Forecast:** The application forecasts enrollment across 11 Computer Science courses using a prerequisite-based Markov model. Users can edit course progression probabilities and generate a four-semester forecast, including a transition matrix, enrollment table, and line chart. Starting enrollment values are synthetic.

**Milestone 3 — Branching Markov Forecast:** The application models students progressing through CS1, CS2, and CS3 before entering two parallel course pathways: CS4 → CS6 and CS5 → CS7. Users can select a forecast horizon of 1–12 semesters and generate a nine-column forecast displayed in a table and line chart. Starting enrollment and transition probabilities are fixed and hypothetical.

All three models are proofs of concept and do not currently use actual UNO enrollment restates. Choose a forecast horizon of 1–12 semesters to view the projected
enrollment records.

## Release notes

### Code Milestone 3 — November 2026

Milestone 3 introduces a branching Markov forecasting model that allows students to progress through two parallel course pathways after completing CS3.

The model begins with CS1 → CS2 → CS3 and then separates into two branches:

- **Branch 1:** CS4 → CS6 → Done CS6
- **Branch 2:** CS5 → CS7 → Done CS7

Students completing CS3 enter both branches, allowing the model to forecast enrollment across multiple course pathways.

#### Implemented Features

- Developed two additional Markov transition matrices for the branching course pathways.
- Combined the original Markov chain and both branches into one forecasting function.
- Generated a nine-column NumPy array containing forecast results for each semester.
- Integrated the branching forecasting function into the Streamlit application.
- Allowed users to select a forecast horizon of 1–12 semesters.
- Displayed projected enrollment in a table and line chart.
- Maintained the Milestone 1 and Milestone 2 forecasting demonstrations.

#### Forecast Output

The model produces forecasts for seven courses (CS1, CS2, CS3, CS4, CS6, CS5, and CS7) and two cumulative branch-completion states (Done CS6 and Done CS7).

#### QA Testing and Validation

The Milestone 3 branching forecast was tested using forecast horizons of 1, 4, and 12 semesters. The application returned one forecast row per requested semester and nine forecast values per row in the expected order: CS1, CS2, CS3, CS4, CS6, CS5, CS7, Done CS6, and Done CS7.

The expected values for the first two semesters of the four-semester forecast were verified:

- Semester 1: 25, 105, 90, 80, 0, 80, 0, 0, 0
- Semester 2: 6.25, 50.25, 91.5, 104, 48, 84, 68, 0, 0

Automated tests also verify the forecast dimensions, course-label ordering, expected calculations, and that forecast values remain finite and non-negative.

The Streamlit integration was manually tested to confirm that forecast results are displayed in both the table and line chart.

#### Model Assumptions and Limitations

- Starting enrollment is synthetic and fixed at 100 students each in CS1, CS2, and CS3.
- Transition probabilities are fixed and hypothetical rather than estimated from historical UNO enrollment data.
- Each student completing CS3 enters both modeled branches, so row totals can exceed the original 300 students.
- Done CS6 and Done CS7 represent cumulative branch-completion counts rather than course enrollment.
- The Streamlit interface restricts forecasts to 1–12 semesters; the forecasting function itself relies on the interface to enforce this range.
- The model remains a proof of concept and should not be interpreted as a validated prediction of actual UNO enrollment.

### Code Milestone 2 — November 2026

Milestone 2 introduces an 11-course Markov enrollment forecasting model for the UNO Computer Science degree plan.

#### Implemented features:
- Dynamic generation of a course transition matrix using prerequisite relationships.
- Editable course progression probabilities through the Streamlit interface.
- Validation of probability values and outgoing transition totals.
- Four-semester enrollment forecasts calculated using NumPy.
- Display of the transition matrix, forecast table, and line chart.
- Continued availability of the Milestone 1 four-state Markov model.

#### Current limitations:
- Starting enrollment counts and progression probabilities are hypothetical.
- Individual student prerequisite eligibility is not fully enforced.
- Students taking multiple courses simultaneously are not fully represented.
- Discrete event simulation is not yet implemented.
- Historical enrollment data is not yet integrated into the forecasting interface.

Milestone 2 is a working proof of concept rather than a validated prediction of actual UNO enrollment.


### Code Milestone 1 — Four-State Baseline

The current submission includes a working Streamlit interface for entering
initial enrollment in CS1, CS2, CS3, and Done, selecting a forecast horizon of
1–12 semesters, and viewing projected enrollment in a table and chart. The
Markov model uses fixed transition probabilities rather than probabilities
estimated from historical enrollment data. Forecasts may be fractional because
they represent expected enrollment.

The discrete event simulation model is not implemented. The CSV ingestion
helper and growth-rate forecast are not connected to the Streamlit interface.

## Branches

- `main` — Contains the main project code and the Milestone 1 four-state Markov forecasting model.
- `feature/markov-milestone2` — Contains the Milestone 2 implementation, including the 11-course dynamic Markov transition matrix, editable progression probabilities, and multi-semester enrollment forecasting.
- `gilberto` — Development and testing branch.
- `michele` — QA and testing branch.

For Code Milestone 2, review `feature/markov-milestone2` for the new forecasting features until they are merged into `main`.

## Project structure

```
app/          GUI, data ingestion, visualization
models/       Forecasting model implementations (common interface)
data/         Local data only — never committed (gitignored)
tests/        pytest test suite
docs/         Project documentation
```

## Running tests

```bash
pytest tests/ -v
```
