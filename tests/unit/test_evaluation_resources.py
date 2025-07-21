from __future__ import annotations

from unittest.mock import patch

import pytest

from together import Together, AsyncTogether
from together.together_response import TogetherResponse
from together.types.evaluation import (
    EvaluationCreateResponse,
    EvaluationJob,
    EvaluationStatus,
    EvaluationStatusResponse,
)


class TestEvaluation:
    @pytest.fixture
    def sync_together_instance(self) -> Together:
        with patch.dict("os.environ", {"TOGETHER_API_KEY": "fake_api_key"}, clear=True):
            return Together()

    @pytest.fixture
    def async_together_instance(self) -> AsyncTogether:
        with patch.dict("os.environ", {"TOGETHER_API_KEY": "fake_api_key"}, clear=True):
            return AsyncTogether()

    def test_create_classify_evaluation(self, mocker, sync_together_instance):
        # Mock the API requestor
        mock_requestor = mocker.MagicMock()
        response_data = {"workflow_id": "eval_123456", "status": "pending"}
        mock_headers = {"x-together-request-id": "req_123"}
        mock_response = TogetherResponse(data=response_data, headers=mock_headers)
        mock_requestor.request.return_value = (mock_response, None, None)
        mocker.patch(
            "together.abstract.api_requestor.APIRequestor", return_value=mock_requestor
        )

        # Test classify evaluation creation
        result = sync_together_instance.evaluation.create(
            type="classify",
            judge_model_name="meta-llama/Llama-3.2-11B-Vision-Instruct-Turbo",
            judge_system_template="You are a helpful assistant",
            input_data_file_path="file_123",
            labels=["accurate", "inaccurate"],
            pass_labels=["accurate"],
            model_to_evaluate="meta-llama/Llama-3.2-90B-Vision-Instruct-Turbo",
        )

        # Verify the request
        mock_requestor.request.assert_called_once()
        call_args = mock_requestor.request.call_args[1]["options"]
        assert call_args.method == "POST"
        assert call_args.url == "evaluation"
        assert call_args.params["type"] == "classify"

        # Verify parameters structure
        params = call_args.params["parameters"]
        assert (
            params["judge"]["model_name"]
            == "meta-llama/Llama-3.2-11B-Vision-Instruct-Turbo"
        )
        assert params["judge"]["system_template"] == "You are a helpful assistant"
        assert params["labels"] == ["accurate", "inaccurate"]
        assert params["pass_labels"] == ["accurate"]
        assert params["input_data_file_path"] == "file_123"
        assert (
            params["model_to_evaluate"]
            == "meta-llama/Llama-3.2-90B-Vision-Instruct-Turbo"
        )

        # Verify response
        assert isinstance(result, EvaluationCreateResponse)
        assert result.workflow_id == "eval_123456"
        assert result.status == EvaluationStatus.PENDING

    def test_create_score_evaluation(self, mocker, sync_together_instance):
        # Mock the API requestor
        mock_requestor = mocker.MagicMock()
        response_data = {"workflow_id": "eval_789012", "status": "queued"}
        mock_headers = {"x-together-request-id": "req_456"}
        mock_response = TogetherResponse(data=response_data, headers=mock_headers)
        mock_requestor.request.return_value = (mock_response, None, None)
        mocker.patch(
            "together.abstract.api_requestor.APIRequestor", return_value=mock_requestor
        )

        # Test score evaluation creation with ModelRequest
        model_request = {
            "model_name": "meta-llama/Llama-3.2-90B-Vision-Instruct-Turbo",
            "max_tokens": 512,
            "temperature": 0.7,
            "system_template": "You are an assistant",
            "input_template": "Question: {input}",
        }

        result = sync_together_instance.evaluation.create(
            type="score",
            judge_model_name="meta-llama/Llama-3.2-11B-Vision-Instruct-Turbo",
            judge_system_template="Rate the response",
            input_data_file_path="file_456",
            min_score=0.0,
            max_score=10.0,
            pass_threshold=7.0,
            model_to_evaluate=model_request,
        )

        # Verify the request
        mock_requestor.request.assert_called_once()
        call_args = mock_requestor.request.call_args[1]["options"]
        params = call_args.params["parameters"]

        assert params["min_score"] == 0.0
        assert params["max_score"] == 10.0
        assert params["pass_threshold"] == 7.0
        assert (
            params["model_to_evaluate"]["model_name"]
            == "meta-llama/Llama-3.2-90B-Vision-Instruct-Turbo"
        )
        assert params["model_to_evaluate"]["max_tokens"] == 512

        # Verify response
        assert result.workflow_id == "eval_789012"
        assert result.status == EvaluationStatus.QUEUED

    def test_create_compare_evaluation(self, mocker, sync_together_instance):
        # Mock the API requestor
        mock_requestor = mocker.MagicMock()
        response_data = {"workflow_id": "eval_345678", "status": "running"}
        mock_headers = {"x-together-request-id": "req_789"}
        mock_response = TogetherResponse(data=response_data, headers=mock_headers)
        mock_requestor.request.return_value = (mock_response, None, None)
        mocker.patch(
            "together.abstract.api_requestor.APIRequestor", return_value=mock_requestor
        )

        # Test compare evaluation creation
        result = sync_together_instance.evaluation.create(
            type="compare",
            judge_model_name="meta-llama/Llama-3.2-11B-Vision-Instruct-Turbo",
            judge_system_template="Compare the two responses",
            input_data_file_path="file_789",
            model_a="model-a-name",
            model_b="model-b-name",
        )

        # Verify the request
        call_args = mock_requestor.request.call_args[1]["options"]
        params = call_args.params["parameters"]
        print(params)
        assert params["model_a"] == "model-a-name"
        assert params["model_b"] == "model-b-name"

        # Verify response
        assert result.workflow_id == "eval_345678"
        assert result.status == EvaluationStatus.RUNNING

    def test_create_evaluation_missing_required_params(self, sync_together_instance):
        # Test missing labels for classify
        with pytest.raises(
            ValueError,
            match="labels are required for classify evaluation",
        ):
            sync_together_instance.evaluation.create(
                type="classify",
                judge_model_name="judge-model",
                judge_system_template="template",
                input_data_file_path="file_123",
                model_to_evaluate="asdfg",
            )

        # Test missing score params
        with pytest.raises(
            ValueError,
            match="min_score, max_score, and pass_threshold are required for score evaluation",
        ):
            sync_together_instance.evaluation.create(
                type="score",
                judge_model_name="judge-model",
                judge_system_template="template",
                input_data_file_path="file_123",
                model_to_evaluate="asdfg",
            )

        # Test invalid type
        with pytest.raises(ValueError, match="Invalid evaluation type"):
            sync_together_instance.evaluation.create(
                type="invalid_type",
                judge_model_name="judge-model",
                judge_system_template="template",
                input_data_file_path="file_123",
                model_to_evaluate="asdfg",
            )

    def test_list_evaluations(self, mocker, sync_together_instance):
        # Mock the API requestor
        mock_requestor = mocker.MagicMock()
        response_data = [
            {
                "workflow_id": "eval_1",
                "type": "classify",
                "status": "completed",
                "results": {"accuracy": 0.95},
                "created_at": "2024-01-01T00:00:00Z",
            },
            {
                "workflow_id": "eval_2",
                "type": "score",
                "status": "running",
                "created_at": "2024-01-02T00:00:00Z",
            },
        ]
        mock_headers = {"x-together-request-id": "req_list"}
        mock_response = TogetherResponse(data=response_data, headers=mock_headers)
        mock_requestor.request.return_value = (mock_response, None, None)
        mocker.patch(
            "together.abstract.api_requestor.APIRequestor", return_value=mock_requestor
        )

        # Test list without filters
        result = sync_together_instance.evaluation.list()

        # Verify the request
        call_args = mock_requestor.request.call_args[1]["options"]
        assert call_args.method == "GET"
        assert call_args.url == "evaluations"
        assert call_args.params is None

        # Verify response
        assert len(result) == 2
        assert all(isinstance(job, EvaluationJob) for job in result)
        assert result[0].workflow_id == "eval_1"
        assert result[1].workflow_id == "eval_2"

    def test_list_evaluations_with_filters(self, mocker, sync_together_instance):
        # Mock the API requestor
        mock_requestor = mocker.MagicMock()
        response_data = []
        mock_headers = {"x-together-request-id": "req_list_filtered"}
        mock_response = TogetherResponse(data=response_data, headers=mock_headers)
        mock_requestor.request.return_value = (mock_response, None, None)
        mocker.patch(
            "together.abstract.api_requestor.APIRequestor", return_value=mock_requestor
        )

        # Test list with filters
        result = sync_together_instance.evaluation.list(status="completed", limit=50)

        # Verify the request
        call_args = mock_requestor.request.call_args[1]["options"]
        assert call_args.params == {"status": "completed", "limit": 50}

        # Verify empty response
        assert result == []

    def test_retrieve_evaluation(self, mocker, sync_together_instance):
        # Mock the API requestor
        mock_requestor = mocker.MagicMock()
        response_data = {
            "workflow_id": "eval_123",
            "type": "classify",
            "status": "completed",
            "results": {"accuracy": 0.92, "pass_rate": 0.88},
            "parameters": {
                "judge": {"model_name": "judge-model", "system_template": "template"}
            },
            "created_at": "2024-01-01T00:00:00Z",
            "updated_at": "2024-01-01T01:00:00Z",
        }
        mock_headers = {"x-together-request-id": "req_retrieve"}
        mock_response = TogetherResponse(data=response_data, headers=mock_headers)
        mock_requestor.request.return_value = (mock_response, None, None)
        mocker.patch(
            "together.abstract.api_requestor.APIRequestor", return_value=mock_requestor
        )

        # Test retrieve
        result = sync_together_instance.evaluation.retrieve("eval_123")

        # Verify the request
        call_args = mock_requestor.request.call_args[1]["options"]
        assert call_args.method == "GET"
        assert call_args.url == "evaluation/eval_123"

        # Verify response
        assert isinstance(result, EvaluationJob)
        assert result.workflow_id == "eval_123"
        assert result.status == EvaluationStatus.COMPLETED
        assert result.results["accuracy"] == 0.92

    def test_status_evaluation(self, mocker, sync_together_instance):
        # Mock the API requestor
        mock_requestor = mocker.MagicMock()
        response_data = {
            "status": "completed",
            "results": {"total_samples": 100, "accuracy": 0.95, "pass_rate": 0.90},
        }
        mock_headers = {"x-together-request-id": "req_status"}
        mock_response = TogetherResponse(data=response_data, headers=mock_headers)
        mock_requestor.request.return_value = (mock_response, None, None)
        mocker.patch(
            "together.abstract.api_requestor.APIRequestor", return_value=mock_requestor
        )

        # Test status
        result = sync_together_instance.evaluation.status("eval_456")

        # Verify the request
        call_args = mock_requestor.request.call_args[1]["options"]
        assert call_args.method == "GET"
        assert call_args.url == "evaluation/eval_456/status"

        # Verify response
        assert isinstance(result, EvaluationStatusResponse)
        assert result.status == EvaluationStatus.COMPLETED
        assert result.results["total_samples"] == 100
        assert result.results["accuracy"] == 0.95

    @pytest.mark.asyncio
    async def test_async_create_evaluation(self, mocker, async_together_instance):
        # Mock the async API requestor
        mock_requestor = mocker.AsyncMock()
        response_data = {"workflow_id": "async_eval_123", "status": "pending"}
        mock_headers = {"x-together-request-id": "async_req_123"}
        mock_response = TogetherResponse(data=response_data, headers=mock_headers)
        mock_requestor.arequest.return_value = (mock_response, None, None)
        mocker.patch(
            "together.abstract.api_requestor.APIRequestor", return_value=mock_requestor
        )

        # Test async classify evaluation creation
        result = await async_together_instance.evaluation.create(
            type="classify",
            judge_model_name="judge-model",
            judge_system_template="template",
            input_data_file_path="file_async",
            labels=["good", "bad"],
            pass_labels=["good"],
        )

        # Verify the request was made with arequest
        mock_requestor.arequest.assert_called_once()

        # Verify response
        assert result.workflow_id == "async_eval_123"
        assert result.status == EvaluationStatus.PENDING

    @pytest.mark.asyncio
    async def test_async_list_evaluations(self, mocker, async_together_instance):
        # Mock the async API requestor
        mock_requestor = mocker.AsyncMock()
        response_data = [{"workflow_id": "async_eval_1", "status": "completed"}]
        mock_headers = {"x-together-request-id": "async_req_list"}
        mock_response = TogetherResponse(data=response_data, headers=mock_headers)
        mock_requestor.arequest.return_value = (mock_response, None, None)
        mocker.patch(
            "together.abstract.api_requestor.APIRequestor", return_value=mock_requestor
        )

        # Test async list
        result = await async_together_instance.evaluation.list()

        # Verify arequest was called
        mock_requestor.arequest.assert_called_once()

        # Verify response
        assert len(result) == 1
        assert result[0].workflow_id == "async_eval_1"

    @pytest.mark.asyncio
    async def test_async_retrieve_evaluation(self, mocker, async_together_instance):
        # Mock the async API requestor
        mock_requestor = mocker.AsyncMock()
        response_data = {"workflow_id": "async_eval_retrieve", "status": "running"}
        mock_headers = {"x-together-request-id": "async_req_retrieve"}
        mock_response = TogetherResponse(data=response_data, headers=mock_headers)
        mock_requestor.arequest.return_value = (mock_response, None, None)
        mocker.patch(
            "together.abstract.api_requestor.APIRequestor", return_value=mock_requestor
        )

        # Test async retrieve
        result = await async_together_instance.evaluation.retrieve(
            "async_eval_retrieve"
        )

        # Verify arequest was called
        mock_requestor.arequest.assert_called_once()

        # Verify response
        assert result.workflow_id == "async_eval_retrieve"
        assert result.status == EvaluationStatus.RUNNING

    @pytest.mark.asyncio
    async def test_async_status_evaluation(self, mocker, async_together_instance):
        # Mock the async API requestor
        mock_requestor = mocker.AsyncMock()
        response_data = {"status": "completed", "results": {"success": True}}
        mock_headers = {"x-together-request-id": "async_req_status"}
        mock_response = TogetherResponse(data=response_data, headers=mock_headers)
        mock_requestor.arequest.return_value = (mock_response, None, None)
        mocker.patch(
            "together.abstract.api_requestor.APIRequestor", return_value=mock_requestor
        )

        # Test async status
        result = await async_together_instance.evaluation.status("async_eval_status")

        # Verify arequest was called
        mock_requestor.arequest.assert_called_once()

        # Verify response
        assert result.status == EvaluationStatus.COMPLETED
        assert result.results["success"] is True
