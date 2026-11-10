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

# --- milestone 1: four-state baseline model ---
with st.expander("Milestone 1 — Four-State Baseline", expanded=False):
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

# --- milestone 2: 11-course markov forecast ---
st.divider()
st.header("Milestone 2 — Course Enrollment Forecast")

st.write(
    "Forecast enrollment across 11 UNO CS courses using a prerequisite-based "
    "Markov chain. Edit the progression probabilities below and generate "
    "a forecast to see how changes affect projected enrollment."
)

#synthetic starting enrollment used for the proof of concept
#not derived from UNO records
default_students = [100, 50, 30, 40, 25, 20, 15, 10, 12, 10, 8]
num_semesters = 4

st.caption(
    f"Starting enrollment is synthetic (total {sum(default_students)} students "
    f"across {len(courses)} courses). The forecast runs {num_semesters} semesters."
)

#show the starting counts so the viewer knows what goes in
with st.expander("Starting enrollment by course"):
    st.dataframe(
        pd.DataFrame({"Course": courses, "Students": default_students}),
        hide_index=True,
        use_container_width=True,
    )

#build the editable probability table from the defaults
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

if st.button("Generate Markov Forecast"):
    try:
        #copy defaults then overlay edits
        updated_rates = {
            course: next_courses.copy()
            for course, next_courses in passing_rates.items()
        }

        for _, row in edited_rates.iterrows():
            course = row["Current course"]
            next_course = row["Next course"]
            rate = float(row["Probability"])

            if not np.isfinite(rate) or rate < 0 or rate > 1:
                raise ValueError(
                    f"Probability for {course} -> {next_course} must be "
                    f"between 0 and 1 (got {rate})."
                )

            updated_rates[course][next_course] = rate

        matrix = build_transition_matrix(updated_rates)

        st.success("Transition matrix rebuilt.")
        st.dataframe(
            pd.DataFrame(matrix, index=courses, columns=courses)
        )

        students = np.array(default_students)
        predictions = predict_enrollment(students, matrix, semesters_ahead=num_semesters)

        forecast_df = pd.DataFrame(predictions, columns=courses)
        forecast_df.index = range(1, num_semesters + 1)
        forecast_df.index.name = "Semester"

        st.subheader("Projected Enrollment")
        st.dataframe(forecast_df)
        st.line_chart(forecast_df)

    except (ValueError, TypeError) as error:
        st.error(str(error))
