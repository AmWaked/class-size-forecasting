# Running the Enrollment Forecast Demo

These instructions start the local Streamlit app for forecasting course
enrollment and viewing the results.

## Setup and start

1. Open PowerShell in the project folder.
2. Create a virtual environment:

   ```powershell
   py -m venv .venv
   ```

3. Activate it:

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

   If PowerShell does not allow script activation, open Command Prompt in the
   project folder and run:

   ```cmd
   .venv\Scripts\activate.bat
   ```

4. Install the project dependencies:

   ```powershell
   python -m pip install -r requirements.txt
   ```

5. Start the app:

   ```powershell
   python -m streamlit run app/main.py
   ```

6. Open the local URL printed in the terminal by Streamlit.

## Try a Milestone 2 forecast

Under **Milestone 2 — Course Enrollment Forecast**, expand **Starting
enrollment by course** to view the initial counts. The sample uses 320
synthetic students across 11 courses and forecasts four semesters. The
default probabilities are hypothetical.

Click **Generate Markov Forecast**. The app displays the transition matrix,
forecast table, and chart. In semester 1, the expected enrollment is 30
for CIST1400 and 55 for CSCI1620.

Change the probability from CIST1400 to CSCI1620 from 0.40 to 0.50.
Press Enter, then click **Generate Markov Forecast** again. The semester 1
counts should change to 20 for CIST1400 and 65 for CSCI1620.

To try an invalid value, change the same probability to 0.80. Leave the
probability from CIST1400 to CSCI2030 at 0.30. Click **Generate Markov
Forecast** again. The app displays an error because the two probabilities
add up to 1.10. Change 0.80 back to 0.40 to restore the default.

## Try the Milestone 1 forecast

Expand **Milestone 1 — Four-State Baseline**.

Enter these initial enrollment counts:

| State | Enrollment |
| ----- | ---------: |
| CS1   |        100 |
| CS2   |         80 |
| CS3   |         50 |
| Done  |          0 |

Set **Semesters to forecast** to `2`, then click **Generate forecast**. The
app displays the projections in a table and chart. Expected projections are:

| Semester | CS1 |  CS2 |  CS3 | Done |
| -------- | --: | ---: | ---: | ---: |
| 1        |  20 |   96 |   74 |   40 |
| 2        |   4 | 35.2 | 91.6 | 99.2 |

The input counts must be non-negative whole numbers. The forecast horizon
must be between 1 and 12 semesters. Projected enrollment may be fractional
because the Markov model calculates expected values.
