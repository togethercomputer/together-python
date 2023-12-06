from __future__ import annotations

import argparse
import json
import re
from typing import Any, Dict, List

import together
from together import Complete
from together.utils import get_logger


logger = get_logger(str(__name__))


def add_parser(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    COMMAND_NAME = "complete"
    subparser = subparsers.add_parser(COMMAND_NAME)

    subparser.add_argument(
        "prompt",
        metavar="PROMPT",
        default=None,
        type=str,
        help="A string providing context for the model to complete.",
    )

    subparser.add_argument(
        "--model",
        "-m",
        default=together.default_text_model,
        type=str,
        help=f"The name of the model to query. Default={together.default_text_model}",
    )

    subparser.add_argument(
        "--no-stream",
        default=False,
        action="store_true",
        help="Indicates wether to disable streaming",
    )

    subparser.add_argument(
        "--max-tokens",
        default=128,
        type=int,
        help="Maximum number of tokens to generate. Default=128",
    )
    subparser.add_argument(
        "--stop",
        default=["<human>"],
        nargs="+",
        type=str,
        metavar="STOP_WORD",
        help="Strings that will truncate (stop) text generation. Default='<human>'",
    )
    subparser.add_argument(
        "--temperature",
        default=0.7,
        type=float,
        help="Determines the degree of randomness in the response. Default=0.7",
    )
    subparser.add_argument(
        "--top-p",
        default=0.7,
        type=float,
        help="Used to dynamically adjust the number of choices for each predicted token based on the cumulative probabilities. Default=0.7",
    )
    subparser.add_argument(
        "--top-k",
        default=50,
        type=int,
        help="Used to limit the number of choices for the next predicted word or token. Default=50",
    )
    subparser.add_argument(
        "--repetition-penalty",
        default=None,
        type=float,
        help="Controls the diversity of generated text by reducing the likelihood of repeated sequences. Higher values decrease repetition.",
    )
    subparser.add_argument(
        "--logprobs",
        default=None,
        type=int,
        help="Specifies how many top token log probabilities are included in the response for each token generation step.",
    )
    subparser.add_argument(
        "--raw",
        default=False,
        action="store_true",
        help="temperature for the LM",
    )
    subparser.add_argument(
        "--safety-model",
        "-sm",
        default=None,
        type=str,
        help="The name of the safety model to use for moderation.",
    )
    subparser.set_defaults(func=_run_complete)


def _enforce_stop_tokens(text: str, stop: List[str]) -> str:
    """Cut off the text as soon as any stop words occur."""
    return re.split("|".join(stop), text)[0]


def no_streamer(args: argparse.Namespace, response: Dict[str, Any]) -> None:
    if args.raw:
        print(json.dumps(response, indent=4))

    else:
        if "output" in response.keys():
            if "choices" in dict(response["output"]).keys():
                text = str(response["output"]["choices"][0]["text"])
                print(text.strip())
            elif "error" in dict(response["output"]).keys():
                raise together.ResponseError(response["output"]["error"])
            else:
                raise together.ResponseError(
                    f"Unknown error occured. Received unhandled response: {response}"
                )

        elif "error" in response.keys():
            if response["error"] == "Returned error: no instance":
                message = f"No running instances for {args.model}. You can start an instance by navigating to the Together Playground at api.together.xyz"
                raise together.InstanceError(model=args.model, message=message)
            else:
                raise together.ResponseError(
                    message=f"Error raised: {response['error']}"
                )

        else:
            raise together.ResponseError("Unknown response received. Please try again.")


def _run_complete(args: argparse.Namespace) -> None:
    complete = Complete()

    if args.no_stream:
        try:
            response = complete.create(
                prompt=args.prompt,
                model=args.model,
                max_tokens=args.max_tokens,
                stop=args.stop,
                temperature=args.temperature,
                top_p=args.top_p,
                top_k=args.top_k,
                repetition_penalty=args.repetition_penalty,
                logprobs=args.logprobs,
                safety_model=args.safety_model,
            )
        except together.AuthenticationError:
            logger.critical(together.MISSING_API_KEY_MESSAGE)
            exit(0)
        assert isinstance(response, dict)
        no_streamer(args, response)
    else:
        try:
            for text in complete.create_streaming(
                prompt=args.prompt,
                model=args.model,
                max_tokens=args.max_tokens,
                stop=args.stop,
                temperature=args.temperature,
                top_p=args.top_p,
                top_k=args.top_k,
                repetition_penalty=args.repetition_penalty,
                safety_model=args.safety_model,
                raw=args.raw,
            ):
                if not args.raw:
                    print(text, end="", flush=True)
                else:
                    print(text)
        except together.AuthenticationError:
            logger.critical(together.MISSING_API_KEY_MESSAGE)
            exit(0)
        if not args.raw:
            print("\n")
