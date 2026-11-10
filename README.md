# Class Size Forecasting

A capstone project for forecasting enrollment in the UNO computer-science degree progression using a Markov chain model and an interactive Streamlit dashboard.

## Overview

This project models student movement across four states:

- CS1
- CS2
- CS3
- Done

The current forecasting logic uses a fixed transition matrix in which:

- 20% of students remain in their current course state
- 80% move to the next state
- students in Done remain in Done

The app allows a user to enter current enrollment counts, choose a forecast horizon from 1 to 12 semesters, and view the projected enrollments in a table and chart.

## Features

- Interactive Streamlit interface for enrollment forecasting
- Markov-chain forecast for course progression states
- Input validation for:
  - non-negative integer enrollment counts
  - valid state names
  - valid probability matrix rows
  - forecast horizon bounds
- Projected enrollment table and line chart output
- Unit tests covering model behavior and validation rules

## Quick start

### 1) Create and activate a virtual environment

On Windows PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2) Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 3) Run the app

```powershell
python -m streamlit run app/main.py
```

Then open the local URL shown in the terminal.

## Example forecast

Enter these starting values:

| State | Enrollment |
|---|---:|
| CS1 | 100 |
| CS2 | 80 |
| CS3 | 50 |
| Done | 0 |

If you forecast 2 semesters, the expected projections are:

| Semester | CS1 | CS2 | CS3 | Done |
|---|---:|---:|---:|---:|
| 1 | 20 | 96 | 74 | 40 |
| 2 | 4 | 35.2 | 91.6 | 99.2 |

The app expects whole-number, non-negative enrollment values and a forecast horizon between 1 and 12 semesters.

## Project structure

```text
app/            Streamlit app, validation helpers, visualization, and baseline forecast logic
models/         Forecasting model implementations and transition logic
requirements.txt  Python dependencies
README.md        Project overview and setup guide
RUNNING_THE_DEMO.md  Step-by-step demo instructions
tests/           Automated pytest checks
data/            Local data directory for project-specific files (not committed)
```

## Model notes

The repo currently includes:

- a Markov model implementation in [models/markov.py](models/markov.py)
- transition logic in [models/markov_model.py](models/markov_model.py)
- a standalone per-course growth-rate baseline in [app/forecast.py](app/forecast.py)
- a CSV loading helper with formula-injection sanitization in [app/ingestion.py](app/ingestion.py)
- a simulation model stub in [models/simulation.py](models/simulation.py)

The primary interactive demo is the Streamlit app in [app/main.py](app/main.py). The growth-rate baseline and CSV helper are not currently connected to the UI. The simulation model is not implemented.

## Release notes

See [RELEASE_NOTES.md](RELEASE_NOTES.md) for release highlights and known limitations.

## Running tests

```powershell
pytest tests/ -v
```

## Notes

- Forecasted enrollment can be fractional because the model calculates expected values rather than integer counts.
- The work is designed as a forecasting prototype and planning tool rather than a production-grade enrollment system.
