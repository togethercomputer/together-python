import argparse


def api_args(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    api_subparser = parser.add_subparsers(dest="api")

    list_model_subparser = api_subparser.add_parser("list-models")
    list_model_subparser.add_argument(
        "--all",
        help="List all models (available and unavailable)",
        default=False,
        action="store_true",
    )

    api_subparser.add_parser("get-raw-supply")

    return parser
