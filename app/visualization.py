"""Charts and output display helpers."""

import pandas as pd


def forecast_chart_data(forecast: pd.DataFrame) -> pd.DataFrame:
    """Return forecast values in the wide format expected by Streamlit charts."""
    return forecast.pivot(
        index="Semester",
        columns="Course",
        values="Projected enrollment",
    )
