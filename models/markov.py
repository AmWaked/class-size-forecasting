"""Markov chain enrollment forecasting model.

References
----------
Gandy et al. 2019
Zhao & Otteson 2024  (arXiv:2405.14007)
Scott 2024
"""

import math
from collections.abc import Mapping
from typing import List, Tuple

from models.markov_model import forecast_enrollment, states, transition_matrix
from models.interface import ForecastModel


class MarkovModel(ForecastModel):
    """Four-state enrollment model using the configured transition probabilities."""

    def __init__(self) -> None:
        self._students = None

    def fit(self, data) -> None:
        """Set initial enrollment counts by state."""
        if not isinstance(data, Mapping):
            raise ValueError("Initial enrollment must be provided for each state.")

        missing_states = [state for state in states if state not in data]
        unknown_states = [state for state in data if state not in states]
        if missing_states or unknown_states:
            details = []
            if missing_states:
                details.append(f"missing states: {', '.join(missing_states)}")
            if unknown_states:
                details.append(f"unknown states: {', '.join(map(str, unknown_states))}")
            raise ValueError(f"Provide enrollment for exactly {', '.join(states)} ({'; '.join(details)}).")

        students = []
        for state in states:
            try:
                enrollment = float(data[state])
            except (TypeError, ValueError):
                raise ValueError(f"Initial enrollment for {state} must be a non-negative whole number.") from None
            if not math.isfinite(enrollment) or enrollment < 0 or not enrollment.is_integer():
                raise ValueError(f"Initial enrollment for {state} must be a non-negative whole number.")
            students.append(enrollment)
        self._students = students

    def predict(self, semesters_ahead: int = 1) -> List[Tuple[str, int, float]]:
        """Return projected enrollment for every state and requested semester."""
        if not isinstance(semesters_ahead, int) or isinstance(semesters_ahead, bool):
            raise ValueError("The number of semesters must be a whole number.")
        if semesters_ahead < 1:
            raise ValueError("Forecast at least one semester ahead.")
        if self._students is None:
            raise ValueError("Set initial enrollment with fit() before forecasting.")

        students = self._students.copy()
        predictions = []
        for semester in range(1, semesters_ahead + 1):
            students = forecast_enrollment(students, transition_matrix)
            predictions.extend(
                (state, semester, enrollment)
                for state, enrollment in zip(states, students)
            )
        return predictions
