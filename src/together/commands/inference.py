from __future__ import annotations

import argparse
import base64
import json
import re
from typing import List

from together.inference import Inference


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
        help="Prompt to complete",
    )

    inf_parser.add_argument(
        "--model",
        "-m",
        default="togethercomputer/RedPajama-INCITE-7B-Chat",
        type=str,
        help="name/path of the model",
    )

    inf_parser.add_argument(
        "--task",
        default="text2text",
        type=str,
        help="Task type: text2text, text2img",
        choices=["text2text", "text2img"],
    )

    text2textargs = inf_parser.add_argument_group("Text2Text Arguments")

    text2textargs.add_argument(
        "--max-tokens",
        default=128,
        type=int,
        help="the maximum number of tokens to generate",
    )
    text2textargs.add_argument(
        "--stop-words",
        default=None,
        nargs="+",
        type=str,
        help="stop word",
    )
    text2textargs.add_argument(
        "--temperature",
        default=0.7,
        type=float,
        help="temperature for the LM",
    )
    text2textargs.add_argument(
        "--top-p",
        default=0.7,
        type=float,
        help="top-p for the LM",
    )
    text2textargs.add_argument(
        "--top-k",
        default=50,
        type=int,
        help="top-k for the LM",
    )
    text2textargs.add_argument(
        "--repetition-penalty",
        default=None,
        type=float,
        help="repetition penaltyfor the LM",
    )
    text2textargs.add_argument(
        "--logprobs",
        default=None,
        type=int,
        help="logprobs for the LM",
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
        help="Height for images in text2img results",
    )
    text2imgargs.add_argument(
        "--width",
        default=512,
        type=int,
        help="Width for images in text2img results",
    )
    # arguments for text2img models
    text2imgargs.add_argument(
        "--steps",
        default=50,
        type=int,
        help="Number of steps for text2img models",
    )
    text2imgargs.add_argument(
        "--seed",
        default=42,
        type=int,
        help="Seed for text2img models",
    )
    text2imgargs.add_argument(
        "--results",
        "-r",
        default=1,
        type=int,
        help="Number of text2img results",
    )
    text2imgargs.add_argument(
        "--output",
        "-o",
        default="image",
        type=str,
        help="File name for text2img output images '-X.png' will be appended to this name, where X is a number.",
    )

    inf_parser.set_defaults(func=_run_complete)


def _enforce_stop_tokens(text: str, stop: List[str]) -> str:
    """Cut off the text as soon as any stop words occur."""
    return re.split("|".join(stop), text)[0]


def _run_complete(args: argparse.Namespace) -> None:
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
        steps=args.steps,
        seed=args.seed,
        results=args.results,
        height=args.height,
        width=args.width,
    )

    response = inference.inference(prompt=args.prompt, stop=args.stop_words)

    if args.raw:
        print(json.dumps(response, indent=4))
    else:
        if args.task == "text2text":
            # TODO Add exception when generated_text has error, See together docs
            try:
                text = str(response["output"]["choices"][0]["text"])
            except Exception as e:
                raise ValueError(f"Error raised: {e}")

            if args.stop_words is not None:
                # TODO remove this and permanently implement api stop_word
                text = _enforce_stop_tokens(text, args.stop_words)

        elif args.task == "text2img":
            try:
                images = response["output"]["choices"]

                for i in range(len(images)):
                    with open(f"{args.output}-{i}.png", "wb") as f:
                        f.write(base64.b64decode(images[i]["image_base64"]))
            except Exception as e:  # This is the correct syntax
                raise ValueError(f"Unknown error raised: {e}")

            text = f"Output images saved to {args.output}-X.png"
        else:
            raise ValueError("Invalid task supplied")

        print(text)
