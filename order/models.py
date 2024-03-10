from django.db import models
from custom_auth.models import UserProfile
from django.core import validators
from django.utils import timezone
from django.utils.functional import cached_property
from products.models import Product
# Create your models here.
from django.core.validators import RegexValidator

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
    price = models.DecimalField(null=True, decimal_places=2, max_digits=10)

    @cached_property
    def cost(self):
        return round(self.quantity * self.price, 2)

    def __str__(self):
        return f"id: {self.id} order: {self.order} price: {self.price}  quantity: {self.quantity} created_at: {self.created_at}"


class Order(models.Model):
    PENDING = "P"
    COMPLETED = "C"
    ON_THE_WAY = "O"

    STATUS_CHOICES = [
        (PENDING, "pending"),
        (COMPLETED, "completed"),
        (ON_THE_WAY, 'on_the_way')
    ]
    phone_number_regex = RegexValidator(
        regex=r'\d{10}$', message="Numbers without +7/8"
    )

    user = models.ForeignKey(UserProfile, related_name="orders", on_delete=models.CASCADE)
    payment_status = models.ForeignKey(PaymentStatus, related_name="payments", on_delete=models.CASCADE)
    address = models.CharField(max_length=255, null=False)
    floor = models.IntegerField(null=True)
    flat = models.IntegerField(null=True)
    comment_for_address = models.TextField(null=True)
    recipient_name = models.CharField(max_length=100, null=True)
    recipient_phone = models.CharField(validators=[phone_number_regex], null=True,  max_length=10)
    order_status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=PENDING)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    product = models.ManyToManyField(Product, through='OrderedProducts')


    @cached_property
    def total_cost(self):
        """
        Total cost of all the items in an order
        """
        return round(sum([order_item.cost for order_item in self.order_items.all()]), 2)