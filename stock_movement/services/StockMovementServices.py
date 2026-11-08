# ---Drf---
from rest_framework.exceptions import ValidationError

# ---Custom pagination---
from common.services.reusable_custom_pagination import reusable_custom_pagination

# ---Model---
from stock_movement.models import StockMovement

# ---Serializer---
from stock_movement.serializers import StockMovementSerializer


class StockMovementServices:
    def get_stock_movement(self, tenant, request, view_instance):
        # Get all Stock movement
        all_stock = StockMovement.objects.filter(tenant=tenant)
        return reusable_custom_pagination(
            queryset=all_stock,
            request=request,
            serializer_class=StockMovementSerializer,
            view_instance=view_instance,
            page_size=10,
        )

    def get_details_stock_movement(self, tenant, stock_movement_id):

        try:
            stock_movement = StockMovement.objects.get(
                tenant=tenant, id=stock_movement_id
            )
        except StockMovement.DoesNotExist:
            raise ValidationError("আপনার চাওয়া স্টক মুভমেন্টটি খুঁজে পাওয়া যায়নি।")

        serializ = StockMovementSerializer(instance=stock_movement)
        return serializ.data
