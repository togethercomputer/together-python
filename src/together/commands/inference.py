from __future__ import annotations

import argparse

from together.inference import Inference


def add_parser(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    COMMAND_NAME = "complete"
    inf_parser = subparsers.add_parser(COMMAND_NAME)

    inf_parser.add_argument(
        "--prompt",
        default=None,
        type=str,
        help="Prompt to complete",
        required=True,
    )
    inf_parser.add_argument(
        "--model",
        default=None,
        type=str,
        help="name/path of the model",
    )
    inf_parser.add_argument(
        "--task",
        default=None,
        type=str,
        help="task",
    )
    inf_parser.add_argument(
        "--max-tokens",
        default=128,
        type=int,
        help="the maximum number of tokens to generate",
    )
    inf_parser.add_argument(
        "--stop-words",
        default=None,
        nargs="+",
        type=str,
        help="stop word",
    )
    inf_parser.add_argument(
        "--temperature",
        default=0.7,
        type=float,
        help="temperature for the LM",
    )
    inf_parser.add_argument(
        "--top-p",
        default=0.7,
        type=float,
        help="top-p for the LM",
    )
    inf_parser.add_argument(
        "--top-k",
        default=50,
        type=int,
        help="top-k for the LM",
    )
    inf_parser.add_argument(
        "--repetition-penalty",
        default=None,
        type=float,
        help="repetition penaltyfor the LM",
    )
    inf_parser.add_argument(
        "--logprobs",
        default=None,
        type=int,
        help="logprobs for the LM",
    )
    inf_parser.add_argument(
        "--raw",
        default=False,
        action="store_true",
        help="temperature for the LM",
    )

    inf_parser.set_defaults(func=run_complete)


def run_complete(args: argparse.Namespace) -> None:
    inference = Inference(
        endpoint_url=args.endpoint,
        task=args.task,
        model=args.model,
        max_tokens=args.max_tokens,
        # stop_word= args.stop_word,
        temperature=args.temperature,
        top_p=args.top_p,
        top_k=args.top_k,
        repetition_penalty=args.repetition_penalty,
        logprobs=args.logprobs,
        raw=args.raw,
    )

    if not args.raw:
        response = inference.inference(prompt=args.prompt, stop=args.stop_words)
        print(response)
    else:
        raw_response = inference.raw_inference(prompt=args.prompt)
        print(raw_response)
