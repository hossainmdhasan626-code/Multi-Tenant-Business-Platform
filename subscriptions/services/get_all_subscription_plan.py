# ---Model---
from subscriptions.models import SubscriptionPlan

# ---Serializer---
from subscriptions.seializers import SubscriptionPlanSerializer


# সব সাবস্ক্রিপশন প্ল্যান বের করে আনা।
def get_all_subscription_plan():

    all_subscription_plan = SubscriptionPlan.objects.filter(is_active=True)

    serializ = SubscriptionPlanSerializer(instance=all_subscription_plan, many=True)

    return serializ.data
