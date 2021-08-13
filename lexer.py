from collections import deque
from typing import Optional, List, Any, Deque

from constants import *

def lex_string(incoming_str: str) -> (Optional[str], str):
    json_seq = []

    if incoming_str[0] != JSON_QUOTE:
        return None, incoming_str

    for i in range(1, len(incoming_str)):
        if incoming_str[i] == JSON_QUOTE:
            return "".join(json_seq), incoming_str[len(json_seq) + 2:]
        else:
            json_seq.append(incoming_str[i])

    raise Exception('Expected end-of-string quote')


def lex_number(string) -> (Optional[float], str):
    json_number = []
    number_characters = {str(k): True for k in range(0, 10)} | {".": True}

    dot_added = False
    for c in string:
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

    rest = string[len(json_number):]

    if not len(json_number):
        return None, string

    if dot_added:
        return float("".join(json_number)), rest

    return int("".join(json_number)), rest


def lex_bool(string: str) -> (Optional[bool], str):
    if len(string) >= TRUE_LEN and string[:TRUE_LEN] == 'true':
        return True, string[TRUE_LEN:]
    if len(string) >= FALSE_LEN and string[:FALSE_LEN] == 'false':
        return False, string[FALSE_LEN:]
    return None, string


def lex_null(string: str) -> (Optional[bool], str):
    string_len = len(string)
    if string_len >= NULL_LEN and string[:NULL_LEN] == 'null':
        return True, string[NULL_LEN:]
    return None, string


def lex(string: str) -> List[Any]:
    tokens = []
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
