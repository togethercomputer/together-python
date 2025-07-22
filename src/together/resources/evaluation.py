from __future__ import annotations

from typing import Any, Dict, List, Optional, Union

from together.abstract import api_requestor
from together.together_response import TogetherResponse
from together.types import (
    TogetherClient,
    TogetherRequest,
)
from together.types.evaluation import (
    ClassifyParameters,
    CompareParameters,
    EvaluationCreateResponse,
    EvaluationJob,
    EvaluationStatusResponse,
    JudgeModelConfig,
    ModelRequest,
    ScoreParameters,
)


class Evaluation:
    def __init__(self, client: TogetherClient) -> None:
        self._client = client

    def create(
        self,
        type: str,
        judge_model_name: str,
        judge_system_template: str,
        input_data_file_path: str,
        # Classify-specific parameters
        labels: Optional[List[str]] = None,
        pass_labels: Optional[List[str]] = None,
        # Score-specific parameters
        min_score: Optional[float] = None,
        max_score: Optional[float] = None,
        pass_threshold: Optional[float] = None,
        # Compare-specific parameters (model_a and model_b handled below)
        # Common optional parameters
        model_a: Optional[Union[str, Dict[str, Any]]] = None,
        model_b: Optional[Union[str, Dict[str, Any]]] = None,
        model_to_evaluate: Optional[Union[str, Dict[str, Any]]] = None,
    ) -> EvaluationCreateResponse:
        """
        Create a new evaluation job.

        Args:
            type: The type of evaluation ("classify", "score", or "compare")
            judge_model_name: Name of the judge model
            judge_system_template: System template for the judge
            input_data_file_path: Path to input data file
            labels: List of classification labels (required for classify)
            pass_labels: List of labels considered as passing (required for classify)
            min_score: Minimum score value (required for score)
            max_score: Maximum score value (required for score)
            pass_threshold: Threshold score for passing (required for score)
            model_to_evaluate: Model to evaluate for classify/score types
            model_a: Model A for compare type
            model_b: Model B for compare type

        Returns:
            EvaluationCreateResponse with workflow_id and status
        """
        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        # Build judge config
        judge_config = JudgeModelConfig(
            model_name=judge_model_name,
            system_template=judge_system_template,
        )
        parameters: Union[ClassifyParameters, ScoreParameters, CompareParameters]
        # Build parameters based on type
        if type == "classify":
            if labels is None or pass_labels is None:
                raise ValueError(
                    "labels and pass_labels are required for classify evaluation"
                )

            # Validate that no score-specific parameters are provided
            if any(
                [
                    min_score is not None,
                    max_score is not None,
                    pass_threshold is not None,
                ]
            ):
                raise ValueError(
                    "min_score, max_score, and pass_threshold parameters are exclusive to the score mode"
                )

            # Validate that no compare-specific parameters are provided
            if any([model_a is not None, model_b is not None]):
                raise ValueError(
                    "model_a and model_b parameters are exclusive to the compare mode"
                )

            parameters = ClassifyParameters(
                judge=judge_config,
                labels=labels,
                pass_labels=pass_labels,
                input_data_file_path=input_data_file_path,
            )

            # Handle model_to_evaluate
            if model_to_evaluate is not None:
                if isinstance(model_to_evaluate, str):
                    parameters.model_to_evaluate = model_to_evaluate
                elif isinstance(model_to_evaluate, dict):
                    # Validate that all required fields are present for model config
                    required_fields = [
                        "model_name",
                        "max_tokens",
                        "temperature",
                        "system_template",
                        "input_template",
                    ]
                    missing_fields = [
                        field
                        for field in required_fields
                        if field not in model_to_evaluate
                    ]
                    if missing_fields:
                        raise ValueError(
                            f"All model config parameters are required when using detailed configuration. "
                            f"Missing: {', '.join(missing_fields)}"
                        )
                    parameters.model_to_evaluate = ModelRequest(**model_to_evaluate)

        elif type == "score":
            if min_score is None or max_score is None or pass_threshold is None:
                raise ValueError(
                    "min_score, max_score, and pass_threshold are required for score evaluation"
                )

            # Validate that no classify-specific parameters are provided
            if any([labels is not None, pass_labels is not None]):
                raise ValueError(
                    "labels and pass_labels parameters are exclusive to the classify mode"
                )

            # Validate that no compare-specific parameters are provided
            if any([model_a is not None, model_b is not None]):
                raise ValueError(
                    "model_a and model_b parameters are exclusive to the compare mode"
                )

            parameters = ScoreParameters(
                judge=judge_config,
                min_score=min_score,
                max_score=max_score,
                pass_threshold=pass_threshold,
                input_data_file_path=input_data_file_path,
            )

            # Handle model_to_evaluate
            if model_to_evaluate is not None:
                if isinstance(model_to_evaluate, str):
                    parameters.model_to_evaluate = model_to_evaluate
                elif isinstance(model_to_evaluate, dict):
                    # Validate that all required fields are present for model config
                    required_fields = [
                        "model_name",
                        "max_tokens",
                        "temperature",
                        "system_template",
                        "input_template",
                    ]
                    missing_fields = [
                        field
                        for field in required_fields
                        if field not in model_to_evaluate
                    ]
                    if missing_fields:
                        raise ValueError(
                            f"All model config parameters are required when using detailed configuration. "
                            f"Missing: {', '.join(missing_fields)}"
                        )
                    parameters.model_to_evaluate = ModelRequest(**model_to_evaluate)

        elif type == "compare":
            # Validate that model_a and model_b are provided
            if model_a is None or model_b is None:
                raise ValueError(
                    "model_a and model_b parameters are required for compare evaluation"
                )

            # Validate that no classify-specific parameters are provided
            if any([labels is not None, pass_labels is not None]):
                raise ValueError(
                    "labels and pass_labels parameters are exclusive to the classify mode"
                )

            # Validate that no score-specific parameters are provided
            if any(
                [
                    min_score is not None,
                    max_score is not None,
                    pass_threshold is not None,
                ]
            ):
                raise ValueError(
                    "min_score, max_score, and pass_threshold parameters are exclusive to the score mode"
                )

            # Validate that model_to_evaluate is not provided
            if model_to_evaluate is not None:
                raise ValueError(
                    "model_to_evaluate parameter is exclusive to classify and score modes"
                )

            parameters = CompareParameters(
                judge=judge_config,
                input_data_file_path=input_data_file_path,
            )

            # Handle model_a
            if isinstance(model_a, str):
                parameters.model_a = model_a
            elif isinstance(model_a, dict):
                # Validate that all required fields are present for model config
                required_fields = [
                    "model_name",
                    "max_tokens",
                    "temperature",
                    "system_template",
                    "input_template",
                ]
                missing_fields = [
                    field for field in required_fields if field not in model_a
                ]
                if missing_fields:
                    raise ValueError(
                        f"All model config parameters are required for model_a when using detailed configuration. "
                        f"Missing: {', '.join(missing_fields)}"
                    )
                parameters.model_a = ModelRequest(**model_a)

            # Handle model_b
            if isinstance(model_b, str):
                parameters.model_b = model_b
            elif isinstance(model_b, dict):
                # Validate that all required fields are present for model config
                required_fields = [
                    "model_name",
                    "max_tokens",
                    "temperature",
                    "system_template",
                    "input_template",
                ]
                missing_fields = [
                    field for field in required_fields if field not in model_b
                ]
                if missing_fields:
                    raise ValueError(
                        f"All model config parameters are required for model_b when using detailed configuration. "
                        f"Missing: {', '.join(missing_fields)}"
                    )
                parameters.model_b = ModelRequest(**model_b)

        else:
            raise ValueError(
                f"Invalid evaluation type: {type}. Must be 'classify', 'score', or 'compare'"
            )

        payload = {
            "type": type,
            "parameters": parameters.model_dump(),
        }

        response, _, _ = requestor.request(
            options=TogetherRequest(
                method="POST",
                url="evaluation",
                params=payload,
            ),
            stream=False,
        )

        assert isinstance(response, TogetherResponse)
        return EvaluationCreateResponse(**response.data)

    def list(
        self,
        status: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> List[EvaluationJob]:
        """
        List evaluation jobs.

        Args:
            status: Optional filter by job status
            limit: Optional limit on number of results (max 100)

        Returns:
            List of EvaluationJob objects
        """
        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        params: Dict[str, Any] = {}
        if status is not None:
            params["status"] = status
        if limit is not None:
            params["limit"] = limit

        response, _, _ = requestor.request(
            options=TogetherRequest(
                method="GET",
                url="evaluations",
                params=params if params else None,
            ),
            stream=False,
        )

        assert isinstance(response, TogetherResponse)
        jobs = response.data or []
        return [EvaluationJob(**job) for job in jobs]

    def retrieve(self, evaluation_id: str) -> EvaluationJob:
        """
        Get details of a specific evaluation job.

        Args:
            evaluation_id: The workflow ID of the evaluation job

        Returns:
            EvaluationJob object with full details
        """
        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        response, _, _ = requestor.request(
            options=TogetherRequest(
                method="GET",
                url=f"evaluation/{evaluation_id}",
            ),
            stream=False,
        )

        assert isinstance(response, TogetherResponse)
        return EvaluationJob(**response.data)

    def status(self, evaluation_id: str) -> EvaluationStatusResponse:
        """
        Get the status and results of a specific evaluation job.

        Args:
            evaluation_id: The workflow ID of the evaluation job

        Returns:
            EvaluationStatusResponse with status and results
        """
        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        response, _, _ = requestor.request(
            options=TogetherRequest(
                method="GET",
                url=f"evaluation/{evaluation_id}/status",
            ),
            stream=False,
        )

        assert isinstance(response, TogetherResponse)
        return EvaluationStatusResponse(**response.data)


class AsyncEvaluation:
    def __init__(self, client: TogetherClient) -> None:
        self._client = client

    async def create(
        self,
        type: str,
        judge_model_name: str,
        judge_system_template: str,
        input_data_file_path: str,
        # Classify-specific parameters
        labels: Optional[List[str]] = None,
        pass_labels: Optional[List[str]] = None,
        # Score-specific parameters
        min_score: Optional[float] = None,
        max_score: Optional[float] = None,
        pass_threshold: Optional[float] = None,
        # Compare-specific parameters (model_a and model_b handled below)
        # Common optional parameters
        model_to_evaluate: Optional[Union[str, Dict[str, Any]]] = None,
        model_a: Optional[Union[str, Dict[str, Any]]] = None,
        model_b: Optional[Union[str, Dict[str, Any]]] = None,
    ) -> EvaluationCreateResponse:
        """
        Create a new evaluation job.

        Args:
            type: The type of evaluation ("classify", "score", or "compare")
            judge_model_name: Name of the judge model
            judge_system_template: System template for the judge
            input_data_file_path: Path to input data file
            labels: List of classification labels (required for classify)
            pass_labels: List of labels considered as passing (required for classify)
            min_score: Minimum score value (required for score)
            max_score: Maximum score value (required for score)
            pass_threshold: Threshold score for passing (required for score)
            model_to_evaluate: Model to evaluate for classify/score types
            model_a: Model A for compare type
            model_b: Model B for compare type

        Returns:
            EvaluationCreateResponse with workflow_id and status
        """
        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        # Build judge config
        judge_config = JudgeModelConfig(
            model_name=judge_model_name,
            system_template=judge_system_template,
        )
        parameters: Union[ClassifyParameters, ScoreParameters, CompareParameters]
        # Build parameters based on type
        if type == "classify":
            if labels is None or pass_labels is None:
                raise ValueError(
                    "labels and pass_labels are required for classify evaluation"
                )

            # Validate that no score-specific parameters are provided
            if any(
                [
                    min_score is not None,
                    max_score is not None,
                    pass_threshold is not None,
                ]
            ):
                raise ValueError(
                    "min_score, max_score, and pass_threshold parameters are exclusive to the score mode"
                )

            # Validate that no compare-specific parameters are provided
            if any([model_a is not None, model_b is not None]):
                raise ValueError(
                    "model_a and model_b parameters are exclusive to the compare mode"
                )

            parameters = ClassifyParameters(
                judge=judge_config,
                labels=labels,
                pass_labels=pass_labels,
                input_data_file_path=input_data_file_path,
            )

            # Handle model_to_evaluate
            if model_to_evaluate is not None:
                if isinstance(model_to_evaluate, str):
                    parameters.model_to_evaluate = model_to_evaluate
                elif isinstance(model_to_evaluate, dict):
                    # Validate that all required fields are present for model config
                    required_fields = [
                        "model_name",
                        "max_tokens",
                        "temperature",
                        "system_template",
                        "input_template",
                    ]
                    missing_fields = [
                        field
                        for field in required_fields
                        if field not in model_to_evaluate
                    ]
                    if missing_fields:
                        raise ValueError(
                            f"All model config parameters are required when using detailed configuration. "
                            f"Missing: {', '.join(missing_fields)}"
                        )
                    parameters.model_to_evaluate = ModelRequest(**model_to_evaluate)

        elif type == "score":
            if min_score is None or max_score is None or pass_threshold is None:
                raise ValueError(
                    "min_score, max_score, and pass_threshold are required for score evaluation"
                )

            # Validate that no classify-specific parameters are provided
            if any([labels is not None, pass_labels is not None]):
                raise ValueError(
                    "labels and pass_labels parameters are exclusive to the classify mode"
                )

            # Validate that no compare-specific parameters are provided
            if any([model_a is not None, model_b is not None]):
                raise ValueError(
                    "model_a and model_b parameters are exclusive to the compare mode"
                )

            parameters = ScoreParameters(
                judge=judge_config,
                min_score=min_score,
                max_score=max_score,
                pass_threshold=pass_threshold,
                input_data_file_path=input_data_file_path,
            )

            # Handle model_to_evaluate
            if model_to_evaluate is not None:
                if isinstance(model_to_evaluate, str):
                    parameters.model_to_evaluate = model_to_evaluate
                elif isinstance(model_to_evaluate, dict):
                    # Validate that all required fields are present for model config
                    required_fields = [
                        "model_name",
                        "max_tokens",
                        "temperature",
                        "system_template",
                        "input_template",
                    ]
                    missing_fields = [
                        field
                        for field in required_fields
                        if field not in model_to_evaluate
                    ]
                    if missing_fields:
                        raise ValueError(
                            f"All model config parameters are required when using detailed configuration. "
                            f"Missing: {', '.join(missing_fields)}"
                        )
                    parameters.model_to_evaluate = ModelRequest(**model_to_evaluate)

        elif type == "compare":
            parameters = CompareParameters(
                judge=judge_config,
                input_data_file_path=input_data_file_path,
            )

            # Validate that model_a and model_b are provided
            if model_a is None or model_b is None:
                raise ValueError(
                    "model_a and model_b parameters are required for compare evaluation"
                )

            # Validate that no classify-specific parameters are provided
            if any([labels is not None, pass_labels is not None]):
                raise ValueError(
                    "labels and pass_labels parameters are exclusive to the classify mode"
                )

            # Validate that no score-specific parameters are provided
            if any(
                [
                    min_score is not None,
                    max_score is not None,
                    pass_threshold is not None,
                ]
            ):
                raise ValueError(
                    "min_score, max_score, and pass_threshold parameters are exclusive to the score mode"
                )

            # Validate that model_to_evaluate is not provided
            if model_to_evaluate is not None:
                raise ValueError(
                    "model_to_evaluate parameter is exclusive to classify and score modes"
                )

            # Handle model_a
            if isinstance(model_a, str):
                parameters.model_a = model_a
            elif isinstance(model_a, dict):
                # Validate that all required fields are present for model config
                required_fields = [
                    "model_name",
                    "max_tokens",
                    "temperature",
                    "system_template",
                    "input_template",
                ]
                missing_fields = [
                    field for field in required_fields if field not in model_a
                ]
                if missing_fields:
                    raise ValueError(
                        f"All model config parameters are required for model_a when using detailed configuration. "
                        f"Missing: {', '.join(missing_fields)}"
                    )
                parameters.model_a = ModelRequest(**model_a)

            # Handle model_b
            if isinstance(model_b, str):
                parameters.model_b = model_b
            elif isinstance(model_b, dict):
                # Validate that all required fields are present for model config
                required_fields = [
                    "model_name",
                    "max_tokens",
                    "temperature",
                    "system_template",
                    "input_template",
                ]
                missing_fields = [
                    field for field in required_fields if field not in model_b
                ]
                if missing_fields:
                    raise ValueError(
                        f"All model config parameters are required for model_b when using detailed configuration. "
                        f"Missing: {', '.join(missing_fields)}"
                    )
                parameters.model_b = ModelRequest(**model_b)

        else:
            raise ValueError(
                f"Invalid evaluation type: {type}. Must be 'classify', 'score', or 'compare'"
            )

        payload = {
            "type": type,
            "parameters": parameters.model_dump(),
        }

        response, _, _ = await requestor.arequest(
            options=TogetherRequest(
                method="POST",
                url="evaluation",
                params=payload,
            ),
            stream=False,
        )

        assert isinstance(response, TogetherResponse)
        return EvaluationCreateResponse(**response.data)

    async def list(
        self,
        status: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> List[EvaluationJob]:
        """
        List evaluation jobs.

        Args:
            status: Optional filter by job status
            limit: Optional limit on number of results (max 100)

        Returns:
            List of EvaluationJob objects
        """
        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        params: Dict[str, Any] = {}
        if status is not None:
            params["status"] = status
        if limit is not None:
            params["limit"] = limit

        response, _, _ = await requestor.arequest(
            options=TogetherRequest(
                method="GET",
                url="evaluations",
                params=params if params else None,
            ),
            stream=False,
        )

        assert isinstance(response, TogetherResponse)
        jobs = response.data or []
        return [EvaluationJob(**job) for job in jobs]

    async def retrieve(self, evaluation_id: str) -> EvaluationJob:
        """
        Get details of a specific evaluation job.

        Args:
            evaluation_id: The workflow ID of the evaluation job

        Returns:
            EvaluationJob object with full details
        """
        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        response, _, _ = await requestor.arequest(
            options=TogetherRequest(
                method="GET",
                url=f"evaluation/{evaluation_id}",
            ),
            stream=False,
        )

        assert isinstance(response, TogetherResponse)
        return EvaluationJob(**response.data)

    async def status(self, evaluation_id: str) -> EvaluationStatusResponse:
        """
        Get the status and results of a specific evaluation job.

        Args:
            evaluation_id: The workflow ID of the evaluation job

        Returns:
            EvaluationStatusResponse with status and results
        """
        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        response, _, _ = await requestor.arequest(
            options=TogetherRequest(
                method="GET",
                url=f"evaluation/{evaluation_id}/status",
            ),
            stream=False,
        )

        assert isinstance(response, TogetherResponse)
        return EvaluationStatusResponse(**response.data)
