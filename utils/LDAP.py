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

import datetime
from ldap3 import Server, Connection, SUBTREE
from egielda import settings


def check_user_existence(user):
    server = Server(settings.LDAP_SERVER_URL)
    conn = Connection(server, user=settings.LDAP_USERNAME, password=settings.LDAP_PASS)
    conn.open()
    if not conn.bind():
        return False

    month = datetime.datetime.now().month
    year = datetime.datetime.now().year
    if 1 <= month <= 6:
        year -= 1

    user_year = year - (int(user.student_class[:1])-1)

    path = settings.LDAP_SEARCH_USER_PATH.format(
        full_name=user.get_short_name(),
        class_letter=user.student_class[1:2],
        year=user_year
    )
    if conn.search(path, '(objectClass=*)', SUBTREE):
        return True

    return False
