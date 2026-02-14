# MIT License
# Copyright (c) 2025 Romashka

from typing import Any

from .types import SupportedTypes
from ._engine import Decoder, Encoder

__all__ = ["encode", "decode"]

def decode(litcode: str) -> Any:
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
    >>> "2l1i12s2"
    [1, "2"]
    >>> "4l1sA2sAB3sABC4sABCD"
    ["A", "AB", "ABC", "ABCD"]
    >>> "2l1bT1bF"
    [True, False]

    ---

    :param litcode: Encoded string in the custom literal serialization format.
    :type litcode: `str`
    :return: Decoded Python object reconstructed from the literal string.
    :rtype: `SupportedTypes`
    """
    return Decoder(litcode).decode()


def encode(literal: SupportedTypes) -> str:
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
    :return: Deterministic encoded string representation.
    :rtype: `str`
    """
    return Encoder(literal).encode()