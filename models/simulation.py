"""Discrete event simulation enrollment forecasting model.

References
----------
Fiallos & Ochoa 2017
"""

from typing import List, Tuple

from models.interface import ForecastModel


class SimulationModel(ForecastModel):
    """DES implementation """

    def fit(self, data) -> None:
        # TODO: calibrate simulation parameters from historical data
        raise NotImplementedError

    def predict(self, semesters_ahead: int = 1) -> List[Tuple[str, str, float]]:
        # TODO: run simulation and aggregate results
        raise NotImplementedError
