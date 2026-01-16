from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=255, unique=True, null=False, blank=False)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    in_stock = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Procut id: {self.id} - Product name: {self.name}"
    