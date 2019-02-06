from django.db import models
from fixkori_api.models import BaseModel

import constants


class Item(BaseModel):

    item_name = models.CharField(max_length=128, null=True, blank=True)
    service_type = models.IntegerField(default=constants.SERVICE_TYPE_ELECTRONIC)
    active = models.BooleanField(default=True)

    class Meta:
        app_label = "fixkori_api"
        db_table = "item"


class Brand(BaseModel):

    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    brand = models.IntegerField(default=constants.SERVICE_TYPE_ELECTRONIC)
    active = models.BooleanField(default=True)

    class Meta:
        app_label = "fixkori_api"
        db_table = "brand"
