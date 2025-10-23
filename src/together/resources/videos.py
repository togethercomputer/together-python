from __future__ import annotations

from typing import Any, Dict, List
import sys

from together.abstract import api_requestor
from together.together_response import TogetherResponse
from together.types import (
    TogetherClient,
    TogetherRequest,
)
from together.types.videos import (
    CreateVideoResponse,
    CreateVideoBody,
    VideoJob,
)

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


class Videos:
    def __init__(self, client: TogetherClient) -> None:
        self._client = client

    def create(
        self,
        *,
        model: str,
        prompt: str | None = None,
        height: int | None = None,
        width: int | None = None,
        seconds: str | None = None,
        fps: int | None = None,
        steps: int | None = None,
        seed: int | None = None,
        guidance_scale: float | None = None,
        output_format: Literal["MP4", "WEBM"] | None = None,
        output_quality: int | None = None,
        negative_prompt: str | None = None,
        frame_images: List[Dict[str, Any]] | None = None,
        reference_images: List[str] | None = None,
        **kwargs: Any,
    ) -> CreateVideoResponse:
        """
        Method to generate videos based on a given prompt using a specified model.

        Args:
            model (str): The model to use for video generation.

            prompt (str): A description of the desired video. Positive prompt for the generation.

            height (int, optional): Height of the video to generate in pixels.

            width (int, optional): Width of the video to generate in pixels.

            seconds (str, optional): Length of generated video in seconds. Min 1 max 10.

            fps (int, optional): Frames per second, min 15 max 60. Defaults to 24.

            steps (int, optional): The number of denoising steps the model performs during video
                generation. More steps typically result in higher quality output but require longer
                processing time. Min 10 max 50. Defaults to 20.

            seed (int, optional): Seed to use in initializing the video generation. Using the same
                seed allows deterministic video generation. If not provided, a random seed is
                generated for each request. Note: When requesting multiple videos with the same
                seed, the seed will be incremented by 1 (+1) for each video generated.

            guidance_scale (float, optional): Controls how closely the video generation follows your
                prompt. Higher values make the model adhere more strictly to your text description,
                while lower values allow more creative freedom. Recommended range is 6.0-10.0 for
                most video models. Values above 12 may cause over-guidance artifacts or unnatural
                motion patterns. Defaults to 8.

            output_format (str, optional): Specifies the format of the output video. Either "MP4"
                or "WEBM". Defaults to "MP4".

            output_quality (int, optional): Compression quality. Defaults to 20.

            negative_prompt (str, optional): Similar to prompt, but specifies what to avoid instead
                of what to include. Defaults to None.

            frame_images (List[Dict[str, Any]], optional): Array of images to guide video generation,
                like keyframes. If size 1, starting frame; if size 2, starting and ending frame;
                if more than 2 then frame must be specified. Defaults to None.

            reference_images (List[str], optional): An array containing reference images
                used to condition the generation process. These images provide visual guidance to
                help the model generate content that aligns with the style, composition, or
                characteristics of the reference materials. Defaults to None.

        Returns:
            CreateVideoResponse: Object containing video generation job id
        """

        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        parameter_payload = CreateVideoBody(
            prompt=prompt,
            model=model,
            height=height,
            width=width,
            seconds=seconds,
            fps=fps,
            steps=steps,
            seed=seed,
            guidance_scale=guidance_scale,
            output_format=output_format,
            output_quality=output_quality,
            negative_prompt=negative_prompt,
            frame_images=frame_images,
            reference_images=reference_images,
            **kwargs,
        ).model_dump(exclude_none=True)

        response, _, _ = requestor.request(
            options=TogetherRequest(
                method="POST",
                url="../v2/videos",
                params=parameter_payload,
            ),
            stream=False,
        )

        assert isinstance(response, TogetherResponse)

        return CreateVideoResponse(**response.data)

    def retrieve(
        self,
        id: str,
    ) -> VideoJob:
        """
        Method to retrieve a video creation job.

        Args:
            id (str): The ID of the video creation job to retrieve.

        Returns:
            VideoJob: Object containing the current status and details of the video creation job
        """

        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        response, _, _ = requestor.request(
            options=TogetherRequest(
                method="GET",
                url=f"../v2/videos/{id}",
            ),
            stream=False,
        )

        assert isinstance(response, TogetherResponse)

        return VideoJob(**response.data)


class AsyncVideos:
    def __init__(self, client: TogetherClient) -> None:
        self._client = client

    async def create(
        self,
        *,
        prompt: str,
        model: str,
        height: int | None = None,
        width: int | None = None,
        seconds: float | None = None,
        fps: int | None = None,
        steps: int | None = None,
        seed: int | None = None,
        guidance_scale: float | None = None,
        output_format: Literal["MP4", "WEBM"] | None = None,
        output_quality: int | None = None,
        negative_prompt: str | None = None,
        frame_images: List[Dict[str, Any]] | None = None,
        reference_images: List[str] | None = None,
        **kwargs: Any,
    ) -> CreateVideoResponse:
        """
        Async method to create videos based on a given prompt using a specified model.

        Args:
            prompt (str): A description of the desired video. Positive prompt for the generation.

            model (str): The model to use for video generation.

            height (int, optional): Height of the video to generate in pixels.

            width (int, optional): Width of the video to generate in pixels.

            seconds (float, optional): Length of generated video in seconds. Min 1 max 10.

            fps (int, optional): Frames per second, min 15 max 60. Defaults to 24.

            steps (int, optional): The number of denoising steps the model performs during video
                generation. More steps typically result in higher quality output but require longer
                processing time. Min 10 max 50. Defaults to 20.

            seed (int, optional): Seed to use in initializing the video generation. Using the same
                seed allows deterministic video generation. If not provided, a random seed is
                generated for each request. Note: When requesting multiple videos with the same
                seed, the seed will be incremented by 1 (+1) for each video generated.

            guidance_scale (float, optional): Controls how closely the video generation follows your
                prompt. Higher values make the model adhere more strictly to your text description,
                while lower values allow more creative freedom. Recommended range is 6.0-10.0 for
                most video models. Values above 12 may cause over-guidance artifacts or unnatural
                motion patterns. Defaults to 8.

            output_format (Literal["MP4", "WEBM"], optional): Specifies the format of the output video. Either "MP4"
                or "WEBM". Defaults to "MP4".

            output_quality (int, optional): Compression quality. Defaults to 20.

            negative_prompt (str, optional): Similar to prompt, but specifies what to avoid instead
                of what to include. Defaults to None.

            frame_images (List[Dict[str, Any]], optional): Array of images to guide video generation,
                like keyframes. If size 1, starting frame; if size 2, starting and ending frame;
                if more than 2 then frame must be specified. Defaults to None.

            reference_images (List[str], optional): An array containing reference images
                used to condition the generation process. These images provide visual guidance to
                help the model generate content that aligns with the style, composition, or
                characteristics of the reference materials. Defaults to None.

        Returns:
            CreateVideoResponse: Object containing video creation job id
        """

        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        parameter_payload = CreateVideoBody(
            prompt=prompt,
            model=model,
            height=height,
            width=width,
            seconds=seconds,
            fps=fps,
            steps=steps,
            seed=seed,
            guidance_scale=guidance_scale,
            output_format=output_format,
            output_quality=output_quality,
            negative_prompt=negative_prompt,
            frame_images=frame_images,
            reference_images=reference_images,
            **kwargs,
        ).model_dump(exclude_none=True)

        response, _, _ = await requestor.arequest(
            options=TogetherRequest(
                method="POST",
                url="../v2/videos",
                params=parameter_payload,
            ),
            stream=False,
        )

        assert isinstance(response, TogetherResponse)

        return CreateVideoResponse(**response.data)

    async def retrieve(
        self,
        id: str,
    ) -> VideoJob:
        """
        Async method to retrieve a video creation job.

        Args:
            id (str): The ID of the video creation job to retrieve.

        Returns:
            VideoJob: Object containing the current status and details of the video creation job
        """

        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        response, _, _ = await requestor.arequest(
            options=TogetherRequest(
                method="GET",
                url=f"../v2/videos/{id}",
            ),
            stream=False,
        )

        assert isinstance(response, TogetherResponse)

        return VideoJob(**response.data)
