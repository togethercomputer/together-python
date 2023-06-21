from __future__ import annotations

import argparse
import json

from together.api import API


def add_parser(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    COMMAND_NAME = "api"
    parser = subparsers.add_parser(COMMAND_NAME)

    child_parsers = parser.add_subparsers(required=True)

    _add_list(child_parsers)
    _add_raw(child_parsers)


def _add_list(parser: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    list_model_subparser = parser.add_parser("list-models")
    list_model_subparser.add_argument(
        "--all",
        "-a",
        help="List all models (available and unavailable)",
        default=False,
        action="store_true",
    )
    list_model_subparser.set_defaults(func=_run_list)


def _add_raw(parser: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    list_parser = parser.add_parser("raw-supply")
    list_parser.set_defaults(func=_run_raw)


def _run_list(args: argparse.Namespace) -> None:
    api = API()

    if args.all:
        response = api.get_all_models()
    else:
        response = api.get_available_models()

    print(json.dumps(response))


def _run_raw(args: argparse.Namespace) -> None:
    api = API()
    response = json.dumps(api.get_supply())
    print(json.dumps(response))
