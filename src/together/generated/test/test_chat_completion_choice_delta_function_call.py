# coding: utf-8

"""
    Together APIs

    The Together REST API. Please see https://docs.together.ai for more details.

    The version of the OpenAPI document: 2.0.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from together.generated.models.chat_completion_choice_delta_function_call import (
    ChatCompletionChoiceDeltaFunctionCall,
)


class TestChatCompletionChoiceDeltaFunctionCall(unittest.TestCase):
    """ChatCompletionChoiceDeltaFunctionCall unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> ChatCompletionChoiceDeltaFunctionCall:
        """Test ChatCompletionChoiceDeltaFunctionCall
        include_optional is a boolean, when False only required
        params are included, when True both required and
        optional params are included"""
        # uncomment below to create an instance of `ChatCompletionChoiceDeltaFunctionCall`
        """
        model = ChatCompletionChoiceDeltaFunctionCall()
        if include_optional:
            return ChatCompletionChoiceDeltaFunctionCall(
                arguments = '',
                name = ''
            )
        else:
            return ChatCompletionChoiceDeltaFunctionCall(
                arguments = '',
                name = '',
        )
        """

    def testChatCompletionChoiceDeltaFunctionCall(self):
        """Test ChatCompletionChoiceDeltaFunctionCall"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == "__main__":
    unittest.main()
