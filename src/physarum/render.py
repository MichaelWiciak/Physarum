import cv2
import numpy as np


def draw_agents(agents, grid):
    trails = np.zeros((grid.shape[0], grid.shape[1]), dtype=np.uint8)
    for agent in agents:
        grid_x = int(agent.x)
        grid_y = int(agent.y)
        trails[grid_y, grid_x] = 255
    return trails


def draw_normalised_trails(grid):
    trails = grid[:, :, 1]
    eps = 1e-8
    trails = (trails - trails.min()) / (trails.max() - trails.min() + eps)
    trails = (trails * 255).astype(np.uint8)
    return trails


def add_step_number_to_frame(frame, step):
    font = cv2.FONT_HERSHEY_SIMPLEX
    text = f"Step: {step + 1}"
    text_size = cv2.getTextSize(text, font, 0.5, 1)[0]
    text_x = (frame.shape[1] - text_size[0]) // 2
    text_y = frame.shape[0] - 10
    cv2.putText(frame, text, (text_x, text_y), font, 0.5, (255, 255, 255), 1)
    return frame


def draw_stimuli(frame, stimulus_points):
    for x, y in stimulus_points:
        cv2.circle(frame, (x, y), 5, (0, 0, 255), -1)
    return frame
