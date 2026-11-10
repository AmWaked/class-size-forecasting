# Class Size Forecasting

Capstone project — forecasting per-course enrollment demand for the UNO CS degree plan using Markov chain and discrete event simulation models.

## Quick start

```bash
pip install -r requirements.txt
streamlit run app/main.py
```

The interface accepts initial enrollment counts for the CS1, CS2, CS3, and Done
states. Choose a forecast horizon of 1–12 semesters to view the projected
enrollment table and chart. The Markov forecast uses fixed probabilities: 20%
of students remain in each course state, 80% advance to the next state, and
students in Done remain there.

## Release notes

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
