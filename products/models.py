from django.db import models
from category.models import Category
from brand.models import Brand
# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=1000)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(null=True, blank=True)
    rating_total = models.DecimalField(max_digits=5, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, related_name="brands", on_delete=models.CASCADE, null=True)
    img_url = models.ImageField(upload_to="01it.group/products/", null=True, blank=True)
    quantity = models.IntegerField()

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=255)


class ProductTags(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)



