# coding: utf-8

"""
    Together APIs

    The Together REST API. Please see https://docs.together.ai for more details.

    The version of the OpenAPI document: 2.0.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from together.generated.models.chat_completion_assistant_message_param import (
    ChatCompletionAssistantMessageParam,
)


class TestChatCompletionAssistantMessageParam(unittest.TestCase):
    """ChatCompletionAssistantMessageParam unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> ChatCompletionAssistantMessageParam:
        """Test ChatCompletionAssistantMessageParam
        include_optional is a boolean, when False only required
        params are included, when True both required and
        optional params are included"""
        # uncomment below to create an instance of `ChatCompletionAssistantMessageParam`
        """
        model = ChatCompletionAssistantMessageParam()
        if include_optional:
            return ChatCompletionAssistantMessageParam(
                content = '',
                role = 'assistant',
                name = '',
                tool_calls = [
                    together.generated.models.tool_choice.ToolChoice(
                        index = 1.337,
                        id = '',
                        type = 'function',
                        function = together.generated.models.tool_choice_function.ToolChoice_function(
                            name = 'function_name',
                            arguments = '', ), )
                    ],
                function_call = together.generated.models.chat_completion_message_function_call.ChatCompletionMessage_function_call(
                    arguments = '',
                    name = '', )
            )
        else:
            return ChatCompletionAssistantMessageParam(
                role = 'assistant',
        )
        """

    def testChatCompletionAssistantMessageParam(self):
        """Test ChatCompletionAssistantMessageParam"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == "__main__":
    unittest.main()
