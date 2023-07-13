from __future__ import annotations

import argparse
import json
from typing import List

from together.files import Files


def add_parser(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
    parents: List[argparse.ArgumentParser],
) -> None:
    COMMAND_NAME = "files"
    parser = subparsers.add_parser(COMMAND_NAME)

    child_parsers = parser.add_subparsers(required=True)

    _add_list(child_parsers, parents=parents)
    _add_upload(child_parsers, parents=parents)
    _add_delete(child_parsers, parents=parents)
    _add_retrieve(child_parsers, parents=parents)
    _add_retrieve_content(child_parsers, parents=parents)


def _add_list(
    parser: argparse._SubParsersAction[argparse.ArgumentParser],
    parents: List[argparse.ArgumentParser],
) -> None:
    list_parser = parser.add_parser("list", parents=parents)
    list_parser.set_defaults(func=_run_list)


def _add_upload(
    parser: argparse._SubParsersAction[argparse.ArgumentParser],
    parents: List[argparse.ArgumentParser],
) -> None:
    upload_file_parser = parser.add_parser("upload", parents=parents)
    upload_file_parser.add_argument(
        "file",
        metavar="FILENAME",
        help="Local file to upload",
        type=str,
    )
    upload_file_parser.set_defaults(func=_run_upload)


def _add_delete(
    parser: argparse._SubParsersAction[argparse.ArgumentParser],
    parents: List[argparse.ArgumentParser],
) -> None:
    delete_file_parser = parser.add_parser("delete", parents=parents)
    delete_file_parser.add_argument(
        "file_id",
        metavar="FILE-ID",
        help="File ID of remote file",
        type=str,
    )
    delete_file_parser.set_defaults(func=_run_delete)


def _add_retrieve(
    parser: argparse._SubParsersAction[argparse.ArgumentParser],
    parents: List[argparse.ArgumentParser],
) -> None:
    retrieve_file_parser = parser.add_parser("retrieve", parents=parents)
    retrieve_file_parser.add_argument(
        "file_id",
        metavar="FILE-ID",
        help="File ID of remote file",
        type=str,
    )
    retrieve_file_parser.set_defaults(func=_run_retrieve)


def _add_retrieve_content(
    parser: argparse._SubParsersAction[argparse.ArgumentParser],
    parents: List[argparse.ArgumentParser],
) -> None:
    retrieve_file_content_parser = parser.add_parser(
        "retrieve-content", parents=parents
    )
    retrieve_file_content_parser.add_argument(
        "file_id",
        metavar="FILE-ID",
        help="File ID of remote file",
        type=str,
    )
    retrieve_file_content_parser.add_argument(
        "--output",
        "-o",
        default=None,
        metavar="OUT_FILENAME",
        help="Optional output filename. Defaults to remote filename.",
        type=str,
        required=False,
    )

    retrieve_file_content_parser.set_defaults(func=_run_retrieve_content)


def _run_list(args: argparse.Namespace) -> None:
    files = Files(args.endpoint, log_level=args.log)
    response = files.list_files()
    print(json.dumps(response, indent=4))


def _run_upload(args: argparse.Namespace) -> None:
    files = Files(args.endpoint, log_level=args.log)
    response = files.upload_file(args.file)
    print(json.dumps(response, indent=4))


def _run_delete(args: argparse.Namespace) -> None:
    files = Files(args.endpoint, log_level=args.log)
    response = files.delete_file(args.file_id)
    print(json.dumps(response, indent=4))


def _run_retrieve(args: argparse.Namespace) -> None:
    files = Files(args.endpoint, log_level=args.log)
    response = files.retrieve_file(args.file_id)
    print(json.dumps(response, indent=4))


def _run_retrieve_content(args: argparse.Namespace) -> None:
    files = Files(args.endpoint, log_level=args.log)
    output = files.retrieve_file_content(args.file_id, args.output)
    print(output)
