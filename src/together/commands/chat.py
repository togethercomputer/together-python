from __future__ import annotations

import argparse
import cmd

import together
import together.utils.conversation as convo
from together import Complete, get_logger


def add_parser(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
) -> None:
    COMMAND_NAME = "chat"
    subparser = subparsers.add_parser(COMMAND_NAME)

    subparser.add_argument(
        "--model",
        "-m",
        default=together.default_text_model,
        type=str,
        help=f"The name of the model to query. Default={together.default_text_model}",
    )
    subparser.add_argument(
        "--prompt_id",
        "-pid",
        default="<human>",
        type=str,
        help="Indicates start of prompt. Defaults to '<human>'. Examples '### User' or '[INST]'",
    )
    subparser.add_argument(
        "--response_id",
        "-rid",
        default="<bot>",
        type=str,
        help="Indicates start of response. Defaults to '<bot>'. Examples '### Assistant' or '[/INST]'",
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

    subparser.set_defaults(func=_run_complete)


class OpenChatKitShell(cmd.Cmd):
    intro = "Type /quit to quit, /help, or /? to list commands.\n"
    prompt = ">>> "

    def __init__(self, infer: Complete, args: argparse.Namespace) -> None:
        super().__init__()
        self.infer = infer
        self.args = args
        self.prompt_id = args.prompt_id
        self.response_id = args.response_id
        print(f"Loading {self.args.model}")

    def preloop(self) -> None:
        self._convo = convo.Conversation(self.prompt_id, self.response_id)

    def precmd(self, line: str) -> str:
        if line.startswith("/"):
            return line[1:]
        else:
            return "say " + line

    def do_say(self, arg: str) -> None:
        self._convo.push_human_turn(arg)
        output = ""
        for token in self.infer.create_streaming(
            prompt=self._convo.get_raw_prompt(),
            model=self.args.model,
            max_tokens=self.args.max_tokens,
            stop=self.args.stop,
            temperature=self.args.temperature,
            top_p=self.args.top_p,
            top_k=self.args.top_k,
            repetition_penalty=self.args.repetition_penalty,
        ):
            print(token, end="", flush=True)
            output += token
        print("\n")
        self._convo.push_model_response(output)

    def do_raw_prompt(self, arg: str) -> None:
        print(self._convo.get_raw_prompt())

    def do_reset(self, arg: str) -> None:
        self._convo = convo.Conversation(self.prompt_id, self.response_id)

    def do_quit(self, arg: str) -> bool:
        return True


def _run_complete(args: argparse.Namespace) -> None:
    get_logger(__name__, log_level=args.log)
    if args.prompt_id not in args.stop:
        args.stop.append(args.prompt_id)

    infer = Complete()

    OpenChatKitShell(infer, args).cmdloop()
