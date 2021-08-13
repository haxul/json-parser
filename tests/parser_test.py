import unittest
from parser import *
from lexer import *


class ParserTest(unittest.TestCase):

    def test_from_string(self):
        self.assertDictEqual(from_string('{"foo": 1}'), {"foo": 1})


class LexerTest(unittest.TestCase):

    def test_lex(self):
        self.assertEqual(lex('{"foo": [1, 2, {"bar": 2}]}'),
                         ['{', 'foo', ':', '[', 1, ',', 2, ',', '{', 'bar', ':', 2, '}', ']', '}'])

    def test_lex_string(self):
        self.assertEqual(lex_string('"foo"'), ("foo", ""))

    def test_lex_string_when_redundant_quote(self):
        self.assertEqual(lex_string('"foo"barr"'), ("foo", 'barr"'))

    def test_lex_number(self):
        self.assertEqual(lex_number("123"), (123, ""))

    def test_lex_number_wrong_format(self):
        self.assertEqual(lex_number("12sd9"), (12, "sd9"))

    def test_lex_number_float(self):
        self.assertEqual(lex_number("1.10"), (1.10, ""))

    def test_lex_number_float_wrong_format(self):
        self.assertEqual(lex_number("1.10ad1.11"), (1.10, "ad1.11"))

    def test_lex_number_float_wrong_format2(self):
        self.assertEqual(lex_number("1.101.11"), (1.101, ".11"))

    def test_lex_boolean_false(self):
        self.assertEqual(lex_bool('false'), (False, ""))

    def test_lex_boolean_true(self):
        self.assertEqual(lex_bool('true'), (True, ""))

    def test_lex_boolean_true_wrong(self):
        self.assertEqual(lex_bool('wrong'), (None, "wrong"))

    def test_lex_boolean_wrong(self):
        self.assertEqual(lex_bool('wrong'), (None, "wrong"))

    def test_lex_boolean_double(self):
        self.assertEqual(lex_bool('truetrue'), (True, "true"))

    def test_lex_null(self):
        self.assertEqual(lex_null('null'), (True, ""))

    def test_lex_null_wrong(self):
        self.assertEqual(lex_null('nulladf'), (True, "adf"))
