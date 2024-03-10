from django.db import models
from custom_auth.models import UserProfile
from django.core import validators
from django.utils import timezone
from django.utils.functional import cached_property
from products.models import Product
# Create your models here.


class Basket(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    product = models.ManyToManyField(Product, through='ProductsInBasket')


class ProductsInBasket(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE, related_name='products')
    quantity = models.IntegerField(validators=[validators.MinValueValidator(1)])
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)