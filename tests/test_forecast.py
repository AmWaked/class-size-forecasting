"""Tests for the enrollment growth-rate baseline."""

import pandas as pd
import pytest

from app.forecast import build_forecast
from app.visualization import forecast_chart_data


def test_build_forecast_compounds_rate_for_each_semester():
    enrollment_data = pd.DataFrame(
        {
            "Course": ["CS 101"],
            "Initial enrollment": [100],
            "Growth rate per semester (%)": [10],
        }
    )

    result = build_forecast(enrollment_data, 2)

    assert result.to_dict("records") == [
        {"Course": "CS 101", "Semester": 1, "Projected enrollment": 110},
        {"Course": "CS 101", "Semester": 2, "Projected enrollment": 121},
    ]
    assert forecast_chart_data(result).to_dict() == {"CS 101": {1: 110, 2: 121}}


@pytest.mark.parametrize(
    ("enrollment", "growth_rate", "message"),
    [
        (-1, 0, "non-negative whole number"),
        (1.5, 0, "non-negative whole number"),
        (10, -101, "at least -100%"),
        (10, float("inf"), "finite growth rate"),
    ],
)
def test_build_forecast_rejects_invalid_values(enrollment, growth_rate, message):
    enrollment_data = pd.DataFrame(
        {
            "Course": ["CS 101"],
            "Initial enrollment": [enrollment],
            "Growth rate per semester (%)": [growth_rate],
        }
    )

    with pytest.raises(ValueError, match=message):
        build_forecast(enrollment_data, 1)


def test_build_forecast_rejects_empty_and_duplicate_courses():
    empty = pd.DataFrame(columns=["Course", "Initial enrollment", "Growth rate per semester (%)"])
    duplicate = pd.DataFrame(
        {
            "Course": ["CS 101", " cs 101 "],
            "Initial enrollment": [10, 12],
            "Growth rate per semester (%)": [0, 0],
        }
    )

    with pytest.raises(ValueError, match="at least one course"):
        build_forecast(empty, 1)
    with pytest.raises(ValueError, match="listed more than once"):
        build_forecast(duplicate, 1)

    
#Verifies that forecast results for multiple courses are organized correctly for chart display
    def test_forecast_chart_data_handles_multiple_courses():
    forecast_data = pd.DataFrame(
        [
            {"Course": "CS 101", "Semester": 1, "Projected enrollment": 110},
            {"Course": "CS 101", "Semester": 2, "Projected enrollment": 121},
            {"Course": "CS 102", "Semester": 1, "Projected enrollment": 80},
            {"Course": "CS 102", "Semester": 2, "Projected enrollment": 88},
        ]
    )

    chart_data = forecast_chart_data(forecast_data)

    assert chart_data.to_dict() == {
        "CS 101": {1: 110, 2: 121},
        "CS 102": {1: 80, 2: 88},
    }

#Verifies that calculated forecast values are passed correctly into the chart data used for display
    def test_calculated_forecast_matches_chart_data():
    enrollment_data = pd.DataFrame(
        {
            "Course": ["CS 101", "CS 102"],
            "Initial enrollment": [100, 50],
            "Growth rate per semester (%)": [10, 20],
        }
    )

    forecast = build_forecast(enrollment_data, 2)
    chart_data = forecast_chart_data(forecast)

    assert chart_data.to_dict() == {
        "CS 101": {1: 110, 2: 121},
        "CS 102": {1: 60, 2: 72},
    }
