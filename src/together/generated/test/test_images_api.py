# coding: utf-8

"""
    Together APIs

    The Together REST API. Please see https://docs.together.ai for more details.

    The version of the OpenAPI document: 2.0.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from together.generated.api.images_api import ImagesApi


class TestImagesApi(unittest.IsolatedAsyncioTestCase):
    """ImagesApi unit test stubs"""

    async def asyncSetUp(self) -> None:
        self.api = ImagesApi()

    async def asyncTearDown(self) -> None:
        await self.api.api_client.close()

    async def test_images_generations_post(self) -> None:
        """Test case for images_generations_post

        Create image
        """
        pass


if __name__ == "__main__":
    unittest.main()
