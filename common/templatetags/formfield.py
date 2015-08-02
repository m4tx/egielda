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

from django import template
from django.template import loader
from django.template import Context
from django.template.base import TagHelperNode
from django.utils.translation import ugettext as _

from utils.tags import parse_args

register = template.Library()


@register.tag
def formfield(parser, token):
    """
    {% formfield %} tag simplifies custom form creating. Removes the need of use boilerplate code
    for each form field, including 'common/form_field.html' template instead.

    It has three keyword arguments:
    * id (optional) - id of the input for the label to point to
    * label - label text in English (it is wrapped by ugettext function, therefore localizing it
    before displaying)
    * has_errors (optional) - whether or not the value provided by user is incorrect
    """
    args, kwargs = parse_args(parser, token, (),
                              kwargs=('id', 'label', 'has_errors'),
                              defaults_kwargs=(None, None, False))
    nodelist = parser.parse(('endformfield',))
    parser.delete_first_token()
    return FormfieldNode(nodelist, kwargs)


class FormfieldNode(TagHelperNode):
    def __init__(self, nodelist, kwargs):
        self.nodelist = nodelist
        super(FormfieldNode, self).__init__(False, [], kwargs)

    def render(self, context):
        output = self.nodelist.render(context)
        args, kwargs = self.get_resolved_arguments(context)

        t = loader.get_template('common/form_field.html')
        return t.render(Context({
            'id': kwargs.get('id', None),
            'label': kwargs['label'],
            'has_errors': kwargs.get('has_errors', False),
            'field': output
        }))
