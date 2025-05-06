import numpy as np
import cv2
from agent import Agent
import random
import imageio
import string
import time


def initialise_grids(width, height):
    grid = np.zeros((height, width, 2), dtype=np.float32)
    return grid


def initialise_agents(num_agents, width, height, SO, SA, RA, depT, seed=None):
    # Initialize agents in unoccupied positions with optional seeding
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)

    agents = []
    occupied = set()

    for _ in range(num_agents):
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)

        while (x, y) in occupied:
            x = random.randint(0, width - 1)
            y = random.randint(0, height - 1)

        agent = Agent(width, height, x, y, SO, SA, RA, depT)
        agents.append(agent)
        occupied.add((x, y))
    return agents, occupied


def create_stimulus_grid(width, height, points, intensity=1.0):
    stimulus_grid = np.zeros((height, width))
    for x, y in points:
        stimulus_grid[y % height, x % width] = intensity
    return stimulus_grid


def filter_trails(grid, decay_rate):
    # 3x3 kernel for averaging.
    kernel = np.ones((3, 3), np.float32) / 9
    grid[:, :, 1] = cv2.filter2D(grid[:, :, 1], -1, kernel)
    grid[:, :, 1] *= 1 - decay_rate
    return grid


def gaussian_blur(grid, k=3, decay_rate=0.01):
    # note that apparenlty the kernel size must be odd.
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


def draw_agents(agents, grid):
    # Draw agents as dots
    trails = np.zeros((grid.shape[0], grid.shape[1]), dtype=np.uint8)
    for agent in agents:
        grid_x = int(agent.x)
        grid_y = int(agent.y)
        trails[grid_y, grid_x] = 255
    return trails


def draw_trails(grid):
    # Draw trails/ weird
    trails = np.zeros((grid.shape[0], grid.shape[1]), dtype=np.uint8)
    trails[:, :] = grid[:, :, 1] * 255
    return trails


def draw_norma_trails(grid):
    trails = grid[:, :, 1]
    eps = 1e-8
    trails = (trails - trails.min()) / (trails.max() - trails.min() + eps)
    trails = (trails * 255).astype(np.uint8)
    return trails


def add_step_number_to_frame(frame, step):
    # Add step number to the frame
    font = cv2.FONT_HERSHEY_SIMPLEX
    text = f"Step: {step + 1}"
    text_size = cv2.getTextSize(text, font, 0.5, 1)[0]
    text_x = (frame.shape[1] - text_size[0]) // 2
    text_y = frame.shape[0] - 10
    cv2.putText(frame, text, (text_x, text_y), font, 0.5, (255, 255, 255), 1)
    return frame


# generate a random string of size n and end it with .csv
def generate_random_filename(n=10):

    letters = string.ascii_lowercase
    random_string = "".join(random.choice(letters) for i in range(n))
    return random_string + ".csv"


def main():
    # maybe get this from config.
    WIDTH, HEIGHT = 800, 600
    DECAY_RATE = 0.01
    NUM_AGENTS = 1  # 15000
    NUM_STEPS = 1000
    frames_per_second = 30

    seed = 42

    boundary = "Toroidal boundaries"  # infinite plane.

    # Agent parameters
    SA = 45 * np.pi / 180  # 45° in radians
    RA = 45 * np.pi / 180  # 45° rotation angle
    SO = 9  # Sensor offset distance (pixels)
    depT = 5  # Chemoattractant deposition per step
    pCD = 0.01  # Probability of random direction change

    show_agents = True  # Set to True to show agents as dots

    # Create a blank grid
    grid = initialise_grids(WIDTH, HEIGHT)
    # Create agents
    agents, occupied = initialise_agents(
        NUM_AGENTS, WIDTH, HEIGHT, SO, SA, RA, depT, seed
    )
    stimulus_points = []
    stimulus_grid = create_stimulus_grid(WIDTH, HEIGHT, stimulus_points)
    stimulus_weight = 0.50  # Weighting factor (0.01-0.1)

    # open the window and wait for a key press (show initial food)
    cv2.namedWindow("Trails", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Trails", WIDTH, HEIGHT)
    cv2.imshow("Trails", grid[:, :, 0] * 255)
    cv2.waitKey(0)

    # Show agent positions.
    trails = np.zeros((HEIGHT, WIDTH), dtype=np.uint8)
    for agent in agents:
        grid_x = int(agent.x)
        grid_y = int(agent.y)
        trails[grid_y, grid_x] = 255
    cv2.imshow("Trails", trails)
    cv2.waitKey(0)

    # Create a list to store frames for the GIF
    frames = []

    # Load a font for drawing the step number
    font = cv2.FONT_HERSHEY_SIMPLEX

    # filename = str(NUM_AGENTS) + ".csv"
    # with open(filename, "w", encoding="utf-8") as f:
    #     f.write("step, sense_time, move_deposit, diffusion\n")

    for step in range(NUM_STEPS):  # change _ to step for debugging
        # write the step number to the file
        # f.write(f"{step},")

        # Project pre-pattern stimuli into the chemo layer
        grid[:, :, 1] += stimulus_grid * stimulus_weight

        # GLOBAL SCHEDULER FOR SENSING (randomize order)
        random.shuffle(agents)
        # Measure the time taken for sensing
        # start_time = time.time()
        for agent in agents:
            # Measure the time taken for sensing
            agent.sense(grid)
        # sense_time = time.time() - start_time
        # f.write(f"{sense_time},")

        # GLOBAL SCHEDULER FOR MOVEMENT (randomize order again)
        random.shuffle(agents)
        # Measure the time taken for movement
        # start_time = time.time()
        for agent in agents:
            if random.random() < pCD:
                agent.reorient()
            old_pos = (agent.x, agent.y)
            projected_x, projected_y = agent.project_move()
            if (projected_x, projected_y) not in occupied:
                try:
                    occupied.remove(old_pos)
                except KeyError:
                    print(
                        "Warning: Tried to remove a position that wasn't occupied!",
                        old_pos,
                    )
                # meaure time for move
                agent.move()
                new_pos = (agent.x, agent.y)
                occupied.add(new_pos)
                # measure time for deposit
                agent.deposit(grid)
            else:
                agent.reorient()
        # move_deposit_time = time.time() - start_time
        # f.write(f"{move_deposit_time},")

        # Apply trail filtering
        # Measure the time taken for diffusion
        # start_time = time.time()

        grid = custom_blur(grid, DECAY_RATE)
        # grid = filter_trails(grid, DECAY_RATE)
        # diffusion_time = time.time() - start_time
        # f.write(f"{diffusion_time}\n")

        # Draw the trails or agents
        if show_agents:
            trails = draw_agents(agents, grid)
        else:
            trails = draw_norma_trails(grid)

        # Add step number to the frame
        trails_with_text = cv2.cvtColor(trails, cv2.COLOR_GRAY2BGR)
        text = f"Step: {step + 1}"
        text_size = cv2.getTextSize(text, font, 0.5, 1)[0]
        text_x = (trails_with_text.shape[1] - text_size[0]) // 2
        text_y = trails_with_text.shape[0] - 10
        cv2.putText(
            trails_with_text, text, (text_x, text_y), font, 0.5, (255, 255, 255), 1
        )

        # append the pre-pattern stimuli to the frame as red dots
        for x, y in stimulus_points:
            cv2.circle(trails_with_text, (x, y), 5, (0, 0, 255), -1)

        # Append the frame to the list
        frames.append(trails_with_text)

        # Show the frame
        cv2.imshow("Trails", trails_with_text)
        cv2.waitKey(1)

    # Save the frames as a GIF
    gif_frames = [cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) for frame in frames]
    out = cv2.VideoWriter(
        "simulation.mp4",
        cv2.VideoWriter_fourcc(*"mp4v"),
        frames_per_second,
        (WIDTH, HEIGHT),
    )
    for frame in frames:
        out.write(frame)
    out.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
