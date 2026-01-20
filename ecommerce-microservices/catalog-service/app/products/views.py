from rest_framework.viewsets import ModelViewSet
from rest_framework import serializers
from rest_framework.permissions import AllowAny, IsAuthenticated

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction

from .models import Product
from .serializers import ProductSerializer

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        return [IsAuthenticated()]
    
    @action(
        detail=True,
        methods=["post"],
        url_path="reserve",
        permission_classes=[IsAuthenticated],
    )
    def reserve_stock(self, request, pk=None):
        quantity = request.data.get("quantity")

        if not quantity or quantity <= 0:
            return Response(
                {"detail": "Invalid quantity"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            with transaction.atomic():
                product = Product.objects.select_for_update().get(pk=pk)

                if product.in_stock < quantity:
                    return Response(
                        {"detail":"Insufficient stock"},
                        status=status.HTTP_409_CONFLICT,
                    )
                product.in_stock -= quantity
                product.save()
            
            return Response(
                {"remaining_stock":product.in_stock},
                status=status.HTTP_200_OK,
            )
        
        except Product.DoesNotExist:
            return Response(
                {"detail":"Product not found"},
                status=status.HTTP_404_NOT_FOUND
            )

