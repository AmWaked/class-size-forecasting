"""Streamlit entry point for the Class Size Forecasting application."""

import pandas as pd
import streamlit as st

from app.forecast import build_forecast
from app.visualization import forecast_chart_data


st.set_page_config(page_title="Class Size Forecasting", page_icon="📚", layout="wide")
st.title("Class Size Forecasting")
st.write(
    "Enter each course's current enrollment and expected growth per semester "
    "to explore a simple enrollment baseline."
)
st.caption(
    "This baseline applies each course's growth rate independently each semester; "
    "it does not use the unfinished Markov or simulation models."
)

with st.form("enrollment_forecast"):
    enrollment_data = st.data_editor(
        pd.DataFrame(
            {
                "Course": pd.Series(dtype="string"),
                "Initial enrollment": pd.Series(dtype="int64"),
                "Growth rate per semester (%)": pd.Series(dtype="float64"),
            }
        ),
        num_rows="dynamic",
        hide_index=True,
        use_container_width=True,
        column_config={
            "Course": st.column_config.TextColumn("Course", required=True),
            "Initial enrollment": st.column_config.NumberColumn(
                "Initial enrollment", min_value=0, step=1, format="%d"
            ),
            "Growth rate per semester (%)": st.column_config.NumberColumn(
                "Growth rate per semester (%)",
                help="For example, enter 5 for 5% growth or -2 for 2% decline.",
                min_value=-100.0,
                step=0.5,
                format="%.1f%%",
            ),
        },
        key="enrollment_data",
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
        forecast = build_forecast(enrollment_data, int(semesters_ahead))
    except ValueError as error:
        st.error(str(error))
    else:
        st.subheader("Forecast results")
        st.dataframe(forecast, hide_index=True, use_container_width=True)
        st.subheader("Enrollment by semester")
        st.line_chart(forecast_chart_data(forecast), y_label="Projected enrollment")
