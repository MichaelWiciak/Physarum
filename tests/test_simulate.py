import random

import numpy as np

from physarum.agent import Agent
from physarum.grid import custom_blur, initialise_grids
from physarum.population import initialise_agents
from physarum.simulate import BLUR_FUNCTIONS, Config, resolve_seed, simulate

WIDTH, HEIGHT = 64, 48
PARAMS = (9, np.pi / 4, np.pi / 4, 5.0)


def test_blur_functions_share_a_signature():
    grid = initialise_grids(WIDTH, HEIGHT)
    grid[10, 10, 1] = 1.0

    for name, blur in BLUR_FUNCTIONS.items():
        result = blur(grid.copy(), 0.1)
        assert result.shape == (HEIGHT, WIDTH, 2), name
        assert np.isfinite(result[:, :, 1]).all(), name


def test_decay_reduces_total_trail_mass():
    grid = initialise_grids(WIDTH, HEIGHT)
    grid[10, 10, 1] = 1.0

    decayed = custom_blur(grid.copy(), 0.5)
    assert decayed[:, :, 1].sum() < grid[:, :, 1].sum()


def test_agents_start_in_distinct_cells():
    agents, occupied = initialise_agents(50, WIDTH, HEIGHT, *PARAMS, seed=7)

    assert len(agents) == 50
    assert len(occupied) == 50
    assert all(0 <= a.x < WIDTH and 0 <= a.y < HEIGHT for a in agents)


def test_movement_wraps_at_boundaries():
    agent = Agent(WIDTH, HEIGHT, 1, 1, *PARAMS)
    agent.direction = (1.0, 0.0)

    for _ in range(WIDTH):
        agent.move()

    assert 0 <= agent.x < WIDTH
    assert agent.y == 1


def test_deposit_writes_to_trail_channel():
    grid = initialise_grids(WIDTH, HEIGHT)
    agent = Agent(WIDTH, HEIGHT, 5, 5, *PARAMS)

    agent.deposit(grid)

    assert grid[5, 5, 1] == agent.depT
    assert grid[:, :, 0].sum() == 0.0


def test_headless_simulation_is_deterministic_under_a_seed():
    config = Config(
        width=WIDTH,
        height=HEIGHT,
        num_agents=20,
        num_steps=15,
        seed=1234,
    )

    first = simulate(config, headless=True)
    second = simulate(config, headless=True)

    np.testing.assert_array_equal(first, second)
    assert first[:, :, 1].sum() > 0.0


def test_resolve_seed_keeps_an_explicit_seed():
    config = Config(seed=99)

    assert resolve_seed(config) == 99
    assert config.seed == 99


def test_generated_seed_ignores_the_seeded_rng():
    random.seed(0)
    first = Config()
    resolve_seed(first)

    random.seed(0)
    second = Config()
    resolve_seed(second)

    assert first.seed != second.seed


def test_seed_defaults_to_random_and_is_reproducible():
    config = Config(width=WIDTH, height=HEIGHT, num_agents=5, num_steps=3)
    assert config.seed is None

    first = simulate(config, headless=True)
    assert isinstance(config.seed, int)

    second = simulate(config, headless=True)
    np.testing.assert_array_equal(first, second)
