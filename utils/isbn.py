# This file is part of e-Giełda.
# Copyright (C) 2014  Mateusz Maćkowski and Tomasz Zieliński
#
# e-Giełda is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# You should have received a copy of the GNU Affero General Public License
# along with e-Giełda.  If not, see <http://www.gnu.org/licenses/>.


def is_isbn_valid(isbn: str):
    """
    Checks whether the ISBN is correct.

    It checks the following things:
    * whether the ISBN is 10 or 13 characters long
    * whether it only contains digits (or digits and 'X' at the end in case of ISBN10)
    * check digit

    :param isbn: the ISBN to check
    :return: ``True`` if the ISBN is valid; ``False`` otherwise
    """
    isbn = ''.join(filter(lambda c: c != '-', isbn))

    if len(isbn) == 10:
        if not isbn[:-1].isdigit() or not (isbn[-1].isdigit() or isbn[-1] == 'X'):
            return False
        check_digit = str(calc_isbn10_check_digit(isbn))
        if isbn[-1] != check_digit:
            return False
    elif len(isbn) == 13:
        check_digit = str(calc_isbn13_check_digit(isbn))
        if isbn[-1] != check_digit:
            return False
    else:
        return False
    return True


def calc_isbn10_check_digit(isbn: str):
    """
    Calculates the check digit for the passed ISBN.
    :param isbn: the ISBN to calculate the check digit from
    :return: calculated check digit
    """
    return _calc_isbn10_check_digit(tuple(int(i) if i != 'X' else 'X' for i in isbn))


def _calc_isbn10_check_digit(isbn):
    tmp = 0
    for i in range(0, 9):
        tmp += (i + 1) * isbn[i]
    tmp %= 11
    return "X" if tmp == 10 else tmp


def calc_isbn13_check_digit(isbn: str):
    """
    Calculates the check digit for the passed ISBN.
    :param isbn: the ISBN to calculate the check digit from
    :return: calculated check digit
    """
    return _calc_isbn13_check_digit(tuple(int(i) for i in isbn))


def _calc_isbn13_check_digit(isbn):
    tmp = 0
    for i in range(0, 12, 2):
        tmp += isbn[i]
    for i in range(1, 12, 2):
        tmp += 3 * isbn[i]
    return (10 - tmp % 10) % 10