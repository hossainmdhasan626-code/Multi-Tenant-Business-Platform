# ---Django---
from django.db import models

# ---Model---
from tenants.models import Tenant


# Create your models here.
class TenantSequence(models.Model):
    tenant = models.OneToOneField(
        Tenant, on_delete=models.CASCADE, related_name="sequence"
    )
    last_id = models.PositiveIntegerField(default=0)
