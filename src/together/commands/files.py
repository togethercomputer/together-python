from __future__ import annotations

import argparse
import json

from tabulate import tabulate

import together
from together import Files
from together.utils import bytes_to_human_readable, extract_time, get_logger


logger = get_logger(str(__name__))


def add_parser(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    COMMAND_NAME = "files"
    parser = subparsers.add_parser(COMMAND_NAME)

    child_parsers = parser.add_subparsers(required=True)

    _add_list(child_parsers)
    _add_check(child_parsers)
    _add_upload(child_parsers)
    _add_delete(child_parsers)
    _add_retrieve(child_parsers)
    _add_retrieve_content(child_parsers)


def _add_list(parser: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    subparser = parser.add_parser("list")
    subparser.add_argument(
        "--raw",
        help="Raw JSON dump of response",
        default=False,
        action="store_true",
    )
    subparser.set_defaults(func=_run_list)


def _add_check(parser: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    subparser = parser.add_parser("check")
    subparser.add_argument(
        "file",
        metavar="FILENAME",
        help="Local file to upload",
        type=str,
    )
    subparser.set_defaults(func=_run_check)


def _add_upload(parser: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    subparser = parser.add_parser("upload")
    subparser.add_argument(
        "file",
        metavar="FILENAME",
        help="Local file to upload",
        type=str,
    )
    subparser.add_argument(
        "--no-check",
        default=False,
        action="store_true",
        help="Indicates whether to disable checking",
    )
    subparser.add_argument(
        "--model",
        "-m",
        default=None,
        metavar="MODELNAME",
        help="check data for this model's special tokens",
        type=str,
        required=False,
    )
    subparser.set_defaults(func=_run_upload)


def _add_delete(parser: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    subparser = parser.add_parser("delete")
    subparser.add_argument(
        "file_id",
        metavar="FILE-ID",
        help="File ID of remote file",
        type=str,
    )
    subparser.set_defaults(func=_run_delete)


def _add_retrieve(parser: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    subparser = parser.add_parser("retrieve")
    subparser.add_argument(
        "file_id",
        metavar="FILE-ID",
        help="File ID of remote file",
        type=str,
    )
    subparser.add_argument(
        "--raw",
        help="Raw JSON dump of response",
        default=False,
        action="store_true",
    )
    subparser.set_defaults(func=_run_retrieve)


def _add_retrieve_content(
    parser: argparse._SubParsersAction[argparse.ArgumentParser],
) -> None:
    subparser = parser.add_parser("retrieve-content")
    subparser.add_argument(
        "file_id",
        metavar="FILE-ID",
        help="File ID of remote file",
        type=str,
    )
    subparser.add_argument(
        "--output",
        "-o",
        default=None,
        metavar="OUTPUT_FILE",
        help="Optional output filename. Defaults to remote filename.",
        type=str,
        required=False,
    )

    subparser.set_defaults(func=_run_retrieve_content)


def _run_list(args: argparse.Namespace) -> None:
    try:
        response = Files.list()
    except together.AuthenticationError:
        logger.critical(together.MISSING_API_KEY_MESSAGE)
        exit(0)
    response["data"].sort(key=extract_time)
    if args.raw:
        print(json.dumps(response, indent=4))
    else:
        display_list = []
        for i in response["data"]:
            display_list.append(
                {
                    "File name": i.get("filename"),
                    "File ID": i.get("id"),
                    "Size": bytes_to_human_readable(
                        float(str(i.get("bytes")))
                    ),  # convert to string for mypy typing
                    "Created At": i.get("created_at"),
                    "Line Count": i.get("LineCount"),
                }
            )
        table = tabulate(display_list, headers="keys", tablefmt="grid", showindex=True)
        print(table)


def _run_check(args: argparse.Namespace) -> None:
    try:
        response = Files.check(args.file)
    except together.AuthenticationError:
        logger.critical(together.MISSING_API_KEY_MESSAGE)
        exit(0)
    print(json.dumps(response, indent=4))


def _run_upload(args: argparse.Namespace) -> None:
    try:
        response = Files.upload(
            file=args.file, check=not args.no_check, model=args.model
        )
    except together.AuthenticationError:
        logger.critical(together.MISSING_API_KEY_MESSAGE)
        exit(0)
    print(json.dumps(response, indent=4))


def _run_delete(args: argparse.Namespace) -> None:
    try:
        response = Files.delete(args.file_id)
    except together.AuthenticationError:
        logger.critical(together.MISSING_API_KEY_MESSAGE)
        exit(0)
    print(json.dumps(response, indent=4))


def _run_retrieve(args: argparse.Namespace) -> None:
    try:
        response = Files.retrieve(args.file_id)
    except together.AuthenticationError:
        logger.critical(together.MISSING_API_KEY_MESSAGE)
        exit(0)
    if args.raw:
        print(json.dumps(response, indent=4))
    else:
        table_data = [{"Key": key, "Value": value} for key, value in response.items()]
        table = tabulate(table_data, tablefmt="grid")
        print(table)


def _run_retrieve_content(args: argparse.Namespace) -> None:
    try:
        output = Files.retrieve_content(args.file_id, args.output)
    except together.AuthenticationError:
        logger.critical(together.MISSING_API_KEY_MESSAGE)
        exit(0)
    print(output)
