# This file is part of e-Giełda.
# Copyright (C) 2014-2015  Mateusz Maćkowski and Tomasz Zieliński
#
# e-Giełda is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# You should have received a copy of the GNU Affero General Public License
# along with e-Giełda.  If not, see <http://www.gnu.org/licenses/>.

from unittest import TestCase

from utils.isbn import is_isbn_valid, calc_isbn10_check_digit, calc_isbn13_check_digit


class IsbnTest(TestCase):
    def test_invalid_isbns(self):
        self.assertFalse(is_isbn_valid("test"))
        self.assertFalse(is_isbn_valid("9780262033847"))  # Invalid check digit
        self.assertFalse(is_isbn_valid("978026203384"))  # Invalid length
        self.assertFalse(is_isbn_valid("8275920185972"))  # Random, 13 digits
        self.assertFalse(is_isbn_valid("2752191620222"))  # Random, 13 digits
        self.assertFalse(is_isbn_valid("912841757X"))  # Random, 10 characters
        self.assertFalse(is_isbn_valid("8219257110"))  # Random, 10 characters

    def test_isbn10(self):
        self.assertTrue(is_isbn_valid("0306406152"))
        self.assertEqual(calc_isbn10_check_digit("0306406152"), 2)

        self.assertTrue(is_isbn_valid("1459245830"))
        self.assertTrue(is_isbn_valid("8375059013"))
        self.assertTrue(is_isbn_valid("839353612X"))

    def test_isbn13(self):
        self.assertTrue(is_isbn_valid("9780262033848"))
        self.assertEqual(calc_isbn13_check_digit("9780262033848"), 8)

        self.assertTrue(is_isbn_valid("9781459245839"))
        self.assertTrue(is_isbn_valid("9788375059014"))
        self.assertTrue(is_isbn_valid("9788393536122"))