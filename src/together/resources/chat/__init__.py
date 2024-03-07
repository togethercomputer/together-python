from together.resources.chat.completions import ChatCompletions
from together.types import (
    TogetherClient,
)

from functools import cached_property

class Chat:
    def __init__(self, client: TogetherClient) -> None:
        self._client = client

    @cached_property
    def completions(self) -> ChatCompletions:
        return ChatCompletions(self._client)
    