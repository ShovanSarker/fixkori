from django.db import models
from fixkori_api.models import BaseModel
from fixkori_api.models import UserClient
from fixkori_api.models import UserServiceProvider
from fixkori_api.models import Area
from fixkori_api.models import Item

import constants


class Order(BaseModel):

    customer = models.ForeignKey(UserClient, on_delete=models.DO_NOTHING)
    service_provider = models.ForeignKey(UserServiceProvider, on_delete=models.DO_NOTHING, null=True, blank=True)
    area = models.ForeignKey(Area, on_delete=models.DO_NOTHING)
    item = models.ForeignKey(Item, on_delete=models.DO_NOTHING)
    brand = models.CharField(max_length=128, null=True, blank=True)
    model = models.CharField(max_length=128, null=True, blank=True)
    service_type = models.IntegerField(default=constants.SERVICE_TYPE_ELECTRONIC)
    date = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    time = models.CharField(max_length=8, null=True, blank=True)
    address = models.CharField(max_length=256, null=True, blank=True)
    instruction = models.CharField(max_length=256, null=True, blank=True)
    description = models.CharField(max_length=512, null=True, blank=True)
    status = models.IntegerField(default=constants.ORDER_STATUS_PENDING)

    class Meta:
        app_label = "fixkori_api"
        db_table = "order"


class OrderIssue(BaseModel):

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    issue = models.CharField(max_length=128, null=True, blank=True)

    class Meta:
        app_label = "fixkori_api"
        db_table = "order_issue"


class OrderOtherInfo(BaseModel):

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    key = models.CharField(max_length=32, null=True, blank=True)
    value = models.CharField(max_length=128, null=True, blank=True)

    class Meta:
        app_label = "fixkori_api"
        db_table = "order_other_info"
