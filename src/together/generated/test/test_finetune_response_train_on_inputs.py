# coding: utf-8

"""
    Together APIs

    The Together REST API. Please see https://docs.together.ai for more details.

    The version of the OpenAPI document: 2.0.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from together.generated.models.finetune_response_train_on_inputs import (
    FinetuneResponseTrainOnInputs,
)


class TestFinetuneResponseTrainOnInputs(unittest.TestCase):
    """FinetuneResponseTrainOnInputs unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> FinetuneResponseTrainOnInputs:
        """Test FinetuneResponseTrainOnInputs
        include_optional is a boolean, when False only required
        params are included, when True both required and
        optional params are included"""
        # uncomment below to create an instance of `FinetuneResponseTrainOnInputs`
        """
        model = FinetuneResponseTrainOnInputs()
        if include_optional:
            return FinetuneResponseTrainOnInputs(
            )
        else:
            return FinetuneResponseTrainOnInputs(
        )
        """

    def testFinetuneResponseTrainOnInputs(self):
        """Test FinetuneResponseTrainOnInputs"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == "__main__":
    unittest.main()
