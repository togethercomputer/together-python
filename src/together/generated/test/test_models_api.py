# coding: utf-8

"""
    Together APIs

    The Together REST API. Please see https://docs.together.ai for more details.

    The version of the OpenAPI document: 2.0.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from together.generated.api.models_api import ModelsApi


class TestModelsApi(unittest.IsolatedAsyncioTestCase):
    """ModelsApi unit test stubs"""

    async def asyncSetUp(self) -> None:
        self.api = ModelsApi()

    async def asyncTearDown(self) -> None:
        await self.api.api_client.close()

    async def test_models(self) -> None:
        """Test case for models

        List all models
        """
        pass


if __name__ == "__main__":
    unittest.main()
