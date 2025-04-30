from __future__ import annotations

from typing import Any, Dict, Literal, Union

from pydantic import Field

from together.types.endpoints import TogetherJSONModel


class FileInput(TogetherJSONModel):
    """File input to be uploaded to the code interpreter session."""

    name: str = Field(description="The name of the file.")
    encoding: Literal["string", "base64"] = Field(
        description="Encoding of the file content. Use 'string' for text files and 'base64' for binary files."
    )
    content: str = Field(description="The content of the file, encoded as specified.")


class InterpreterOutput(TogetherJSONModel):
    """Base class for interpreter output types."""

    type: Literal["stdout", "stderr", "error", "display_data", "execute_result"] = (
        Field(description="The type of output")
    )
    data: Union[str, Dict[str, Any]] = Field(description="The output data")


class ExecuteResponseData(TogetherJSONModel):
    """Data from code execution response."""

    outputs: list[InterpreterOutput] = Field(
        description="List of outputs from execution", default_factory=list
    )
    errors: Union[str, None] = Field(
        description="Any errors that occurred during execution", default=None
    )
    session_id: str = Field(
        description="Identifier of the current session. Used to make follow-up calls."
    )
    status: str = Field(description="Status of the execution", default="completed")


class ExecuteResponse(TogetherJSONModel):
    """Response from code execution."""

    data: ExecuteResponseData = Field(
        description="The response data containing outputs and session information"
    )


__all__ = [
    "FileInput",
    "InterpreterOutput",
    "ExecuteResponseData",
    "ExecuteResponse",
]
