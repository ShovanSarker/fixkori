from __future__ import absolute_import

from dashboard.views.user_access import AddAdmin
from dashboard.views.user_access import AddVendor
from dashboard.views.user_access import AddUser
from dashboard.views.user_access import AddItem
from dashboard.views.user_access import AddArea
from dashboard.views.user_access import Login
from dashboard.views.user_access import Logout

from dashboard.views.home import Home


__all__ = [
    'AddAdmin',
    'AddVendor',
    'AddUser',
    'AddItem',
    'AddArea',
    'Login',
    'Logout',
    'Home',
]
