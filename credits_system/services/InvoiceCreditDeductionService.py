# ---Django---
from django.db import transaction

# ---DRF---
from rest_framework.exceptions import ValidationError

# ---Model---
from credits_system.models import CreditTransaction, TenantCreditBalance


class InvoiceCreditDeductionService:
    @transaction.atomic
    def deduct_credit(self, tenant, amount, reference, salesman):

        # মূল ক্রেডিট কত আছে বের করে আনা।
        credit = TenantCreditBalance.objects.select_for_update().get(tenant=tenant)

        transaction_type = None
        credit_bucket = None

        if credit.is_unlimited == True:
            return True

        elif credit.free_credits and credit.free_credits >= amount:
            transaction_type = CreditTransaction.TransactionType.SALE_DEDUCTION
            credit_bucket = "FREE"
            credit.free_credits -= amount
            credit.save()

        elif credit.purchased_credits and credit.purchased_credits >= amount:
            transaction_type = CreditTransaction.TransactionType.SALE_DEDUCTION
            credit_bucket = "PURCHASED"
            credit.purchased_credits -= amount
            credit.save()

        else:
            raise ValidationError("আপনার পর্যপ্ত ক্রেডিট নেই. দয়া করে ক্রেডিট রিচার্জ করুন।")

        total_balance_after = credit.free_credits + credit.purchased_credits

        # ক্রেডিট তৈরি করা।
        CreditTransaction.objects.create(
            tenant=tenant,
            amount=-amount,
            transaction_type=transaction_type,
            credit_bucket=credit_bucket,
            balance_after=total_balance_after,
            reference=reference,
            created_by=salesman,
        )

        return True
