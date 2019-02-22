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
from dashboard.views import PlaceOrder

from dashboard.views import CustomerDashboard
from dashboard.views import CustomerServiceList
from dashboard.views import CustomerServiceDetail
from dashboard.views import CustomerProfile

from dashboard.views import OrderLogin
from dashboard.views import NewOrder
from dashboard.views import OrderElectronic
from dashboard.views import OrderVehicle

from dashboard.views import Login
from dashboard.views import Logout
from dashboard.views import Home
from dashboard.views import Register
from dashboard.views import ChangePassword



urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', view=Home.as_view(), name='home'),
    url(r'^add_admin/', view=AddAdmin.as_view(), name='add_admin'),
    url(r'^add_vendor/', view=AddVendor.as_view(), name='add_vendor'),
    url(r'^add_user/', view=AddUser.as_view(), name='add_user'),
    url(r'^list_vendor/', view=ListVendor.as_view(), name='list_vendor'),
    url(r'^list_user/', view=ListUser.as_view(), name='list_user'),
    url(r'^detail_vendor/(?P<vendor_id>[0-9]+)/', view=DetailVendor.as_view(), name='detail_vendor'),
    url(r'^detail_user/(?P<client_id>[0-9]+)/', view=DetailUser.as_view(), name='detail_user'),

    url(r'^place_order/', view=PlaceOrder.as_view(), name='place_order'),
    url(r'^register/', view=Register.as_view(), name='register'),
    url(r'^change_password/', view=ChangePassword.as_view(), name='change_password'),

    url(r'^admin_index/', view=AdminIndex.as_view(), name='admin_index'),
    url(r'^list_order/', view=ListOrder.as_view(), name='list_order'),
    url(r'^add_item/', view=AddItem.as_view(), name='add_item'),
    url(r'^add_area/', view=AddArea.as_view(), name='add_area'),
    url(r'^detail_order/(?P<order_id>[0-9]+)/', view=DetailOrder.as_view(), name='detail_order'),
    url(r'^order_manage/', view=OrderManage.as_view(), name='order_manage'),
    url(r'^manage/', view=Manage.as_view(), name='manage'),
    url(r'^user/', view=CustomerDashboard.as_view(), name='user'),
    url(r'^service_list/', view=CustomerServiceList.as_view(), name='service_list'),
    url(r'^service_detail/(?P<order_id>[0-9]+)/', view=CustomerServiceDetail.as_view(), name='service_detail'),
    url(r'^profile/', view=CustomerProfile.as_view(), name='profile'),
    url(r'^order_login/', view=OrderLogin.as_view(), name='order_login'),
    url(r'^order/', view=NewOrder.as_view(), name='order'),
    url(r'^electronic/', view=OrderElectronic.as_view(), name='electronic'),
    url(r'^vehicle/', view=OrderVehicle.as_view(), name='vehicle'),
    url(r'^login/', view=Login.as_view(), name='login'),
    url(r'^logout/', view=Logout.as_view(), name='logout'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
