from __future__ import annotations

import argparse
import json
from typing import List

from together.api import API


def add_parser(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
    parents: List[argparse.ArgumentParser],
) -> None:
    COMMAND_NAME = "api"
    parser = subparsers.add_parser(COMMAND_NAME)

    child_parsers = parser.add_subparsers(required=True)

    _add_list(child_parsers, parents=parents)


def _add_list(
    parser: argparse._SubParsersAction[argparse.ArgumentParser],
    parents: List[argparse.ArgumentParser],
) -> None:
    list_model_subparser = parser.add_parser("list", parents=parents)
    list_model_subparser.add_argument(
        "--raw",
        help="Raw details of all models",
        default=False,
        action="store_true",
    )
    list_model_subparser.set_defaults(func=_run_list)


def _run_list(args: argparse.Namespace) -> None:
    api = API(endpoint_url=args.endpoint, log_level=args.log)
    response = api.get_models()
    if args.raw:
        print(json.dumps(response, indent=4))
    else:
        models = []
        for i in response:
            models.append(i["name"])
        print(json.dumps(models, indent=4))
