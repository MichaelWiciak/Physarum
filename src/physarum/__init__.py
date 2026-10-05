"""Physarum slime mould simulation."""

from physarum.agent import Agent
from physarum.grid import (
    bilateral_filter,
    create_stimulus_grid,
    custom_blur,
    filter_trails,
    gaussian_blur,
    initialise_grids,
)
from physarum.population import initialise_agents
from physarum.simulate import Config, main, simulate

__all__ = [
    "Agent",
    "Config",
    "bilateral_filter",
    "create_stimulus_grid",
    "custom_blur",
    "filter_trails",
    "gaussian_blur",
    "initialise_agents",
    "initialise_grids",
    "main",
    "simulate",
]

__version__ = "0.1.0"
