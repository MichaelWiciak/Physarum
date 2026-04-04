# Physarum Slime Mold Simulation

A biologically-inspired optimisation algorithm that simulates the foraging behaviour of _Physarum polycephalum_ (slime mold) to solve graph-based problems like the Minimum Spanning Tree.

## Demo Videos

|                                     MST optimisation                                      |                                      Dense Start Simulation                                       |                                       Agent Visualization                                        |
| :---------------------------------------------------------------------------------------: | :-----------------------------------------------------------------------------------------------: | :----------------------------------------------------------------------------------------------: |
| [![MST Demo](https://img.youtube.com/vi/7ZkC3MxK37Q/0.jpg)](https://youtu.be/7ZkC3MxK37Q) | [![Dense Start Demo](https://img.youtube.com/vi/TFyH6HfQy6c/0.jpg)](https://youtu.be/TFyH6HfQy6c) | [![Agent View Demo](https://img.youtube.com/vi/dhvJkvUcZjE/0.jpg)](https://youtu.be/dhvJkvUcZjE) |

## Results

### Minimum Spanning Tree Experiments

Evolution of network topology as the slime mold finds optimal connections between nodes.

|                         Step 1                         |                         Step 2                         |                         Step 3                         |
| :----------------------------------------------------: | :----------------------------------------------------: | :----------------------------------------------------: |
| ![MST 1](Interesting_data/MinimumSpaningTree/mst1.png) | ![MST 2](Interesting_data/MinimumSpaningTree/mst2.png) | ![MST 3](Interesting_data/MinimumSpaningTree/mst3.png) |
| ![MST 4](Interesting_data/MinimumSpaningTree/mst4.png) | ![MST 5](Interesting_data/MinimumSpaningTree/mst5.png) | ![MST 6](Interesting_data/MinimumSpaningTree/mst6.png) |
| ![MST 7](Interesting_data/MinimumSpaningTree/mst7.png) |                                                        |                                                        |

### Dense Start Simulation

Agents initialized in high density, spreading to explore and optimize paths.

|                       Step 1                        |                       Step 2                        |                       Step 3                        |                       Step 4                        |
| :-------------------------------------------------: | :-------------------------------------------------: | :-------------------------------------------------: | :-------------------------------------------------: |
| ![Dense 1](Interesting_data/DenseStart/trail1.png)  | ![Dense 2](Interesting_data/DenseStart/trails2.png) | ![Dense 3](Interesting_data/DenseStart/trails3.png) | ![Dense 4](Interesting_data/DenseStart/trails4.png) |
| ![Dense 5](Interesting_data/DenseStart/trails5.png) | ![Dense 6](Interesting_data/DenseStart/trails6.png) | ![Dense 7](Interesting_data/DenseStart/trails7.png) |                                                     |

### Agent Visualization

Individual agent behavior and decision-making process visualized in real-time.

|                         1                         |                         2                         |                         3                         |                         4                         |
| :-----------------------------------------------: | :-----------------------------------------------: | :-----------------------------------------------: | :-----------------------------------------------: |
| ![Agent 1](Interesting_data/AgentView/agent1.png) | ![Agent 2](Interesting_data/AgentView/agent2.png) | ![Agent 3](Interesting_data/AgentView/agent3.png) | ![Agent 4](Interesting_data/AgentView/agent4.png) |
| ![Agent 5](Interesting_data/AgentView/agent5.png) | ![Agent 6](Interesting_data/AgentView/agent6.png) | ![Agent 7](Interesting_data/AgentView/agent7.png) |                                                   |

### Parameter Experiments

Comparative analysis of different simulation configurations.

|                                                       Test 1                                                       |                                                       Test 2                                                       |                                                       Test 3                                                       |
| :----------------------------------------------------------------------------------------------------------------: | :----------------------------------------------------------------------------------------------------------------: | :----------------------------------------------------------------------------------------------------------------: |
| ![Bi](Interesting_data/Test1/bi.png) ![Bi2](Interesting_data/Test1/bi2.png) ![Bi3](Interesting_data/Test1/bi3.png) | ![Co](Interesting_data/Test2/co.png) ![Co2](Interesting_data/Test2/co2.png) ![Co3](Interesting_data/Test2/co3.png) | ![Ga](Interesting_data/Test3/ga.png) ![Ga2](Interesting_data/Test3/ga2.png) ![Ga3](Interesting_data/Test3/ga3.png) |

## Quick Start

```bash
# Create virtual environment
python -m venv .venv && source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run simulation
python physarum.py
```

Modify `physarum.py` to adjust simulation parameters.

## Project Structure

```
.
├── physarum.py          # Main simulation engine
├── agent.py             # Agent behavior logic
├── requirements.txt     # Dependencies
├── Interesting_data/    # Experiment results and visualizations
│   ├── MinimumSpaningTree/   # MST optimisation experiments
│   ├── DenseStart/           # Dense initialization tests
│   ├── AgentView/            # Agent behavior visualization
│   ├── Test1-3/              # Parameter variation experiments
│   └── Gifs/                 # Animated outputs
└── cw2-2025-MiniProject(1).pdf  # Full technical report
```
