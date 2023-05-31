import argparse
from api import API
from finetune import Finetune
from files import Files
import json


def main():
    parser = argparse.ArgumentParser(
        description="CLI client for Together API",
        prog="together",
    )
    # parser.add_argument('SUBCOMMAND', choices=['complete', 'finetune', 'list-models'])
    subparser = parser.add_subparsers(dest="base")

    # -----Inference-----
    complete_parse = subparser.add_parser("complete")
    complete_parse.add_argument("--model", default=None, help="name/path of the model")
    complete_parse.add_argument(
        "--max-tokens",
        default=128,
        type=int,
        help="the maximum number of tokens to generate",
    )
    complete_parse.add_argument(
        "--sample",
        default=True,
        action="store_true",
        help="indicates whether to sample",
    )
    complete_parse.add_argument(
        "--temperature", default=0.6, type=float, help="temperature for the LM"
    )
    complete_parse.add_argument(
        "--top-k", default=40, type=int, help="top-k for the LM"
    )

    # change this to only work when SUBCOMMAND = list-models
    complete_parse.add_argument(
        "--all",
        default=False,
        action="store_true",
        help="list all models (available and unavailable)",
    )
    # -----End Inference-----

    # -----Fine tune-----
    finetune_parser = subparser.add_parser("finetune")

    # Required key for any finetune operation
    # TODO get key from env var
    finetune_parser.add_argument(
        "--key", "-k", help="Together API Key", type=str, required=True
    )

    finetune_subparser = finetune_parser.add_subparsers(dest="finetune")

    # Create_finetune
    create_finetune_parser = finetune_subparser.add_parser("create_finetune")
    create_finetune_parser.add_argument(
        "--training_file",
        "-t",
        help="The ID of an uploaded file that contains training data.",
        required=True,
        type=str,
    )
    create_finetune_parser.add_argument(
        "--validation_file",
        "-v",
        default=None,
        help="The ID of an uploaded file that contains validation data.",
        type=str,
    )
    create_finetune_parser.add_argument(
        "--model",
        "-m",
        default=None,
        help="The name of the base model to fine-tune.",
        type=str,
    )
    create_finetune_parser.add_argument(
        "--n_epochs",
        "-ne",
        default=4,
        help="The number of epochs to train the model for. An epoch refers to one full cycle through the training dataset.",
        type=int,
    )
    create_finetune_parser.add_argument(
        "--batch_size",
        "-b",
        default=None,
        help="The batch size to use for training. The batch size is the number of training examples used to train a single forward and backward pass.",
        type=int,
    )
    create_finetune_parser.add_argument(
        "--learning_rate_multiplier",
        "-lrm",
        default=None,
        help="The learning rate multiplier to use for training. The fine-tuning learning rate is the original learning rate used for pretraining multiplied by this value.",
        type=float,
    )
    create_finetune_parser.add_argument(
        "--prompt_loss_weight",
        "-plw",
        default=0.01,
        help="The weight to use for loss on the prompt tokens. This controls how much the model tries to learn to generate the prompt (as compared to the completion which always has a weight of 1.0), and can add a stabilizing effect to training when completions are short.",
        type=float,
    )
    create_finetune_parser.add_argument(
        "--compute_classification_metrics",
        "-ccm",
        default=False,
        action="store_true",
        help="If set, we calculate classification-specific metrics such as accuracy and F-1 score using the validation set at the end of every epoch",
    )
    create_finetune_parser.add_argument(
        "--classification_n_classes",
        "-cnc",
        default=None,
        help="The number of classes in a classification task.",
        type=int,
    )
    create_finetune_parser.add_argument(
        "--classification_positive_class",
        "-cpc",
        default=None,
        help="The positive class in binary classification.",
        type=str,
    )
    create_finetune_parser.add_argument(
        "--classification_betas",
        "-cb",
        default=None,
        help="If this is provided, we calculate F-beta scores at the specified beta values. The F-beta score is a generalization of F-1 score. This is only used for binary classification.",
        type=list,
    )
    create_finetune_parser.add_argument(
        "--suffix",
        "-s",
        default=None,
        help="A string of up to 40 characters that will be added to your fine-tuned model name.",
        type=str,
    )
    # End of create_finetune

    # List_Finetune
    list_finetune_parser = finetune_subparser.add_parser("list_finetune")
    retrieve_finetune_parser = finetune_subparser.add_parser("retrieve_finetune")
    retrieve_finetune_parser.add_argument(
        "--fine_tune_id",
        "-ft",
        default=None,
        help="Fine-tuning ID",
        type=str,
        required=True,
    )

    # Cancel Finetune
    cancel_finetune_parser = finetune_subparser.add_parser("cancel_finetune")
    cancel_finetune_parser.add_argument(
        "--fine_tune_id",
        "-ft",
        default=None,
        help="Fine-tuning ID",
        type=str,
        required=True,
    )

    # List finetune events
    list_finetune_events_parser = finetune_subparser.add_parser("list_finetune_events")
    list_finetune_events_parser.add_argument(
        "--fine_tune_id",
        "-ft",
        default=None,
        help="Fine-tuning ID",
        type=str,
        required=True,
    )

    # Delete finetune model
    delete_finetune_model_parser = finetune_subparser.add_parser(
        "delete_finetune_model"
    )
    delete_finetune_model_parser.add_argument(
        "--model",
        "-m",
        default=None,
        help="Model name",
        type=str,
        required=True,
    )
    # -----End Fine tune-----

    # -----Files-----
    files_parse = subparser.add_parser("files")

    # Required key for any finetune operation
    # TODO get key from env var
    files_parse.add_argument(
        "--key", "-k", help="Together API Key", type=str, required=True
    )

    files_subparser = files_parse.add_subparsers(dest="files")

    list_files_parser = files_subparser.add_parser("list_files")

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
    # -----End Files-----

    # -----API-----
    api_parse = subparser.add_parser("api")

    api_subparser = api_parse.add_subparsers(dest="api")

    # Create_finetune
    list_model_subparser = api_subparser.add_parser("list_models")
    list_model_subparser.add_argument(
        "--all",
        help="List all models (available and unavailable)",
        default=False,
        action="store_true",
    )
    raw_supply_subparser = api_subparser.add_parser("get_raw_supply")

    # -----End API-----
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
