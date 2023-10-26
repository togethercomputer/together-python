from __future__ import annotations

import argparse
import json

from tabulate import tabulate

import together
from together.utils import get_logger


logger = get_logger(str(__name__))


def add_parser(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
) -> None:
    COMMAND_NAME = "models"
    parser = subparsers.add_parser(COMMAND_NAME)

    child_parsers = parser.add_subparsers(required=True)

    _add_list(child_parsers)
    _add_info(child_parsers)
    _add_instances(child_parsers)
    _add_start(child_parsers)
    _add_stop(child_parsers)
    _add_ready(child_parsers)


def _add_list(
    parser: argparse._SubParsersAction[argparse.ArgumentParser],
) -> None:
    subparser = parser.add_parser("list")
    subparser.add_argument(
        "--details",
        help="List all details",
        default=False,
        action="store_true",
    )
    subparser.add_argument(
        "--raw",
        help="Raw JSON dump of response",
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


def _add_instances(
    parser: argparse._SubParsersAction[argparse.ArgumentParser],
) -> None:
    subparser = parser.add_parser("instances")
    subparser.add_argument(
        "--raw",
        help="Raw list of instances",
        default=False,
        action="store_true",
    )
    subparser.set_defaults(func=_run_instances)


def _add_start(
    parser: argparse._SubParsersAction[argparse.ArgumentParser],
) -> None:
    subparser = parser.add_parser("start")
    subparser.add_argument(
        "model",
        metavar="MODEL",
        help="Proper Model API string name",
        type=str,
    )
    subparser.set_defaults(func=_run_start)


def _add_stop(
    parser: argparse._SubParsersAction[argparse.ArgumentParser],
) -> None:
    subparser = parser.add_parser("stop")
    subparser.add_argument(
        "model",
        metavar="MODEL",
        help="Proper Model API string name",
        type=str,
    )
    subparser.set_defaults(func=_run_stop)


def _add_ready(
    parser: argparse._SubParsersAction[argparse.ArgumentParser],
) -> None:
    subparser = parser.add_parser("ready")
    subparser.add_argument(
        "model",
        metavar="MODEL",
        help="Proper Model API string name",
        type=str,
    )
    subparser.set_defaults(func=_run_ready)


def _run_list(args: argparse.Namespace) -> None:
    try:
        response = together.Models.list()
    except together.AuthenticationError:
        logger.critical(together.MISSING_API_KEY_MESSAGE)
        exit(0)
    if args.raw:
        print(json.dumps(response, indent=4))
    else:
        if not args.details:
            display_list = []
            for i in response:
                display_list.append(
                    {
                        "Name": i.get("display_name"),
                        "Model String": i.get("name"),
                        "Type": i.get("display_type"),
                    }
                )
        else:
            display_list = []
            for i in response:
                display_list.append(
                    {
                        "Name": i.get("display_name"),
                        "Model String": i.get("name"),
                        "Type": i.get("display_type"),
                        "Parameters": i.get("num_parameters"),
                        "Context": i.get("context_length"),
                        "Hardware": i.get("hardware_label"),
                    }
                )
        table = tabulate(display_list, headers="keys", tablefmt="grid")
        print(table)


def _run_info(args: argparse.Namespace) -> None:
    try:
        model_info = together.Models.info(args.model)
    except together.AuthenticationError:
        logger.critical(together.MISSING_API_KEY_MESSAGE)
        exit(0)

    if args.raw:
        print(json.dumps(model_info, indent=4))
    else:
        hidden_keys = [
            "_id",
            "modelInstanceConfig",
            "created_at",
            "update_at",
            "pricing",
            "show_in_playground",
            "access",
            "pricing_tier",
            "hardware_label",
            "depth",
            "descriptionLink",
        ]

        table_data = [
            {"Key": key, "Value": value}
            for key, value in model_info.items()
            if key not in hidden_keys
        ]
        table = tabulate(table_data, tablefmt="grid")
        print(table)


def _run_instances(args: argparse.Namespace) -> None:
    try:
        response = together.Models.instances()
    except together.AuthenticationError:
        logger.critical(together.MISSING_API_KEY_MESSAGE)
        exit(0)

    if args.raw:
        print(json.dumps(response, indent=4))
    else:
        started_instances = [key for key in response.keys() if response[key] is True]
        print(json.dumps(started_instances, indent=4))


def _run_start(args: argparse.Namespace) -> None:
    try:
        response = together.Models.start(args.model)
    except together.AuthenticationError:
        logger.critical(together.MISSING_API_KEY_MESSAGE)
        exit(0)
    print(json.dumps(response, indent=4))


def _run_stop(args: argparse.Namespace) -> None:
    try:
        response = together.Models.stop(args.model)
    except together.AuthenticationError:
        logger.critical(together.MISSING_API_KEY_MESSAGE)
        exit(0)
    print(json.dumps(response, indent=4))


def _run_ready(args: argparse.Namespace) -> None:
    try:
        response = together.Models.ready(args.model)
    except together.AuthenticationError:
        logger.critical(together.MISSING_API_KEY_MESSAGE)
        exit(0)
    print(json.dumps(response, indent=4))
