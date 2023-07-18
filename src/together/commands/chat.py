from __future__ import annotations

import argparse
import cmd
from typing import List

import together.utils.conversation as convo
from together.inference import Inference
from together.utils.utils import get_logger


def add_parser(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
    parents: List[argparse.ArgumentParser],
) -> None:
    COMMAND_NAME = "chat"
    inf_parser = subparsers.add_parser(COMMAND_NAME, parents=parents)

    inf_parser.add_argument(
        "--model",
        "-m",
        default="togethercomputer/RedPajama-INCITE-7B-Chat",
        type=str,
        help="The name of the model to query. Default='togethercomputer/RedPajama-INCITE-7B-Chat'",
    )
    inf_parser.add_argument(
        "--user_id",
        "-u",
        default="<human>",
        type=str,
        help="The tag the user's prompt should have. Defaults to '<human>'. Examples '### User' or 'prompt:'",
    )
    inf_parser.add_argument(
        "--bot_id",
        "-b",
        default="<bot>",
        type=str,
        help="The tag the bot's response should have. Defaults to '<bot>'. Examples '### Assistant' or 'response:'",
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

    inf_parser.set_defaults(func=_run_complete)


class OpenChatKitShell(cmd.Cmd):
    intro = "Type /quit to exit, /help, or /? to list commands.\n"
    prompt = ">>> "

    def __init__(self, inference: Inference, args: argparse.Namespace) -> None:
        super().__init__()
        self.inference = inference
        self.args = args
        self.human_id = args.user_id
        self.bot_id = args.bot_id
        print(f"Loading {self.args.model}")

    def preloop(self) -> None:
        self._convo = convo.Conversation(self.human_id, self.bot_id)

    def precmd(self, line: str) -> str:
        if line.startswith("/"):
            return line[1:]
        else:
            return "say " + line

    def do_say(self, arg: str) -> None:
        self._convo.push_human_turn(arg)
        output = self.inference.streaming_inference(prompt=self._convo.get_raw_prompt())
        self._convo.push_model_response(output)

    def do_raw_prompt(self, arg: str) -> None:
        print(self._convo.get_raw_prompt())

    def do_reset(self, arg: str) -> None:
        self._convo = convo.Conversation(self.human_id, self.bot_id)

    def do_quit(self, arg: str) -> bool:
        return True


def _run_complete(args: argparse.Namespace) -> None:
    get_logger(__name__, log_level=args.log)
    if args.user_id not in args.stop:
        args.stop.append(args.user_id)

    inference = Inference(
        endpoint_url=args.endpoint,
        task="text2text",
        model=args.model,
        max_tokens=args.max_tokens,
        stop=args.stop,
        temperature=args.temperature,
        top_p=args.top_p,
        top_k=args.top_k,
        repetition_penalty=args.repetition_penalty,
        logprobs=args.logprobs,
    )

    OpenChatKitShell(inference, args).cmdloop()
