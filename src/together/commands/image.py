from __future__ import annotations

import argparse
import base64
import json
import logging
import sys
from typing import Any, Dict, List

import together
from together.image import Image
from together.utils.utils import exit_1, get_logger


def add_parser(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
    parents: List[argparse.ArgumentParser],
) -> None:
    COMMAND_NAME = "image"
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
        default=together.default_image_model,
        type=str,
        help=f"The name of the model to query. Default={together.default_image_model}",
    )

    inf_parser.add_argument(
        "--height",
        default=512,
        type=int,
        help="Pixel height for generated image results",
    )
    inf_parser.add_argument(
        "--width",
        default=512,
        type=int,
        help="Pixel width for generated image results",
    )
    inf_parser.add_argument(
        "--steps",
        default=50,
        type=int,
        help="Number of steps",
    )
    inf_parser.add_argument(
        "--seed",
        default=42,
        type=int,
        help="Seed for image generation",
    )
    inf_parser.add_argument(
        "--results",
        "-r",
        default=1,
        type=int,
        help="Number of image results to return",
    )
    inf_parser.add_argument(
        "--output-prefix",
        "-o",
        default="image",
        type=str,
        help="Prefix for the file names the output images will be saved to. An image number will be appended to this name. Default=image",
    )
    inf_parser.add_argument(
        "--raw",
        default=False,
        action="store_true",
        help="Indicates whether to output raw image to CLI. Enabling this option does not save the image to disk.",
    )

    inf_parser.set_defaults(func=_run_complete)


def _save_image(
    args: argparse.Namespace, response: Dict[str, Any], logger: logging.Logger
) -> None:
    if args.raw:
        print(json.dumps(response, indent=4))
        sys.exit()

    if "output" in response.keys():
        try:
            images = response["output"]["choices"]

            for i in range(len(images)):
                with open(f"{args.output_prefix}-{i}.png", "wb") as f:
                    f.write(base64.b64decode(images[i]["image_base64"]))
        except Exception as e:  # This is the correct syntax
            logger.critical(f"Error raised: {e}")
            exit_1(logger)

        out_string = f"Output images saved to {args.output_prefix}-X.png"

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

    print(out_string.strip())


def _run_complete(args: argparse.Namespace) -> None:
    logger = get_logger(__name__, log_level=args.log)

    complete = Image()

    response = complete.create(
        prompt=args.prompt,
        model=args.model,
        steps=args.steps,
        seed=args.seed,
        results=args.results,
        height=args.height,
        width=args.width,
    )

    _save_image(args, response, logger)
