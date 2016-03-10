#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
Unit tests for pytracery
"""
from __future__ import print_function
try:
    import unittest2 as unittest
except ImportError:
    import unittest

import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from tracery import modifiers


class TestModifiers(unittest.TestCase):

    def test_replace(self):
        # Arrange
        input = "a big ship"

        # Act
        output = modifiers.replace(input, "ship", "shop")

        # Assert
        self.assertEqual(output, "a big shop")

    def test_capitalize_all(self):
        # Arrange
        input = "abc def"

        # Act
        output = modifiers.capitalizeAll(input)

        # Assert
        self.assertEqual(output, "Abc Def")

    def test_capitalize_(self):
        # Arrange
        input = "abc def"

        # Act
        output = modifiers.capitalize_(input)

        # Assert
        self.assertEqual(output, "Abc def")

    def test_a_consonant(self):
        # Arrange
        input = "house"

        # Act
        output = modifiers.a(input)

        # Assert
        self.assertEqual(output, "a house")

    def test_a_u_something_i(self):
        # Arrange
        input = "unicorn"

        # Act
        output = modifiers.a(input)

        # Assert
        self.assertEqual(output, "a unicorn")

    def test_a_u_not_i(self):
        # Arrange
        input = "underdog"

        # Act
        output = modifiers.a(input)

        # Assert
        self.assertEqual(output, "an underdog")

    def test_a_vowel(self):
        # Arrange
        input = "elephant"

        # Act
        output = modifiers.a(input)

        # Assert
        self.assertEqual(output, "an elephant")

    def test_first_s(self):
        # Arrange
        input = "elephant in a phonebox"

        # Act
        output = modifiers.firstS(input)

        # Assert
        self.assertEqual(output, "elephants in a phonebox")

    def test_s_ends_in_x(self):
        # Arrange
        input = "box"

        # Act
        output = modifiers.s(input)

        # Assert
        self.assertEqual(output, "boxes")

    def test_s_ends_in_non_s(self):
        # Arrange
        input = "goat"

        # Act
        output = modifiers.s(input)

        # Assert
        self.assertEqual(output, "goats")

    def test_s_ends_in_vowel_y(self):
        # Arrange
        input = "monkey"

        # Act
        output = modifiers.s(input)

        # Assert
        self.assertEqual(output, "monkeys")

    def test_s_ends_in_y_but_not_vowel_y(self):
        # Arrange
        input = "telly"

        # Act
        output = modifiers.s(input)

        # Assert
        self.assertEqual(output, "tellies")

    def test_ed_ends_in_e(self):
        # Arrange
        input = "glide"

        # Act
        output = modifiers.ed(input)

        # Assert
        self.assertEqual(output, "glided")

    def test_ed_ends_in_y_but_not_vowel_y(self):
        # Arrange
        input = "shimmy"

        # Act
        output = modifiers.ed(input)

        # Assert
        self.assertEqual(output, "shimmied")

    def test_ed_ends_in_non_e_and_non_y(self):
        # Arrange
        input = "jump"

        # Act
        output = modifiers.ed(input)

        # Assert
        self.assertEqual(output, "jumped")


if __name__ == "__main__":
    unittest.main()

# End of file
