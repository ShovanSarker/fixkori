from __future__ import absolute_import

from dashboard.views.user_access import AdminIndex
from dashboard.views.user_access import AddAdmin
from dashboard.views.user_access import AddVendor
from dashboard.views.user_access import AddUser
from dashboard.views.user_access import AddItem
from dashboard.views.user_access import AddArea
from dashboard.views.user_access import ListOrder
from dashboard.views.user_access import ListUser
from dashboard.views.user_access import ListVendor
from dashboard.views.user_access import DetailOrder
from dashboard.views.user_access import DetailUser
from dashboard.views.user_access import DetailVendor
from dashboard.views.user_access import OrderManage
from dashboard.views.user_access import Manage
from dashboard.views.user_access import Login
from dashboard.views.user_access import Logout

from dashboard.views.home import Home


__all__ = [
    'AdminIndex',
    'AddAdmin',
    'AddVendor',
    'AddUser',
    'AddItem',
    'AddArea',
    'ListOrder',
    'ListUser',
    'ListVendor',
    'DetailOrder',
    'DetailUser',
    'DetailVendor',
    'OrderManage',
    'Manage',
    'Login',
    'Logout',
    'Home',
]