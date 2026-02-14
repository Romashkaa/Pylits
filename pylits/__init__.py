# MIT License
#
# Copyright (c) 2025 Romashka
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# This library contains the official implementation of the **Pylit** data serialization format,  
# authored and originally developed by Romashka.  
#
# Pylit is an open serialization format designed to store nested data structures (such as lists,  
# dictionaries, sets, and tuples) in a compact, efficient, and machine-friendly way.  
#
# This Python codebase represents the reference implementation of the Pylit format.  
# Both the format itself and this implementation are released under the terms of the MIT license.  
#
# You are free to use, modify, and distribute this implementation, as well as adopt the Pylit  
# format in your own software, tools, or libraries — commercial or non-commercial —  
# as long as the terms below are respected.

from ._version import __version__, ENGINE_VERSION
from ._engine import SupportedTypes
from ._api import encode, decode
from .types import SupportedTypes, SupportedHashableTypes
from . import types

__all__ = [
    "encode", "decode",
    "SupportedTypes", "SupportedHashableTypes",
    "types",
    "ENGINE_VERSION", "__version__"
]

# –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
#  SUPPORTED TYPES
# –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
#
#  list  →  l
#  dict  →  d
#  str   →  s
#  int   →  i
#  float →  f
#  bool  →  b
#  tuple →  t
#  set   →  e
#  None  →  n

# –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
#  EXAMPLE
# –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
#
# [1, "2"]                2l1i12s2
# ["A","AB","ABC","ABCD"] 4l1sA2sAB3sABC4sABCD
# [True, False]           2l1bT1bF