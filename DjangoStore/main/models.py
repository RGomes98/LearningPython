from django.contrib.auth.models import User
from django.db import models


class Cart(models.Model):
    is_purchased = models.BooleanField(default=False)
    purchased_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.owner}"[0].upper() + f"{self.owner}'s Cart"[1:] + f" - Purchased: {self.is_purchased}"


class Product(models.Model):
    description = models.TextField()
    name = models.CharField(max_length=255)
    image = models.CharField(max_length=255)
    quantity = models.IntegerField(default=1)
    updated_at = models.DateTimeField(auto_now=True)
    added_at = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)
    belongs_to = models.ForeignKey(Cart, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
