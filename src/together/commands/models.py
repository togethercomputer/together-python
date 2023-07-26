from __future__ import annotations

import argparse
import json

from together import Models


def add_parser(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
) -> None:
    COMMAND_NAME = "models"
    parser = subparsers.add_parser(COMMAND_NAME)

    child_parsers = parser.add_subparsers(required=True)

    _add_list(child_parsers)
    _add_info(child_parsers)


def _add_list(
    parser: argparse._SubParsersAction[argparse.ArgumentParser],
) -> None:
    subparser = parser.add_parser("list")
    subparser.add_argument(
        "--raw",
        help="Raw details of all models",
        default=False,
        action="store_true",
    )
    subparser.set_defaults(func=_run_list)


def _add_info(
    parser: argparse._SubParsersAction[argparse.ArgumentParser],
) -> None:
    subparser = parser.add_parser("info")
    subparser.add_argument(
        "model",
        metavar="MODEL",
        help="Proper Model API string name",
        type=str,
    )
    subparser.add_argument(
        "--raw",
        help="Raw details of all models",
        default=False,
        action="store_true",
    )
    subparser.set_defaults(func=_run_info)


def _run_list(args: argparse.Namespace) -> None:
    models = Models()
    response = models.list()
    if args.raw:
        print(json.dumps(response, indent=4))
    else:
        model_list = []
        for i in response:
            model_list.append(i["name"])
        print(json.dumps(model_list, indent=4))


def _run_info(args: argparse.Namespace) -> None:
    models = Models()
    response = models.list()

    # list of keys to display by default from models info dict
    visible_keys = [
        "name",
        "display_name",
        "display_type",
        "description",
        "creator_organization",
        "hardware_label",
        "pricing_tier",
        "config",
        "base",
    ]

    for i in response:
        if i["name"] == args.model:
            if args.raw:
                print(json.dumps(i, indent=4))
            else:
                model_info = {key: i[key] for key in visible_keys if key in i}
                print(json.dumps(model_info, indent=4))
            break
