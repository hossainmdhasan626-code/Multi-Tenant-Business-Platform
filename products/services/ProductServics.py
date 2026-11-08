# ---Django---
from django.db import DataError, IntegrityError, transaction
from django.db.models import Q

# ---Drf---
from rest_framework.exceptions import (
    NotFound,
    ValidationError,
)

# ---Services---
from common.services.create_stock_movement import create_stock_movement
from common.services.parse_int import parse_int

# ---Custom pagination---
from common.services.reusable_custom_pagination import reusable_custom_pagination

# ---Model---
from products.models import Product

# ---Serializer---
from products.serializer import ProductSerializer, ProductUpdateSerializer

# ---Model---
from stock_movement.models import StockMovement


class ProductServics:
    # সব প্রোডাক্ট এর ডাটা বের করা ও সার্চ করে প্রোডাক্ট এর ডাটা বের করা।
    def get_products(self, tenant, request, view_instance, search_query=None):

        if request and request.user.role in ("TENANT_OWNER", "STORE_MANAGER"):
            product_data = Product.objects.filter(tenant=tenant)
        else:
            product_data = Product.objects.filter(tenant=tenant, active_status=True)

        if search_query:
            product_data = product_data.filter(
                Q(name__icontains=search_query) | Q(sku__icontains=search_query)
            )

        # serializer = ProductSerializer(product_data, many=True)
        # return serializer.data
        return reusable_custom_pagination(
            queryset=product_data,
            request=request,
            serializer_class=ProductSerializer,
            view_instance=view_instance,
            page_size=10,
        )

    # নতুন প্রোডাক্ট তৈরী করা।
    @transaction.atomic
    def product_create(self, tenant, data, salesmen, request):

        serializer = ProductSerializer(data=data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        product_instance = serializer.save(tenant=tenant)

        # স্টক মুভমেন্ট তৈরি করা।
        if not product_instance.stock_quantity <= 0:
            create_stock_movement(
                tenant=tenant,
                product_data=product_instance,
                salesmen=salesmen,
                movement_type=StockMovement.MovementType.STOCK_IN,
                quantity=product_instance.stock_quantity,
            )
        return serializer.data

    # নির্দিষ্ট প্রোডাক্ট এর ডাটা বের করা।
    def get_products_details(self, request, tenant, product_id):

        try:
            if request and request.user.role in ("TENANT_OWNER", "STORE_MANAGER"):
                product_data = Product.objects.get(tenant=tenant, id=product_id)
            else:
                product_data = Product.objects.get(
                    tenant=tenant, id=product_id, active_status=True
                )
        except Product.DoesNotExist:
            raise NotFound("প্রোডাক্টটি খুঁজে পাওয়া যায়নি।")

        if not product_data:
            return None

        serializer = ProductSerializer(product_data)
        return serializer.data

    # নির্দিষ্ট প্রোডাক্ট এর ডাটা আপডেটেড করা।
    def patch_updatese_single_product(self, request, tenant, product_id, product_data):

        try:
            product = Product.objects.get(tenant=tenant, id=product_id)
        except Product.DoesNotExist:
            raise NotFound("প্রোডাক্টটি খুঁজে পাওয়া যায়নি।")

        if not product:
            return None

        serializer = ProductUpdateSerializer(
            instance=product,
            data=product_data,
            context={"request": request},
            partial=True,
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data

    @transaction.atomic
    def patch_product_stock(
        self, product_id, tenant, salesmen, product_quantity, update_type
    ):

        if product_quantity != "":
            product_quantity = parse_int(data=product_quantity, field="প্রোডাক্ট কোয়ান্টিটি")
        else:
            raise ValidationError(
                "প্রোডাক্ট কোয়ান্টিটি পরিবর্তন এর জন্য প্রোডাক্ট কোয়ান্টিটি দেয়া বাধ্যতামূলক।"
            )

        if product_quantity <= 0:
            raise ValidationError(
                "প্রোডাক্ট কোয়ান্টিটি এর পরিমাণ অবশ্যই '0' (শূন্য) এর বেশি এবং ধনাত্মক সংখ্যা হতে হবে।"
            )

        if (
            not update_type
            or not isinstance(update_type, str)
            or update_type.strip() == ""
        ):
            raise ValidationError("প্রোডাক্ট কোয়ান্টিটি পরিবর্তন এর জন্য 'type' দেওয়া বাধ্যতামূলক।")
        else:
            update_type = update_type.lower()

        if not update_type in ("increment", "decrement"):
            raise ValidationError(
                "আপডেট টাইপ অবশ্যই 'increment' অথবা 'decrement' হতে হবে। অন্য কোনো মান গ্রহণযোগ্য নয়।"
            )

        try:
            product_instance = Product.objects.select_for_update().get(
                tenant=tenant, id=product_id, active_status=True
            )

            if update_type == "increment":
                product_instance.stock_quantity += product_quantity
            elif update_type == "decrement":
                if product_instance.stock_quantity < product_quantity:
                    raise ValidationError(
                        f"পর্যাপ্ত স্টক নেই! বর্তমানে স্টকে মাত্র {product_instance.stock_quantity} টি পণ্য রয়েছে, তাই আপনি এর বেশি কমাতে বা স্টক আউট করতে পারবেন না।"
                    )
                product_instance.stock_quantity -= product_quantity

            product_instance.save()

            stock_movement = create_stock_movement(
                tenant=tenant,
                salesmen=salesmen,
                product_data=product_instance,
                movement_type=StockMovement.MovementType.ADJUSTMENT,
                quantity=product_quantity,
                update_type=update_type,
            )
        except Product.DoesNotExist:
            raise NotFound("আপনার চাওয়া প্রোডকাটটি খুঁজে পাওয়া যায়নি।")
        except IntegrityError as e:
            raise ValidationError("ডেটাবেজ ইন্টেগ্রিটি এরর:", e)
        except DataError as e:
            raise ValidationError("ভুল ডেটা ফরম্যাট বা ডাটা:", e)

        return stock_movement

    # প্রোডাক্ট ডিলিট করা।
    @transaction.atomic
    def get_delete_product(self, tenant, product_id):

        try:
            product = Product.objects.select_for_update().get(
                tenant=tenant, id=product_id, active_status=True
            )

            product.active_status = False
            product.save()

        except Product.DoesNotExist:
            raise NotFound("প্রোডাক্টটি খুঁজে পাওয়া যায়নি।")

        except (IntegrityError, DataError):
            raise ValidationError(
                "ডেটা ডিলিট করার সময় ডাটাবেজে সমস্যা হয়েছে। দয়া করে আবার চেষ্টা করুন।"
            )

        return True
