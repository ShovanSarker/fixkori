from django.db import models
from fixkori_api.models import BaseModel
from fixkori_api.models.area import Area
from fixkori_api.models.item import Item

import constants


class UserList(BaseModel):

    user_name = models.CharField(max_length=128, null=True, blank=True)
    phone_number = models.CharField(max_length=32, null=True, blank=True)
    user_email = models.CharField(max_length=128, null=True, blank=True)
    user_id = models.CharField(max_length=36, primary_key=True)
    user_type = models.IntegerField(default=constants.USER_TYPE_CLIENT)

    class Meta:
        app_label = "fixkori_api"
        db_table = "user_list"


class UserClient(BaseModel):

    user = models.ForeignKey(UserList, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=32, null=True, blank=True)
    last_name = models.CharField(max_length=32, null=True, blank=True)
    phone_number = models.CharField(max_length=32, null=True, blank=True)
    user_email = models.CharField(max_length=128, null=True, blank=True)
    address = models.CharField(max_length=256, null=True, blank=True)
    active = models.BooleanField(default=True)

    class Meta:
        app_label = "fixkori_api"
        db_table = "user_client"


class UserClientOtherInfo(BaseModel):

    user = models.ForeignKey(UserClient, on_delete=models.CASCADE)
    key = models.CharField(max_length=32, null=True, blank=True)
    value = models.CharField(max_length=128, null=True, blank=True)

    class Meta:
        app_label = "fixkori_api"
        db_table = "user_client_other_info"


class UserServiceProvider(BaseModel):

    user = models.ForeignKey(UserList, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=32, null=True, blank=True)
    last_name = models.CharField(max_length=32, null=True, blank=True)
    address = models.CharField(max_length=256, null=True, blank=True)
    phone_number = models.CharField(max_length=32, null=True, blank=True)
    email = models.CharField(max_length=128, null=True, blank=True)
    service_point_name = models.CharField(max_length=32, null=True, blank=True)
    image_1 = models.FileField('image_1', upload_to='service_provider/photo', blank=True, null=True)
    image_2 = models.FileField('image_2', upload_to='service_provider/photo', blank=True, null=True)
    image_3 = models.FileField('image_3', upload_to='service_provider/photo', blank=True, null=True)
    image_4 = models.FileField('image_4', upload_to='service_provider/photo', blank=True, null=True)
    image_5 = models.FileField('image_5', upload_to='service_provider/photo', blank=True, null=True)
    about = models.CharField(max_length=2048, null=True, blank=True)
    services = models.CharField(max_length=2048, null=True, blank=True)
    facebook_url = models.CharField(max_length=128, null=True, blank=True)
    google_map_url = models.CharField(max_length=128, null=True, blank=True)
    active = models.BooleanField(default=True)

    class Meta:
        app_label = "fixkori_api"
        db_table = "user_service_provider"


class UserServiceProviderOtherInfo(BaseModel):

    user = models.ForeignKey(UserServiceProvider, on_delete=models.CASCADE)
    key = models.CharField(max_length=32, null=True, blank=True)
    value = models.CharField(max_length=128, null=True, blank=True)

    class Meta:
        app_label = "fixkori_api"
        db_table = "user_service_provider_other_info"


class UserServiceProviderArea(BaseModel):

    user = models.ForeignKey(UserServiceProvider, on_delete=models.CASCADE)
    area = models.ForeignKey(Area, on_delete=models.DO_NOTHING)

    class Meta:
        app_label = "fixkori_api"
        db_table = "user_service_provider_area"


class UserServiceProviderItem(BaseModel):

    user = models.ForeignKey(UserServiceProvider, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.DO_NOTHING)

    class Meta:
        app_label = "fixkori_api"
        db_table = "user_service_provider_item"


class UserAdmin(BaseModel):

    user = models.ForeignKey(UserList, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=32, null=True, blank=True)
    last_name = models.CharField(max_length=32, null=True, blank=True)
    phone_number = models.CharField(max_length=32, null=True, blank=True)
    user_email = models.CharField(max_length=128, null=True, blank=True)
    active = models.BooleanField(default=True)

    class Meta:
        app_label = "fixkori_api"
        db_table = "user_admin"
