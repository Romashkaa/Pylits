![PyLits Logo](./images/banner.png)

# Pylits

**pylits** is a high-performance, deterministic serialization format for **pure Python literals**.

It provides extremely fast and reliable encoding/decoding while intentionally supporting **only safe literal types**, making it suitable for:

- Зберігання даних в файлі надійніше ніж "eval()"
- Перетворення вашої БД на динамічно типізовану з підтримкою списків та словників
- hashing

## Key Features

- ⚡ **Very fast** — minimal parsing overhead compared to JSON-like formats
- 🔒 **Safe by design** — supports only pure Python literals
- 🎯 **Deterministic** — identical data always produces identical encoded output
- 🧩 **Zero dependencies** — pure Python implementation
- 🔁 **Lossless round-trip** — `decode(encode(x)) == x`

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

### Booleans

```python
pylits.encode([True, False])
# "2l1bT1bF"
```

## Deterministic Encoding

A modified internal encoder guarantees **stable output** even when:

- dictionary key order differs  
- set element order differs  

This makes `pylits` suitable for hashing.

## License

MIT License  
Copyright (c) 2025 Ving Studio, Romashka