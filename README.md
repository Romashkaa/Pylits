![PyLits Logo](https://github.com/Romashkaa/Pylits/raw/main/images/shadow_banner.png)

# Pylits

**pylits** is a high-performance, deterministic serialization format for **pure Python literals**.

It provides extremely fast and reliable encoding/decoding while intentionally supporting **only safe literal types**, making it suitable for:

- Storing data in files _(safer than `eval()`)_
- Transforming your DB into dynamically typed structures _with support for lists and dictionaries_
- Hashing

> ## 🔗 Try it online
>
> ### **[romashkaa.github.io/Pylits](https://romashkaa.github.io/Pylits/)**
>
> Convert between **Python**, **JSON** and **Pylits** in your browser.
> A **Blocks** view shows the structure of a Pylits string as a tree, and **Auto length** keeps the length prefixes correct while you type.

## Table of Contents

- [Key Features](#key-features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Supported Types](#supported-types)
- [The Format](#the-format)
- [Examples](#examples)
- [Deterministic Encoding](#deterministic-encoding)
- [Why length prefixes?](#why-length-prefixes)
- [Limitations](#limitations)
- [Online Converter](#online-converter)
- [License](#license)

## Key Features

- **Very fast** — minimal parsing overhead compared to JSON-like formats
- **Safe by design** — supports only pure Python literals
- **Deterministic** — identical data always produces identical encoded output
- **No escaping** — strings are stored as-is, never quoted or escaped
- **Zero dependencies** — pure Python implementation
- **Lossless round-trip** — `decode(encode(x)) == x`

## Installation

```bash
pip install pylits
```

## Quick Start

```python
import pylits

data = [1, "2", True, (None, {"Pylits": 21})]

encoded = pylits.encode(data)
decoded = pylits.decode(encoded)

assert decoded == data
```

## Supported Types

`pylits` works strictly with Python literal structures:

```python
SupportedTypes = (
    bool
    | int
    | float
    | str
    | list["SupportedTypes"]
    | tuple["SupportedTypes", ...]
    | set["SupportedTypes"]
    | dict["SupportedTypes", "SupportedTypes"]
    | None
)
```

Anything outside this set is intentionally **not supported**.

## The Format

Every value is written as three parts, with **no separators, no brackets and no quotes**:

```
<length><type><payload>
```

| Part      | Meaning                                                              |
| --------- | -------------------------------------------------------------------- |
| `length`  | A decimal number. Its meaning depends on the type (see below).       |
| `type`    | A single letter that says what kind of value follows.                |
| `payload` | The value itself: raw characters for scalars, child values for containers. |

### Type letters

| Letter | Python type | `length` means                  | Payload                                  | Example                |
| ------ | ----------- | ------------------------------- | ---------------------------------------- | ---------------------- |
| `n`    | `None`      | always `0`                      | nothing                                  | `0n`                   |
| `b`    | `bool`      | always `1`                      | `T` or `F`                               | `1bT`, `1bF`           |
| `i`    | `int`       | number of characters in the number | the decimal digits (with `-` if negative) | `2i42`, `3i-17`     |
| `f`    | `float`     | number of characters in the number | the float as text (`3.14`, `1e-05`, `inf`, `nan`) | `4f3.14`   |
| `s`    | `str`       | number of **characters** (Unicode code points) | the raw text, unescaped    | `5shello`, `0s`        |
| `l`    | `list`      | number of **elements**          | the elements, one after another          | `2l1i11i2`             |
| `t`    | `tuple`     | number of **elements**          | the elements, one after another          | `2t1i11i2`             |
| `e`    | `set`       | number of **elements**          | the elements, one after another          | `2e1i11i2`             |
| `d`    | `dict`      | number of **key–value pairs**   | `key value key value …`                  | `1d1sa1i1`             |

### Containers

A container stores how many items it has, and then simply writes the items one after another. There is no closing marker: the decoder knows where the container ends because it has already read exactly `length` children.

- **List / tuple / set** — `length` elements follow.
- **Dict** — `length` **pairs** follow, each pair being a key value and then its value value (`k1 v1 k2 v2 …`).
- Containers can be nested to any depth.
- Dict keys must be hashable, so a key can be `None`, `bool`, `int`, `float`, `str` or a `tuple` — but **not** a `list`, `set` or `dict`.
- Empty containers are valid: `0l`, `0t`, `0e`, `0d`.

### Strings

The length of a string is counted in **characters**, not bytes. Because the decoder knows exactly how many characters to take, the text can contain _anything_: quotes, backslashes, newlines, digits, even text that looks like Pylits itself. Nothing needs to be escaped.

```python
pylits.encode("héllo")      # "5shéllo"
pylits.encode('say "hi"')   # '8ssay "hi"'
pylits.encode("")           # "0s"
```

### Walkthrough

Let's encode `[1, "2", True, (None, {"Pylits": 21})]` piece by piece:

```
4l                  list with 4 elements
  1i1               int      →  1 character:  "1"
  1s2               str      →  1 character:  "2"
  1bT               bool     →  True
  2t                tuple with 2 elements
    0n              None
    1d              dict with 1 pair
      6sPylits      key:   str, 6 characters: "Pylits"
      2i21          value: int, 2 characters: "21"
```

Written without the line breaks:

```
4l1i11s21bT2t0n1d6sPylits2i21
```

### Grammar

```
value     = length type payload
length    = digit+
type      = "n" | "b" | "i" | "f" | "s" | "l" | "t" | "e" | "d"

payload   = ""                        ; type n   (length = 0)
          | "T" | "F"                 ; type b   (length = 1)
          | char{length}              ; types i, f, s
          | value{length}             ; types l, t, e
          | (value value){length}     ; type d
```

## Examples

### Lists

```python
pylits.encode([1, "2"])
# "2l1i11s2"

pylits.decode("2l1i11s2")
# [1, "2"]
```

### Strings

```python
pylits.encode(["A", "AB", "ABC", "ABCD"])
# "4l1sA2sAB3sABC4sABCD"
```

### Booleans and None

```python
pylits.encode([True, False, None])
# "3l1bT1bF0n"
```

### Numbers

```python
pylits.encode([42, -7, 3.14])
# "3l2i422i-74f3.14"
```

### Dicts

```python
pylits.encode({"a": 1, "b": [2, 3]})
# "2d1sa1i11sb2l1i21i3"
```

### Tuples and sets

```python
pylits.encode((1, 2))
# "2t1i11i2"

pylits.encode({3, 1, 2})
# "3e1i11i21i3"
```

## Deterministic Encoding

A modified internal encoder guarantees **stable output** even when:

- dictionary key order differs
- set element order differs

Dict pairs and set elements are written in a fixed order (sorted by their encoded form), so equal data always produces exactly the same string. This makes `pylits` suitable for hashing:

```python
import hashlib, pylits

a = {"x": 1, "y": 2}
b = {"y": 2, "x": 1}

assert pylits.encode(a) == pylits.encode(b)
print(hashlib.sha256(pylits.encode(a).encode()).hexdigest())
```

## Why length prefixes?

Formats like JSON have to _scan_ every character to find where a string ends, which is why quotes must be escaped. Pylits flips this around: it says **how much** to read before reading it.

- **Fast decoding** — a string is a single slice, with no scanning, no escape handling and no quote matching.
- **No escaping** — any text is stored verbatim.
- **No delimiters** — no commas, colons, brackets or whitespace, so the output is compact.
- **Unambiguous** — there is exactly one valid encoding of every value, which is what makes it deterministic.

The trade-off is that the format is meant for machines: if you edit a value by hand, you have to update its length. The [online converter](https://romashkaa.github.io/Pylits/) does this for you with its **Auto length** option.

## Limitations

- Only the types listed in [Supported Types](#supported-types) can be encoded. Custom classes, `bytes`, `datetime`, etc. are rejected on purpose.
- Dict keys must be hashable (no `list`, `set` or `dict` keys).
- Tuple and set _types_ are preserved, so `[1, 2]`, `(1, 2)` and `{1, 2}` all encode differently.
- Pylits is not designed to be written by hand; use the converter for that.

## Online Converter

👉 **<https://romashkaa.github.io/Pylits/>**

- Convert **Python ⇄ JSON ⇄ Pylits** in either direction
- **Blocks** view: see nesting as a tree and key → value pairs as arrows
- **Text** view: a minimal editor with highlighted length/type tags
- **Auto length**: edit a string or number and its length prefix updates automatically
- **Deterministic** switch: sort dict keys and set elements
- Shows how many characters Pylits saves compared to compact JSON

## License

MIT License
Copyright (c) 2026 Romashka