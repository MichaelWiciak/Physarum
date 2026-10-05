import random

from physarum.agent import Agent


def initialise_agents(num_agents, width, height, SO, SA, RA, depT, seed=None):
    if seed is not None:
        random.seed(seed)

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
