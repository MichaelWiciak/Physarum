Benchmarks
==========

Per-step timing data captured by instrumenting the simulation loop.

- `agents_1.csv` — timing per sub-component (sense, move, deposit, diffusion)
  with a single agent.
- `agents_1000.csv` — same measurements across 1000 agents, used to check that
  each component takes a consistent amount of time as the run progresses.

Columns in `agents_1.csv`:
`step`, `sense_time`, `move_time`, `deposit_time`, `diffusion_time`

Columns in `agents_1000.csv`:
`step`, `sense_time`, `move_deposit`, `diffusion`