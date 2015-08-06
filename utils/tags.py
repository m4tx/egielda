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

from django.template.base import parse_bits


def parse_args(parser, token, args, kwargs, defaults_args=(), defaults_kwargs=()):
    """
    Parses the arguments passed to the tag. Returns tuple with args and kwargs, where
    in both cases the values are stored as FilterExpressions.

    Please note that providing default_args, default_kwargs or both does not mean that
    kwargs[<optional-arg>] will always work. The argument only prevents the parser from
    complaining about arguments being not passed.

    :param parser: TokenParser to use
    :param token: token to parse
    :param args: list of positional arguments
    :param kwargs: list of keyword arguments
    :param defaults_args: default values for the arguments
    :param defaults_kwargs: default values for the keyword arguments
    :return: args, kwargs tuple with parsed arguments
    """
    bits = token.split_contents()
    params = args + kwargs
    return parse_bits(parser, bits[1:], params, args, kwargs, defaults_args + defaults_kwargs,
                      False, bits[0])
