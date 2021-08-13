from collections import deque
from typing import Optional, Any, Deque

from constants import *


def lex_string(incoming: str) -> (Optional[str], str):
    json_seq = []

    if incoming[0] != JSON_QUOTE:
        return None, incoming

    for i in range(1, len(incoming)):
        if incoming[i] == JSON_QUOTE:
            return "".join(json_seq), incoming[len(json_seq) + 2:]
        else:
            json_seq.append(incoming[i])

    raise Exception('Expected end-of-string quote')


def lex_number(incoming) -> (Optional[float], str):
    json_number = []
    number_characters = {str(k): True for k in range(0, 10)} | {".": True}

    dot_added = False
    for c in incoming:
        if c in number_characters:
            if c == "." and not dot_added:
                dot_added = True
                json_number.append(c)
            elif c == "." and dot_added:
                break
            else:
                json_number.append(c)
        else:
            break

    rest = incoming[len(json_number):]

    if not len(json_number):
        return None, incoming

    if dot_added:
        return float("".join(json_number)), rest

    return int("".join(json_number)), rest


def lex_bool(incoming: str) -> (Optional[bool], str):
    if len(incoming) >= TRUE_LEN and incoming[:TRUE_LEN] == 'true':
        return True, incoming[TRUE_LEN:]
    if len(incoming) >= FALSE_LEN and incoming[:FALSE_LEN] == 'false':
        return False, incoming[FALSE_LEN:]
    return None, incoming


def lex_null(string: str) -> (Optional[bool], str):
    string_len = len(string)
    if string_len >= NULL_LEN and string[:NULL_LEN] == 'null':
        return True, string[NULL_LEN:]
    return None, string


def lex(string: str) -> Deque[Any]:
    tokens = deque([])
    while len(string):
        json_string, string = lex_string(string)
        if json_string is not None:
            tokens.append(json_string)
            continue

        json_number, string = lex_number(string)
        if json_number is not None:
            tokens.append(json_number)
            continue

        json_bool, string = lex_bool(string)
        if json_bool is not None:
            tokens.append(json_bool)
            continue

        json_null, string = lex_null(string)
        if json_null is not None:
            tokens.append(None)
            continue

        c = string[0]
        if c in JSON_WHITESPACE:
            # Ignore whitespace
            string = string[1:]
        elif c in JSON_SYNTAX:
            tokens.append(c)
            string = string[1:]
        else:
            raise Exception('Unexpected character: {}'.format(c))

    return tokens
