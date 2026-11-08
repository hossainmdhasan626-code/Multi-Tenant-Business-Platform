from django.db import models

# ---Custom reuable field---
from common.models import TimeStampedModel


# Create your models here.
class Tenant(TimeStampedModel):
    business_name = models.CharField(max_length=100)
    status = models.BooleanField(default=True)
