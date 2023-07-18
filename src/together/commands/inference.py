from __future__ import annotations

import argparse
import base64
import json
import logging
import re
import sys
from typing import Any, Dict, List

from together.inference import Inference
from together.utils.utils import exit_1, get_logger


def add_parser(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
    parents: List[argparse.ArgumentParser],
) -> None:
    COMMAND_NAME = "complete"
    inf_parser = subparsers.add_parser(COMMAND_NAME, parents=parents)

    inf_parser.add_argument(
        "prompt",
        metavar="PROMPT",
        default=None,
        type=str,
        help="A string providing context for the model to complete.",
    )

    inf_parser.add_argument(
        "--model",
        "-m",
        default="togethercomputer/RedPajama-INCITE-7B-Chat",
        type=str,
        help="The name of the model to query. Default='togethercomputer/RedPajama-INCITE-7B-Chat'",
    )

    inf_parser.add_argument(
        "--task",
        default="text2text",
        type=str,
        help="Task type: text2text, text2img. Default=text2text",
        choices=["text2text", "text2img"],
    )

    inf_parser.add_argument(
        "--no-stream",
        default=False,
        action="store_true",
        help="Indicates wether to disable streaming",
    )

    text2textargs = inf_parser.add_argument_group("Text2Text Arguments")

    text2textargs.add_argument(
        "--max-tokens",
        default=128,
        type=int,
        help="Maximum number of tokens to generate. Default=128",
    )
    text2textargs.add_argument(
        "--stop",
        default=["<human>"],
        nargs="+",
        type=str,
        help="Strings that will truncate (stop) inference text output. Default='<human>'",
    )
    text2textargs.add_argument(
        "--temperature",
        default=0.7,
        type=float,
        help="Determines the degree of randomness in the response. Default=0.7",
    )
    text2textargs.add_argument(
        "--top-p",
        default=0.7,
        type=float,
        help="Used to dynamically adjust the number of choices for each predicted token based on the cumulative probabilities. Default=0.7",
    )
    text2textargs.add_argument(
        "--top-k",
        default=50,
        type=int,
        help="Used to limit the number of choices for the next predicted word or token. Default=50",
    )
    text2textargs.add_argument(
        "--repetition-penalty",
        default=None,
        type=float,
        help="Controls the diversity of generated text by reducing the likelihood of repeated sequences. Higher values decrease repetition.",
    )
    text2textargs.add_argument(
        "--logprobs",
        default=None,
        type=int,
        help="Specifies how many top token log probabilities are included in the response for each token generation step.",
    )
    text2textargs.add_argument(
        "--raw",
        default=False,
        action="store_true",
        help="temperature for the LM",
    )

    text2imgargs = inf_parser.add_argument_group("Text2Image Arguments")

    text2imgargs.add_argument(
        "--height",
        default=512,
        type=int,
        help="Pixel height for generated image results",
    )
    text2imgargs.add_argument(
        "--width",
        default=512,
        type=int,
        help="Pixel width for generated image results",
    )
    # arguments for text2img models
    text2imgargs.add_argument(
        "--steps",
        default=50,
        type=int,
        help="Number of steps",
    )
    text2imgargs.add_argument(
        "--seed",
        default=42,
        type=int,
        help="Seed for image generation",
    )
    text2imgargs.add_argument(
        "--results",
        "-r",
        default=1,
        type=int,
        help="Number of image results to return",
    )
    text2imgargs.add_argument(
        "--output-prefix",
        "-o",
        default="image",
        type=str,
        help="Prefix for the file names the output images will be saved to. An image number will be appended to this name. Default=image",
    )

    inf_parser.set_defaults(func=_run_complete)


def _enforce_stop_tokens(text: str, stop: List[str]) -> str:
    """Cut off the text as soon as any stop words occur."""
    return re.split("|".join(stop), text)[0]


def no_streamer(
    args: argparse.Namespace, response: Dict[str, Any], logger: logging.Logger
) -> None:
    if args.raw:
        print(json.dumps(response, indent=4))
        sys.exit()

    if "output" in response.keys():
        if args.task == "text2text":
            try:
                text = str(response["output"]["choices"][0]["text"])
            except Exception:
                try:
                    logger.critical(f"Error raised: {response['output']['error']}")
                    exit_1(logger)
                except Exception as e:
                    logger.critical(f"Error raised: {e}")
                    exit_1(logger)

            # if args.stop is not None:
            #    text = _enforce_stop_tokens(text, args.stop)

        elif args.task == "text2img":
            try:
                images = response["output"]["choices"]

                for i in range(len(images)):
                    with open(f"{args.output}-{i}.png", "wb") as f:
                        f.write(base64.b64decode(images[i]["image_base64"]))
            except Exception as e:  # This is the correct syntax
                logger.critical(f"Error raised: {e}")
                exit_1(logger)

            text = f"Output images saved to {args.output}-X.png"
        else:
            logger.critical(
                f"Invalid task: {args.task}. Pick from either text2text or text2img."
            )
            exit_1(logger)

    elif "error" in response.keys():
        if response["error"] == "Returned error: no instance":
            logger.critical(
                f"No running instances for {args.model}. You can start an instance by navigating to the Together Playground at api.together.xyz"
            )
            exit_1(logger)
        else:
            logger.critical(f"Error raised: {response['error']}")

    else:
        logger.critical("Unknown response received")
        exit_1(logger)

    print(text.strip())


def _run_complete(args: argparse.Namespace) -> None:
    logger = get_logger(__name__, log_level=args.log)

    inference = Inference(
        endpoint_url=args.endpoint,
        task=args.task,
        model=args.model,
        max_tokens=args.max_tokens,
        stop=args.stop,
        temperature=args.temperature,
        top_p=args.top_p,
        top_k=args.top_k,
        repetition_penalty=args.repetition_penalty,
        logprobs=args.logprobs,
        steps=args.steps,
        seed=args.seed,
        results=args.results,
        height=args.height,
        width=args.width,
    )

    if args.no_stream:
        response = inference.inference(prompt=args.prompt)
        no_streamer(args, response, logger)
    else:
        _ = inference.streaming_inference(prompt=args.prompt)
