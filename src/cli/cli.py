#! python

import argparse
import json

from together.api import API
from together.finetune import Finetune
from together.files import Files

from commands.inference import inference_args
from commands.finetune import finetune_args
from commands.files import files_args
from commands.api import api_args


def main():
    parser = argparse.ArgumentParser(
        description="CLI client for Together API",
        prog="together",
    )

    subparser = parser.add_subparsers(dest="base")

    complete_parse = subparser.add_parser("complete")
    complete_parse = inference_args(complete_parse)

    finetune_parser = subparser.add_parser("finetune")
    finetune_parser = finetune_args(finetune_parser)

    files_parser = subparser.add_parser("files")
    files_parser = files_args(files_parser)

    api_parse = subparser.add_parser("api")
    api_parse = api_args(api_parse)

    args = parser.parse_args()
    if args.base == "complete":
        print("complete")
    elif args.base == "finetune":
        finetune = Finetune(args.key)

        if args.finetune == "create_finetune":
            response = finetune.create_finetune(
                training_file=args.training_file,  # training file_id
                validation_file=args.validation_file,  # validation file_id
                model=args.model,
                n_epochs=args.n_epochs,
                batch_size=args.batch_size,
                learning_rate_multiplier=args.learning_rate_multiplier,
                prompt_loss_weight=args.prompt_loss_weight,
                compute_classification_metrics=args.compute_classification_metrics,
                classification_n_classes=args.classification_n_classes,
                classification_positive_class=args.classification_positive_class,
                classification_betas=args.classification_betas,
                suffix=args.suffix,
            )
            print(response)

        elif args.finetune == "list_finetune":
            response = finetune.list_finetune()
            print(response)

        elif args.finetune == "retrieve_finetune":
            response = finetune.retrieve_finetune(args.fine_tune_id)
            print(response)

        elif args.finetune == "cancel_finetune":
            response = finetune.cancel_finetune(args.fine_tune_id)
            print(response)

        elif args.finetune == "list_finetune_events":
            response = finetune.list_finetune_events(args.fine_tune_id)
            print(response)

        elif args.finetune == "delete_finetune_model":
            response = finetune.delete_finetune_model(args.model)
            print(response)

    elif args.base == "files":
        files = Files(args.key)

        if args.files == "list_files":
            response = files.list_files()
            print(response)

        elif args.files == "upload_file":
            response = files.upload_file(args.file)
            print(response)

        elif args.files == "delete_file":
            response = files.delete_file(args.file_id)
            print(response)

        elif args.files == "retrieve_file":
            response = files.retrieve_file(args.file_id)
            print(response)

        elif args.files == "retrieve_file_content":
            response = files.retrieve_file_content(args.file_id, args.output)
            print(response)

    elif args.base == "api":
        api = API()
        if args.api == "list_models":
            if args.all:
                api.print_all_models()
            else:
                api.print_available_models()
        elif args.api == "get_raw_supply":
            response = api.get_supply()
            print(json.dumps(response))


if __name__ == "__main__":
    main()
