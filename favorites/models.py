from django.db import models
from custom_auth.models import UserProfile
from products.models import Product
# Create your models here.


class Favorites(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)