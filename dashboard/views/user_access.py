from __future__ import print_function
from django.views import View

from django.shortcuts import render, redirect, HttpResponse
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

from django.urls import reverse


from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash

from utility.session import Session

from fixkori_api.models import Item
from fixkori_api.models import Area
from fixkori_api.models import UserList
from fixkori_api.models import UserAdmin
from fixkori_api.models import UserClient
from fixkori_api.models import UserServiceProvider
from fixkori_api.models import UserServiceProviderArea
from fixkori_api.models import UserServiceProviderItem
from fixkori_api.models import Order

from utility import UUID
from utility import RandomPassword
from utility import send_now
import constants


class AdminIndex(View):
    @staticmethod
    def get(request):
        return render(request, 'admin_vendor/admin_index.html')


class AddArea(View):
    @staticmethod
    def get(request):
        # new_area = Area(area_name=request.GET['area_name'],
        #                 district=request.GET['district'],
        #                 division=request.GET['division'])
        # new_area.save()
        return render(request, 'admin_vendor/add_area.html')


class AddItem(View):
    @staticmethod
    def get(request):
        # new_item = Item(item_name=request.GET['item_name'],
        #                 service_type=request.GET['service_type'])
        # new_item.save()
        return render(request, 'admin_vendor/add_item.html')


class AddAdmin(View):
    @staticmethod
    def post(request):
        if 'token' not in request.session:
            return render(request, 'customer/index.html')
        logged_in_user = Session.get_user_by_session(request.session['token'])
        if logged_in_user is None:
            return render(request, 'customer/index.html')

        if logged_in_user.user_type == constants.USER_TYPE_ADMIN:
            '''admin'''
            logged_in_user_object = UserAdmin.objects.get(user=logged_in_user)

            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            user_name = request.POST['user_name']
            phone_number = request.POST['phone_number']
            user_email = request.POST['user_email']
            password = request.POST['password']
            if is_new_user(user_name, phone_number, user_email):
                hash_key = UUID.uuid_generator()
                add_to_login_list(hash_key, user_email, password)
                listed_user = add_to_user_list(user_name, phone_number, user_email, hash_key, constants.USER_TYPE_ADMIN)
                new_user = UserAdmin(user=listed_user,
                                     first_name=first_name,
                                     last_name=last_name,
                                     phone_number=phone_number,
                                     user_email=user_email)
                new_user.save()
                return render(request, 'admin_vendor/add_admin.html',
                              {'success': True,
                               'admin': True,
                               'logged_in_user_object': logged_in_user_object,
                               'message': 'Successfully Added!'})
            else:
                return render(request, 'admin_vendor/add_admin.html',
                              {'alert': True,
                               'admin': True,
                               'logged_in_user_object': logged_in_user_object,
                               'message': 'User Already Registered!'})
        else:
            return render(request, 'customer/index.html')

    @staticmethod
    def get(request):
        if 'token' not in request.session:
            return render(request, 'customer/index.html')
        logged_in_user = Session.get_user_by_session(request.session['token'])
        if logged_in_user is None:
            return render(request, 'customer/index.html')

        if logged_in_user.user_type == constants.USER_TYPE_ADMIN:
            '''admin'''
            logged_in_user_object = UserAdmin.objects.get(user=logged_in_user)
            return render(request, 'admin_vendor/add_admin.html', {'admin': True,
                                                                   'logged_in_user_object': logged_in_user_object})
        else:
            return render(request, 'customer/index.html')


class AddFirstAdmin(View):

    @staticmethod
    def get(request):
        first_name = 'Fixkori'
        last_name = 'Admin'
        user_name = 'fixkori_admin'
        phone_number = '00000000000'
        user_email = 'admin@fixkori.com'
        password = 'abcd1234'
        if is_new_user(user_name, phone_number, user_email):
            hash_key = UUID.uuid_generator()
            add_to_login_list(hash_key, user_email, password)
            listed_user = add_to_user_list(user_name, phone_number, user_email, hash_key, constants.USER_TYPE_ADMIN)
            new_user = UserAdmin(user=listed_user,
                                 first_name=first_name,
                                 last_name=last_name,
                                 phone_number=phone_number,
                                 user_email=user_email)
            new_user.save()
            return HttpResponse('Admin Successfully Added!')
        else:
            return HttpResponse('Stop Kidding me!')


class AddUser(View):
    @staticmethod
    def post(request):
        if 'token' not in request.session:
            return render(request, 'customer/index.html')
        logged_in_user = Session.get_user_by_session(request.session['token'])
        if logged_in_user is None:
            return render(request, 'customer/index.html')

        if logged_in_user.user_type == constants.USER_TYPE_ADMIN:
            '''admin'''
            logged_in_user_object = UserAdmin.objects.get(user=logged_in_user)

            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            user_name = None
            phone_number = request.POST['phone_number']
            user_email = request.POST['user_email']
            address = request.POST['address']
            password = 'abcd1234'
            if is_new_user(user_name, phone_number, user_email):
                hash_key = UUID.uuid_generator()
                add_to_login_list(hash_key, user_email, password)
                listed_user = add_to_user_list(user_name, phone_number, user_email, hash_key,
                                               constants.USER_TYPE_CLIENT)
                new_user = UserClient(user=listed_user,
                                      first_name=first_name,
                                      last_name=last_name,
                                      phone_number=phone_number,
                                      address=address,
                                      user_email=user_email)
                new_user.save()
                return render(request, 'admin_vendor/add_user.html',
                              {'success': True,
                               'admin': True,
                               'logged_in_user_object': logged_in_user_object,
                               'message': 'Successfully Added!'})
            else:
                return render(request, 'admin_vendor/add_user.html',
                              {'alert': True,
                               'admin': True,
                               'logged_in_user_object': logged_in_user_object,
                               'message': 'User Already Registered!'})
        else:
            return render(request, 'customer/index.html')

    @staticmethod
    def get(request):
        if 'token' not in request.session:
            return render(request, 'customer/index.html')
        logged_in_user = Session.get_user_by_session(request.session['token'])
        if logged_in_user is None:
            return render(request, 'customer/index.html')

        if logged_in_user.user_type == constants.USER_TYPE_ADMIN:
            '''admin'''
            logged_in_user_object = UserAdmin.objects.get(user=logged_in_user)
            return render(request, 'admin_vendor/add_user.html', {'admin': True,
                                                                  'logged_in_user_object': logged_in_user_object})
        else:
            return render(request, 'customer/index.html')


class AddVendor(View):
    @staticmethod
    def post(request):
        if 'token' not in request.session:
            return render(request, 'customer/index.html')
        logged_in_user = Session.get_user_by_session(request.session['token'])
        if logged_in_user is None:
            return render(request, 'customer/index.html')

        if logged_in_user.user_type == constants.USER_TYPE_ADMIN:
            '''admin'''
            logged_in_user_object = UserAdmin.objects.get(user=logged_in_user)
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            user_name = request.POST['user_name']
            phone_number = request.POST['phone_number']
            email = request.POST['email']
            address = request.POST['address']
            service_point_name = request.POST['service_point_name']
            image_1 = request.FILES['image_1']
            image_2 = request.FILES['image_2']
            image_3 = request.FILES['image_3']
            image_4 = request.FILES['image_4']
            image_5 = request.FILES['image_5']
            about = request.POST['about']
            services = request.POST['services']
            facebook_url = request.POST['facebook_url']
            google_map_url = request.POST['google_map_url']

            password = 'abcd1234'
            all_items = Item.objects.filter(active=True)
            all_areas = Area.objects.filter(active=True).order_by('area_name').reverse()
            # todo have to add random number and send it to user via SMS
            if is_new_user(user_name, phone_number, email):
                hash_key = UUID.uuid_generator()
                add_to_login_list(hash_key, email, password)
                listed_user = add_to_user_list(user_name, phone_number, email,
                                               hash_key, constants.USER_TYPE_SERVICE_PROVIDER)
                new_user = UserServiceProvider(user=listed_user,
                                               first_name=first_name,
                                               last_name=last_name,
                                               address=address,
                                               phone_number=phone_number,
                                               service_point_name=service_point_name,
                                               image_1=image_1,
                                               image_2=image_2,
                                               image_3=image_3,
                                               image_4=image_4,
                                               image_5=image_5,
                                               about=about,
                                               services=services,
                                               facebook_url=facebook_url,
                                               google_map_url=google_map_url,
                                               email=email)
                new_user.save()
                areas = request.POST.getlist('area')
                items = request.POST.getlist('item')
                for area in areas:
                    selected_area = Area.objects.get(id=area)
                    new_assigned_area = UserServiceProviderArea(user=new_user,
                                                                area=selected_area)
                    new_assigned_area.save()

                for item in items:
                    selected_item = Item.objects.get(id=item)
                    new_assigned_item = UserServiceProviderItem(user=new_user,
                                                                item=selected_item)
                    new_assigned_item.save()

                return render(request, 'admin_vendor/add_vendor.html',
                              {'admin': True,
                               'success': True,
                               'message': 'Successfully Added!',
                               'all_areas': all_areas,
                               'all_items': all_items,
                               'logged_in_user_object': logged_in_user_object})
            else:
                return render(request, 'admin_vendor/add_vendor.html',
                              {'admin': True,
                               'alert': True,
                               'message': 'User Already Registered!',
                               'all_areas': all_areas,
                               'all_items': all_items,
                               'logged_in_user_object': logged_in_user_object})

    @staticmethod
    def get(request):
        if 'token' not in request.session:
            return render(request, 'customer/index.html')
        logged_in_user = Session.get_user_by_session(request.session['token'])
        if logged_in_user is None:
            return render(request, 'customer/index.html')

        if logged_in_user.user_type == constants.USER_TYPE_ADMIN:
            '''admin'''
            logged_in_user_object = UserAdmin.objects.get(user=logged_in_user)
            all_items = Item.objects.filter(active=True)
            all_areas = Area.objects.filter(active=True).order_by('area_name')
            return render(request, 'admin_vendor/add_vendor.html', {'admin': True,
                                                                    'all_areas': all_areas,
                                                                    'all_items': all_items,
                                                                    'logged_in_user_object': logged_in_user_object})
        else:
            return render(request, 'customer/index.html')


class ListOrder(View):
    @staticmethod
    def get(request):
        if 'token' not in request.session:
            return render(request, 'customer/index.html')
        logged_in_user = Session.get_user_by_session(request.session['token'])
        if logged_in_user is None:
            return render(request, 'customer/index.html')

        if logged_in_user.user_type == constants.USER_TYPE_ADMIN:
            '''admin'''
            logged_in_user_object = UserAdmin.objects.get(user=logged_in_user)
            all_orders = Order.objects.all()
            all_items = Item.objects.filter(active=True)
            all_areas = Area.objects.filter(active=True).order_by('area_name')
            return render(request, 'admin_vendor/list_order.html', {'admin': True,
                                                                    'all_orders': all_orders,
                                                                    'all_areas': all_areas,
                                                                    'all_items': all_items,
                                                                    'logged_in_user_object': logged_in_user_object})
        else:
            return render(request, 'customer/index.html')


class ListUser(View):
    @staticmethod
    def get(request):
        if 'token' not in request.session:
            return render(request, 'customer/index.html')
        logged_in_user = Session.get_user_by_session(request.session['token'])
        if logged_in_user is None:
            return render(request, 'customer/index.html')

        if logged_in_user.user_type == constants.USER_TYPE_ADMIN:
            '''admin'''
            logged_in_user_object = UserAdmin.objects.get(user=logged_in_user)
            if 'toggle' in request.GET:
                toggle_client = UserClient.objects.get(pk=request.GET['toggle'])
                toggle_client.active = not toggle_client.active
                toggle_client.save()
                return redirect(reverse('list_user'))
            clients = UserClient.objects.all()
            return render(request, 'admin_vendor/list_user.html', {'admin': True,
                                                                   'logged_in_user_object': logged_in_user_object,
                                                                   'clients': clients})
        else:
            return render(request, 'customer/index.html')


class ListVendor(View):
    @staticmethod
    def get(request):
        if 'token' not in request.session:
            return render(request, 'customer/index.html')
        logged_in_user = Session.get_user_by_session(request.session['token'])
        if logged_in_user is None:
            return render(request, 'customer/index.html')

        if logged_in_user.user_type == constants.USER_TYPE_ADMIN:
            '''admin'''
            logged_in_user_object = UserAdmin.objects.get(user=logged_in_user)
            if 'toggle' in request.GET:
                toggle_vendor = UserServiceProvider.objects.get(pk=request.GET['toggle'])
                toggle_vendor.active = not toggle_vendor.active
                toggle_vendor.save()
                return redirect(reverse('list_vendor'))
            vendors = UserServiceProvider.objects.all()
            return render(request, 'admin_vendor/list_vendor.html', {'admin': True,
                                                                     'logged_in_user_object': logged_in_user_object,
                                                                     'vendors': vendors})
        else:
            return render(request, 'customer/index.html')


class DetailOrder(View):
    @staticmethod
    def get(request, order_id):
        if 'token' not in request.session:
            return render(request, 'customer/index.html')
        logged_in_user = Session.get_user_by_session(request.session['token'])
        if logged_in_user is None:
            return render(request, 'customer/index.html')

        if logged_in_user.user_type == constants.USER_TYPE_ADMIN:
            '''admin'''
            selected_order = Order.objects.get(pk=order_id)
            logged_in_user_object = UserAdmin.objects.get(user=logged_in_user)
            all_orders = Order.objects.all()
            all_vendors = UserServiceProvider.objects.filter(active=True)
            all_items = Item.objects.filter(active=True)
            all_areas = Area.objects.filter(active=True).order_by('area_name')
            return render(request, 'admin_vendor/detail_order.html', {'admin': True,
                                                                      'all_vendors': all_vendors,
                                                                      'selected_order': selected_order,
                                                                      'all_areas': all_areas,
                                                                      'all_items': all_items,
                                                                      'logged_in_user_object': logged_in_user_object})
        else:
            return render(request, 'customer/index.html')


class DetailUser(View):
    @staticmethod
    def get(request, client_id):
        if 'token' not in request.session:
            return render(request, 'customer/index.html')
        logged_in_user = Session.get_user_by_session(request.session['token'])
        if logged_in_user is None:
            return render(request, 'customer/index.html')

        if logged_in_user.user_type == constants.USER_TYPE_ADMIN:
            '''admin'''
            logged_in_user_object = UserAdmin.objects.get(user=logged_in_user)
            client_object = UserClient.objects.get(pk=client_id)
            client_orders = Order.objects.filter(customer=client_object)
            return render(request, 'admin_vendor/detail_user.html', {'admin': True,
                                                                     'logged_in_user_object': logged_in_user_object,
                                                                     'client_object': client_object,
                                                                     'client_orders': client_orders})
        else:
            return render(request, 'customer/index.html')


class DetailVendor(View):
    @staticmethod
    def get(request, vendor_id):
        if 'token' not in request.session:
            return render(request, 'customer/index.html')
        logged_in_user = Session.get_user_by_session(request.session['token'])
        if logged_in_user is None:
            return render(request, 'customer/index.html')

        if logged_in_user.user_type == constants.USER_TYPE_ADMIN:
            '''admin'''
            logged_in_user_object = UserAdmin.objects.get(user=logged_in_user)
            vendor_object = UserServiceProvider.objects.get(pk=vendor_id)
            vendor_services = UserServiceProviderItem.objects.filter(user=vendor_object)
            vendor_areas = UserServiceProviderArea.objects.filter(user=vendor_object)
            return render(request, 'admin_vendor/detail_vendor.html', {'admin': True,
                                                                       'logged_in_user_object': logged_in_user_object,
                                                                       'vendor_object': vendor_object,
                                                                       'vendor_areas': vendor_areas,
                                                                       'vendor_services': vendor_services})
        else:
            return render(request, 'customer/index.html')


class OrderManage(View):
    @staticmethod
    def post(request):
        print(request.POST)
        selected_order = Order.objects.get(pk=request.POST['order_id'])
        if not request.POST['status'] == '----':
            selected_order.status = int(request.POST['status'])
        if not request.POST['service_provider'] == '----':
            selected_service_provider = UserServiceProvider.objects.get(pk=request.POST['service_provider'])
            selected_order.service_provider = selected_service_provider
        selected_order.save()
        return HttpResponseRedirect(reverse("detail_order", args=[request.POST['order_id']]))


class Manage(View):
    @staticmethod
    def get(request):
        return render(request, 'admin_vendor/manage.html')


class CustomerDashboard(View):
    @staticmethod
    def get(request):
        return render(request, 'customer/dashboard.html')


class CustomerServiceList(View):
    @staticmethod
    def get(request):
        if 'token' not in request.session:
            return redirect(reverse('home'))
        logged_in_user = Session.get_user_by_session(request.session['token'])
        if logged_in_user is None:
            return redirect(reverse('home'))

        if logged_in_user.user_type == constants.USER_TYPE_CLIENT:
            '''client'''
            logged_in_user_object = UserClient.objects.get(user=logged_in_user)
            all_orders = Order.objects.filter(customer=logged_in_user_object)
            return render(request, 'customer/service_list.html', {'admin': True,
                                                                  'all_orders': all_orders,
                                                                  'logged_in_user_object': logged_in_user_object})
        return redirect(reverse('home'))


class CustomerServiceDetail(View):
    @staticmethod
    def get(request, order_id):
        print(order_id)
        if 'token' not in request.session:
            return redirect(reverse('home'))
        logged_in_user = Session.get_user_by_session(request.session['token'])
        if logged_in_user is None:
            return redirect(reverse('home'))

        if logged_in_user.user_type == constants.USER_TYPE_CLIENT:
            '''client'''
            logged_in_user_object = UserClient.objects.get(user=logged_in_user)
            selected_order = Order.objects.get(pk=order_id)
            if selected_order.customer == logged_in_user_object:

                return render(request, 'customer/service_detail.html', {'admin': True,
                                                                        'selected_order': selected_order,
                                                                        'logged_in_user_object': logged_in_user_object})
            else:
                return redirect(reverse('service_list'))
        return redirect(reverse('home'))


class CustomerProfile(View):
    @staticmethod
    def get(request):
        return render(request, 'customer/profile_settings.html')


class OrderLogin(View):
    @staticmethod
    def get(request):
        return render(request, 'order/login.html')


class OrderSignUp(View):
    @staticmethod
    def get(request):
        return render(request, 'order/signup.html')


class NewOrder(View):
    @staticmethod
    def get(request):
        if 'token' not in request.session:
            return redirect(reverse('home'))
        logged_in_user = Session.get_user_by_session(request.session['token'])
        if logged_in_user is None:
            return redirect(reverse('home'))

        if logged_in_user.user_type == constants.USER_TYPE_CLIENT:
            '''client'''
            logged_in_user_object = UserClient.objects.get(user=logged_in_user)
            return render(request, 'order/index.html', {'admin': True,
                                                        'logged_in_user_object': logged_in_user_object})
        return redirect(reverse('home'))


class OrderElectronic(View):
    @staticmethod
    def get(request):
        if 'token' not in request.session:
            return redirect(reverse('home'))
        logged_in_user = Session.get_user_by_session(request.session['token'])
        if logged_in_user is None:
            return redirect(reverse('home'))

        if logged_in_user.user_type == constants.USER_TYPE_CLIENT:
            '''client'''
            logged_in_user_object = UserClient.objects.get(user=logged_in_user)
            electric_items = Item.objects.filter(service_type=constants.SERVICE_TYPE_ELECTRONIC)
            areas = Area.objects.all()
            return render(request, 'order/electronic.html', {'admin': True,
                                                             'electric_items': electric_items,
                                                             'areas': areas,
                                                             'logged_in_user_object': logged_in_user_object})
        return redirect(reverse('home'))

    @staticmethod
    def post(request):
        print(request.POST)
        return render(request, 'order/electronic.html')


class OrderVehicle(View):
    @staticmethod
    def get(request):
        if 'token' not in request.session:
            return redirect(reverse('home'))
        logged_in_user = Session.get_user_by_session(request.session['token'])
        if logged_in_user is None:
            return redirect(reverse('home'))

        if logged_in_user.user_type == constants.USER_TYPE_CLIENT:
            '''client'''
            logged_in_user_object = UserClient.objects.get(user=logged_in_user)
            electric_items = Item.objects.filter(service_type=constants.SERVICE_TYPE_VEHICLE)
            areas = Area.objects.all()
            return render(request, 'order/vehicle.html', {'admin': True,
                                                          'electric_items': electric_items,
                                                          'areas': areas,
                                                          'logged_in_user_object': logged_in_user_object})
        return redirect(reverse('home'))

    @staticmethod
    def post(request):
        print(request.POST)
        return render(request, 'order/vehicle.html')


def add_to_user_list(user_name, phone_number, user_email, user_id, user_type):
    listed_user = UserList(user_name=user_name,
                           phone_number=phone_number,
                           user_email=user_email,
                           user_id=user_id,
                           user_type=user_type)
    listed_user.save()
    return listed_user


def add_to_login_list(hash_key, user_email, password):
    user = User.objects.create_user(hash_key, user_email, password)
    user.is_stuff = False
    user.save()
    return True


def is_new_user(user_name, phone_number, user_email):
    if user_name is not None and UserList.objects.filter(user_name=user_name).exists():
        return False
    if phone_number is not None and UserList.objects.filter(phone_number=phone_number).exists():
        return False
    if user_email is not None and UserList.objects.filter(user_email=user_email).exists():
        return False
    return True


def find_user_from_credentials(uep):
    if UserList.objects.filter(Q(user_name=uep) | Q(phone_number=uep) | Q(user_email=uep)).exists():
        return UserList.objects.filter(Q(user_name=uep) | Q(phone_number=uep) | Q(user_email=uep))[0]
    else:
        return None


class Login(View):

    @staticmethod
    def get(request):

        return render(request, 'order/login.html')

    @staticmethod
    def post(request):
        """

        Args:
            request (http-request): This is the http request for calling this function.

        Returns:
            response: render the html page with page title, alert.

        Description : This function renders the html page where user cal login. If username and password in the request,
                    then this function checks if the username and password is correct or not. If correct then this
                    function authenticate the user and redirect to home page. Otherwise keeps on the same page showing
                    the error alert.

        """

        post_data = request.POST
        print(post_data)
        if 'username' and 'password' in post_data:
            user_object = find_user_from_credentials(post_data['username'])
            if user_object is None:
                return render(request, 'order/login.html', {
                    'alert': True,
                    'message': 'User Not Registered'})
            else:
                user_name = user_object.user_id

            user = authenticate(username=user_name, password=post_data['password'])
            if user is None:
                return render(request, 'order/login.html', {
                    'alert': True,
                    'message': 'Password is incorrect. Please Try again !'})
            else:
                login(request, user)
                request.session['token'] = Session.session_create(user_object)
                return redirect(reverse('home'))
        return render(request, 'order/login.html', {'alert': False,
                                                    'message': 'Something bad happened!'})


class Logout(View):
    @staticmethod
    def get(request):
        """

        Args:
            request (http-request): This is the http request for calling this function.

        Returns:
            response: redirect the user to login page.

        Description : This function logout the user and clean the api_session data .

        """
        Session.session_delete(request.session['token'])
        logout(request)
        return redirect(reverse('home'))


class Register(View):
    @staticmethod
    def get(request):
        if 'token' not in request.session:
            return render(request, 'order/signup.html')
        else:
            return redirect(reverse('home'))

    @staticmethod
    def post(request):
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        user_name = None
        phone_number = request.POST['phone_number']
        user_email = request.POST['user_email']
        address = None
        password = RandomPassword.random_password_generator(6)
        print(password)
        if is_new_user(user_name, phone_number, user_email):
            hash_key = UUID.uuid_generator()
            add_to_login_list(hash_key, user_email, password)
            listed_user = add_to_user_list(user_name, phone_number, user_email, hash_key,
                                           constants.USER_TYPE_CLIENT)
            new_user = UserClient(user=listed_user,
                                  first_name=first_name,
                                  last_name=last_name,
                                  phone_number=phone_number,
                                  address=address,
                                  user_email=user_email)
            new_user.save()
            greeting_text = 'Welcome to fixkori! Your Password is: ' + password + \
                            '. Please change the password once you log in. Thank you!'
            send_now(phone_number, greeting_text)
            return render(request, 'order/login.html',
                          {'success': True,
                           'message': 'Successfully Added!'})
        else:
            return render(request, 'order/signup.html',
                          {'alert': True,
                           'message': 'User Already Registered!'})


class ChangePassword(View):

    @staticmethod
    @login_required(login_url='/login/')
    def get(request):
        if 'token' not in request.session:
            return redirect(reverse('home'))
        logged_in_user = Session.get_user_by_session(request.session['token'])
        if logged_in_user is None:
            return redirect(reverse('home'))
        logged_in_user_object = UserClient.objects.get(user=logged_in_user)
        return render(request, 'order/change_password.html', {'logged_in_user_object': logged_in_user_object})

    @staticmethod
    @login_required(login_url='/login/')
    def post(request):
        logged_in_user = Session.get_user_by_session(request.session['token'])
        logged_in_user_object = UserClient.objects.get(user=logged_in_user)
        if 'csrfmiddlewaretoken' in request.POST:

            u = User.objects.get(username=logged_in_user.user_id)
            u.set_password(request.POST['password'])
            u.save()
            update_session_auth_hash(request, u)
            return render(request, 'order/change_password.html', {'page_title': 'CHANGE PASSWORD',
                                                                  'success': True,
                                                                  'message': 'Password Successfully Changed',
                                                                  'logged_in_user_object': logged_in_user_object})

        else:
            return render(request, 'order/change_password.html', {'page_title': 'CHANGE PASSWORD',
                                                                  'logged_in_user_object': logged_in_user_object})
