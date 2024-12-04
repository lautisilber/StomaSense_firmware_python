def clamp(n: int | float, smallest: int | float, biggest: int | float) -> int | float:
    return smallest if n < smallest else biggest if n > biggest else n

def is_number(v: int | str) -> bool:
    if isinstance(v, int):
        return True
    elif isinstance(v, str):
        starting_index = 1 if v.startswith("-") else 0
        for c in v[starting_index:]:
            asc = ord(c)
            if asc < 48 or asc > 57:
                return False
        return True
    return False

def has_keys(obj: dict, keys: tuple) -> bool:
    return all(map(lambda k: k in obj, keys))

from .sdcard_helper import SD
import json

def load_json_sd(file: str) -> dict | None:
    try:
        with SD() as sd:
            with sd.open(file, "r") as f:
                try:
                    obj = json.load(f)
                except ValueError as e:
                    print(e)
                    return None
    except OSError as e:
        print(e)
        return None
    return obj

def load_json_fs(file: str) -> dict | None:
    try:
        with open(file, "r") as f:
            try:
                obj = json.load(f)
            except ValueError as e:
                print(e)
                return None
    except OSError as e:
        print(e)
        return None
    return obj

def dump_json_sd(file: str, obj: dict | list) -> bool:
    try:
        with SD() as sd:
            with sd.open(file, "w") as f:
                try:
                    json.dump(obj, f)
                except ValueError as e:
                    print(e)
                    return False
    except OSError as e:
        print(e)
        return False
    return True

def dump_json_fs(file: str, obj: dict | list) -> bool:
    try:
        with open(file, "w") as f:
            try:
                json.dump(obj, f)
            except ValueError as e:
                print(e)
                return False
    except OSError as e:
        print(e)
        return False
    return True