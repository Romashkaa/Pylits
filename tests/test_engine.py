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

SIMPLE_LITERALS = [
    None,
    True,
    False,
    0,
    1,
    -1,
    3.14,
    "",
    "A",
    "Hello",
]

COLLECTION_LITERALS = [
    [],
    [1, 2, 3],
    ["A", "AB", "ABC"],
    [True, False, None],
    (),
    (1,),
    (1, 2, 3),
    set(),
    {1, 2, 3},
    {},
    {"A": 1, "B": 2},
]

NESTED_LITERALS = [
    [1, [2, [3]]],
    {"A": [1, 2, {"B": 3}]},
    ({"A", "B"}, ("C", "D")),
    [{"nested": {"deep": [1, 2, 3]}}],
]

ALL_LITERALS = SIMPLE_LITERALS + COLLECTION_LITERALS + NESTED_LITERALS


# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------

def deep_equal(a, b):
    """
    Strict deep comparison that correctly handles sets and nested structures.
    """
    if type(a) is not type(b):
        return False

    if isinstance(a, dict):
        if a.keys() != b.keys():
            return False
        return all(deep_equal(a[k], b[k]) for k in a)

    if isinstance(a, (list, tuple)):
        if len(a) != len(b):
            return False
        return all(deep_equal(x, y) for x, y in zip(a, b))

    if isinstance(a, set):
        if len(a) != len(b):
            return False
        return {repr(x) for x in a} == {repr(x) for x in b}

    return a == b


# -----------------------------------------------------------------------------
# Core round-trip test (MAIN GUARANTEE)
# -----------------------------------------------------------------------------

@pytest.mark.parametrize("value", ALL_LITERALS)
def test_literal_roundtrip(value):
    """
    Literal → encode → decode → strict equality with original literal.
    This is the fundamental correctness guarantee of the serialization format.
    """
    logger.info("Original literal: %r", value)

    encoded = pylits.encode(value)
    logger.info("Encoded form: %r", encoded)

    decoded = pylits.decode(encoded)
    logger.info("Decoded literal: %r", decoded)

    assert isinstance(encoded, str), "Encoded result must be a string"
    assert deep_equal(decoded, value), "Round-trip mismatch between original and decoded literal"


# -----------------------------------------------------------------------------
# Known canonical samples
# -----------------------------------------------------------------------------

def test_known_samples_roundtrip():
    """
    Ensure known literal codes decode correctly and re-encode deterministically.
    """
    samples = {
        "2l1i11s2": [1, "2"],
        "4l1sA2sAB3sABC4sABCD": ["A", "AB", "ABC", "ABCD"],
        "2l1bT1bF": [True, False],
    }

    for litcode, expected in samples.items():
        logger.info("Canonical code: %s", litcode)

        decoded = pylits.decode(litcode)
        logger.info("Decoded literal: %r", decoded)

        reencoded = pylits.encode(decoded)
        logger.info("Re-encoded form: %r", reencoded)

        assert deep_equal(decoded, expected), "Decoded value does not match expected literal"
        assert reencoded == litcode, "Encoding is not deterministic for canonical sample"