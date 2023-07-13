from __future__ import annotations

import argparse
import json
from typing import Any, Dict, List

from together.finetune import Finetune


def extract_time(json_obj: Dict[str, Any]) -> int:
    try:
        return int(json_obj["updated_at"])
    except KeyError:
        return 0


def add_parser(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
    parents: List[argparse.ArgumentParser],
) -> None:
    COMMAND_NAME = "finetune"
    parser = subparsers.add_parser(COMMAND_NAME)

    child_parsers = parser.add_subparsers(required=True)

    _add_create(child_parsers, parents=parents)
    _add_list(child_parsers, parents=parents)
    _add_retrieve(child_parsers, parents=parents)
    _add_list_events(child_parsers, parents=parents)
    _add_cancel(child_parsers, parents=parents)
    _add_download(child_parsers, parents=parents)
    _add_status(child_parsers, parents=parents)
    _add_checkpoints(child_parsers, parents=parents)
    # _add_delete_model(child_parsers)


def _add_create(
    parser: argparse._SubParsersAction[argparse.ArgumentParser],
    parents: List[argparse.ArgumentParser],
) -> None:
    # Create_finetune
    create_finetune_parser = parser.add_parser("create", parents=parents)
    create_finetune_parser.add_argument(
        "--training-file",
        "-t",
        metavar="FILE-ID",
        help="File-ID of an uploaded file that contains training data.",
        required=True,
        type=str,
    )
    # create_finetune_parser.add_argument(
    #     "--validation-file",
    #     "-v",
    #     default=None,
    #     help="The ID of an uploaded file that contains validation data.",
    #     type=str,
    # )
    create_finetune_parser.add_argument(
        "--model",
        "-m",
        metavar="MODEL",
        default=None,
        help="The name of the base model to fine-tune. Default='togethercomputer/RedPajama-INCITE-7B-Chat'.",
        type=str,
    )
    create_finetune_parser.add_argument(
        "--n-epochs",
        "-ne",
        metavar="EPOCHS",
        default=4,
        help="The number of epochs to train the model for. Default=4",
        type=int,
    )
    create_finetune_parser.add_argument(
        "--batch-size",
        "-b",
        metavar="BATCH_SIZE",
        default=32,
        help="The batch size to use for training. Default=32",
        type=int,
    )
    create_finetune_parser.add_argument(
        "--learning-rate",
        "-lr",
        metavar="LEARNING_RATE",
        default=0.00001,
        help="The learning rate multiplier to use for training. Default=0.00001",
        type=float,
    )
    # create_finetune_parser.add_argument(
    #     "--warmup-steps",
    #     "-ws",
    #     default=0,
    #     help="Warmup steps",
    #     type=int,
    # )
    # create_finetune_parser.add_argument(
    #     "--train-warmup-steps",
    #     "-tws",
    #     default=0,
    #     help="Train warmup steps",
    #     type=int,
    # )
    # create_finetune_parser.add_argument(
    #     "--sequence-length",
    #     "-sl",
    #     default=2048,
    #     help="Max sequence length",
    #     type=int,
    # )
    # create_finetune_parser.add_argument(
    #     "--seed",
    #     default=42,
    #     help="Training seed",
    #     type=int,
    # )
    # create_finetune_parser.add_argument(
    #     "--fp32",
    #     help="Enable FP32 training. Defaults to false (FP16 training).",
    #     default=False,
    #     action="store_true",
    # )
    # create_finetune_parser.add_argument(
    #     "--checkpoint-steps",
    #     "-b",
    #     default=0,
    #     help="Number of steps between each checkpoint. Defaults to 0 = checkpoints per epoch.",
    #     type=int,
    # )
    create_finetune_parser.add_argument(
        "--suffix",
        "-s",
        metavar="SUFFIX",
        default=None,
        help="Up to 40 characters that will be added to your fine-tuned model name.",
        type=str,
    )
    create_finetune_parser.set_defaults(func=_run_create)

    # End of create_finetune


def _add_list(
    parser: argparse._SubParsersAction[argparse.ArgumentParser],
    parents: List[argparse.ArgumentParser],
) -> None:
    # List_Finetune
    list_parser = parser.add_parser("list", parents=parents)
    list_parser.set_defaults(func=_run_list)


def _add_retrieve(
    parser: argparse._SubParsersAction[argparse.ArgumentParser],
    parents: List[argparse.ArgumentParser],
) -> None:
    retrieve_finetune_parser = parser.add_parser("retrieve", parents=parents)
    retrieve_finetune_parser.add_argument(
        "fine_tune_id",
        metavar="FINETUNE-ID",
        default=None,
        help="Fine-tuning ID",
        type=str,
    )
    retrieve_finetune_parser.set_defaults(func=_run_retrieve)


def _add_cancel(
    parser: argparse._SubParsersAction[argparse.ArgumentParser],
    parents: List[argparse.ArgumentParser],
) -> None:
    # Cancel Finetune
    cancel_finetune_parser = parser.add_parser("cancel", parents=parents)
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
    parents: List[argparse.ArgumentParser],
) -> None:
    # List finetune events
    list_finetune_events_parser = parser.add_parser("list-events", parents=parents)
    list_finetune_events_parser.add_argument(
        "fine_tune_id",
        metavar="FINETUNE-ID",
        default=None,
        help="Fine-tuning ID",
        type=str,
    )
    list_finetune_events_parser.set_defaults(func=_run_list_events)


def _add_download(
    parser: argparse._SubParsersAction[argparse.ArgumentParser],
    parents: List[argparse.ArgumentParser],
) -> None:
    # List finetune events
    download_parser = parser.add_parser("download", parents=parents)
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
    # download_parser.add_argument(
    #     "--checkpoint-num",
    #     "-n",
    #     default=-1,
    #     help="Checkpoint number. Defaults to the latest checkpoint = -1.",
    #     type=int,
    #     required=False,
    # )
    download_parser.set_defaults(func=_run_download)


def _add_status(
    parser: argparse._SubParsersAction[argparse.ArgumentParser],
    parents: List[argparse.ArgumentParser],
) -> None:
    # List finetune events
    status_parser = parser.add_parser("status", parents=parents)
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
    parents: List[argparse.ArgumentParser],
) -> None:
    # List finetune events
    checkpoint_parser = parser.add_parser("checkpoints", parents=parents)
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
    finetune = Finetune(args.endpoint, log_level=args.log)

    response = finetune.create_finetune(
        training_file=args.training_file,  # training file_id
        # validation_file=args.validation_file,  # validation file_id
        model=args.model,
        n_epochs=args.n_epochs,
        batch_size=args.batch_size,
        learning_rate=args.learning_rate,
        # warmup_steps=args.warmup_steps,
        # train_warmup_steps=args.train_warmup_steps,
        # seq_length=args.sequence_length,
        # seed=args.seed,
        # fp16=not args.fp32,
        # checkpoint_steps=args.checkpoint_steps,
        suffix=args.suffix,
    )

    print(json.dumps(response, indent=4))


def _run_list(args: argparse.Namespace) -> None:
    finetune = Finetune(args.endpoint, log_level=args.log)
    response = finetune.list_finetune()
    for item in response["data"]:
        item.pop("events", None)
    response["data"].sort(key=extract_time)
    print(json.dumps(response, indent=4))


def _run_retrieve(args: argparse.Namespace) -> None:
    finetune = Finetune(args.endpoint, log_level=args.log)
    response = finetune.retrieve_finetune(args.fine_tune_id)
    print(json.dumps(response, indent=4))


def _run_cancel(args: argparse.Namespace) -> None:
    finetune = Finetune(args.endpoint, log_level=args.log)
    response = finetune.cancel_finetune(args.fine_tune_id)
    print(json.dumps(response, indent=4))


def _run_list_events(args: argparse.Namespace) -> None:
    finetune = Finetune(args.endpoint, log_level=args.log)
    response = finetune.list_finetune_events(args.fine_tune_id)
    print(json.dumps(response, indent=4))


def _run_download(args: argparse.Namespace) -> None:
    finetune = Finetune(args.endpoint, log_level=args.log)
    args.checkpoint_num = -1  # hardcoded until enabled in remote
    response = finetune.download(args.fine_tune_id, args.output, args.checkpoint_num)
    print(response)


def _run_status(args: argparse.Namespace) -> None:
    finetune = Finetune(args.endpoint, log_level=args.log)
    response = finetune.get_job_status(args.fine_tune_id)
    print(response)


def _run_checkpoint(args: argparse.Namespace) -> None:
    finetune = Finetune(args.endpoint, log_level=args.log)
    checkpoints = finetune.get_checkpoints(args.fine_tune_id)
    print(json.dumps(checkpoints, indent=4))
    print(f"\n{len(checkpoints)} checkpoints found")


# def _run_delete_model(args: argparse.Namespace) -> None:
#     finetune = Finetune(args.endpoint)
#     response = finetune.delete_finetune_model(args.model)
#     print(json.dumps(response))
