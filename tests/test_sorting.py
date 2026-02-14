import random
import logging
import pytest

import pylits

# -----------------------------------------------------------------------------
# Logging configuration
# -----------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger("pylits.tests")

# -----------------------------------------------------------------------------
# Test data
# -----------------------------------------------------------------------------
COLLECTIONS_TO_TEST = [
    [1, 2, 5, (3, 4), 3, 4, "string", "string2", "Romashka", "1", {2: 4, 1: 1, 3: 0}, {2, 4, 2, 5}],
    {1, 4, 5, 3, "hello", (5, 3)},
    {"a": [3, 2, 1], "b": {5, 4, 3}, "c": (2, 1)},
]

# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------
def shuffled_copy(x):
    """Return a shuffled copy of a list or tuple, unchanged for sets/dicts."""
    if isinstance(x, list):
        c = x.copy()
        random.shuffle(c)
        return c
    if isinstance(x, tuple):
        lst = list(x)
        random.shuffle(lst)
        return tuple(lst)
    if isinstance(x, set):
        lst = list(x)
        random.shuffle(lst)
        return set(lst)
    # dicts are shuffled by keys in list
    if isinstance(x, dict):
        items = list(x.items())
        random.shuffle(items)
        return dict(items)
    return x

# -----------------------------------------------------------------------------
# Tests
# -----------------------------------------------------------------------------
@pytest.mark.parametrize("collection", COLLECTIONS_TO_TEST)
def test_deterministic_encode_after_shuffle(collection):
    """
    Test that encoding with sort=True is deterministic,
    even if the collection is shuffled.
    """
    logger.info("Original collection: %r", collection)

    # Shuffle a copy
    shuffled = shuffled_copy(collection)
    logger.info("Shuffled collection: %r", shuffled)

    # Encode both with sort=True
    encoded_original = pylits.encode(collection, sort=True)
    encoded_shuffled = pylits.encode(shuffled, sort=True)

    logger.info("Encoded original: %r", encoded_original)
    logger.info("Encoded shuffled: %r", encoded_shuffled)

    # The encoded forms must be identical
    assert encoded_original == encoded_shuffled, "Deterministic encoding failed after shuffle"