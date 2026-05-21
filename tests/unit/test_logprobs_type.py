import warnings

from together.types.common import LogprobsPart


def test_logprobs_part_top_logprobs_is_list():
    """LogprobsPart.top_logprobs must accept a list of per-token dicts (issue #443)."""
    lp = LogprobsPart(
        tokens=["Hello", "."],
        token_logprobs=[-2.6e-06, -4.8e-05],
        top_logprobs=[
            {"Hello": -2.6e-06, "hello": -13.5, " Hello": -13.875},
            {".": -4.8e-05, "!": -10.2},
        ],
    )
    assert isinstance(lp.top_logprobs, list)
    assert len(lp.top_logprobs) == 2
    assert isinstance(lp.top_logprobs[0], dict)
    assert lp.top_logprobs[0]["Hello"] == -2.6e-06


def test_logprobs_part_model_dump_no_warning():
    """model_dump() must not emit PydanticSerializationUnexpectedValue for top_logprobs."""
    lp = LogprobsPart(
        tokens=["Hello"],
        token_logprobs=[-2.6e-06],
        top_logprobs=[{"Hello": -2.6e-06, "hello": -13.5}],
    )
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        dumped = lp.model_dump()
    assert isinstance(dumped["top_logprobs"], list)
    assert dumped["top_logprobs"][0]["Hello"] == -2.6e-06


def test_logprobs_part_top_logprobs_optional():
    """top_logprobs defaults to None when not supplied."""
    lp = LogprobsPart(tokens=["hi"], token_logprobs=[-0.5])
    assert lp.top_logprobs is None
