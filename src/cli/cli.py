#! python

import argparse

from commands.api import api_args
from commands.files import files_args
from commands.finetune import finetune_args
from commands.inference import inference_args

from together.api import dispatch_api
from together.files import dispatch_files
from together.finetune import dispatch_finetune
from together.inference import dispatch_inference


def main():
    parser = argparse.ArgumentParser(
        description="CLI client for Together API",
        prog="together",
    )

    parser.add_argument("--key", "-k", help="Together API Key", type=str, required=False)

    subparser = parser.add_subparsers(dest="base")

    complete_parse = subparser.add_parser("complete")
    complete_parse = inference_args(complete_parse)
    complete_parse.set_defaults(func=dispatch_inference)

    finetune_parser = subparser.add_parser("finetune")
    finetune_parser = finetune_args(finetune_parser)
    finetune_parser.set_defaults(func=dispatch_finetune)

    files_parser = subparser.add_parser("files")
    files_parser = files_args(files_parser)
    files_parser.set_defaults(func=dispatch_files)

    api_parse = subparser.add_parser("api")
    api_parse = api_args(api_parse)
    api_parse.set_defaults(func=dispatch_api)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
