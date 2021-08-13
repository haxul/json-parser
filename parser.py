from typing import Dict, Any, Deque
from constants import *


def parse_array(tokens: Deque[Any]) -> (Any, Deque[Any]):
    json_arr = []
    while True:
        element, tokens = parse(tokens)
        json_arr.append(element)
        head = tokens.popleft()
        if head == JSON_RIGHT_BRACKET:
            return json_arr, tokens
        elif head == JSON_COMMA:
            tokens = tokens
        else:
            raise Exception("missed comma in array")


def parse_object(tokens: Deque[Any]) -> (Dict[Any, Any], Deque[Any]):
    json_object = {}

    if tokens[0] == JSON_RIGHT_BRACE:
        tokens.popleft()
        return json_object, tokens

    while True:
        json_key = tokens[0]
        if type(json_key) is str:
            tokens.popleft()
        else:
            raise Exception(f'Expected string key, got: {json_key}')

        if tokens[0] != JSON_COLON:
            raise Exception(f'Expected colon after key in object, got: {tokens[0]}')

        tokens.popleft()
        json_value, tokens = parse(tokens)

        json_object[json_key] = json_value

        t = tokens[0]
        if t == JSON_RIGHT_BRACE:
            tokens.popleft()
            return json_object, tokens
        elif t != JSON_COMMA:
            raise Exception(f'Expected comma after pair in object, got: {t}')

        tokens.popleft()


def parse(tokens: Deque[Any]) -> (Any, Deque[Any]):
    head = tokens.popleft()
    if head == JSON_LEFT_BRACKET:
        return parse_array(tokens)
    elif head == JSON_LEFT_BRACE:
        return parse_object(tokens)
    else:
        return head, tokens
