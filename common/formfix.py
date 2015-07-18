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

"""
Fixes some issues in forms:
* adds required="required" attribute wherever required is set to True in form field
* adds "form-control" class so fields look nicely with Bootstrap
"""

from django.forms import Field

old_widget_attrs = Field.widget_attrs


def new_widget_attrs(self, widget):
    attrs = old_widget_attrs(self, widget)
    if self.required:
        attrs.update({'required': 'required'})

    if 'class' in attrs:
        attrs['class'] += ' form-control'
    else:
        attrs.update({'class': 'form-control'})
    return attrs


Field.widget_attrs = new_widget_attrs