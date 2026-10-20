# Class Size Forecasting

Capstone project — forecasting per-course enrollment demand for the UNO CS degree plan using Markov chain and discrete event simulation models.

## Quick start

```bash
pip install -r requirements.txt
streamlit run app/main.py
```

The interface accepts a course name, its initial enrollment, and its expected
growth rate per semester. Choose a forecast horizon of 1–12 semesters to view
the projected enrollment table and chart. The growth-rate baseline compounds
each course's rate independently and rounds projections to the nearest student;
it does not currently use the placeholder Markov or simulation models.

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
