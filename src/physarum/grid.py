import cv2
import numpy as np


def initialise_grids(width, height):
    grid = np.zeros((height, width, 2), dtype=np.float32)
    return grid


def create_stimulus_grid(width, height, points, intensity=1.0):
    stimulus_grid = np.zeros((height, width))
    for x, y in points:
        stimulus_grid[y % height, x % width] = intensity
    return stimulus_grid


def filter_trails(grid, decay_rate):
    kernel = np.ones((3, 3), np.float32) / 9
    grid[:, :, 1] = cv2.filter2D(grid[:, :, 1], -1, kernel)
    grid[:, :, 1] *= 1 - decay_rate
    return grid


def gaussian_blur(grid, decay_rate=0.01, k=3):
    grid[:, :, 1] = cv2.GaussianBlur(grid[:, :, 1], (k, k), sigmaX=0)
    grid[:, :, 1] *= 1 - decay_rate
    return grid


def bilateral_filter(grid, decay_rate=0.01):
    grid[:, :, 1] = cv2.bilateralFilter(
        grid[:, :, 1].astype(np.float32), d=3, sigmaColor=75, sigmaSpace=75
    )
    grid[:, :, 1] *= 1 - decay_rate
    return grid


def custom_blur(grid, decay_rate=0.01):
    kernel = np.array([[1, 2, 1], [2, 4, 2], [1, 2, 1]], dtype=np.float32)
    kernel /= kernel.sum()
    grid[:, :, 1] = cv2.filter2D(grid[:, :, 1], -1, kernel)
    grid[:, :, 1] *= 1 - decay_rate
    return grid
