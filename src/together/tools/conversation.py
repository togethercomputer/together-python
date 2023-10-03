import re
import time


MEANINGLESS_WORDS = ["<pad>", "</s>", "<|endoftext|>"]
PRE_PROMPT = """\
Current Date: {}
Current Time: {}

"""


def clean_response(response: str) -> str:
    for word in MEANINGLESS_WORDS:
        response = response.replace(word, "")
    response = response.strip("\n")
    return response


class Conversation:
    def __init__(self, prompt_id: str, response_id: str) -> None:
        cur_date = time.strftime("%Y-%m-%d")
        cur_time = time.strftime("%H:%M:%S %p %Z")

        self._prompt_id = prompt_id
        self._response_id = response_id
        self._prompt = PRE_PROMPT.format(cur_date, cur_time)

    def push_context_turn(self, context: str) -> None:
        # for now, context is represented as a human turn
        self._prompt += f"{self._prompt_id}: {context}\n"

    def push_human_turn(self, query: str) -> None:
        self._prompt += f"{self._prompt_id}: {query}\n"
        self._prompt += f"{self._response_id}:"

    def push_model_response(self, response: str) -> None:
        # has_finished = self._prompt_id in response
        bot_turn = response.split(f"{self._prompt_id}:")[0]
        bot_turn = clean_response(bot_turn)
        # if it is truncated, then append "..." to the end of the response
        # if not has_finished:
        #    bot_turn += "..."

        self._prompt += f"{bot_turn}\n"

    def get_last_turn(self) -> str:
        human_tag = f"{self._prompt_id}:"
        bot_tag = f"{self._response_id}:"
        turns = re.split(f"({human_tag}|{bot_tag})\W?", self._prompt)
        return turns[-1]

    def get_raw_prompt(self) -> str:
        return self._prompt

    @classmethod
    def from_raw_prompt(cls, prompt_id: str, response_id: str, prompt: str):  # type: ignore
        convo = Conversation(prompt_id, response_id)
        convo._prompt = prompt
        return convo
