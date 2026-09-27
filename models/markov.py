"""Markov chain enrollment forecasting model.

References
----------
Gandy et al. 2019
Zhao & Otteson 2024  (arXiv:2405.14007)
Scott 2024
"""

from typing import List, Tuple

from models.interface import ForecastModel


class MarkovModel(ForecastModel):
    """Markov chain implementation"""

    def fit(self, data) -> None:
        # TODO: build transition matrix from historical data
        raise NotImplementedError

    def predict(self, semesters_ahead: int = 1) -> List[Tuple[str, str, float]]:
        # TODO: multiply state vector by transition matrix
        raise NotImplementedError
