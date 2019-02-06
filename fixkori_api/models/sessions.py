from django.db import models

from fixkori_api.models import BaseModel
from fixkori_api.models.user import UserList


class LoginSession (BaseModel):
    user = models.ForeignKey(UserList, on_delete=models.CASCADE)
    token = models.CharField(max_length=36, primary_key=True)

    class Meta:
        app_label = "fixkori_api"
        db_table = "sessions"
