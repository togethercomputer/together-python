#! python
import argparse

from together.commands import api, files, finetune, inference


def main() -> None:
    parser = argparse.ArgumentParser(
        description="CLI client for Together API",
        prog="together",
    )

    parser.add_argument(
        "--endpoint",
        "-e",
        help="[Optional] Together API Endpoint URL",
        type=str,
        required=False,
        default=None,
    )

    subparser = parser.add_subparsers(dest="base")

    api.add_parser(subparser)
    inference.add_parser(subparser)
    finetune.add_parser(subparser)
    files.add_parser(subparser)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
