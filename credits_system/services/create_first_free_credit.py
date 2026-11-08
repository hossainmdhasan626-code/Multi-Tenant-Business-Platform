# ---Django---
from django.db import transaction

# ---Model---
from credits_system.models import CreditTransaction, TenantCreditBalance


# ফ্রি ক্রেডিট তৈরি করা।
@transaction.atomic
def create_first_free_credit(tenant, salesman):

    free_credit = 333

    credit = TenantCreditBalance.objects.create(tenant=tenant, free_credits=free_credit)

    total_credit = credit.free_credits + credit.purchased_credits
    CreditTransaction.objects.create(
        tenant=tenant,
        amount=+free_credit,
        transaction_type=CreditTransaction.TransactionType.FREE_CREDIT,
        credit_bucket="FREE",
        balance_after=total_credit,
        created_by=salesman,
    )

    return total_credit
