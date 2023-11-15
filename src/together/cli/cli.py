#! python
import argparse

import together
from together.commands import chat, complete, embeddings, files, finetune, image, models
from together.utils import get_logger


logger = get_logger(str(__name__))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Together CLI",
        prog="together",
    )

    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version="%(prog)s " + together.version,
    )

    parser.add_argument(
        "--endpoint",
        "-e",
        help="[Optional] Together API Endpoint URL",
        type=str,
        required=False,
        default=None,
    )

    parser.add_argument(
        "--verbose",
        "-v",
        default=together.log_level,
        choices=["CRITICAL", "ERROR", "WARNING", "SUCCESS", "INFO", "DEBUG", "TRACE"],
        type=str,
        help="Set logging level. Defaults to WARNING. DEBUG will show all logs.",
        required=False,
    )

    subparser = parser.add_subparsers(dest="base")

    models.add_parser(subparser)
    chat.add_parser(subparser)
    complete.add_parser(subparser)
    image.add_parser(subparser)
    files.add_parser(subparser)
    finetune.add_parser(subparser)
    embeddings.add_parser(subparser)

    args = parser.parse_args()

    # Setup logging
    together.log_level = args.verbose

    try:
        args.func(args)
    except AttributeError as e:
        # print error, but ignore if `together` is run.
        if str(e) != "'Namespace' object has no attribute 'func'":
            raise together.AttributeError(e)
        parser.print_help()


if __name__ == "__main__":
    main()
