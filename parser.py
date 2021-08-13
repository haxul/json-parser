from typing import Dict, Any, Deque, List
from constants import *


def parse_array(tokens: List[Any]) -> (Any, List[Any]):
    json_arr = []
    while True:
        element, tokens = parse(tokens)
        json_arr.append(element)
        head, *tail = tokens
        if head == JSON_RIGHT_BRACKET:
            return json_arr, tail
        elif head == JSON_COMMA:
            tokens = tail
        else:
            raise Exception("missed comma in array")


def parse_object(tokens: List[Any]) -> (Dict[Any, Any], List[Any]):
    json_object = {}

    if tokens[0] == JSON_RIGHT_BRACE:
        return json_object, tokens[1:]

    while True:
        json_key = tokens[0]
        if type(json_key) is str:
            tokens = tokens[1:]
        else:
            raise Exception(f'Expected string key, got: {json_key}')

        if tokens[0] != JSON_COLON:
            raise Exception(f'Expected colon after key in object, got: {tokens[0]}')

        json_value, tokens = parse(tokens[1:])

        json_object[json_key] = json_value

        t = tokens[0]
        if t == JSON_RIGHT_BRACE:
            return json_object, tokens[1:]
        elif t != JSON_COMMA:
            raise Exception(f'Expected comma after pair in object, got: {t}')

        tokens = tokens[1:]


def parse(tokens: List[Any]) -> (Any, List[Any]):
    head, *tail = tokens
    if head == JSON_LEFT_BRACKET:
        return parse_array(tail)
    elif head == JSON_LEFT_BRACE:
        return parse_object(tail)
    else:
        return head, tail
