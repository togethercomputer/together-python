import random

import pytest


@pytest.fixture
def random_temperature():
    """Fixture to generate a random float between 0 and 2."""
    return random.uniform(0, 2)


@pytest.fixture
def random_top_p():
    """Fixture to generate a random float between 0 and 1."""
    return random.uniform(0, 1)


@pytest.fixture
def random_top_k():
    """Fixture to generate a random float between 0 and 100."""
    return random.randint(1, 100)


@pytest.fixture
def random_max_tokens():
    """Fixture to generate a random float between 0 and 128."""
    return random.randint(1, 128)


@pytest.fixture
def random_repetition_penalty():
    """Fixture to generate a random float between 0 and 1."""
    return random.uniform(0, 2)


@pytest.fixture
def random_presence_penalty():
    """Fixture to generate a random float between -2 and 2."""
    return random.uniform(-2, 2)


@pytest.fixture
def random_frequency_penalty():
    """Fixture to generate a random float between -2 and 2."""
    return random.uniform(-2, 2)


@pytest.fixture
def random_min_p():
    """Fixture to generate a random float between 0 and 1."""
    return random.uniform(0, 1)
