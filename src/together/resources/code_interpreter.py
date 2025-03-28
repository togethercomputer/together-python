from __future__ import annotations

from typing import Dict, Literal, Optional

from together.abstract import api_requestor
from together.together_response import TogetherResponse
from together.types import TogetherClient, TogetherRequest
from together.types.code_interpreter import ExecuteResponse


class CodeInterpreter:
    """Code Interpreter resource for executing code snippets."""

    def __init__(self, client: TogetherClient) -> None:
        self._client = client

    def run(
        self,
        code: str,
        language: Literal["python"],
        session_id: Optional[str] = None,
    ) -> ExecuteResponse:
        """Execute a code snippet.

        Args:
            code (str): Code snippet to execute
            language (str): Programming language for the code to execute. Currently only supports Python.
            session_id (str, optional): Identifier of the current session. Used to make follow-up calls.

        Returns:
            ExecuteResponse: Object containing execution results and outputs
        """
        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        data: Dict[str, str] = {
            "code": code,
            "language": language,
        }

        if session_id is not None:
            data["session_id"] = session_id

        # Use absolute URL to bypass the /v1 prefix
        response, _, _ = requestor.request(
            options=TogetherRequest(
                method="POST",
                url="/tci/execute",
                params=data,
            ),
            stream=False,
        )

        assert isinstance(response, TogetherResponse)

        # Return the response data directly since our types match the API structure
        return ExecuteResponse(**response.data)
