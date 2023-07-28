from __future__ import annotations

import argparse
import json

from together import Files, extract_time


def add_parser(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    COMMAND_NAME = "files"
    parser = subparsers.add_parser(COMMAND_NAME)

    child_parsers = parser.add_subparsers(required=True)

    _add_list(child_parsers)
    _add_upload(child_parsers)
    _add_delete(child_parsers)
    _add_retrieve(child_parsers)
    _add_retrieve_content(child_parsers)


def _add_list(parser: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    subparser = parser.add_parser("list")
    subparser.set_defaults(func=_run_list)


def _add_upload(parser: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    subparser = parser.add_parser("upload")
    subparser.add_argument(
        "file",
        metavar="FILENAME",
        help="Local file to upload",
        type=str,
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
    files = Files()
    response = files.list()
    response["data"].sort(key=extract_time)
    print(json.dumps(response, indent=4))


def _run_upload(args: argparse.Namespace) -> None:
    files = Files()
    response = files.upload(args.file)
    print(json.dumps(response, indent=4))


def _run_delete(args: argparse.Namespace) -> None:
    files = Files()
    response = files.delete(args.file_id)
    print(json.dumps(response, indent=4))


def _run_retrieve(args: argparse.Namespace) -> None:
    files = Files()
    response = files.retrieve(args.file_id)
    print(json.dumps(response, indent=4))


def _run_retrieve_content(args: argparse.Namespace) -> None:
    files = Files()
    output = files.retrieve_content(args.file_id, args.output)
    print(output)
