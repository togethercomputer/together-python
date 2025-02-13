# coding: utf-8

"""
    Together APIs

    The Together REST API. Please see https://docs.together.ai for more details.

    The version of the OpenAPI document: 2.0.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from together.generated.models.chat_completion_chunk_choices_inner import (
    ChatCompletionChunkChoicesInner,
)


class TestChatCompletionChunkChoicesInner(unittest.TestCase):
    """ChatCompletionChunkChoicesInner unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> ChatCompletionChunkChoicesInner:
        """Test ChatCompletionChunkChoicesInner
        include_optional is a boolean, when False only required
        params are included, when True both required and
        optional params are included"""
        # uncomment below to create an instance of `ChatCompletionChunkChoicesInner`
        """
        model = ChatCompletionChunkChoicesInner()
        if include_optional:
            return ChatCompletionChunkChoicesInner(
                index = 56,
                finish_reason = 'stop',
                logprobs = 1.337,
                seed = 56,
                delta = together.generated.models.chat_completion_choice_delta.ChatCompletionChoiceDelta(
                    token_id = 56,
                    role = 'system',
                    content = '',
                    tool_calls = [
                        together.generated.models.tool_choice.ToolChoice(
                            index = 1.337,
                            id = '',
                            type = 'function',
                            function = together.generated.models.tool_choice_function.ToolChoice_function(
                                name = 'function_name',
                                arguments = '', ), )
                        ],
                    function_call = together.generated.models.chat_completion_choice_delta_function_call.ChatCompletionChoiceDelta_function_call(
                        arguments = '',
                        name = '', ), )
            )
        else:
            return ChatCompletionChunkChoicesInner(
                index = 56,
                finish_reason = 'stop',
                delta = together.generated.models.chat_completion_choice_delta.ChatCompletionChoiceDelta(
                    token_id = 56,
                    role = 'system',
                    content = '',
                    tool_calls = [
                        together.generated.models.tool_choice.ToolChoice(
                            index = 1.337,
                            id = '',
                            type = 'function',
                            function = together.generated.models.tool_choice_function.ToolChoice_function(
                                name = 'function_name',
                                arguments = '', ), )
                        ],
                    function_call = together.generated.models.chat_completion_choice_delta_function_call.ChatCompletionChoiceDelta_function_call(
                        arguments = '',
                        name = '', ), ),
        )
        """

    def testChatCompletionChunkChoicesInner(self):
        """Test ChatCompletionChunkChoicesInner"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == "__main__":
    unittest.main()
