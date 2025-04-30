from __future__ import annotations

from typing import Any, Dict, List, Literal, Optional
from pydantic import ValidationError

from together.abstract import api_requestor
from together.together_response import TogetherResponse
from together.types import TogetherClient, TogetherRequest
from together.types.code_interpreter import ExecuteResponse, FileInput


class CodeInterpreter:
    """Code Interpreter resource for executing code snippets."""

    def __init__(self, client: TogetherClient) -> None:
        self._client = client

    def run(
        self,
        code: str,
        language: Literal["python"],
        session_id: Optional[str] = None,
        files: Optional[List[Dict[str, Any]]] = None,
    ) -> ExecuteResponse:
        """Execute a code snippet, optionally with files.

        Args:
            code (str): Code snippet to execute
            language (str): Programming language for the code to execute. Currently only supports Python.
            session_id (str, optional): Identifier of the current session. Used to make follow-up calls.
            files (List[Dict], optional): Files to upload to the session before executing the code.

        Returns:
            ExecuteResponse: Object containing execution results and outputs

        Raises:
            ValidationError: If any dictionary in the `files` list does not conform to the
                required structure or types.
        """
        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        data: Dict[str, Any] = {
            "code": code,
            "language": language,
        }

        if session_id is not None:
            data["session_id"] = session_id

        if files is not None:
            serialized_files = []
            try:
                for file_dict in files:
                    # Validate the dictionary by creating a FileInput instance
                    validated_file = FileInput(**file_dict)
                    # Serialize the validated model back to a dict for the API call
                    serialized_files.append(validated_file.model_dump())
            except ValidationError as e:
                raise ValueError(f"Invalid file input format: {e}") from e
            except TypeError as e:
                raise ValueError(
                    f"Invalid file input: Each item in 'files' must be a dictionary. Error: {e}"
                ) from e

            data["files"] = serialized_files

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
