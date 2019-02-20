import json
import os
import datetime

from django.views import View
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from django.shortcuts import render, redirect
from django.http import HttpResponse

# import urllib2
from django.urls import reverse

# from consts.request_params import RequestParams
from utility import UUID
from utility import send_now

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash

from utility.session import Session

from fixkori_api.models import UserClient
from fixkori_api.models import UserServiceProvider
from fixkori_api.models import UserAdmin
from fixkori_api.models import Order
from fixkori_api.models import Area
from fixkori_api.models import Item

import constants


class Home(View):

    @staticmethod
    def get(request):
        if 'token' not in request.session:
            return render(request, 'customer/index.html')

        logged_in_user = Session.get_user_by_session(request.session['token'])
        if logged_in_user is None:
            return render(request, 'customer/index.html')

        if logged_in_user.user_type == constants.USER_TYPE_CLIENT:
            logged_in_user_object = UserClient.objects.get(user=logged_in_user)
            return render(request, 'customer/index.html', {'client': True,
                                                           'logged_in_user_object': logged_in_user_object})

        elif logged_in_user.user_type == constants.USER_TYPE_SERVICE_PROVIDER:
            '''service provider'''
            return render(request, 'admin_vendor/vendor_index.html')

        elif logged_in_user.user_type == constants.USER_TYPE_ADMIN:
            '''admin'''
            yesterday = datetime.date.today() - datetime.timedelta(days=1)
            total_order = Order.objects.all().count()
            pending_order = Order.objects.filter(status=constants.ORDER_STATUS_PENDING).count()
            total_user = UserClient.objects.all().count()
            new_users = UserClient.objects.filter(created_at__gt=yesterday).count()
            total_vendor = UserServiceProvider.objects.all().count()
            service_today = Order.objects.filter(status=constants.ORDER_STATUS_COMPLETED,
                                                 last_updated__gt=yesterday).count()
            last_5_orders = Order.objects.filter(status=constants.ORDER_STATUS_PENDING)[:5]
            last_5_users = UserClient.objects.all()[:5]
            last_5_vendors = UserServiceProvider.objects.all()[:5]
            logged_in_user_object = UserAdmin.objects.get(user=logged_in_user)
            return render(request, 'admin_vendor/admin_index.html', {'admin': True,
                                                                     'total_order': total_order,
                                                                     'logged_in_user_object': logged_in_user_object,
                                                                     'pending_order': pending_order,
                                                                     'total_user': total_user,
                                                                     'new_users': new_users,
                                                                     'total_vendor': total_vendor,
                                                                     'service_today': service_today,
                                                                     'last_5_orders': last_5_orders,
                                                                     'last_5_users': last_5_users,
                                                                     'last_5_vendors': last_5_vendors})


class PlaceOrder(View):

    @staticmethod
    @login_required(login_url='/login/')
    def post(request):
        logged_in_user = Session.get_user_by_session(request.session['token'])
        client = UserClient.objects.get(user=logged_in_user)
        area = Area.objects.get(area_name=request.POST['area'])
        item = Item.objects.get(item_name=request.POST['item'])
        new_order = Order(customer=client,
                          area=area,
                          item=item,
                          brand=request.POST['brand'],
                          model=request.POST['model'],
                          service_type=int(request.POST['service_type']),
                          date=request.POST['date'],
                          address=request.POST['address'],
                          instruction=request.POST['instruction'],
                          description=request.POST['description'])
        new_order.save()
        return redirect(reverse('home'))

    @staticmethod
    @login_required(login_url='/login/')
    def get(request):
        logged_in_user = Session.get_user_by_session(request.session['token'])
        client = UserClient.objects.get(user=logged_in_user)
        # todo have to add a order taking page with client info
        return redirect(reverse('home'))


class OrderList(View):

    @staticmethod
    @login_required(login_url='/login/')
    def get(request):
        logged_in_user = Session.get_user_by_session(request.session['token'])
        client = UserClient.objects.get(user=logged_in_user)
        all_orders = Order.objects.filter(customer=client)
        # todo have to add a order taking page with client info and all_order List
        return redirect(reverse('home'))


class OrderDetails(View):

    @staticmethod
    @login_required(login_url='/login/')
    def get(request, oid):
        logged_in_user = Session.get_user_by_session(request.session['token'])
        client = UserClient.objects.get(user=logged_in_user)
        order = Order.objects.get(ok=oid)
        if order.customer == client:
            # send data
            pass
        else:
            # do not send data
            pass
        # todo have to add a order taking page with client info and order details
        return redirect(reverse('home'))


class CancelOrder(View):

    @staticmethod
    @login_required(login_url='/login/')
    def get(request, oid):
        logged_in_user = Session.get_user_by_session(request.session['token'])
        client = UserClient.objects.get(user=logged_in_user)
        order = Order.objects.get(ok=oid)
        if order.customer == client:
            # change order state
            pass
        else:
            # do not change order state
            pass
        # todo have to add a order taking page with client info and order details
        return redirect(reverse('home'))


class UserProfile(View):

    @staticmethod
    @login_required(login_url='/login/')
    def get(request, oid):
        logged_in_user = Session.get_user_by_session(request.session['token'])
        client = UserClient.objects.get(user=logged_in_user)
        # todo have to send user object
        return redirect(reverse('home'))
