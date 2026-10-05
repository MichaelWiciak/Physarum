import dataclasses
import random

import cv2
import numpy as np

from physarum import grid as grid_ops
from physarum import render
from physarum.population import initialise_agents


@dataclasses.dataclass
class Config:
    width: int = 800
    height: int = 600
    decay_rate: float = 0.01
    num_agents: int = 1
    num_steps: int = 1000
    frames_per_second: int = 30
    seed: int = 42

    sensor_angle: float = 45 * np.pi / 180
    rotation_angle: float = 45 * np.pi / 180
    sensor_offset: int = 9
    deposit_rate: float = 5
    random_direction_change: float = 0.01

    stimulus_weight: float = 0.50
    show_agents: bool = True
    blur: str = "custom"

    stimulus_points: tuple = ()
    output: str = "simulation.mp4"


BLUR_FUNCTIONS = {
    "mean": grid_ops.filter_trails,
    "gaussian": grid_ops.gaussian_blur,
    "bilateral": grid_ops.bilateral_filter,
    "custom": grid_ops.custom_blur,
}


def simulate(config, headless=False, writer=None):
    blur = BLUR_FUNCTIONS[config.blur]

    if config.seed is not None:
        random.seed(config.seed)
        np.random.seed(config.seed)

    grid = grid_ops.initialise_grids(config.width, config.height)
    agents, occupied = initialise_agents(
        config.num_agents,
        config.width,
        config.height,
        config.sensor_offset,
        config.sensor_angle,
        config.rotation_angle,
        config.deposit_rate,
        config.seed,
    )
    stimulus_grid = grid_ops.create_stimulus_grid(
        config.width, config.height, config.stimulus_points
    )

    for step in range(config.num_steps):
        grid[:, :, 1] += stimulus_grid * config.stimulus_weight

        random.shuffle(agents)
        for agent in agents:
            agent.sense(grid)

        random.shuffle(agents)
        for agent in agents:
            if random.random() < config.random_direction_change:
                agent.reorient()
            old_pos = (agent.x, agent.y)
            projected_x, projected_y = agent.project_move()
            if (projected_x, projected_y) not in occupied:
                occupied.discard(old_pos)
                agent.move()
                occupied.add((agent.x, agent.y))
                agent.deposit(grid)
            else:
                agent.reorient()

        grid = blur(grid, config.decay_rate)

        if config.show_agents:
            trails = render.draw_agents(agents, grid)
        else:
            trails = render.draw_normalised_trails(grid)

        frame = cv2.cvtColor(trails, cv2.COLOR_GRAY2BGR)
        render.add_step_number_to_frame(frame, step)
        render.draw_stimuli(frame, config.stimulus_points)

        if writer is not None:
            writer.write(frame)
        if not headless:
            cv2.imshow("Trails", frame)
            cv2.waitKey(1)

    return grid


def open_writer(config):
    return cv2.VideoWriter(
        config.output,
        cv2.VideoWriter_fourcc(*"mp4v"),
        config.frames_per_second,
        (config.width, config.height),
    )


def main(config=None):
    if config is None:
        config = Config()

    if config.show_agents:
        cv2.namedWindow("Trails", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Trails", config.width, config.height)

    writer = open_writer(config)
    try:
        simulate(config, headless=False, writer=writer)
    finally:
        writer.release()
        cv2.destroyAllWindows()
