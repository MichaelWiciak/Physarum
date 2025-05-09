import random
import numpy as np


class Agent:
    def __init__(self, width, height, x, y, SO, SA, RA, depT):
        self.width = width
        self.height = height
        self.x = float(x)
        self.y = float(y)
        self.direction = (random.uniform(-1, 1), random.uniform(-1, 1))
        self.sensor_offset = SO
        self.SA = SA
        self.SO = SO
        self.RA = RA
        self.depT = depT

        # can make it sense 180 or 360. current is 360. 180 is: random.uniform(0, np.pi). different behaviousr. very.
        self.sensor_angle = random.uniform(0, 2 * np.pi)

    def sense(self, local_grid):
        sensor_angles = [
            self.sensor_angle - self.SA,
            self.sensor_angle,
            self.sensor_angle + self.SA,
        ]
        sensor_positions = [
            (
                int((self.x + np.cos(angle) * self.SO) % self.width),
                int((self.y + np.sin(angle) * self.SO) % self.height),
            )
            for angle in sensor_angles
        ]
        sensor_values = [local_grid[y, x, 1] for x, y in sensor_positions]

        max_index = np.argmax(sensor_values)
        # Rotate the agent's direction based on RA
        self.direction = (
            np.cos(self.sensor_angle + (max_index - 1) * self.RA),
            np.sin(self.sensor_angle + (max_index - 1) * self.RA),
        )

    # different boundaries. infinite plane. it still behaves weidly.
    def move(self):
        self.x = (self.x + self.direction[0]) % self.width
        self.y = (self.y + self.direction[1]) % self.height

    def project_move(self):
        projected_x = (self.x + self.direction[0]) % self.width
        projected_y = (self.y + self.direction[1]) % self.height
        return projected_x, projected_y

    def deposit(self, local_grid):
        # Convert position to integers for grid indexing
        grid_x = int(self.x)
        grid_y = int(self.y)
        # hmmm.
        # local_grid[grid_y, grid_x, 0] += 0.1
        local_grid[grid_y, grid_x, 1] += self.depT

    def reorient(self):
        self.direction = (random.uniform(-1, 1), random.uniform(-1, 1))
