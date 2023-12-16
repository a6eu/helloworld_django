from django.db import models
from custom_auth.models import UserProfile
from django.core import validators
from django.utils import timezone
from django.utils.functional import cached_property
from products.models import Product
# Create your models here.


class PaymentStatus(models.Model):
    status = models.CharField(max_length=255)

    def __str__(self):
        return self.status


class OrderedProducts(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey('Order',  related_name="order_items", on_delete=models.CASCADE)
    quantity = models.IntegerField(null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    @cached_property
    def cost(self):
        return round(self.quantity * self.product.price, 2)


class Order(models.Model):
    user = models.ForeignKey(UserProfile, related_name="orders", on_delete=models.CASCADE)
    status = models.ForeignKey(PaymentStatus, on_delete=models.CASCADE)
    # cost = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    product = models.ManyToManyField(Product, through='OrderedProducts')

    @cached_property
    def total_cost(self):
        """
        Total cost of all the items in an order
        """
        return round(sum([order_item.cost for order_item in self.order_items.all()]), 2)