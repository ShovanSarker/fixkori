from __future__ import print_function
from django.views import View

from django.shortcuts import render, redirect, HttpResponse
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

from utility.uuid_generator import UUID
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
            return render(request, 'admin_vendor/add_admin.html', {'success': True, 'message': 'Successfully Added!'})
        else:
            return render(request, 'admin_vendor/add_admin.html', {'alert': True, 'message': 'User Already Registered!'})

    @staticmethod
    def get(request):
        return render(request, 'admin_vendor/add_admin.html')


class AddUser(View):
    @staticmethod
    def post(request):
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
            listed_user = add_to_user_list(user_name, phone_number, user_email, hash_key, constants.USER_TYPE_CLIENT)
            new_user = UserClient(user=listed_user,
                                  first_name=first_name,
                                  last_name=last_name,
                                  phone_number=phone_number,
                                  address=address,
                                  user_email=user_email)
            new_user.save()
            return render(request, 'admin_vendor/add_user.html', {'success': True, 'message': 'Successfully Added!'})
        else:
            return render(request, 'admin_vendor/add_user.html', {'alert': True, 'message': 'User Already Registered!'})

    @staticmethod
    def get(request):
        return render(request, 'admin_vendor/add_user.html')


class AddVendor(View):
    @staticmethod
    def post(request):
        print(request.FILES)
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
                          {'success': True,
                           'message': 'Successfully Added!',
                           'all_areas': all_areas,
                           'all_items': all_items})
        else:
            return render(request, 'admin_vendor/add_vendor.html',
                          {'alert': True,
                           'message': 'User Already Registered!',
                           'all_areas': all_areas,
                           'all_items': all_items})

    @staticmethod
    def get(request):
        all_items = Item.objects.filter(active=True)
        all_areas = Area.objects.filter(active=True).order_by('area_name')
        return render(request, 'admin_vendor/add_vendor.html',
                      {'all_areas': all_areas,
                       'all_items': all_items})


class ListOrder(View):
    @staticmethod
    def get(request):
        return render(request, 'admin_vendor/list_order.html')


class ListUser(View):
    @staticmethod
    def get(request):
        return render(request, 'admin_vendor/list_user.html')


class ListVendor(View):
    @staticmethod
    def get(request):
        return render(request, 'admin_vendor/list_vendor.html')


class DetailOrder(View):
    @staticmethod
    def get(request):
        return render(request, 'admin_vendor/detail_order.html')


class DetailUser(View):
    @staticmethod
    def get(request):
        return render(request, 'admin_vendor/detail_user.html')


class DetailVendor(View):
    @staticmethod
    def get(request):
        return render(request, 'admin_vendor/detail_vendor.html')


class OrderManage(View):
    @staticmethod
    def get(request):
        return render(request, 'admin_vendor/order_manage.html')


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
        return render(request, 'customer/service_list.html')


class CustomerServiceDetail(View):
    @staticmethod
    def get(request):
        return render(request, 'customer/service_detail.html')


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


class Order(View):
    @staticmethod
    def get(request):
        return render(request, 'order/index.html')


class OrderElectronic(View):
    @staticmethod
    def get(request):
        return render(request, 'order/electronic.html')


class OrderVehicle(View):
    @staticmethod
    def get(request):
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

        return render(request, 'admin_vendor/login.html')

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
                return render(request, 'admin_vendor/login.html', {
                    'alert': True,
                    'message': 'User Not Registered'})
            else:
                user_name = user_object.user_id

            user = authenticate(username=user_name, password=post_data['password'])
            if user is None:
                return render(request, 'admin_vendor/login.html', {
                    'alert': True,
                    'message': 'Password is incorrect. Please Try again !'})
            else:
                login(request, user)
                request.session['token'] = Session.session_create(user_object)
                return redirect(reverse('home'))
        return render(request, 'admin_vendor/login.html', {'alert': False,
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


class ChangePassword(View):
    @staticmethod
    @login_required(login_url='/login/')
    def get(request):
        user = Session.get_user_by_session(request.session['token'])
        if user is False:
            logout(request)
            return redirect(reverse('home'))
        return render(request, 'change_pass.html', {'page_title': 'CHANGE PASSWORD',
                                                    'username': user.user_name})

    @staticmethod
    @login_required(login_url='/login/')
    def post(request):
        user = Session.get_user_by_session(request.session['token'])
        if 'csrfmiddlewaretoken' in request.POST:

            u = User.objects.get(username=user.user_id)
            u.set_password(request.POST['password'])
            u.save()
            update_session_auth_hash(request, u)
            return render(request, 'change_pass.html', {'page_title': 'CHANGE PASSWORD',
                                                        'success': True,
                                                        'message': 'Password Successfully Changed',
                                                        'username': user.user_name})

        else:
            return render(request, 'change_pass.html', {'page_title': 'CHANGE PASSWORD',
                                                        'username': user.user_name})
