# Physarum Slime Mold Simulation

A biologically-inspired optimisation algorithm that simulates the foraging behaviour of _Physarum polycephalum_ (slime mold) to solve graph-based problems like the Minimum Spanning Tree.

## Demo Videos

|                                     MST optimisation                                      |                                      Dense Start Simulation                                       |                                       Agent Visualization                                        |
| :---------------------------------------------------------------------------------------: | :-----------------------------------------------------------------------------------------------: | :----------------------------------------------------------------------------------------------: |
| [![MST Demo](https://img.youtube.com/vi/7ZkC3MxK37Q/0.jpg)](https://youtu.be/7ZkC3MxK37Q) | [![Dense Start Demo](https://img.youtube.com/vi/TFyH6HfQy6c/0.jpg)](https://youtu.be/TFyH6HfQy6c) | [![Agent View Demo](https://img.youtube.com/vi/dhvJkvUcZjE/0.jpg)](https://youtu.be/dhvJkvUcZjE) |

## Quick Start

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export PYTHONPATH=src
```

Run the default simulation with a live preview window:

```bash
python -m physarum
```

### How it works

Each step of the loop does four things:

1. **Sense** — every agent samples the chemoattractant layer at three sensor
   positions arranged around its sensor angle.
2. **Move** — agents pick a direction, and deposit chemoattractant where they
   land, unless another agent already occupies the target cell.
3. **Diffuse** — the trail layer is convolved with a blur kernel and decayed.
4. **Render** — the frame is annotated with the step number, and optional
   stimulus sources are drawn as red dots.

## CLI Options

| Flag                        | Default          | Description                                                 |
| :-------------------------- | :--------------- | :---------------------------------------------------------- |
| `--width` / `--height`      | `800` / `600`    | Grid dimensions in pixels                                   |
| `--num-agents`              | `1`              | Number of agents to spawn                                   |
| `--num-steps`               | `1000`           | Simulation steps to run                                     |
| `--decay-rate`              | `0.01`           | Fraction of trail lost each step                            |
| `--seed`                    | `42`             | RNG seed; a fixed seed makes runs reproducible              |
| `--sensor-offset`           | `9`              | Sensor distance from the agent, in pixels                   |
| `--deposit-rate`            | `5`              | Chemoattractant deposited per step                          |
| `--random-direction-change` | `0.01`           | Probability of a random reorientation                       |
| `--blur`                    | `custom`         | Diffusion kernel: `mean`, `gaussian`, `bilateral`, `custom` |
| `--stimulus X,Y`            | none             | Chemoattractant source; repeatable                          |
| `--output`                  | `simulation.mp4` | Output video path                                           |
| `--trails`                  | off              | Render trail intensity instead of agent dots                |
| `--headless`                | off              | Run without opening a window                                |

## Results

### Minimum Spanning Tree Experiments

Evolution of network topology as the slime mold finds optimal connections between nodes.

|                          Step 1                           |                             Step 2                             |                          Step 3                           |
| :-------------------------------------------------------: | :------------------------------------------------------------: | :-------------------------------------------------------: |
| ![MST 1](results/images/minimum_spanning_tree/mst_01.png) |   ![MST 2](results/images/minimum_spanning_tree/mst_02.png)    | ![MST 3](results/images/minimum_spanning_tree/mst_03.png) |
| ![MST 4](results/images/minimum_spanning_tree/mst_04.png) |   ![MST 5](results/images/minimum_spanning_tree/mst_05.png)    | ![MST 6](results/images/minimum_spanning_tree/mst_06.png) |
| ![MST 7](results/images/minimum_spanning_tree/mst_07.png) | ![Result](results/images/minimum_spanning_tree/mst_result.png) |       ![Simulation](results/images/simulation.gif)        |

### Dense Start Simulation

Agents initialized in high density, spreading to explore and optimize paths.

|                       Step 1                        |                       Step 2                        |                       Step 3                        |                       Step 4                        |
| :-------------------------------------------------: | :-------------------------------------------------: | :-------------------------------------------------: | :-------------------------------------------------: |
| ![Dense 1](results/images/dense_start/trail_01.png) | ![Dense 2](results/images/dense_start/trail_02.png) | ![Dense 3](results/images/dense_start/trail_03.png) | ![Dense 4](results/images/dense_start/trail_04.png) |
| ![Dense 5](results/images/dense_start/trail_05.png) | ![Dense 6](results/images/dense_start/trail_06.png) | ![Dense 7](results/images/dense_start/trail_07.png) |                                                     |

### Agent Visualization

Individual agent behavior and decision-making process visualized in real-time.

|                         1                          |                         2                          |                         3                          |                         4                          |
| :------------------------------------------------: | :------------------------------------------------: | :------------------------------------------------: | :------------------------------------------------: |
| ![Agent 1](results/images/agent_view/agent_01.png) | ![Agent 2](results/images/agent_view/agent_02.png) | ![Agent 3](results/images/agent_view/agent_03.png) | ![Agent 4](results/images/agent_view/agent_04.png) |
| ![Agent 5](results/images/agent_view/agent_05.png) | ![Agent 6](results/images/agent_view/agent_06.png) | ![Agent 7](results/images/agent_view/agent_07.png) |                                                    |

### Parameter Experiments

Comparative analysis of different diffusion kernels.

|                                                                           Test 1                                                                            |                                                                           Test 2                                                                            |                                                                           Test 3                                                                            |
| :---------------------------------------------------------------------------------------------------------------------------------------------------------: | :---------------------------------------------------------------------------------------------------------------------------------------------------------: | :---------------------------------------------------------------------------------------------------------------------------------------------------------: |
| ![Bi 1](results/images/param_sweep/test1_bi_01.png) ![Bi 2](results/images/param_sweep/test1_bi_02.png) ![Bi 3](results/images/param_sweep/test1_bi_03.png) | ![Co 1](results/images/param_sweep/test2_co_01.png) ![Co 2](results/images/param_sweep/test2_co_02.png) ![Co 3](results/images/param_sweep/test2_co_03.png) | ![Ga 1](results/images/param_sweep/test3_ga_01.png) ![Ga 2](results/images/param_sweep/test3_ga_02.png) ![Ga 3](results/images/param_sweep/test3_ga_03.png) |

## Benchmarks

Per-step timing data is recorded in [`results/benchmarks/`](results/benchmarks/), with one CSV per agent count.

## Development

```bash
pip install -e ".[dev]"
ruff check .
pytest -q
```

## Project Structure

```
.
├── src/physarum/           # Simulation package
│   ├── agent.py            # Agent behaviour: sense, move, deposit
│   ├── grid.py             # Grid init, stimulus, diffusion kernels
│   ├── population.py       # Agent spawning and seeding
│   ├── render.py           # Frame drawing and annotation
│   ├── simulate.py         # Step loop and configuration
│   └── cli.py              # Command-line interface
├── tests/                  # Pytest suite
├── results/
│   ├── images/             # Experiment renders
│   └── benchmarks/         # Per-step timing CSVs
└── pyproject.toml          # Dependencies and tooling config
```

## License

MIT — see [LICENSE](LICENSE).
