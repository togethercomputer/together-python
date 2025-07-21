from __future__ import annotations

import pytest
from pydantic import ValidationError

from together.resources.code_interpreter import CodeInterpreter
from together.together_response import TogetherResponse
from together.types.code_interpreter import (
    ExecuteResponse,
    ExecuteResponseData,
    InterpreterOutput,
)


def test_interpreter_output_validation():
    # Test stdout output
    stdout = InterpreterOutput(type="stdout", data="Hello, world!")
    assert stdout.type == "stdout"
    assert stdout.data == "Hello, world!"

    # Test stderr output
    stderr = InterpreterOutput(type="stderr", data="Warning message")
    assert stderr.type == "stderr"
    assert stderr.data == "Warning message"

    # Test error output
    error = InterpreterOutput(type="error", data="Error occurred")
    assert error.type == "error"
    assert error.data == "Error occurred"

    # Test display_data output with dict data
    display_data = InterpreterOutput(
        type="display_data",
        data={
            "text/plain": "Hello",
            "text/html": "<p>Hello</p>",
        },
    )
    assert display_data.type == "display_data"
    assert isinstance(display_data.data, dict)
    assert display_data.data.get("text/plain") == "Hello"
    assert display_data.data.get("text/html") == "<p>Hello</p>"

    # Test execute_result output
    execute_result = InterpreterOutput(type="execute_result", data="42")
    assert execute_result.type == "execute_result"
    assert execute_result.data == "42"


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
    mocker.patch(
        "together.abstract.api_requestor.APIRequestor", return_value=mock_requestor
    )

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
    mocker.patch(
        "together.abstract.api_requestor.APIRequestor", return_value=mock_requestor
    )

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


def test_code_interpreter_error_handling(mocker):
    # Mock the API requestor to simulate an error
    mock_requestor = mocker.MagicMock()
    response_data = {
        "data": {
            "session_id": "test_session",
            "status": "error",
            "outputs": [{"type": "error", "data": "Division by zero"}],
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
    mocker.patch(
        "together.abstract.api_requestor.APIRequestor", return_value=mock_requestor
    )

    # Create code interpreter instance
    client = mocker.MagicMock()
    interpreter = CodeInterpreter(client)

    # Test run method with code that would cause an error
    response = interpreter.run(
        code="1/0",  # This will cause a division by zero error
        language="python",
        session_id="test_session",
    )

    # Verify the error response
    assert isinstance(response, ExecuteResponse)
    assert response.data.status == "error"
    assert len(response.data.outputs) == 1
    assert response.data.outputs[0].type == "error"
    assert "Division by zero" in response.data.outputs[0].data


def test_code_interpreter_multiple_outputs(mocker):
    # Mock the API requestor
    mock_requestor = mocker.MagicMock()
    response_data = {
        "data": {
            "session_id": "test_session",
            "status": "success",
            "outputs": [
                {"type": "stdout", "data": "First line"},
                {"type": "stderr", "data": "Warning message"},
                {"type": "execute_result", "data": "42"},
            ],
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
    mocker.patch(
        "together.abstract.api_requestor.APIRequestor", return_value=mock_requestor
    )

    # Create code interpreter instance
    client = mocker.MagicMock()
    interpreter = CodeInterpreter(client)

    # Test run method with code that produces multiple outputs
    response = interpreter.run(
        code='print("First line")\nimport sys\nsys.stderr.write("Warning message")\n42',
        language="python",
        session_id="test_session",
    )

    # Verify the response with multiple outputs
    assert isinstance(response, ExecuteResponse)
    assert response.data.status == "success"
    assert len(response.data.outputs) == 3
    assert response.data.outputs[0].type == "stdout"
    assert response.data.outputs[1].type == "stderr"
    assert response.data.outputs[2].type == "execute_result"


def test_code_interpreter_session_management(mocker):
    # Mock the API requestor
    mock_requestor = mocker.MagicMock()

    # First response - create new session
    response_data1 = {
        "data": {
            "session_id": "new_session",
            "status": "success",
            "outputs": [{"type": "stdout", "data": "First execution"}],
        }
    }

    # Second response - use existing session
    response_data2 = {
        "data": {
            "session_id": "new_session",
            "status": "success",
            "outputs": [{"type": "stdout", "data": "Second execution"}],
        }
    }

    mock_headers = {
        "cf-ray": "test-ray-id",
        "x-ratelimit-remaining": "100",
        "x-hostname": "test-host",
        "x-total-time": "42.0",
    }

    mock_response1 = TogetherResponse(data=response_data1, headers=mock_headers)
    mock_response2 = TogetherResponse(data=response_data2, headers=mock_headers)
    mock_requestor.request.side_effect = [
        (mock_response1, None, None),
        (mock_response2, None, None),
    ]

    mocker.patch(
        "together.abstract.api_requestor.APIRequestor", return_value=mock_requestor
    )

    # Create code interpreter instance
    client = mocker.MagicMock()
    interpreter = CodeInterpreter(client)

    # First execution - no session ID
    response1 = interpreter.run(
        code='print("First execution")',
        language="python",
    )

    # Second execution - using session ID from first execution
    response2 = interpreter.run(
        code='print("Second execution")',
        language="python",
        session_id=response1.data.session_id,
    )

    # Verify both responses
    assert response1.data.session_id == "new_session"
    assert response2.data.session_id == "new_session"
    assert len(response1.data.outputs) == 1
    assert len(response2.data.outputs) == 1
    assert response1.data.outputs[0].data == "First execution"
    assert response2.data.outputs[0].data == "Second execution"

    # Verify API calls
    assert mock_requestor.request.call_count == 2
    calls = mock_requestor.request.call_args_list

    # First call should not have session_id
    assert "session_id" not in calls[0][1]["options"].params

    # Second call should have session_id
    assert calls[1][1]["options"].params["session_id"] == "new_session"


def test_code_interpreter_run_with_files(mocker):
    mock_requestor = mocker.MagicMock()
    response_data = {
        "data": {
            "session_id": "test_session_files",
            "status": "success",
            "outputs": [{"type": "stdout", "data": "File content read"}],
        }
    }
    mock_headers = {
        "cf-ray": "test-ray-id-files",
        "x-ratelimit-remaining": "98",
        "x-hostname": "test-host",
        "x-total-time": "42.0",
    }
    mock_response = TogetherResponse(data=response_data, headers=mock_headers)
    mock_requestor.request.return_value = (mock_response, None, None)
    mocker.patch(
        "together.abstract.api_requestor.APIRequestor", return_value=mock_requestor
    )

    # Create code interpreter instance
    client = mocker.MagicMock()
    interpreter = CodeInterpreter(client)

    # Define files
    files_to_upload = [
        {"name": "test.txt", "encoding": "string", "content": "Hello from file!"},
        {"name": "image.png", "encoding": "base64", "content": "aW1hZ2UgZGF0YQ=="},
    ]

    # Test run method with files (passing list of dicts)
    response = interpreter.run(
        code='with open("test.txt") as f: print(f.read())',
        language="python",
        files=files_to_upload,  # Pass the list of dictionaries directly
    )

    # Verify the response
    assert isinstance(response, ExecuteResponse)
    assert response.data.session_id == "test_session_files"
    assert response.data.status == "success"
    assert len(response.data.outputs) == 1
    assert response.data.outputs[0].type == "stdout"

    # Verify API request includes files (expected_files_payload remains the same)
    mock_requestor.request.assert_called_once_with(
        options=mocker.ANY,
        stream=False,
    )
    request_options = mock_requestor.request.call_args[1]["options"]
    assert request_options.method == "POST"
    assert request_options.url == "/tci/execute"
    expected_files_payload = [
        {"name": "test.txt", "encoding": "string", "content": "Hello from file!"},
        {"name": "image.png", "encoding": "base64", "content": "aW1hZ2UgZGF0YQ=="},
    ]
    assert request_options.params == {
        "code": 'with open("test.txt") as f: print(f.read())',
        "language": "python",
        "files": expected_files_payload,
    }


def test_code_interpreter_run_with_invalid_file_dict_structure(mocker):
    """Test that run raises ValueError for missing keys in file dict."""
    client = mocker.MagicMock()
    interpreter = CodeInterpreter(client)

    invalid_files = [
        {"name": "test.txt", "content": "Missing encoding"}  # Missing 'encoding'
    ]

    with pytest.raises(ValueError, match="Invalid file input format"):
        interpreter.run(
            code="print('test')",
            language="python",
            files=invalid_files,
        )


def test_code_interpreter_run_with_invalid_file_dict_encoding(mocker):
    """Test that run raises ValueError for invalid encoding value."""
    client = mocker.MagicMock()
    interpreter = CodeInterpreter(client)

    invalid_files = [
        {
            "name": "test.txt",
            "encoding": "utf-8",
            "content": "Invalid encoding",
        }  # Invalid 'encoding' value
    ]

    with pytest.raises(ValueError, match="Invalid file input format"):
        interpreter.run(
            code="print('test')",
            language="python",
            files=invalid_files,
        )


def test_code_interpreter_run_with_invalid_file_list_item(mocker):
    """Test that run raises ValueError for non-dict item in files list."""
    client = mocker.MagicMock()
    interpreter = CodeInterpreter(client)

    invalid_files = [
        {"name": "good.txt", "encoding": "string", "content": "Good"},
        "not a dictionary",  # Invalid item type
    ]

    with pytest.raises(
        ValueError,
        match="Invalid file input: Each item in 'files' must be a dictionary",
    ):
        interpreter.run(
            code="print('test')",
            language="python",
            files=invalid_files,
        )
