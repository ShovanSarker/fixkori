from django.db import models


class BaseModel (models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = "fixkori_api"
        abstract = True
