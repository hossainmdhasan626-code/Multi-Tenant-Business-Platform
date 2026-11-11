# ---Django---
from django.db.models import Sum

# ---Drf---
from rest_framework import serializers

# ---Model---
from customers.models import Customer
from invoices.models import Invoice


class CustomerSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        max_length=100,
        error_messages={
            "blank": "নাম খালি বা ফাঁকা রাখা যাবে না।",
            "required": "নাম দেওয়া বাধ্যতামূলক।",
            "max_length": "নাম ১০০ অক্ষরের বেশি হতে পারবে না।",
        },
    )

    phone = serializers.CharField(
        required=False,
        error_messages={
            "blank": "নম্বর খালি বা ফাঁকা রাখা যাবে না।",
        },
    )

    total_orders = serializers.SerializerMethodField()
    lifetime_spending = serializers.SerializerMethodField()

    class Meta:
        model = Customer
        fields = [
            "id",
            "tenant",
            "name",
            "phone",
            "address",
            "total_orders",
            "lifetime_spending",
            "active_status",
            "created_date",
            "updated_date",
        ]
        read_only_fields = ["id", "tenant", "created_date", "updated_date"]

    # নাম কে খালি রাখা যাবে না।
    # def validate_name(self, value):

    #     # এক্সট্রা স্পেস ছাটাই করা।
    #     name = value.strip()

    #     if name == "":
    #         raise serializers.ValidationError("")
    #     return name

    # নম্বর এর ভ্যালিডেশন চেক করা।
    def validate_phone(self, value):

        # এক্সট্রা স্পেস ছাটাই করা।
        number = value.strip()

        # নাম্বার যদি কান্ট্রি কোড সহ আসে।
        if len(number) == 14 and number.startswith("+8801"):
            return number

        # নাম্বার যদি কান্ট্রি কোড ছাড়া আসে।
        if len(number) == 11 and number.startswith("01"):
            return number

        raise serializers.ValidationError("অনুগ্রহ করে একটি বৈধ নম্বর দিন।")

    def validate(self, data):

        tenant = self.context["request"].user.tenant
        phone = data.get("phone")

        if phone:
            phone_query = Customer.objects.filter(tenant=tenant, phone=phone)

            if self.instance:
                phone_query = phone_query.exclude(pk=self.instance.pk)

            if phone_query.exists():
                raise serializers.ValidationError(
                    {"phone": "এই নম্বর দিয়ে একটি কাস্টমার আগেই রেজিস্টার হয়েছে।"}
                )

        return data

    def get_total_orders(self, obj):

        request = self.context.get("request")
        tenant = request.user.tenant

        total_orders = Invoice.objects.filter(
            tenant=tenant, status=Invoice.Status.PAID, customer=obj
        ).count()

        return total_orders

    def get_lifetime_spending(self, obj):

        request = self.context.get("request")
        tenant = request.user.tenant

        invoice = Invoice.objects.filter(
            tenant=tenant, status=Invoice.Status.PAID, customer=obj
        ).aggregate(lifetime_spending=Sum("total"))

        lifetime_spending = invoice["lifetime_spending"] or 0

        return lifetime_spending
