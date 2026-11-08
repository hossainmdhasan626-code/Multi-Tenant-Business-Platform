# ---Model---
from stock_movement.models import StockMovement

# ---Serializer---
from stock_movement.serializers import StockMovementSerializer


def create_stock_movement(
    tenant, salesmen, product_data, movement_type, quantity, update_type=None
):

    if update_type:
        if update_type == "increment":
            quantity = abs(quantity)
        elif update_type == "decrement":
            quantity = -abs(quantity)

    data = StockMovement.objects.create(
        tenant=tenant,
        product=product_data,
        quantity=quantity,
        movement_type=movement_type,
        created_by=salesmen,
    )

    serializer = StockMovementSerializer(instance=data)

    return serializer.data
