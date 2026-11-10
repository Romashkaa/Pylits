# MIT License
# Copyright (c) 2025 Romashka

from typing import Any

from .types import SupportedTypes
from ._engine import Decoder, Encoder
from ._deterministic_encoder import DeterministicEncoder

try:
    from beartype.door import die_if_unbearable # pyright: ignore[reportMissingImports]
    _beartype_available = True
except ImportError:
    # pip install beartype
    _beartype_available = False

__all__ = ["encode", "decode"]

def decode(litcode: str, expected: str | None = None) -> Any:
    """
    Decode a string produced by the PyLits' literal serialization format.

    This decoder reconstructs a Python value from a compact, deterministic,
    and high-performance literal encoding designed for speed and reliability.
    The format is intentionally restricted and supports only Python literal
    structures defined by `SupportedTypes`.

    Supported values include:
    `bool`, `int`, `float`, `str`, `list`, `tuple`, `set`,
    `dict`, and `None` with arbitrary nesting.

    ---

    Examples
    --------
    >>> decode("2l1i12s2")
    [1, "2"]
    >>> decode("4l1sA2sAB3sABC4sABCD")
    ["A", "AB", "ABC", "ABCD"]
    >>> decode("2l1bT1bF")
    [True, False]

    Beartype:
    >>> decode("1l2d1sa1i11sb1i2", expected=list[dict[str, int]])
    [{"a": 1, "b": 2}]

    ---

    :param litcode: Encoded string in the custom literal serialization format.
    :type litcode: `str`
    :param expected: Optional type hint to validate the decoded value against.
        Requires `beartype` to be installed. Example: `list[dict[str, int]]`.
    :type expected: `Any`

    :return: Decoded Python object reconstructed from the literal string.
    :rtype: `SupportedTypes`
    """
    result = Decoder(litcode).decode()

    if expected is not None:
        if not _beartype_available:
            raise ImportError(
                "Type validation requires `beartype`. Install it with: pip install beartype"
            )
        if not die_if_unbearable(result, expected): # pyright: ignore[reportPossiblyUnboundVariable]
            raise TypeError(
                f"Decoded value does not match expected type '{expected}'. "
                f"Got: {type(result).__name__}"
            )
   
    return result


def encode(literal: SupportedTypes, sort: bool=False) -> str:
    """
    Encode a Python literal into the PyLits' high-performance serialization format.

    This encoder converts supported Python literal values into a compact,
    deterministic string representation optimized for speed, minimal overhead,
    and reliable round-trip decoding. Only structures defined by
    `SupportedTypes` are supported.

    Supported values include:
    `bool`, `int`, `float`, `str`, `list`, `tuple`, `set`,
    `dict`, and `None` with arbitrary nesting.

    ---

    Examples
    --------
    >>> [1, "2"]
    "2l1i12s2"
    >>> ["A", "AB", "ABC", "ABCD"]
    "4l1sA2sAB3sABC4sABCD"
    >>> [True, False]
    "2l1bT1bF"

    ---

    :param literal: Python literal value to serialize.
    :type literal: `SupportedTypes`
    :param sort: Whether to use deterministic sorting for sets, dicts, lists, and tuples.
    :type sort: `bool`
    
    :return: Deterministic encoded string representation.
    :rtype: `str`
    """
    if sort:
        return DeterministicEncoder(literal).encode()

    return Encoder(literal).encode()