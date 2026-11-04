# Release Notes

## Version 0.1.0 - Initial project release

### Highlights

- Added an interactive Streamlit app for forecasting CS-state enrollment.
- Implemented a four-state Markov-chain model for CS1, CS2, CS3, and Done progression.
- Added fixed transition probabilities: 20% remain in each state, 80% advance, and Done remains complete.
- Added input validation for enrollment counts, probability matrices, and forecast horizon limits.
- Included a simple growth-rate forecasting baseline for comparison and testing.
- Added automated tests to validate forecast logic and validation rules.

### User-visible behavior

- Users can enter initial enrollment for each state and select a forecast horizon from 1 to 12 semesters.
- The app displays a projected enrollment table and chart for all states.
- The model accepts non-negative whole-number enrollments and rejects invalid values.

### Known limitations

- The Markov model uses fixed transition probabilities rather than historical calibration.
- The simulation model is still a stub and is not yet connected to the UI.
- Forecast output may include fractional enrollments because expected values are calculated across transitions.

### Project status

This release establishes the core project structure and forecasting workflow, while leaving room for future data-driven calibration and richer simulation features.
