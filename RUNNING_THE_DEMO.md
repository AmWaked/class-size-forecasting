# Running the Enrollment Forecast Demo

These instructions start the local Streamlit app for entering initial
enrollment and viewing the forecast.

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

## Try a sample forecast

Enter these initial enrollment counts:

| State | Enrollment |
|---|---:|
| CS1 | 100 |
| CS2 | 80 |
| CS3 | 50 |
| Done | 0 |

Set **Semesters to forecast** to `2`, then click **Generate forecast**. The
app displays the projections in a table and chart. Expected projections are:

| Semester | CS1 | CS2 | CS3 | Done |
|---|---:|---:|---:|---:|
| 1 | 20 | 96 | 74 | 40 |
| 2 | 4 | 35.2 | 91.6 | 99.2 |

The input counts must be non-negative whole numbers. The forecast horizon
must be between 1 and 12 semesters. Projected enrollment may be fractional
because the Markov model calculates expected values.
