from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from custom_auth.models import UserProfile

from django.utils import timezone


class Question(models.Model):
    question_text = models.CharField(max_length=255)

    def str(self):
        return f"question text : {self.question_text} "


class Tag(models.Model):
    name = models.CharField(max_length=255)


class Brand(models.Model):
    name = models.CharField(unique=True, max_length=255)
    description = models.TextField()
    logo_url = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Category(MPTTModel):
    name = models.CharField(max_length=255)
    img_url = models.CharField(max_length=255)
    parent = TreeForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name="children")

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name


class ParentCategory(models.Model):
    child = models.ForeignKey(Category, related_name='child_categories', on_delete=models.CASCADE)
    parent = models.ForeignKey(Category, related_name='parent_categories', on_delete=models.CASCADE)


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    rating_total = models.DecimalField(max_digits=5, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    img_url = models.CharField(max_length=255)
    quantity = models.IntegerField()

    def __str__(self):
        return self.name


class ProductTags(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)


class OrderedProducts(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey('Order', on_delete=models.CASCADE)


class Order(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    status = models.ForeignKey('PaymentStatus', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()


class PaymentStatus(models.Model):
    status = models.CharField(max_length=255)

    def __str__(self):
        return self.status


class Basket(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    product = models.ManyToManyField(Product, through='ProductsInBasket')


class ProductsInBasket(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE)
    quantity = models.IntegerField()


class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    content = models.TextField()
    rating = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)


class Favorites(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)


class Reply(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
