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

The current submission includes a working Streamlit interface for entering
initial enrollment in CS1, CS2, CS3, and Done, selecting a forecast horizon of
1–12 semesters, and viewing projected enrollment in a table and chart. The
Markov model uses fixed transition probabilities rather than probabilities
estimated from historical enrollment data. Forecasts may be fractional because
they represent expected enrollment.

The discrete event simulation model is not implemented. The CSV ingestion
helper and growth-rate forecast are not connected to the Streamlit interface.

## Branches

Review `main` as the final submission branch. `gilberto` is my development and
testing branch, where I check my changes before committing them to `main`; it
is not a separate implementation or feature branch.

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
