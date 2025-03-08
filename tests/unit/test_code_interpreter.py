from __future__ import annotations

import pytest

from together.resources.code_interpreter import CodeInterpreter
from together.together_response import TogetherResponse
from together.types.code_interpreter import ExecuteResponse, ExecuteResponseData, InterpreterOutput


def test_interpreter_output_validation():
    # Test valid stdout output
    stdout = InterpreterOutput(type="stdout", data="Hello, world!")
    assert stdout.type == "stdout"
    assert stdout.data == "Hello, world!"

    # Test valid display_data output
    display_data = InterpreterOutput(
        type="display_data",
        data={
            "text/plain": "Hello",
            "text/html": "<p>Hello</p>",
        },
    )
    assert display_data.type == "display_data"
    assert display_data.data["text/plain"] == "Hello"

    # Test invalid type
    with pytest.raises(ValueError):
        InterpreterOutput(type="invalid", data="test")


def test_execute_response_validation():
    # Test valid response
    outputs = [
        InterpreterOutput(type="stdout", data="Hello"),
        InterpreterOutput(type="stderr", data="Warning"),
    ]
    response = ExecuteResponse(
        data=ExecuteResponseData(
            session_id="test_session",
            status="success",
            outputs=outputs,
        )
    )
    assert response.data.session_id == "test_session"
    assert response.data.status == "success"
    assert len(response.data.outputs) == 2
    assert response.data.outputs[0].type == "stdout"
    assert response.data.outputs[1].type == "stderr"


def test_code_interpreter_run(mocker):
    # Mock the API requestor
    mock_requestor = mocker.MagicMock()
    response_data = {
        "data": {
            "session_id": "test_session",
            "status": "success",
            "outputs": [{"type": "stdout", "data": "Hello, world!"}],
        }
    }
    mock_headers = {
        "cf-ray": "test-ray-id",
        "x-ratelimit-remaining": "100",
        "x-hostname": "test-host",
        "x-total-time": "42.0",
    }
    mock_response = TogetherResponse(data=response_data, headers=mock_headers)
    mock_requestor.request.return_value = (mock_response, None, None)
    mocker.patch("together.abstract.api_requestor.APIRequestor", return_value=mock_requestor)

    # Create code interpreter instance
    client = mocker.MagicMock()
    interpreter = CodeInterpreter(client)

    # Test run method
    response = interpreter.run(
        code='print("Hello, world!")',
        language="python",
        session_id="test_session",
    )

    # Verify the response
    assert isinstance(response, ExecuteResponse)
    assert response.data.session_id == "test_session"
    assert response.data.status == "success"
    assert len(response.data.outputs) == 1
    assert response.data.outputs[0].type == "stdout"
    assert response.data.outputs[0].data == "Hello, world!"

    # Verify API request
    mock_requestor.request.assert_called_once_with(
        options=mocker.ANY,
        stream=False,
    )
    request_options = mock_requestor.request.call_args[1]["options"]
    assert request_options.method == "POST"
    assert request_options.url == "/tci/execute"
    assert request_options.params == {
        "code": 'print("Hello, world!")',
        "language": "python",
        "session_id": "test_session",
    }


def test_code_interpreter_run_without_session(mocker):
    # Mock the API requestor
    mock_requestor = mocker.MagicMock()
    response_data = {
        "data": {
            "session_id": "new_session",
            "status": "success",
            "outputs": [],
        }
    }
    mock_headers = {
        "cf-ray": "test-ray-id-2",
        "x-ratelimit-remaining": "99",
        "x-hostname": "test-host",
        "x-total-time": "42.0",
    }
    mock_response = TogetherResponse(data=response_data, headers=mock_headers)
    mock_requestor.request.return_value = (mock_response, None, None)
    mocker.patch("together.abstract.api_requestor.APIRequestor", return_value=mock_requestor)

    # Create code interpreter instance
    client = mocker.MagicMock()
    interpreter = CodeInterpreter(client)

    # Test run method without session_id
    response = interpreter.run(
        code="x = 1",
        language="python",
    )

    # Verify the response
    assert isinstance(response, ExecuteResponse)
    assert response.data.session_id == "new_session"

    # Verify API request doesn't include session_id
    request_options = mock_requestor.request.call_args[1]["options"]
    assert request_options.params == {
        "code": "x = 1",
        "language": "python",
    }
