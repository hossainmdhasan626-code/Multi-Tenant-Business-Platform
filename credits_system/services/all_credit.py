# ---Django---
from django.db.models import Sum
from django.utils import timezone

# ---Model---
from credits_system.models import CreditTransaction, TenantCreditBalance

# ---Serializer---
from credits_system.serializer import TenantCreditBalanceSerializer


# সব ক্রেডিট বের করে আনা।
def all_credit(tenant):

    current_month = timezone.now().month
    current_year = timezone.now().year

    # সব ক্রেডিট বের করে আনা।
    all_credit = TenantCreditBalance.objects.get(tenant=tenant)

    spent_this_month = CreditTransaction.objects.filter(
        tenant=tenant,
        transaction_type=CreditTransaction.TransactionType.SALE_DEDUCTION,
        created_date__month=current_month,
        created_date__year=current_year,
    ).aggregate(spent_this_month=Sum("amount"))

    spent_this_month = abs(spent_this_month["spent_this_month"] or 0)

    all_credit.spent_this_month = spent_this_month

    # ডাটা সেরিয়ালাইজ করা।
    serializer = TenantCreditBalanceSerializer(instance=all_credit)
    return serializer.data
