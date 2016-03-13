#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
Unit tests for pytracery
"""
from __future__ import print_function, unicode_literals
try:
    import unittest2 as unittest
except ImportError:
    import unittest

import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

import tracery
from tracery.modifiers import base_english


test_grammar = {
    'deepHash': ["\\#00FF00", "\\#FF00FF"],
    'deeperHash': ["#deepHash#"],
    'animal': ["bear", "cat", "dog", "fox", "giraffe", "hippopotamus"],
    'mood': ["quiet", "morose", "gleeful", "happy", "bemused", "clever",
             "jovial", "vexatious", "curious", "anxious", "obtuse", "serene",
             "demure"],
    'nonrecursiveStory': ["The #pet# went to the beach."],
    'recursiveStory': [
        "The #pet# opened a book about[pet:#mood# #animal#] #pet.a#. "
        "#story#[pet:POP] The #pet# closed the book."],
    'svgColor': ["rgb(120,180,120)", "rgb(240,140,40)", "rgb(150,45,55)",
                 "rgb(150,145,125)", "rgb(220,215,195)", "rgb(120,250,190)"],
    'svgStyle': ['style="fill:#svgColor#;stroke-width:3;stroke:#svgColor#"'],
    "name": ["Cheri", "Fox", "Morgana", "Jedoo", "Brick", "Shadow", "Krox",
             "Urga", "Zelph"],
    "story": ["#hero.capitalize# was a great #occupation#, and this song "
              "tells of #heroTheir# adventure. #hero.capitalize# #didStuff#, "
              "then #heroThey# #didStuff#, then #heroThey# went home "
              "to read a book."],
    "monster": ["dragon", "ogre", "witch", "wizard", "goblin", "golem",
                "giant", "sphinx", "warlord"],
    "setPronouns": [
        "[heroThey:they][heroThem:them][heroTheir:their][heroTheirs:theirs]",
        "[heroThey:she][heroThem:her][heroTheir:her][heroTheirs:hers]",
        "[heroThey:he][heroThem:him][heroTheir:his][heroTheirs:his]"],
    "setOccupation": [
        "[occupation:baker][didStuff:baked bread,decorated cupcakes,"
        "folded dough,made croissants,iced a cake]",
        "[occupation:warrior][didStuff:fought #monster.a#,saved a village "
        "from #monster.a#,battled #monster.a#,defeated #monster.a#]"],
    "origin": ["#[#setPronouns#][#setOccupation#][hero:#name#]story#"]
    }


class TestPytracery(unittest.TestCase):
    """Common setUp and helpers"""

    def setUp(self):
        self.grammar = tracery.Grammar(test_grammar)
        self.grammar.add_modifiers(base_english)

    def assert_starts_with(self, a, b, msg=None):
        self.assertTrue(
            a.startswith(b),
            msg or "{0} does not start with {1}".format(a, b))

    def assert_ends_with(self, a, b, msg=None):
        self.assertTrue(
            a.endswith(b),
            msg or "{0} does not end with {1}".format(a, b))


class TestBasics(TestPytracery):

    def test_plaintext_short(self):
        # Arrange
        src = "a"

        # Act
        ret = self.grammar.flatten(src)

        # Assert
        self.assertEqual(ret, "a")
        self.assertEqual(self.grammar.errors, [])

    def test_plaintext_long(self):
        # Arrange
        src = ("Emma Woodhouse, handsome, clever, and rich, with a "
               "comfortable home and happy disposition, seemed to unite some "
               "of the best blessings of existence; and had lived nearly "
               "twenty-one years in the world with very little to distress or "
               "vex her.")

        # Act
        ret = self.grammar.flatten(src)

        # Assert
        self.assertEqual(
            ret,
            "Emma Woodhouse, handsome, clever, and rich, with a "
            "comfortable home and happy disposition, seemed to unite some "
            "of the best blessings of existence; and had lived nearly "
            "twenty-one years in the world with very little to distress or "
            "vex her.")
        self.assertEqual(self.grammar.errors, [])


class TestEscapeChars(TestPytracery):

    def test_escape_character(self):
        # Arrange
        src = "\\#escape hash\\# and escape slash\\\\"

        # Act
        ret = self.grammar.flatten(src)

        # Assert
        self.assertEqual(ret, "#escape hash# and escape slash\\")
        self.assertEqual(self.grammar.errors, [])

    def test_escape_deep(self):
        # Arrange
        src = "#deepHash# [myColor:#deeperHash#] #myColor#"

        # Act
        ret = self.grammar.flatten(src)

        # Assert
        self.assertIn(
            ret,
            ["#00FF00  #00FF00",
             "#00FF00  #FF00FF",
             "#FF00FF  #00FF00",
             "#FF00FF  #FF00FF"])
        self.assertEqual(self.grammar.errors, [])

    def test_escape_quotes(self):
        # Arrange
        src = "\"test\" and \'test\'"

        # Act
        ret = self.grammar.flatten(src)

        # Assert
        self.assertEqual(ret, "\"test\" and 'test'")
        self.assertEqual(self.grammar.errors, [])

    def test_escape_brackets(self):
        # Arrange
        src = "\\[\\]"

        # Act
        ret = self.grammar.flatten(src)

        # Assert
        self.assertEqual(ret, "[]")
        self.assertEqual(self.grammar.errors, [])

    def test_escape_hash(self):
        # Arrange
        src = "\\#"

        # Act
        ret = self.grammar.flatten(src)

        # Assert
        self.assertEqual(ret, "#")
        self.assertEqual(self.grammar.errors, [])

    def test_unescape_char_slash(self):
        # Arrange
        src = "\\\\"

        # Act
        ret = self.grammar.flatten(src)

        # Assert
        self.assertEqual(ret, "\\")
        self.assertEqual(self.grammar.errors, [])

    def test_escape_melange1(self):
        # Arrange
        src = "An action can have inner tags: \[key:\#rule\#\]"

        # Act
        ret = self.grammar.flatten(src)

        # Assert
        self.assertEqual(ret, "An action can have inner tags: [key:#rule#]")
        self.assertEqual(self.grammar.errors, [])

    def test_escape_melange2(self):
        # Arrange
        src = ("A tag can have inner actions: "
               "\"\\#\\[myName:\\#name\\#\\]story\\[myName:POP\\]\\#\"")

        # Act
        ret = self.grammar.flatten(src)

        # Assert
        self.assertEqual(
            ret,
            "A tag can have inner actions: "
            "\"#[myName:#name#]story[myName:POP]#\"")
        self.assertEqual(self.grammar.errors, [])


class TestWebSpecifics(TestPytracery):

    def test_emoji(self):
        # Arrange
        src = "💻🐋🌙🏄🍻"

        # Act
        ret = self.grammar.flatten(src)

        # Assert
        self.assertEqual(
            ret,
            "\U0001f4bb\U0001f40b\U0001f319\U0001f3c4\U0001f37b")
        self.assertEqual(self.grammar.errors, [])

    def test_unicode(self):
        # Arrange
        src = "&\\#x2665; &\\#x2614; &\\#9749; &\\#x2665;"

        # Act
        ret = self.grammar.flatten(src)

        # Assert
        self.assertEqual(ret, "&#x2665; &#x2614; &#9749; &#x2665;")
        self.assertEqual(self.grammar.errors, [])

    def test_svg(self):
        # Arrange
        src = ('<svg width="100" height="70">'
               '<rect x="0" y="0" width="100" height="100" #svgStyle#/> '
               '<rect x="20" y="10" width="40" height="30" #svgStyle#/>'
               '</svg>')

        # Act
        ret = self.grammar.flatten(src)

        # Assert
        self.assert_starts_with(
            ret,
            '<svg width="100" height="70">'
            '<rect x="0" y="0" width="100" height="100" style="fill:rgb(')
        self.assertIn('/> <rect x="20" y="10" width="40" height="30" ', ret)
        self.assert_ends_with(ret, '"/></svg>')
        self.assertEqual(self.grammar.errors, [])


class TestPush(TestPytracery):

    def test_push_basic(self):
        # Arrange
        src = "[pet:#animal#]You have a #pet#. Your #pet# is #mood#."

        # Act
        ret = self.grammar.flatten(src)

        # Assert
        self.assert_starts_with(ret, "You have a ")
        self.assertIn(". Your ", ret)
        self.assert_ends_with(ret, ".")
        self.assertEqual(self.grammar.errors, [])

    def test_push_pop(self):
        # Arrange
        src = ("[pet:#animal#]You have a #pet#. [pet:#animal#]Pet:#pet# "
               "[pet:POP]Pet:#pet#")

        # Act
        ret = self.grammar.flatten(src)

        # Assert
        self.assert_starts_with(ret, "You have a ")
        self.assertIn(". Pet:", ret)
        self.assertEqual(self.grammar.errors, [])

    def test_tag_action(self):
        # Arrange
        src = "#[pet:#animal#]nonrecursiveStory# post:#pet#"

        # Act
        ret = self.grammar.flatten(src)

        # Assert
        self.assert_starts_with(ret, "The ")
        self.assertIn(" went to the beach. post:", ret)
        self.assertEqual(self.grammar.errors, [])

    def test_test_complex_grammar(self):
        # Arrange
        src = "#origin#"

        # Act
        ret = self.grammar.flatten(src)

        # Assert
        self.assertIn(", and this song tells of ", ret)
        self.assertEqual(self.grammar.errors, [])

    def test_missing_modifier(self):
        # Arrange
        src = "#animal.foo#"

        # Act
        ret = self.grammar.flatten(src)

        # Assert
        self.assert_ends_with(ret, "((.foo))")
        self.assertEqual(self.grammar.errors, [])

    def test_modifier_with_params(self):
        # Arrange
        src = ("[pet:#animal#]#nonrecursiveStory# -> #nonrecursiveStory"
               ".replace(beach,mall)#")

        # Act
        ret = self.grammar.flatten(src)

        # Assert
        self.assertIn(" went to the beach. -> ", ret)
        self.assert_ends_with(ret, " went to the mall.")
        self.assertEqual(self.grammar.errors, [])

    def test_recursive_push(self):
        # Arrange
        src = "[pet:#animal#]#recursiveStory#"

        # Act
        ret = self.grammar.flatten(src)

        # Assert
        self.assertIn(" opened a book about a", ret)
        self.assert_ends_with(ret, " closed the book.")
        self.assertEqual(self.grammar.errors, [])


class TestErrors(TestPytracery):

    def test_plaintext_short(self):
        # Arrange
        src = "a"

        # Act
        ret = self.grammar.flatten(src)

        # Assert
        self.assertEqual(ret, "a")
        self.assertEqual(self.grammar.errors, [])

    def test_unmatched_hash(self):
        # Arrange
        src = "#unmatched"

        # Act
        ret = self.grammar.flatten(src)

        # Assert
        self.assertEqual(ret, "unmatched")
        self.assertEqual(self.grammar.errors, ["unclosed tag"])

    def test_missing_symbol(self):
        # Arrange
        src = "#unicorns#"

        # Act
        ret = self.grammar.flatten(src)

        # Assert
        self.assertEqual(ret, "((unicorns))")
        self.assertEqual(self.grammar.errors, [])

    def test_missing_right_bracket(self):
        # Arrange
        src = "[pet:unicorn"

        # Act
        ret = self.grammar.flatten(src)

        # Assert
        self.assertEqual(ret, "pet:unicorn")
        self.assertEqual(self.grammar.errors, ["too many ["])

    def test_missing_left_bracket(self):
        # Arrange
        src = "pet:unicorn]"

        # Act
        ret = self.grammar.flatten(src)

        # Assert
        self.assertEqual(ret, "pet:unicorn]")
        self.assertEqual(self.grammar.errors, ["too many ]"])

    def test_just_a_lot_of_brackets(self):
        # Arrange
        src = "[][]][][][[[]]][[]]]]"

        # Act
        ret = self.grammar.flatten(src)

        # Assert
        self.assertEqual(ret, "][][][][]]]")
        self.assertEqual(
            self.grammar.errors,
            ["1: empty action", "1: empty action", "3: empty action",
             "17: empty action", "too many ]"])

    def test_bracket_tag_melange(self):
        # Arrange
        src = "[][#]][][##][[[##]]][#[]]]]"

        # Act
        ret = self.grammar.flatten(src)

        # Assert
        self.assertEqual(ret, "][][((None))][][[]]]]")
        self.assertEqual(
            self.grammar.errors,
            ["unclosed tag", "1: empty tag", "1: empty action",
             "10: empty tag", "unclosed tag", "too many ]"])


if __name__ == "__main__":
    unittest.main()

# End of file
