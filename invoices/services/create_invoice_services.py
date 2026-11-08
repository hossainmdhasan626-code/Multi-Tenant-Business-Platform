# ---Django---
from django.db import transaction
from django.db.models import F

# ---Drf---
from rest_framework.exceptions import ValidationError

# ---Services---
from common.services.parse_int import parse_int
from credits_system.services.InvoiceCreditDeductionService import (
    InvoiceCreditDeductionService,
)

# ---Model---
from customers.models import Customer
from invoices.models import Invoice
from invoices.serializers import InvoicesSerializer
from products.models import Product
from sale_items.models import SaleItem
from sequence.models import TenantSequence
from stock_movement.models import StockMovement
from tenants.models import Tenant


# class InvoicesServices:
@transaction.atomic
def create_invoice(
    tenant,
    products_data,
    salesman,
    discount,
    customer_id=None,
    customer_data=None,
):

    # Tenant ভ্যালিডেশন
    if tenant:
        try:
            tenant = Tenant.objects.get(
                id=tenant.id, business_name=tenant.business_name, status=True
            )
        except Tenant.DoesNotExist:
            raise ValidationError(f"{tenant.business_name} টি ভ্যালিড নয়।")

    # ---কাস্টমার ভ্যালিডেশন or তৈরী।---
    if customer_id:
        try:
            customer_id = parse_int(data=customer_id, field="কাস্টমার আইডি")
            customer = Customer.objects.get(
                tenant=tenant, id=customer_id, active_status=True
            )
        except Customer.DoesNotExist:
            raise ValidationError("কাস্টমার ভ্যালিড নয়।")

    elif customer_data:
        if not isinstance(customer_data, dict):
            raise ValidationError("কাস্টমার ডাটা 'dict' পাঠান। ")

        # কাস্টমার তৈরী।
        name = customer_data.get("name")
        phone = customer_data.get("phone")

        if not (name and phone):
            raise ValidationError("কাস্টমার তৈরির জন্য নাম ও ফোন দেয়া বাধ্যতামূলক।")

        if not (isinstance(name, str) and isinstance(phone, str)):
            raise ValidationError("কাস্টমার নাম ও ফোন 'str' পাঠান ।")

        clean_name = name.strip()

        if clean_name == "":
            raise ValidationError("কাস্টমার তৈরির জন্য নাম প্রয়োজন।")

        phone = phone.strip()

        if phone == "":
            raise ValidationError("কাস্টমার তৈরির জন্য নম্বর প্রয়োজন।")

        is_valid_phone = (len(phone) == 14 and phone.startswith("+880")) or (
            len(phone) == 11 and phone.startswith("01")
        )
        if not is_valid_phone:
            raise ValidationError("কাস্টমার তৈরির জন্য নম্বর প্রয়োজন।")

        customer, _ = Customer.objects.get_or_create(
            tenant=tenant,
            phone=phone,
            defaults={"name": clean_name},
        )

        if customer and customer.active_status == False:
            raise ValidationError(
                f"অভ্যন্তরীণ কারন বসত {customer.name} কে কিছু সময় এর জন্য বন্ধ করা হয়েছে।"
            )

    else:
        customer, _ = Customer.objects.get_or_create(
            tenant=tenant, name="Walk in customer"
        )

        if customer and customer.active_status == False:
            raise ValidationError(
                f"অভ্যন্তরীণ কারন বসত '{customer.name}' কে কিছু সময় এর জন্য বন্ধ করা হয়েছে।"
            )

    if discount is None:
        raise ValidationError("ডিসকাউন্ট অবশ্যই পূর্ণসংখ্যা হতে হবে।")

    if not isinstance(discount, int):
        raise ValidationError("ডিসকাউন্ট অবশ্যই পূর্ণসংখ্যা হতে হবে।")

    if discount < 0:
        raise ValidationError("ডিসকাউন্ট কখনো ঋণাত্মক হতে পারবে না।")

    if not products_data:
        raise ValidationError("ইনভয়েস তৈরির জন্য প্রোডাক্ট ডাটা দেয়া বাধ্যতামূলক।")

    if not isinstance(products_data, list):
        raise ValidationError("প্রোডাক্ট ডাটা 'list' পাঠান।")

    # Create a custom sequence/id
    sequence, _ = TenantSequence.objects.select_for_update().get_or_create(
        tenant=tenant
    )
    sequence.last_id += 1
    sequence.save()

    # ইনভয়েস তৈরী।
    invoice = Invoice.objects.create(
        sequence=sequence.last_id,
        tenant=tenant,
        customer=customer,
        created_by=salesman,
        subtotal=0,
        discount=discount,
        total=0,
        status=Invoice.Status.PAID,
    )

    sub_total = 0
    sale_item_list = []
    stock_movement = []

    for pro in products_data:
        if not isinstance(pro, dict):
            raise ValidationError("প্রোডাক্ট ডাটা 'dict' এ পাঠান। ")

        product_id = pro.get("product_id")
        product_quantity = pro.get("quantity")

        if product_id is None:
            raise ValidationError("ইনভয়েস তৈরির জন্য প্রোডাক্ট আইডি দেয়া বাধ্যতামূলক।")

        if not product_id:
            raise ValidationError("ইনভয়েস তৈরির জন্য প্রোডাক্ট আইডি দেয়া বাধ্যতামূলক।")

        product_id = parse_int(data=product_id, field="প্রোডাক্ট আইডি")

        if product_quantity is None:
            raise ValidationError("ইনভয়েস তৈরির জন্য প্রোডাক্ট এর পরিমান দেয়া বাধ্যতামূলক।")

        product_quantity = parse_int(data=product_quantity, field="প্রোডাক্ট এর পরিমান")

        if product_quantity <= 0:
            raise ValidationError("প্রোডাক্ট এর পরিমান ঋণাত্মক করা যাবে না।")

        try:
            product = Product.objects.select_for_update().get(
                tenant=tenant, id=product_id, active_status=True
            )
        except Product.DoesNotExist:
            raise ValidationError("প্রোডাক্ট এর ডাটা খুঁজে পাওয়া যায়নি।")

        existing_product_quantity = product.stock_quantity

        if product_quantity > existing_product_quantity:
            raise ValidationError(
                f"{product_quantity} দেয়া সম্ভব নয়। সর্বোচ্চ {existing_product_quantity} দেয়া যাবে।"
            )

        line_total = product_quantity * product.selling_price
        sub_total += line_total

        Product.objects.filter(tenant=tenant, id=product_id).update(
            stock_quantity=F("stock_quantity") - product_quantity
        )

        sale_item_list.append(
            SaleItem(
                sale=invoice,
                product=product,
                product_name=product.name,
                quantity=product_quantity,
                selling_price_snapshot=product.selling_price,
                cost_price_snapshot=product.cost_price,
                line_total=line_total,
            )
        )

        stock_movement.append(
            StockMovement(
                tenant=tenant,
                product=product,
                quantity=-product_quantity,
                movement_type=StockMovement.MovementType.SALE,
                reference=invoice.sequence,
                created_by=salesman,
            )
        )

    if discount > sub_total:
        raise ValidationError("ডিসকাউন্ট মোট পরিমাণের (Subtotal) চেয়ে বেশি হতে পারবে না।")

    # ক্রেডিট তৈরি করা।
    InvoiceCreditDeductionService().deduct_credit(
        tenant=tenant, amount=1, reference=invoice.sequence, salesman=salesman
    )

    # স্যাসল মুভমেন্ট তৈরী।
    SaleItem.objects.bulk_create(sale_item_list)

    # স্টক মুভমেন্ট তৈরী।
    StockMovement.objects.bulk_create(stock_movement)

    invoice.subtotal = sub_total
    invoice.total = sub_total - discount
    invoice.save()
    serializer = InvoicesSerializer(invoice)
    return serializer.data
