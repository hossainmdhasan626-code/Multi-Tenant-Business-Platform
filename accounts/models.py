# ---Django---
from django.contrib.auth.models import AbstractUser
from django.db import models

# ---Model---
from common.models import TimeStampedModel

# Create your models here.b


class User(AbstractUser, TimeStampedModel):
    class Role(models.TextChoices):
        # DB Value       DB Value        UI Label
        TENANT_OWNER = "TENANT_OWNER", "Tenant Owner"
        STORE_MANAGER = "STORE_MANAGER", "Store Manager"
        SALESMAN = "SALESMAN", "Salesman"

    # Custom field
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.SALESMAN)
    tenant = models.ForeignKey(
        "tenants.Tenant",
        on_delete=models.CASCADE,
        related_name="users",
        null=True,
        blank=True,
    )
