#! python
import argparse

from together.commands import api, chat, files, finetune, inference
from together.utils.utils import get_logger


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

    base_subparser = argparse.ArgumentParser(add_help=False)
    base_subparser.add_argument(
        "--log",
        default="WARNING",
        choices=["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"],
        type=str,
        help="Set logging level. Defaults to WARNING. DEBUG will show all logs.",
        required=False,
    )

    subparser = parser.add_subparsers(dest="base")

    api.add_parser(subparser, parents=[base_subparser])
    inference.add_parser(subparser, parents=[base_subparser])
    finetune.add_parser(subparser, parents=[base_subparser])
    files.add_parser(subparser, parents=[base_subparser])
    chat.add_parser(subparser, parents=[base_subparser])

    args = parser.parse_args()

    # Setup logging
    try:
        get_logger(__name__, log_level=args.log)
    except Exception:
        get_logger(__name__, log_level="WARNING")

    # try:
    args.func(args)
    # except AttributeError as e:
    #    # print error, but ignore if `together` is run.
    ##    if str(e) != "'Namespace' object has no attribute 'func'":
    #        logger.critical(f"Error raised: {e}")
    #        exit_1(logger)
    #    parser.print_help()


if __name__ == "__main__":
    main()
