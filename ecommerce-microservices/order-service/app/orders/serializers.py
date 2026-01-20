from rest_framework import serializers
from .models import Order, OrderItem


class OrderItemInputSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemInputSerializer(many=True)

    class Meta:
        model = Order
        fields = ["id", "items", "total_amount", "status", "created_at", "updated_at"]
        read_only_fields = ["total_amount", "status", "created_at", "updated_at"]
