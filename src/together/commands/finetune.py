from __future__ import annotations

import argparse
import json
import os

from together import Finetune, extract_time


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
    # _add_delete_model(child_parsers)


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
    # subparser.add_argument(
    #     "--validation-file",
    #     "-v",
    #     default=None,
    #     help="The ID of an uploaded file that contains validation data.",
    #     type=str,
    # )
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
        default=32,
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
    # subparser.add_argument(
    #     "--warmup-steps",
    #     "-ws",
    #     default=0,
    #     help="Warmup steps",
    #     type=int,
    # )
    # subparser.add_argument(
    #     "--train-warmup-steps",
    #     "-tws",
    #     default=0,
    #     help="Train warmup steps",
    #     type=int,
    # )
    # subparser.add_argument(
    #     "--sequence-length",
    #     "-sl",
    #     default=2048,
    #     help="Max sequence length",
    #     type=int,
    # )
    # subparser.add_argument(
    #     "--seed",
    #     default=42,
    #     help="Training seed",
    #     type=int,
    # )
    # subparser.add_argument(
    #     "--fp32",
    #     help="Enable FP32 training. Defaults to false (FP16 training).",
    #     default=False,
    #     action="store_true",
    # )
    # subparser.add_argument(
    #     "--checkpoint-steps",
    #     "-b",
    #     default=0,
    #     help="Number of steps between each checkpoint. Defaults to 0 = checkpoints per epoch.",
    #     type=int,
    # )
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

    subparser.set_defaults(func=_run_create)

    # End of create_finetune


def _add_list(parser: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    # List_Finetune
    list_parser = parser.add_parser("list")
    list_parser.set_defaults(func=_run_list)


def _add_retrieve(parser: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    retrieve_finetune_parser = parser.add_parser("retrieve")
    retrieve_finetune_parser.add_argument(
        "fine_tune_id",
        metavar="FINETUNE-ID",
        default=None,
        help="Fine-tuning ID",
        type=str,
    )
    retrieve_finetune_parser.set_defaults(func=_run_retrieve)


def _add_cancel(parser: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    # Cancel Finetune
    cancel_finetune_parser = parser.add_parser("cancel")
    cancel_finetune_parser.add_argument(
        "fine_tune_id",
        metavar="FINETUNE-ID",
        default=None,
        help="Fine-tuning ID",
        type=str,
    )
    cancel_finetune_parser.set_defaults(func=_run_cancel)


def _add_list_events(
    parser: argparse._SubParsersAction[argparse.ArgumentParser],
) -> None:
    # List finetune events
    list_finetune_events_parser = parser.add_parser("list-events")
    list_finetune_events_parser.add_argument(
        "fine_tune_id",
        metavar="FINETUNE-ID",
        default=None,
        help="Fine-tuning ID",
        type=str,
    )
    list_finetune_events_parser.set_defaults(func=_run_list_events)


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


# def _add_delete_model(
#     parser: argparse._SubParsersAction[argparse.ArgumentParser],
# ) -> None:
#     # Delete finetune model
#     delete_finetune_model_parser = parser.add_parser("delete-model")
#     delete_finetune_model_parser.add_argument(
#         "--model",
#         "-m",
#         default=None,
#         help="Model name",
#         type=str,
#         required=True,
#     )
#     delete_finetune_model_parser.set_defaults(func=_run_delete_model)


def _run_create(args: argparse.Namespace) -> None:
    finetune = Finetune()

    response = finetune.create(
        training_file=args.training_file,  # training file_id
        # validation_file=args.validation_file,  # validation file_id
        model=args.model,
        n_epochs=args.n_epochs,
        n_checkpoints=args.n_checkpoints,
        batch_size=args.batch_size,
        learning_rate=args.learning_rate,
        # warmup_steps=args.warmup_steps,
        # train_warmup_steps=args.train_warmup_steps,
        # seq_length=args.sequence_length,
        # seed=args.seed,
        # fp16=not args.fp32,
        # checkpoint_steps=args.checkpoint_steps,
        suffix=args.suffix,
        wandb_api_key=args.wandb_api_key if not args.no_wandb_api_key else None,
    )

    print(json.dumps(response, indent=4))


def _run_list(args: argparse.Namespace) -> None:
    finetune = Finetune()
    response = finetune.list()
    for item in response["data"]:
        item.pop("events", None)
    response["data"].sort(key=extract_time)
    print(json.dumps(response, indent=4))


def _run_retrieve(args: argparse.Namespace) -> None:
    finetune = Finetune()
    response = finetune.retrieve(args.fine_tune_id)
    print(json.dumps(response, indent=4))


def _run_cancel(args: argparse.Namespace) -> None:
    finetune = Finetune()
    response = finetune.cancel(args.fine_tune_id)
    print(json.dumps(response, indent=4))


def _run_list_events(args: argparse.Namespace) -> None:
    finetune = Finetune()
    response = finetune.list_events(args.fine_tune_id)
    print(json.dumps(response, indent=4))


def _run_download(args: argparse.Namespace) -> None:
    finetune = Finetune()
    response = finetune.download(args.fine_tune_id, args.output, args.checkpoint_step)
    print(response)


def _run_status(args: argparse.Namespace) -> None:
    finetune = Finetune()
    response = finetune.get_job_status(args.fine_tune_id)
    print(response)


def _run_checkpoint(args: argparse.Namespace) -> None:
    finetune = Finetune()
    checkpoints = finetune.get_checkpoints(args.fine_tune_id)
    print(json.dumps(checkpoints, indent=4))
    print(f"\n{len(checkpoints)} checkpoints found")


# def _run_delete_model(args: argparse.Namespace) -> None:
#     finetune = Finetune(args.endpoint)
#     response = finetune.delete_finetune_model(args.model)
#     print(json.dumps(response))
