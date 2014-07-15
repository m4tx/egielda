from django import template
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

import books
import categories
import managemenu
import settings
import users


register = template.Library()


@register.tag(name="manage_header")
def do_manage_header(parser, token):
    contents = token.split_contents()
    tag_name = contents[0]
    path = contents[1] if len(contents) == 2 else '""'

    if not (len(contents) == 1 or len(contents) == 2):
        raise template.TemplateSyntaxError("%r tag requires zero or one argument" % token.contents.split()[0])
    if not (path[0] == path[-1] and path[0] in ('"', "'")):
        raise template.TemplateSyntaxError("%r tag's argument should be in quotes" % tag_name)
    return ManageHeaderNode(path[1:-1])


class ManageHeaderNode(template.Node):
    def __init__(self, path):
        self.path = path

    def render(self, context):
        # Manage pages tree
        # Each item is a list of following: [view class, (display) name, (optional) children]
        tree = [managemenu.views.index, _("Manage"), {
            'categories': [categories.views.index, _("Categories"), {
                'add': [categories.views.add_category, _("Add new")],
                'edit': [categories.views.edit_category, _("Edit")],
                'remove': [categories.views.remove_category, _("Remove")],
                'list': [categories.views.list_books, _("Book list")],
            }],
            'books': [books.views.index, _("Books"), {
                'add': [books.views.add_book, _("Add new")],
                'edit': [books.views.edit_book, _("Edit")],
                'remove': [books.views.remove_book, _("Remove")],
            }],
            'users': [users.views.index, _("Users"), {
                'unaccepted': [users.views.unaccepted, _("With unaccepted books")],
                'list_books': [users.views.list_books, _("User's books")],
                'accept_books': [users.views.accept_books, _("Accept user's books")],
            }],
            'settings': [settings.views.index, _("Settings"), {
                'dates': [settings.views.dates, _("Dates")],
            }]
        }]

        # Split the path
        split = self.path.split("/")
        if len(split) == 1 and split[0] == "":
            split = []

        # Iterate through the items in path and add the items from the tree to the temporary list
        nodes = [tree]
        parent = tree
        for node in split:
            parent = parent[2][node]
            nodes.append(parent)

        # Generate HTML
        result = "<ol class=\"breadcrumb\">"
        for node in nodes[:-1]:
            result += "<li><a href=\"%s\">%s</a></li>" % (reverse(node[0]), str(node[1]))
        result += "<li class=\"active\">%s</li>" % str(nodes[-1][1])
        result += "</ol>"

        return result