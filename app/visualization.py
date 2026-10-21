"""Charts and output display helpers."""

import pandas as pd


def forecast_chart_data(forecast: pd.DataFrame, category_column: str = "Course") -> pd.DataFrame:
    """Return forecast values in the wide format expected by Streamlit charts."""
    return forecast.pivot(
        index="Semester",
        columns=category_column,
        values="Projected enrollment",
    )
