from __future__ import annotations

import argparse
import json
import os

from tabulate import tabulate

import together
from together import Finetune
from together.utils import finetune_price_to_dollars, get_logger, parse_timestamp


logger = get_logger(str(__name__))


def add_parser(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    COMMAND_NAME = "finetune"
    parser = subparsers.add_parser(COMMAND_NAME)

    child_parsers = parser.add_subparsers(required=True)

    _add_create(child_parsers)
    _add_list(child_parsers)
    _add_retrieve(child_parsers)
    _add_list_events(child_parsers)
    _add_cancel(child_parsers)
    _add_download(child_parsers)
    _add_status(child_parsers)
    _add_checkpoints(child_parsers)


def _add_create(parser: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    # Create_finetune
    subparser = parser.add_parser("create")
    subparser.add_argument(
        "--training-file",
        "-t",
        metavar="FILE-ID",
        help="File-ID of an uploaded file that contains training data.",
        required=True,
        type=str,
    )
    subparser.add_argument(
        "--estimate-price",
        "-e",
        help="Estimate the price of the fine tune job",
        required=False,
        action="store_true",
    )
    subparser.add_argument(
        "--model",
        "-m",
        metavar="MODEL",
        default=None,
        help="The name of the base model to fine-tune. Default='togethercomputer/RedPajama-INCITE-7B-Chat'.",
        type=str,
    )
    subparser.add_argument(
        "--n-epochs",
        "-ne",
        metavar="EPOCHS",
        default=4,
        help="The number of epochs to train the model for. Default=4",
        type=int,
    )
    subparser.add_argument(
        "--n-checkpoints",
        "-c",
        metavar="CHECKPOINTS",
        default=1,
        help="The number of checkpoints to save during training. Default=1 (a checkpoint is always saved on the last epoch for the trained model).",
        type=int,
    )
    subparser.add_argument(
        "--batch-size",
        "-b",
        metavar="BATCH_SIZE",
        default=None,
        help="The batch size to use for training. Default=32",
        type=int,
    )
    subparser.add_argument(
        "--learning-rate",
        "-lr",
        metavar="LEARNING_RATE",
        default=0.00001,
        help="The learning rate multiplier to use for training. Default=0.00001",
        type=float,
    )
    subparser.add_argument(
        "--suffix",
        "-s",
        metavar="SUFFIX",
        default=None,
        help="Up to 40 characters that will be added to your fine-tuned model name.",
        type=str,
    )
    subparser.add_argument(
        "--wandb-api-key",
        "-wb",
        metavar="WANDB_API_KEY",
        default=os.getenv("WANDB_API_KEY"),
        help="Wandb API key to report metrics to wandb.ai. If not set WANDB_API_KEY environment variable is used.",
        type=str,
    )
    subparser.add_argument(
        "--no-wandb-api-key",
        "-nwb",
        default=False,
        help="Do not report metrics to wandb.ai.",
        action="store_true",
    )
    subparser.add_argument(
        "--quiet",
        default=False,
        action="store_true",
        help="Indicates whether to disable checking",
    )

    subparser.set_defaults(func=_run_create)


def _add_list(parser: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    # List_Finetune
    subparser = parser.add_parser("list")
    subparser.add_argument(
        "--raw",
        help="Raw JSON dump of response",
        default=False,
        action="store_true",
    )
    subparser.set_defaults(func=_run_list)


def _add_retrieve(parser: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    subparser = parser.add_parser("retrieve")
    subparser.add_argument(
        "fine_tune_id",
        metavar="FINETUNE-ID",
        default=None,
        help="Fine-tuning ID",
        type=str,
    )
    subparser.add_argument(
        "--raw",
        help="Raw JSON dump of response",
        default=False,
        action="store_true",
    )
    subparser.set_defaults(func=_run_retrieve)


def _add_cancel(parser: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    # Cancel Finetune
    subparser = parser.add_parser("cancel")
    subparser.add_argument(
        "fine_tune_id",
        metavar="FINETUNE-ID",
        default=None,
        help="Fine-tuning ID",
        type=str,
    )
    subparser.set_defaults(func=_run_cancel)


def _add_list_events(
    parser: argparse._SubParsersAction[argparse.ArgumentParser],
) -> None:
    # List finetune events
    subparser = parser.add_parser("list-events")
    subparser.add_argument(
        "fine_tune_id",
        metavar="FINETUNE-ID",
        default=None,
        help="Fine-tuning ID",
        type=str,
    )
    subparser.add_argument(
        "--raw",
        help="Raw JSON dump of response",
        default=False,
        action="store_true",
    )
    subparser.set_defaults(func=_run_list_events)


def _add_download(parser: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    # List finetune events
    download_parser = parser.add_parser("download")
    download_parser.add_argument(
        "fine_tune_id",
        metavar="FINETUNE-ID",
        default=None,
        help="Fine-tuning ID",
        type=str,
    )
    download_parser.add_argument(
        "--output",
        "-o",
        metavar="FILENAME",
        default=None,
        help="Output filename. Defaults to remote name.",
        type=str,
        required=False,
    )
    download_parser.add_argument(
        "--checkpoint-step",
        "-s",
        default=-1,
        help="Checkpoint step to download. Defaults to the latest checkpoint = -1.",
        type=int,
        required=False,
    )
    download_parser.set_defaults(func=_run_download)


def _add_status(parser: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    # List finetune events
    status_parser = parser.add_parser("status")
    status_parser.add_argument(
        "fine_tune_id",
        metavar="FINETUNE-ID",
        default=None,
        help="Fine-tuning ID",
        type=str,
    )
    status_parser.set_defaults(func=_run_status)


def _add_checkpoints(
    parser: argparse._SubParsersAction[argparse.ArgumentParser],
) -> None:
    # List finetune events
    checkpoint_parser = parser.add_parser("checkpoints")
    checkpoint_parser.add_argument(
        "fine_tune_id",
        metavar="FINETUNE-ID",
        default=None,
        help="Fine-tuning ID",
        type=str,
    )
    checkpoint_parser.set_defaults(func=_run_checkpoint)


def _run_create(args: argparse.Namespace) -> None:
    finetune = Finetune()

    # Set default batch size based on model
    if args.batch_size is None:
        if args.model in [
            "togethercomputer/llama-2-70b",
            "togethercomputer/llama-2-70b-chat",
        ]:
            args.batch_size = 144
        else:
            args.batch_size = 32
    try:
        response = finetune.create(
            training_file=args.training_file,  # training file_id
            model=args.model,
            n_epochs=args.n_epochs,
            n_checkpoints=args.n_checkpoints,
            batch_size=args.batch_size,
            learning_rate=args.learning_rate,
            suffix=args.suffix,
            estimate_price=args.estimate_price,
            wandb_api_key=args.wandb_api_key if not args.no_wandb_api_key else None,
            confirm_inputs=not args.quiet,
        )
    except together.AuthenticationError:
        logger.critical(together.MISSING_API_KEY_MESSAGE)
        exit(0)

    print(json.dumps(response, indent=4))


def _run_list(args: argparse.Namespace) -> None:
    try:
        response = Finetune.list()
    except together.AuthenticationError:
        logger.critical(together.MISSING_API_KEY_MESSAGE)
        exit(0)
    response["data"].sort(key=lambda x: parse_timestamp(x["created_at"]))
    if args.raw:
        print(json.dumps(response, indent=4))
    else:
        display_list = []
        for i in response["data"]:
            display_list.append(
                {
                    "Fine-tune ID": i.get("id"),
                    "Model Output Name": i.get("model_output_name"),
                    "Status": i.get("status"),
                    "Created At": i.get("created_at"),
                    "Price": finetune_price_to_dollars(
                        float(str(i.get("total_price")))
                    ),  # convert to string for mypy typing
                }
            )
        table = tabulate(display_list, headers="keys", tablefmt="grid", showindex=True)
        print(table)


def _run_retrieve(args: argparse.Namespace) -> None:
    try:
        response = Finetune.retrieve(args.fine_tune_id)
    except together.AuthenticationError:
        logger.critical(together.MISSING_API_KEY_MESSAGE)
        exit(0)
    if args.raw:
        print(json.dumps(response, indent=4))
    else:
        table_data = [
            {"Key": key, "Value": value}
            for key, value in response.items()
            if key not in ["events", "model_output_path"]
        ]
        table = tabulate(table_data, tablefmt="grid")
        print(table)


def _run_cancel(args: argparse.Namespace) -> None:
    try:
        response = Finetune.cancel(args.fine_tune_id)
    except together.AuthenticationError:
        logger.critical(together.MISSING_API_KEY_MESSAGE)
        exit(0)
    print(json.dumps(response, indent=4))


def _run_list_events(args: argparse.Namespace) -> None:
    try:
        response = Finetune.list_events(args.fine_tune_id)
    except together.AuthenticationError:
        logger.critical(together.MISSING_API_KEY_MESSAGE)
        exit(0)
    if args.raw:
        print(json.dumps(response, indent=4))
    else:
        display_list = []
        for i in response["data"]:
            display_list.append(
                {
                    "Message": i.get("message"),
                    "Type": i.get("type"),
                    "Hash": i.get("hash"),
                }
            )
        table = tabulate(display_list, headers="keys", tablefmt="grid", showindex=True)
        print(table)


def _run_download(args: argparse.Namespace) -> None:
    try:
        response = Finetune.download(
            args.fine_tune_id, args.output, args.checkpoint_step
        )
    except together.AuthenticationError:
        logger.critical(together.MISSING_API_KEY_MESSAGE)
        exit(0)
    print(response)


def _run_status(args: argparse.Namespace) -> None:
    try:
        response = Finetune.get_job_status(args.fine_tune_id)
    except together.AuthenticationError:
        logger.critical(together.MISSING_API_KEY_MESSAGE)
        exit(0)
    print(response)


def _run_checkpoint(args: argparse.Namespace) -> None:
    try:
        checkpoints = Finetune.get_checkpoints(args.fine_tune_id)
    except together.AuthenticationError:
        logger.critical(together.MISSING_API_KEY_MESSAGE)
        exit(0)
    print(json.dumps(checkpoints, indent=4))
    print(f"\n{len(checkpoints)} checkpoints found")
