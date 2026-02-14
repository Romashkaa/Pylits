from ._engine import Encoder
from .types import SupportedHashableTypes, SupportedTypes

class DeterministicEncoder(Encoder):
    def encode_list(self, items: list[SupportedTypes]) -> str:
        sorted_items = sorted(items, key=lambda x: repr(x))
        return f"{len(sorted_items)}l{''.join(map(self.encode_item, sorted_items))}"

    def encode_tuple(self, items: tuple[SupportedTypes, ...]) -> str:
        sorted_items = sorted(items, key=lambda x: repr(x))
        return f"{len(sorted_items)}t{''.join(map(self.encode_item, sorted_items))}"

    def encode_set(self, items: set[SupportedTypes]) -> str:
        sorted_items = sorted(items, key=lambda x: repr(x))
        return f"{len(sorted_items)}e{''.join(map(self.encode_item, sorted_items))}"

    def encode_dict(self, items: dict[SupportedHashableTypes, SupportedTypes]) -> str:
        sorted_items = sorted(items.items(), key=lambda kv: repr(kv[0]))
        return f"{len(sorted_items)}d{''.join(self.encode_item(k) + self.encode_item(v) for k, v in sorted_items)}"