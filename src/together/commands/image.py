from __future__ import annotations

import argparse
import base64
import json
import logging
import sys
from typing import Any, Dict

import together
from together import Image, get_logger


def add_parser(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    COMMAND_NAME = "image"
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
        default=together.default_image_model,
        type=str,
        help=f"The name of the model to query. Default={together.default_image_model}",
    )

    subparser.add_argument(
        "--height",
        default=256,
        type=int,
        help="Pixel height for generated image results",
    )
    subparser.add_argument(
        "--width",
        default=256,
        type=int,
        help="Pixel width for generated image results",
    )
    subparser.add_argument(
        "--steps",
        default=20,
        type=int,
        help="Number of steps",
    )
    subparser.add_argument(
        "--seed",
        default=42,
        type=int,
        help="Seed for image generation",
    )
    subparser.add_argument(
        "--results",
        "-r",
        default=1,
        type=int,
        help="Number of image results to return",
    )
    subparser.add_argument(
        "--output-prefix",
        "-o",
        default="image",
        type=str,
        metavar="PREFIX",
        help="Prefix for the file names the output images will be saved to. An image number will be appended to this name. Default=image",
    )
    subparser.add_argument(
        "--raw",
        default=False,
        action="store_true",
        help="Indicates whether to output raw image to CLI. Enabling this option does not save the image to disk.",
    )

    subparser.set_defaults(func=_run_complete)


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
                print(f"Image saved to {args.output_prefix}-{i}.png")
        except Exception as e:  # This is the correct syntax
            logger.critical(f"Error raised: {e}")
            raise together.ResponseError(e)

    elif "error" in response.keys():
        if response["error"] == "Returned error: no instance":
            logger.critical(
                f"No running instances for {args.model}. You can start an instance by navigating to the Together Playground at api.together.xyz"
            )
            raise together.InstanceError(model=args.model)
        else:
            logger.critical(f"Error raised: {response['error']}")

    else:
        logger.critical("Unknown response received.")
        raise together.ResponseError("Unknown response received.")


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
