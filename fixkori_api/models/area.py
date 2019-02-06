from django.db import models
from fixkori_api.models import BaseModel


class Area(BaseModel):

    area_name = models.CharField(max_length=128, null=True, blank=True)
    district = models.CharField(max_length=32, null=True, blank=True)
    division = models.CharField(max_length=32, null=True, blank=True)
    active = models.BooleanField(default=True)

    class Meta:
        app_label = "fixkori_api"
        db_table = "area"
