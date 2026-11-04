"""Streamlit entry point for the Class Size Forecasting application."""

import pandas as pd
import streamlit as st

from models.markov import MarkovModel
from models.markov_model import states, transition_matrix
from app.input_validation import validate_all
from app.visualization import forecast_chart_data


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
