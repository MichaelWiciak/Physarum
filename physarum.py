import numpy as np
import cv2
from agent import Agent
import random


def initialise_grids(width, height):
    grid = np.zeros((height, width, 2), dtype=np.float32)
    return grid


def initialise_agents(num_agents, width, height, SO, SA, RA, depT):
    # need to initialise agents in a unoccpied position
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


def initialise_food(grid, food_size, width, height):
    # Initialise the grid with two small squares of food.
    center_y = height // 2
    # Left square
    grid[
        center_y - food_size // 2 : center_y + food_size // 2,
        width // 4 - food_size // 2 : width // 4 + food_size // 2,
        0,
    ] = 1.0

    # Right square
    grid[
        center_y - food_size // 2 : center_y + food_size // 2,
        3 * width // 4 - food_size // 2 : 3 * width // 4 + food_size // 2,
        0,
    ] = 1.0


def filter_trails(grid, decay_rate):
    # Apply a Gaussian filter to the trail map
    kernel = np.ones((3, 3), np.float32) / 9
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
    # Draw trails
    trails = np.zeros((grid.shape[0], grid.shape[1]), dtype=np.uint8)
    trails[:, :] = grid[:, :, 1] * 255
    return trails


def main():
    # maybe get this from config.
    WIDTH, HEIGHT = 800, 600
    DECAY_RATE = 0.01
    NUM_AGENTS = 1500
    NUM_STEPS = 13000

    # paremets from the paper
    p = 2.08  # in our case we got this val. percentage of agents over the screen. they want 3-15 percent.
    diffK = 3  # diffusion kernel.
    decayT = 0.1  # Trail decay rate
    wProj = 0.05  # Pre-pattern stimulus projection weight
    boundary = (
        "periodic"  # Toroidal boundaries (not implemented here) aka infinite plane.
    )

    # Agent parameters
    SA = 45 * np.pi / 180  # 45° in radians
    RA = 45 * np.pi / 180  # 45° rotation angle
    SO = 9  # Sensor offset distance (pixels)
    SS = 1  # Step size
    depT = 5  # Chemoattractant deposition per step
    pCD = 0.01  # Probability of random direction change

    show_agents = False  # Set to True to show agents as dots

    # Create a blank grid
    grid = initialise_grids(WIDTH + 10, HEIGHT + 10)
    # Create agents
    agents, occupied = initialise_agents(NUM_AGENTS, WIDTH, HEIGHT, SO, SA, RA, depT)

    # Initialise food/ need to fix
    # food_size = 10
    # initialise_food(grid, food_size, WIDTH, HEIGHT)

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

    for _ in range(NUM_STEPS):  # change _ to i when debugging
        for agent in agents:
            agent.sense(grid)
            # old_pos = (int(agent.x), int(agent.y))
            old_pos = (agent.x, agent.y)
            # this should be float but int causes errors, not sure why.
            # print("Step", i, "Agent", agents.index(agent))
            # print("old position", old_pos)
            # as the paper wanted, random chance of changing direction.
            if random.random() < pCD:
                agent.reorient()

            projected_x, projected_y = agent.project_move()
            if (projected_x, projected_y) not in occupied:
                try:
                    occupied.remove(old_pos)
                except KeyError:
                    print(
                        "Warning: Tried to remove a position that wasn't occupied!",
                        old_pos,
                    )
                agent.move()
                # new_pos = (int(agent.x), int(agent.y))
                new_pos = (agent.x, agent.y)
                occupied.add(new_pos)
                agent.deposit(grid)
            else:
                # Stay in place, reorient randomly
                agent.reorient()

        # option 1: 3×3 mean filter
        filter_trails(grid, DECAY_RATE)

        if show_agents:
            trails = draw_agents(agents, grid)
            cv2.imshow("Trails", trails)
        else:
            # Use trail-map (channel 1)
            trails = draw_trails(grid)
            cv2.imshow("Trails", trails)

        cv2.waitKey(1)

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
