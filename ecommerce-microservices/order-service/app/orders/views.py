from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import Order, OrderItem
from .serializers import OrderSerializer
from .catalog_client import fetch_product, reserve_stock


class CreateOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user_id = request.user.id
        items = request.data.get("items", [])
        auth_header = request.headers.get("Authorization", "")
        if not items:
            return Response(
                {"error": "Order must contain items"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        total = 0
        validated_items = []

        for item in items:
            product = fetch_product(item["product_id"])
            if not product:
                return Response(
                    {"error": f"Product {item['product_id']} not found"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            price = float(product["price"])
            quantity = item["quantity"]
            remaining_stock = reserve_stock(item["product_id"], quantity, auth_header)
            if remaining_stock.status_code == 404:
                return Response(
                    {"error": f"Product {item['product_id']} not found"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            elif remaining_stock.status_code == 409:
                return Response(
                    {"error": f"Insufficient stock for product {item['product_id']}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            elif remaining_stock.status_code != 200:
                return Response(
                    {"error": "Error reserving stock"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
            total += price * quantity

            validated_items.append(
                (item["product_id"], quantity, price)
            )
        
        order = Order.objects.create(
            user_id=user_id,
            total_amount=total,
        )

        for product_id, quantity, price in validated_items:
            OrderItem.objects.create(
                order=order,
                product_id=product_id,
                quantity=quantity,
                price=price
            )
        
        return Response(
            OrderSerializer(order).data,
            status=status.HTTP_201_CREATED,
        )