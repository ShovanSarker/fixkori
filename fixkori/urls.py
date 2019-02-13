"""fixkori URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from django.conf.urls.static import static
from django.conf import settings

from dashboard.views import AdminIndex
from dashboard.views import AddAdmin
from dashboard.views import AddVendor
from dashboard.views import AddUser
from dashboard.views import AddItem
from dashboard.views import ListOrder
from dashboard.views import ListUser
from dashboard.views import ListVendor
from dashboard.views import DetailOrder
from dashboard.views import DetailUser
from dashboard.views import DetailVendor
from dashboard.views import OrderManage
from dashboard.views import Manage
from dashboard.views import AddArea

from dashboard.views import Login
from dashboard.views import Logout
from dashboard.views import Home



urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^admin_index/', view=AdminIndex.as_view(), name='admin_index'),
    url(r'^add_admin/', view=AddAdmin.as_view(), name='add_admin'),
    url(r'^add_vendor/', view=AddVendor.as_view(), name='add_vendor'),
    url(r'^add_user/', view=AddUser.as_view(), name='add_user'),
    url(r'^add_item/', view=AddItem.as_view(), name='add_item'),
    url(r'^add_area/', view=AddArea.as_view(), name='add_area'),
    url(r'^list_order/', view=ListOrder.as_view(), name='list_order'),
    url(r'^list_user/', view=ListUser.as_view(), name='list_user'),
    url(r'^list_vendor/', view=ListVendor.as_view(), name='list_vendor'),
    url(r'^detail_order/', view=DetailOrder.as_view(), name='detail_order'),
    url(r'^detail_user/', view=DetailUser.as_view(), name='detail_user'),
    url(r'^detail_vendor/', view=DetailVendor.as_view(), name='detail_vendor'),
    url(r'^order_manage/', view=OrderManage.as_view(), name='order_manage'),
    url(r'^manage/', view=Manage.as_view(), name='manage'),
    url(r'^login/', view=Login.as_view(), name='login'),
    url(r'^logout/', view=Logout.as_view(), name='logout'),
    url(r'^$', view=Home.as_view(), name='home'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
