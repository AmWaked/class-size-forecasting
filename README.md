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
