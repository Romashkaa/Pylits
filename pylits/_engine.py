# MIT License
# Copyright (c) 2025 Romashka

from .types import SupportedTypes, SupportedHashableTypes

class Encoder:
    def __init__(self, data: SupportedTypes):
        self.data: SupportedTypes = data

    def encode(self) -> str:
        return self.encode_item(self.data)
    
    def encode_item(self, item: SupportedTypes) -> str:
        match item: # TODO encoders[type(item)] (faster search)
            case None:
                return self.encode_none()
            case bool():
                return self.encode_bool(item)
            case int():
                return self.encode_int(item)
            case float():
                return self.encode_float(item)
            case str():
                return self.encode_str(item)
            case list():
                return self.encode_list(item)
            case tuple():
                return self.encode_tuple(item)
            case set():
                return self.encode_set(item)
            case dict():
                return self.encode_dict(item)

    def encode_none(self) -> str:
        return "0n"
            
    def encode_bool(self, value: bool) -> str:
        return "1bT" if value else "1bF"

    def encode_int(self, integer: int) -> str:
        return f"{len(str(integer))}i{integer}"
    
    def encode_float(self, number: float) -> str:
        return f"{len(str(number))}f{number}"
    
    def encode_str(self, string: str) -> str:
        return f"{len(string)}s{string}"
    
    def encode_list(self, items: list) -> str:
        return f"{len(items)}l{"".join(map(self.encode_item, items))}"
    
    def encode_tuple(self, items: tuple) -> str:
        return f"{len(items)}t{"".join(map(self.encode_item, items))}"

    def encode_set(self, items: set) -> str:
        _items = tuple(items)
        return f"{len(_items)}e{"".join(map(self.encode_item, _items))}"
    
    def encode_dict(self, items) -> str:
        return f"{len(items)}d{"".join([f"{self.encode_item(k)}{self.encode_item(v)}" for k, v in items.items()])}"
    

class Decoder:
    def __init__(self, code: str):
        self.code = code
        self.code_length = len(code)
        self.position = 0

    def decode(self):
        return self.decode_item()

    def decode_item(self) -> SupportedTypes:
        length: int = self.scan_length()

        item_type: str = self.consume()

        match item_type:
            case "n":
                return self.decode_none()
            case "b":
                return self.decode_bool()
            case "i":
                return self.decode_int(length)
            case "f":
                return self.decode_float(length)
            case "s":
                return self.decode_str(length)
            case "l":
                return self.decode_list(length)
            case "t":
                return self.decode_tuple(length)
            case "e":
                return self.decode_set(length) 
            case "d":
                return self.decode_dict(length) 
            case _:
                raise Exception() # TODO "message"
            
    def decode_hashable(self) -> SupportedHashableTypes:
        length: int = self.scan_length()

        item_type: str = self.consume()

        match item_type:
            case "n":
                return self.decode_none()
            case "b":
                return self.decode_bool()
            case "i":
                return self.decode_int(length)
            case "f":
                return self.decode_float(length)
            case "s":
                return self.decode_str(length)
            case "t":
                return self.decode_tuple(length) 
            case _:
                raise Exception() # TODO "message"
            
    def decode_none(self) -> None:
        return None
            
    def decode_bool(self) -> bool:
        return self.consume().upper() == "T" # 1bT | 1bF
    
    def decode_int(self, length: int) -> int:
        return int(self.scan_chunk(length))
    
    def decode_float(self, length: int) -> float:
        return float(self.scan_chunk(length))
    
    def decode_str(self, length: int) -> str:
        return str(self.scan_chunk(length))
    
    def decode_list(self, length: int) -> list:
        return [self.decode_item() for _ in range(length)]
    
    def decode_tuple(self, length: int) -> tuple:
        return tuple([self.decode_item() for _ in range(length)])
    
    def decode_set(self, length: int) -> set:
        return set([self.decode_item() for _ in range(length)])
    
    def decode_dict(self, length: int) -> dict[SupportedHashableTypes, SupportedTypes]:
        return dict([(self.decode_hashable(), self.decode_item()) for _ in range(length)])
    
    def scan_chunk(self, length: int) -> str:
        return "".join([self.consume() for _ in range(length)])

    def scan_length(self) -> int:
        char: str = self.char()
        length: str = ""

        while char.isdigit():
            length += char
            char = self.next()

        return int(length) # TODO .isdigit()

    def char(self) -> str:
        if self.position >= self.code_length:
            return ""
        
        return self.code[self.position]
    
    def skip(self):
        self.position += 1
    
    def next(self) -> str:
        self.position += 1
        return self.char()
    
    def consume(self) -> str:
        char: str = self.char()
        self.position += 1
        return char
    
    def is_eof(self) -> bool:
        return self.position >= self.code_length
