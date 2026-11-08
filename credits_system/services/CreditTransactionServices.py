# ---Model---
from credits_system.models import CreditTransaction

# ---Serializer---
from credits_system.serializer import CreditTransactionSerializer


class CreditTransactionServices:
    # সব ক্রেডিট এর ট্রানসাকশান বের করে আনা।
    def CreditTransaction(self, tenant):

        # সব ক্রেডিট এর ট্রানসাকশান বের করে আনা।
        all_credit_transaction = CreditTransaction.objects.filter(tenant=tenant)

        # ডাটা সিরিয়ালাইজ করা।
        serializ = CreditTransactionSerializer(
            instance=all_credit_transaction, many=True
        )

        return serializ.data

    def CreditTransactionDetails(self, tenant, id):

        # নির্দিষ্ট ক্রেডিট এর ট্রানসাকশান বের করে আনা।
        credit_details = CreditTransaction.objects.get(tenant=tenant, id=id)

        # ডাটা সিরিয়ালাইজ করা।
        serializ = CreditTransactionSerializer(instance=credit_details)

        return serializ.data
