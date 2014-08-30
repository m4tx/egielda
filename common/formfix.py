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

"""
Adds required="required" attribute wherever required is set to True in form field.
"""

from django.forms import Field

old_widget_attrs = Field.widget_attrs


def new_widget_attrs(self, widget):
    attrs = old_widget_attrs(self, widget)
    if self.required:
        attrs.update({'required': 'required'})
    return attrs


Field.widget_attrs = new_widget_attrs