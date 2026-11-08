# ---Django---
from django.db import models

# ---Custom reuable field---
from common.models import TimeStampedModel


# Create your models here.
class Customer(TimeStampedModel):
    # tenant field add korbo jokhon tenant modle ke banabo
    tenant = models.ForeignKey(
        "tenants.Tenant", on_delete=models.CASCADE, related_name="customer"
    )
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=100, blank=True)
    active_status = models.BooleanField(default=True)
