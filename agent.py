import random
import numpy as np


class Agent:
    def __init__(self, width, height, x, y):
        self.width = width
        self.height = height
        self.x = float(x)
        self.y = float(y)
        self.direction = (random.uniform(-1, 1), random.uniform(-1, 1))
        self.sensor_angle = random.uniform(0, np.pi)

    def sense(self, local_grid):
        sensor_positions = [
            (
                int(self.x + np.cos(self.sensor_angle - np.pi / 4) * 5),
                int(self.y + np.sin(self.sensor_angle - np.pi / 4) * 5),
            ),
            (
                int(self.x + np.cos(self.sensor_angle) * 5),
                int(self.y + np.sin(self.sensor_angle) * 5),
            ),
            (
                int(self.x + np.cos(self.sensor_angle + np.pi / 4) * 5),
                int(self.y + np.sin(self.sensor_angle + np.pi / 4) * 5),
            ),
        ]
        sensor_values = [
            # local grid 1 or 0 different simulations.
            local_grid[y, x, 1] if 0 <= x < self.width and 0 <= y < self.height else 0
            for x, y in sensor_positions
        ]
        max_index = np.argmax(sensor_values)
        self.direction = (
            np.cos(self.sensor_angle + (max_index - 1) * np.pi / 4),
            np.sin(self.sensor_angle + (max_index - 1) * np.pi / 4),
        )

    def move(self):
        self.x += self.direction[0] * 2
        self.y += self.direction[1] * 2
        self.x = max(0, min(self.width - 1, self.x))
        self.y = max(0, min(self.height - 1, self.y))

    def deposit(self, local_grid):
        # Convert position to integers for grid indexing
        grid_x = int(self.x)
        grid_y = int(self.y)
        # hmmm.
        # local_grid[grid_y, grid_x, 0] += 0.1
        local_grid[grid_y, grid_x, 1] += 0.1
