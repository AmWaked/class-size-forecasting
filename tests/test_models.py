"""Basic tests for model interface compliance."""

import pytest

from models.markov import MarkovModel
from models.simulation import SimulationModel


def test_markov_implements_interface():
    model = MarkovModel()
    assert hasattr(model, "fit")
    assert hasattr(model, "predict")


def test_simulation_implements_interface():
    model = SimulationModel()
    assert hasattr(model, "fit")
    assert hasattr(model, "predict")
