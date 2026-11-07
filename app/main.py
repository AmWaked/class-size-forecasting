"""Streamlit entry point for the Class Size Forecasting application."""

import pandas as pd
import streamlit as st
import numpy as np

from models.markov import MarkovModel
from models.markov_model import states, transition_matrix
from app.input_validation import validate_all
from app.visualization import forecast_chart_data
from app.forecast import build_forecast

from app.markov_forecast import (
    courses,
    passing_rates,
    build_transition_matrix,
    predict_enrollment
)


st.set_page_config(page_title="Class Size Forecasting", page_icon="📚", layout="wide")
st.title("Class Size Forecasting")
st.write(
    "Enter the current enrollment in each course-plan state to forecast enrollment "
    "over the next several semesters."
)
st.caption(
    "Forecasts use fixed transition probabilities: 20% remain in each course state "
    "and 80% advance to the next state; students in Done remain there."
)

with st.form("enrollment_forecast"):
    st.write("Initial enrollment by state")
    enrollment_columns = st.columns(len(states))
    initial_enrollment = {}
    for column, state in zip(enrollment_columns, states):
        with column:
            initial_enrollment[state] = st.number_input(
                state,
                min_value=0,
                value=0,
                step=1,
                key=f"initial_{state}",
            )
    semesters_ahead = st.number_input(
        "Semesters to forecast",
        min_value=1,
        max_value=12,
        value=4,
        step=1,
    )
    submitted = st.form_submit_button("Generate forecast", type="primary")

if submitted:
    try:
        validate_all(initial_enrollment, transition_matrix, int(semesters_ahead))
        model = MarkovModel()
        model.fit(initial_enrollment)
        forecast = pd.DataFrame(
            model.predict(int(semesters_ahead)),
            columns=("State", "Semester", "Projected enrollment"),
        )
    except ValueError as error:
        st.error(str(error))
    else:
        st.subheader("Forecast results")
        st.dataframe(forecast, hide_index=True, use_container_width=True)
        st.subheader("Enrollment by semester")
        st.line_chart(
            forecast_chart_data(forecast, category_column="State"),
            y_label="Projected enrollment",
        )

# Markov forecasting section
st.divider()
st.header("Markov Course Enrollment Forecast")

st.write(
    "Edit the progression probabilities for each course "
    "to explore how they affect future enrollment."
)

# Display default probabilities in an editable table
rate_rows = []

for course, next_courses in passing_rates.items():
    for next_course, rate in next_courses.items():
        rate_rows.append({
            "Current course": course,
            "Next course": next_course,
            "Probability": rate
        })

rates_df = pd.DataFrame(rate_rows)

edited_rates = st.data_editor(
    rates_df,
    hide_index=True,
    disabled=["Current course", "Next course"],
    use_container_width=True
)

# Generate a Markov forecast using the edited probabilities
if st.button("Generate Markov Forecast"):
    try:
        # Copy the default probabilities
        updated_rates = {
            course: next_courses.copy()
            for course, next_courses in passing_rates.items()
        }

        # Replace defaults with the user's edited values
        for _, row in edited_rates.iterrows():
            course = row["Current course"]
            next_course = row["Next course"]
            rate = float(row["Probability"])

            if not np.isfinite(rate) or not 0 <= rate <= 1:
                raise ValueError("Probabilities must be between 0 and 1.")

            updated_rates[course][next_course] = rate

        # Rebuild the transition matrix
        matrix = build_transition_matrix(updated_rates)


        st.success("Transition matrix updated successfully!")
        st.dataframe(
            pd.DataFrame(matrix, index=courses, columns=courses)
        )

        # Hypothetical enrollment for the 11 courses
        students = np.array([100, 50, 30, 40, 25, 20, 15, 10, 12, 10, 8])

        # Calculate enrollment projections for four semesters
        predictions = predict_enrollment(
            students, matrix, semesters_ahead=4
        )

        # Organize the predictions into a table
        forecast_df = pd.DataFrame(predictions, columns=courses)
        forecast_df.index = range(1, 5)
        forecast_df.index.name = "Semester"

        # Display the enrollment forecast
        st.subheader("Markov Enrollment Forecast")
        st.dataframe(forecast_df)

        # Display the forecast as a line chart
        st.line_chart(forecast_df)

    except (ValueError, TypeError) as error:
        st.error(str(error))
