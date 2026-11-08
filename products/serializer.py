# ---Drf---
from rest_framework import serializers

# ---Model---
from products.models import Product


class ProductSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        max_length=100,
        error_messages={
            "blank": "পণ্যের নাম খালি রাখা যাবে না।",
            "required": "পণ্যের নাম দেওয়া বাধ্যতামূলক।",
            "max_length": "নাম ১০০ অক্ষরের বেশি হতে পারবে না।",
        },
    )

    sku = serializers.CharField(
        max_length=100,
        error_messages={
            "blank": "SKU প্রদান করা আবশ্যক।",
            "required": "SKU দেওয়া বাধ্যতামূলক",
            "max_length": " SKU ১০০ অক্ষরের বেশি হতে পারবে না।",
        },
    )

    stock_quantity = serializers.IntegerField(
        default=0,
        min_value=0,
        error_messages={
            "required": "স্টকের পরিমাণ দেওয়া বাধ্যতামূলক।",
            "invalid": "স্টক অবশ্যই একটি পূর্ণ সংখ্যা হতে হবে।",
            "min_value": "স্টকের পরিমাণ শূন্য বা তার বেশি হতে হবে, ঋণাত্মক (-) হতে পারবে না।",
        },
    )

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "sku",
            "tenant",
            "cost_price",
            "selling_price",
            "stock_quantity",
            "active_status",
        ]

        read_only_fields = ["id", "tenant"]

    def validate(self, data):

        # ---SKU চেক।---
        tenant = self.context["request"].user.tenant
        sku = data.get("sku")

        if sku:
            sku_query = Product.objects.filter(tenant=tenant, sku=sku)

            if self.instance:
                sku_query = sku_query.exclude(pk=self.instance.pk)

            if sku_query.exists():
                raise serializers.ValidationError(
                    {"sku": "এই প্রোডাক্ট কোড বা SKU দিয়ে ইতিমধ্যে একটি পণ্য রেজিস্টার্ড রয়েছে।"}
                )

        # ---ঋণাত্মক নম্বর চেক।---
        fields_to_check = ["cost_price", "selling_price", "stock_quantity"]
        errors = {}

        for field in fields_to_check:
            value = data.get(field)

            if value is not None and value < 0:
                errors[field] = "এই মানটি ঋণাত্মক হতে পারে না।"

        if errors:
            raise serializers.ValidationError(errors)

        return data


class ProductUpdateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        max_length=100,
        error_messages={
            "blank": "পণ্যের নাম খালি রাখা যাবে না।",
            "required": "পণ্যের নাম দেওয়া বাধ্যতামূলক।",
            "max_length": "নাম ১০০ অক্ষরের বেশি হতে পারবে না।",
        },
    )
    sku = serializers.CharField(
        max_length=100,
        error_messages={
            "blank": "SKU প্রদান করা আবশ্যক।",
            "required": "SKU দেওয়া বাধ্যতামূলক",
            "max_length": " SKU ১০০ অক্ষরের বেশি হতে পারবে না।",
        },
    )
    stock_quantity = serializers.IntegerField(
        default=0,
        min_value=0,
        read_only=True,
        error_messages={
            "required": "স্টকের পরিমাণ দেওয়া বাধ্যতামূলক।",
            "invalid": "স্টক অবশ্যই একটি পূর্ণ সংখ্যা হতে হবে।",
            "min_value": "স্টকের পরিমাণ শূন্য বা তার বেশি হতে হবে, ঋণাত্মক (-) হতে পারবে না।",
        },
    )

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "sku",
            "tenant",
            "cost_price",
            "selling_price",
            "stock_quantity",
            "active_status",
        ]
        read_only_fields = ["id", "tenant", "stock_quantity"]

    def validate(self, data):

        # ---SKU চেক।---
        tenant = self.context["request"].user.tenant
        sku = data.get("sku")

        if sku:
            sku_query = Product.objects.filter(tenant=tenant, sku=sku)

            if self.instance:
                sku_query = sku_query.exclude(pk=self.instance.pk)

            if sku_query.exists():
                raise serializers.ValidationError(
                    {"sku": "এই প্রোডাক্ট কোড বা SKU দিয়ে ইতিমধ্যে একটি পণ্য রেজিস্টার্ড রয়েছে।"}
                )

        # ---ঋণাত্মক নম্বর চেক।---
        fields_to_check = ["cost_price", "selling_price", "stock_quantity"]
        errors = {}

        for field in fields_to_check:
            value = data.get(field)

            if value is not None and value < 0:
                errors[field] = "এই মানটি ঋণাত্মক হতে পারে না।"

        if errors:
            raise serializers.ValidationError(errors)

        return data
