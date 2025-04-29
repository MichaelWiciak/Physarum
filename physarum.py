import numpy as np
import cv2
from agent import Agent
import random


# i think i do this differently that he does. will check.
def find_unique_position(a_agent, a_occupied, a_width, a_height):
    """
    Moves the agent to the nearest unoccupied position within grid bounds.
    Expands search radius outward until a position is found.
    """
    radius = 1
    while True:
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                if dx == 0 and dy == 0:
                    continue  # Skip original position
                new_x, new_y = a_agent.x + dx, a_agent.y + dy
                if 0 <= new_x < a_width and 0 <= new_y < a_height:
                    new_pos = (new_x, new_y)
                    if new_pos not in a_occupied:
                        a_agent.x, a_agent.y = new_x, new_y
                        a_occupied.add(new_pos)
                        return  # Exit as soon as we place the agent
        radius += 1


def initialise_grids(width, height):
    """
    Initializes the grid with pheromone and trail channels.
    """
    # making two channels for the grid
    # one for the pheromone and one for the trail
    grid = np.zeros((height, width, 2), dtype=np.float32)
    # for food/obstacles
    data_layer = np.zeros((height, width), dtype=np.float32)
    return grid, data_layer


def initialise_agents(num_agents, width, height):
    # need to initialise agents in a unoccpied position
    agents = []
    occupied = set()

    for _ in range(num_agents):
        # get a random position
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)

        # check if the position is occupied
        while (x, y) in occupied:
            x = random.randint(0, width - 1)
            y = random.randint(0, height - 1)

        # create the agent
        agent = Agent(width, height, x, y)
        agents.append(agent)
        occupied.add((x, y))
    return agents, occupied


def laplacian_diffusion(grid, diffusion_rate):
    """
    Applies a Laplacian diffusion to the grid.
    """
    laplacian = (
        np.roll(grid[:, :, 0], 1, axis=0)
        + np.roll(grid[:, :, 0], -1, axis=0)
        + np.roll(grid[:, :, 0], 1, axis=1)
        + np.roll(grid[:, :, 0], -1, axis=1)
        - 4 * grid[:, :, 0]
    )
    return grid[:, :, 0] + diffusion_rate * laplacian


def main():
    # maybe get this from config.
    WIDTH, HEIGHT = 800, 600
    DIFFUSION_RATE = 0.1
    DECAY_RATE = 0.01
    NUM_AGENTS = 10000
    NUM_STEPS = 1000

    # Create a window to display the grid
    cv2.namedWindow("Trails", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Trails", WIDTH, HEIGHT)

    # Create a blank grid
    grid, data_layer = initialise_grids(WIDTH, HEIGHT)
    # Create agents
    agents, occupied = initialise_agents(NUM_AGENTS, WIDTH, HEIGHT)

    for i in range(NUM_STEPS):
        for agent in agents:
            agent.sense(grid)

            old_pos = (agent.x, agent.y)
            print("Step", i, "Agent", agents.index(agent))
            print("old position", old_pos)

            if old_pos in occupied:
                occupied.remove(old_pos)
            else:
                print(
                    "Warning: Tried to remove a position that wasn't occupied!", old_pos
                )

            agent.move()

            new_pos = (agent.x, agent.y)
            print("new position", new_pos)
            print("----")

            occupied.add(new_pos)

            agent.deposit(grid)

        # diffuse and decay step.

        # option 1: Laplacian diffusion
        # grid[:, :, 0] = laplacian(grid, DIFFUSION_RATE)

        # option 1:3×3 mean filter / not really
        # grid[:, :, 0] = (
        #     grid[:, :, 0] * (1 - DIFFUSION_RATE)
        #     + DIFFUSION_RATE
        #     * (
        #         np.roll(grid[:, :, 0], 1, axis=0)
        #         + np.roll(grid[:, :, 0], -1, axis=0)
        #         + np.roll(grid[:, :, 0], 1, axis=1)
        #         + np.roll(grid[:, :, 0], -1, axis=1)
        #         + grid[:, :, 0]  # Include the center cell
        #     )
        #     / 5
        # )

        # option 1: 3×3 mean filter
        kernel = np.ones((3, 3), np.float32) / 9
        grid[:, :, 1] = cv2.filter2D(grid[:, :, 1], -1, kernel)

        # option 2: 3×3 mean filter but without the center cell
        # grid[:, :, 0] = grid[:, :, 0] * (1 - DECAY_RATE) + DIFFUSION_RATE * (
        #     np.roll(grid[:, :, 0], 1, axis=0)
        #     + np.roll(grid[:, :, 0], -1, axis=0)
        #     + np.roll(grid[:, :, 0], 1, axis=1)
        #     + np.roll(grid[:, :, 0], -1, axis=1)
        # )

        grid[:, :, 1] *= 1 - DECAY_RATE  # decay the trail

        trails = grid[:, :, 1]
        trails = (trails - trails.min()) / (trails.max() - trails.min())  # normalize
        trails = (trails * 255).astype(np.uint8)

        # display the image
        cv2.imshow("Trails", trails)
        cv2.waitKey(1)

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
