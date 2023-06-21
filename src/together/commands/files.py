from __future__ import annotations

import argparse

from together.files import Files


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
    list_parser = parser.add_parser("list")
    list_parser.set_defaults(func=_run_list)


def _add_upload(parser: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    upload_file_parser = parser.add_parser("upload")
    upload_file_parser.add_argument(
        "--file",
        "-f",
        help="File to upload",
        type=str,
        required=True,
    )
    upload_file_parser.set_defaults(func=_run_upload)


def _add_delete(parser: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    delete_file_parser = parser.add_parser("delete")
    delete_file_parser.add_argument(
        "--file-id",
        "-f",
        help="File ID",
        type=str,
        required=True,
    )
    delete_file_parser.set_defaults(func=_run_delete)


def _add_retrieve(parser: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    retrieve_file_parser = parser.add_parser("retrieve")
    retrieve_file_parser.add_argument(
        "--file-id",
        "-f",
        help="File ID",
        type=str,
        required=True,
    )
    retrieve_file_parser.set_defaults(func=_run_retrieve)


def _add_retrieve_content(
    parser: argparse._SubParsersAction[argparse.ArgumentParser],
) -> None:
    retrieve_file_content_parser = parser.add_parser("retrieve-content")
    retrieve_file_content_parser.add_argument(
        "--file-id",
        "-f",
        help="File ID",
        type=str,
        required=True,
    )
    retrieve_file_content_parser.add_argument(
        "--output",
        "-o",
        help="Output filename",
        type=str,
        required=True,
    )

    retrieve_file_content_parser.set_defaults(func=_run_retrieve_content)


def _run_list(args: argparse.Namespace) -> None:
    files = Files(args.endpoint)
    response = files.list_files()
    print(response)


def _run_upload(args: argparse.Namespace) -> None:
    files = Files(args.endpoint)
    response = files.upload_file(args.file)
    print(response)


def _run_delete(args: argparse.Namespace) -> None:
    files = Files(args.endpoint)
    response = files.delete_file(args.file_id)
    print(response)


def _run_retrieve(args: argparse.Namespace) -> None:
    files = Files(args.endpoint)
    response = files.retrieve_file(args.file_id)
    print(response)


def _run_retrieve_content(args: argparse.Namespace) -> None:
    files = Files(args.endpoint)
    response = files.retrieve_file_content(args.file_id, args.output)
    print(response)