def files_args(parser):
    files_subparser = parser.add_subparsers(dest="files")

    files_subparser.add_parser("list_files")

    upload_file_parser = files_subparser.add_parser("upload_file")
    upload_file_parser.add_argument(
        "--file",
        "-f",
        help="File to upload",
        type=str,
        required=True,
    )

    delete_file_parser = files_subparser.add_parser("delete_file")
    delete_file_parser.add_argument(
        "--file_id",
        "-f",
        help="File ID",
        type=str,
        required=True,
    )

    retrieve_file_parser = files_subparser.add_parser("retrieve_file")
    retrieve_file_parser.add_argument(
        "--file_id",
        "-f",
        help="File ID",
        type=str,
        required=True,
    )

    retrieve_file_content_parser = files_subparser.add_parser("retrieve_file_content")
    retrieve_file_content_parser.add_argument(
        "--file_id",
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

    return parser
