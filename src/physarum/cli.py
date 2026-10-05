import argparse

from physarum.simulate import Config, main


def build_parser():
    parser = argparse.ArgumentParser(
        prog="physarum",
        description="Physarum slime mould simulation.",
    )
    parser.add_argument("--width", type=int, default=Config.width)
    parser.add_argument("--height", type=int, default=Config.height)
    parser.add_argument("--num-agents", type=int, default=Config.num_agents)
    parser.add_argument("--num-steps", type=int, default=Config.num_steps)
    parser.add_argument("--decay-rate", type=float, default=Config.decay_rate)
    parser.add_argument("--seed", type=int, default=Config.seed)
    parser.add_argument("--sensor-offset", type=int, default=Config.sensor_offset)
    parser.add_argument(
        "--deposit-rate", type=float, default=Config.deposit_rate
    )
    parser.add_argument(
        "--random-direction-change",
        type=float,
        default=Config.random_direction_change,
    )
    parser.add_argument(
        "--blur",
        choices=["mean", "gaussian", "bilateral", "custom"],
        default=Config.blur,
    )
    parser.add_argument(
        "--stimulus",
        nargs="*",
        default=[],
        metavar="X,Y",
        help="Chemoattractant source coordinates.",
    )
    parser.add_argument("--output", default=Config.output)
    parser.add_argument(
        "--trails",
        action="store_true",
        help="Render trail intensity instead of agent dots.",
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run without opening a window (still writes video).",
    )
    return parser


def parse_stimulus(values):
    points = []
    for value in values:
        x, y = value.split(",")
        points.append((int(x), int(y)))
    return tuple(points)


def config_from_args(args):
    return Config(
        width=args.width,
        height=args.height,
        num_agents=args.num_agents,
        num_steps=args.num_steps,
        decay_rate=args.decay_rate,
        seed=args.seed,
        sensor_offset=args.sensor_offset,
        deposit_rate=args.deposit_rate,
        random_direction_change=args.random_direction_change,
        blur=args.blur,
        stimulus_points=parse_stimulus(args.stimulus),
        show_agents=not args.trails,
        output=args.output,
    )


def run(argv=None):
    args = build_parser().parse_args(argv)
    config = config_from_args(args)

    if args.headless:

        from physarum.simulate import open_writer, simulate

        writer = open_writer(config)
        try:
            simulate(config, headless=True, writer=writer)
        finally:
            writer.release()
        return

    main(config)


if __name__ == "__main__":
    run()
