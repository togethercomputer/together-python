# coding: utf-8

"""
    Together APIs

    The Together REST API. Please see https://docs.together.ai for more details.

    The version of the OpenAPI document: 2.0.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from together.generated.models.list_hardware200_response import ListHardware200Response


class TestListHardware200Response(unittest.TestCase):
    """ListHardware200Response unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> ListHardware200Response:
        """Test ListHardware200Response
        include_optional is a boolean, when False only required
        params are included, when True both required and
        optional params are included"""
        # uncomment below to create an instance of `ListHardware200Response`
        """
        model = ListHardware200Response()
        if include_optional:
            return ListHardware200Response(
                object = 'list',
                data = [
                    null
                    ]
            )
        else:
            return ListHardware200Response(
                object = 'list',
                data = [
                    null
                    ],
        )
        """

    def testListHardware200Response(self):
        """Test ListHardware200Response"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == "__main__":
    unittest.main()
