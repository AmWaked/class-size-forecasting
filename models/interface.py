"""Common interface for forecasting models.

Both the Markov chain model and the discrete event simulation
implement this ABC so the GUI and output layer stay model-agnostic.
"""

from abc import ABC, abstractmethod
from typing import List, Tuple


class ForecastModel(ABC):
    """Base class every forecasting model must implement."""

    @abstractmethod
    def fit(self, data) -> None:
        """Train / calibrate the model on historical enrollment data.

        Parameters
        ----------
        data :
            Historical student progression records.
        """

    @abstractmethod
    def predict(self, semesters_ahead: int = 1) -> List[Tuple[str, str, float]]:
        """Produce enrollment forecasts.

        Parameters
        ----------
        semesters_ahead : int

        Returns
        -------
        list of (course, semester, projected_enrollment) tuples.
        """
