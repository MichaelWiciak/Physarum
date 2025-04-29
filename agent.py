import random
import numpy as np


class Agent:
    def __init__(self, width, height, x, y):
        self.width = width
        self.height = height

        # need to initalise the x and y positions so they are not occupied.
        self.x = x
        self.y = y
        self.direction = (random.uniform(-1, 1), random.uniform(-1, 1))
        self.sensor_angle = random.uniform(0, np.pi)

    def sense(self, local_grid):
        sensor_positions = [
            (
                self.x + int(np.cos(self.sensor_angle - np.pi / 4) * 5),
                self.y + int(np.sin(self.sensor_angle - np.pi / 4) * 5),
            ),
            (
                self.x + int(np.cos(self.sensor_angle) * 5),
                self.y + int(np.sin(self.sensor_angle) * 5),
            ),
            (
                self.x + int(np.cos(self.sensor_angle + np.pi / 4) * 5),
                self.y + int(np.sin(self.sensor_angle + np.pi / 4) * 5),
            ),
        ]
        sensor_values = [
            local_grid[y, x, 0] if 0 <= x < self.width and 0 <= y < self.height else 0
            for x, y in sensor_positions
        ]
        max_index = np.argmax(sensor_values)
        self.direction = (
            np.cos(self.sensor_angle + (max_index - 1) * np.pi / 4),
            np.sin(self.sensor_angle + (max_index - 1) * np.pi / 4),
        )

    def move(self):
        self.x = int(self.x + self.direction[0] * 2)
        self.y = int(self.y + self.direction[1] * 2)
        self.x = max(0, min(self.width - 1, self.x))
        self.y = max(0, min(self.height - 1, self.y))

    def deposit(self, local_grid):
        # should it deposit into both grids? just local?
        local_grid[self.y, self.x, 0] += 0.1
        local_grid[self.y, self.x, 1] += 0.1
