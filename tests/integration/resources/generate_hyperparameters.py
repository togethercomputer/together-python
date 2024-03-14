import random

import pytest


@pytest.fixture
def random_temperature():
    """Fixture to generate a random float between 0 and 1."""
    return random.uniform(0, 2)


@pytest.fixture
def random_top_p():
    """Fixture to generate a random float between 0 and 1."""
    return random.uniform(0, 1)


@pytest.fixture
def random_top_k():
    """Fixture to generate a random float between 0 and 1."""
    return random.randint(1, 100)


@pytest.fixture
def random_max_tokens():
    """Fixture to generate a random float between 0 and 1."""
    return random.randint(1, 128)


@pytest.fixture
def random_repetition_penalty():
    """Fixture to generate a random float between 0 and 1."""
    return random.uniform(0, 2)
