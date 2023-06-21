from __future__ import annotations

import argparse
import json

from together.finetune import Finetune


def add_parser(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    COMMAND_NAME = "finetune"
    parser = subparsers.add_parser(COMMAND_NAME)

    child_parsers = parser.add_subparsers(required=True)

    _add_create(child_parsers)
    _add_list(child_parsers)
    _add_retrieve(child_parsers)
    _add_cancel(child_parsers)
    _add_list_events(child_parsers)
    _add_delete_model(child_parsers)


def _add_create(parser: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    # Create_finetune
    create_finetune_parser = parser.add_parser("create")
    create_finetune_parser.add_argument(
        "--training-file",
        "-t",
        help="The ID of an uploaded file that contains training data.",
        required=True,
        type=str,
    )
    create_finetune_parser.add_argument(
        "--validation-file",
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
        "--n-epochs",
        "-ne",
        default=4,
        help="The number of epochs to train the model for.",
        type=int,
    )
    create_finetune_parser.add_argument(
        "--batch-size",
        "-b",
        default=None,
        help="The batch size to use for training.",
        type=int,
    )
    create_finetune_parser.add_argument(
        "--learning-rate-multiplier",
        "-lrm",
        default=None,
        help="The learning rate multiplier to use for training.",
        type=float,
    )
    create_finetune_parser.add_argument(
        "--prompt-loss-weight",
        "-plw",
        default=0.01,
        help="The weight to use for loss on the prompt tokens.",
        type=float,
    )
    create_finetune_parser.add_argument(
        "--compute-classification-metrics",
        "-ccm",
        default=False,
        action="store_true",
        help="Calculate classification-specific metrics using the validation set.",
    )
    create_finetune_parser.add_argument(
        "--classification-n-classes",
        "-cnc",
        default=None,
        help="The number of classes in a classification task.",
        type=int,
    )
    create_finetune_parser.add_argument(
        "--classification-positive-class",
        "-cpc",
        default=None,
        help="The positive class in binary classification.",
        type=str,
    )
    create_finetune_parser.add_argument(
        "--classification-betas",
        "-cb",
        default=None,
        help="Calculate F-beta scores at the specified beta values.",
        nargs="+",
        type=float,
    )
    create_finetune_parser.add_argument(
        "--suffix",
        "-s",
        default=None,
        help="Up to 40 characters that will be added to your fine-tuned model name.",
        type=str,
    )
    create_finetune_parser.set_defaults(func=_run_create)

    # End of create_finetune


def _add_list(parser: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    # List_Finetune
    list_parser = parser.add_parser("list")
    list_parser.set_defaults(func=_run_list)


def _add_retrieve(parser: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    retrieve_finetune_parser = parser.add_parser("retrieve")
    retrieve_finetune_parser.add_argument(
        "--fine-tune-id",
        "-ft",
        default=None,
        help="Fine-tuning ID",
        type=str,
        required=True,
    )
    retrieve_finetune_parser.set_defaults(func=_run_retrieve)


def _add_cancel(parser: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    # Cancel Finetune
    cancel_finetune_parser = parser.add_parser("cancel")
    cancel_finetune_parser.add_argument(
        "--fine-tune-id",
        "-ft",
        default=None,
        help="Fine-tuning ID",
        type=str,
        required=True,
    )
    cancel_finetune_parser.set_defaults(func=_run_cancel)


def _add_list_events(
    parser: argparse._SubParsersAction[argparse.ArgumentParser],
) -> None:
    # List finetune events
    list_finetune_events_parser = parser.add_parser("list-events")
    list_finetune_events_parser.add_argument(
        "--fine-tune-id",
        "-ft",
        default=None,
        help="Fine-tuning ID",
        type=str,
        required=True,
    )
    list_finetune_events_parser.set_defaults(func=_run_list_events)


def _add_delete_model(
    parser: argparse._SubParsersAction[argparse.ArgumentParser],
) -> None:
    # Delete finetune model
    delete_finetune_model_parser = parser.add_parser("delete-model")
    delete_finetune_model_parser.add_argument(
        "--model",
        "-m",
        default=None,
        help="Model name",
        type=str,
        required=True,
    )
    delete_finetune_model_parser.set_defaults(func=_run_delete_model)


def _run_create(args: argparse.Namespace) -> None:
    finetune = Finetune(args.endpoint)

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


def _run_list(args: argparse.Namespace) -> None:
    finetune = Finetune(args.endpoint)
    response = finetune.list_finetune()
    print(json.dumps(response))


def _run_retrieve(args: argparse.Namespace) -> None:
    finetune = Finetune(args.endpoint)
    response = finetune.retrieve_finetune(args.fine_tune_id)
    print(json.dumps(response))


def _run_cancel(args: argparse.Namespace) -> None:
    finetune = Finetune(args.endpoint)
    response = finetune.cancel_finetune(args.fine_tune_id)
    print(json.dumps(response))


def _run_list_events(args: argparse.Namespace) -> None:
    finetune = Finetune(args.endpoint)
    response = finetune.list_finetune_events(args.fine_tune_id)
    print(json.dumps(response))


def _run_delete_model(args: argparse.Namespace) -> None:
    finetune = Finetune(args.endpoint)
    response = finetune.delete_finetune_model(args.model)
    print(json.dumps(response))
