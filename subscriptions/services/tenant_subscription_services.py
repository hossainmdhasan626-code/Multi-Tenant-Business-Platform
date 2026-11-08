# ---Django---
from datetime import timedelta

from django.db import transaction
from django.utils import timezone

# ---Model---
from subscriptions.models import SubscriptionPlan, TenantSubscription

# ---serializer---
from subscriptions.seializers import TenantSubscriptionSerializer


@transaction.atomic
def tenant_subscription_services(data, tenant):
    subscription_id = data.get("id")

    if not subscription_id:
        raise ValueError("প্ল্যান আইডি প্রদান করা বাধ্যতামূলক।")

    # সিলেক্ট করা সাবস্ক্রিপশন বের করে আনা।
    try:
        plan = SubscriptionPlan.objects.get(id=subscription_id, is_active=True)
    except SubscriptionPlan.DoesNotExist:
        raise ValueError("সঠিক বা সক্রিয় কোনো সাবস্ক্রিপশন প্ল্যান পাওয়া যায়নি।")

    start_date = timezone.now()
    if plan.billing_cycle == SubscriptionPlan.BillingCycle.MONTHLY:
        end_date = start_date + timedelta(days=30)
    elif plan.billing_cycle == SubscriptionPlan.BillingCycle.YEARLY:
        end_date = start_date + timedelta(days=365)
    elif plan.billing_cycle == SubscriptionPlan.BillingCycle.LIFETIME:
        end_date = None
    else:
        end_date = start_date + timedelta(days=30)

    tenant_subscription = TenantSubscription.objects.create(
        tenant=tenant,
        plan=plan,
        status=TenantSubscription.Status.TRIALLING,
        start_date=start_date,
        end_date=end_date,
        price_snapshot=plan.price,
    )

    serializer = TenantSubscriptionSerializer(instance=tenant_subscription)

    return serializer.data
