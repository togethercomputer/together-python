import argparse


def inference_args(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    parser.add_argument(
        "--prompt",
        default=None,
        type=str,
        help="Prompt to complete",
        required=True,
    )
    parser.add_argument(
        "--model",
        default=None,
        type=str,
        help="name/path of the model",
    )
    parser.add_argument(
        "--task",
        default=None,
        type=str,
        help="task",
    )
    parser.add_argument(
        "--max-tokens",
        default=128,
        type=int,
        help="the maximum number of tokens to generate",
    )
    parser.add_argument(
        "--stop-words",
        default=None,
        nargs="+",
        type=str,
        help="stop word",
    )
    parser.add_argument(
        "--temperature",
        default=0.7,
        type=float,
        help="temperature for the LM",
    )
    parser.add_argument(
        "--top-p",
        default=0.7,
        type=float,
        help="top-p for the LM",
    )
    parser.add_argument(
        "--top-k",
        default=50,
        type=int,
        help="top-k for the LM",
    )
    parser.add_argument(
        "--repetition-penalty",
        default=None,
        type=float,
        help="repetition penaltyfor the LM",
    )
    parser.add_argument(
        "--logprobs",
        default=None,
        type=int,
        help="logprobs for the LM",
    )

    return parser
