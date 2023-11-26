from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class Question(models.Model):
    question_text = models.CharField(max_length=255)

    def __str__(self):
        return f"question text : {self.question_text} "


class Role(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=255, blank=True, null=True)
    birth_day = models.DateField(blank=True, null=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Category(MPTTModel):
    name = models.CharField(max_length=255)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

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
    rating_total = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    brand = models.ForeignKey('Brand', on_delete=models.SET_NULL, null=True)
    img_url = models.CharField(max_length=255)
    quantity = models.IntegerField()

    def __str__(self):
        return self.name


class OrderedProducts(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey('Order', on_delete=models.CASCADE)


class Order(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    status = models.ForeignKey('PaymentStatus', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()


class PaymentStatus(models.Model):
    status = models.CharField(max_length=255)

    def __str__(self):
        return self.status


class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)


class ProductsInBasket(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    basket = models.ForeignKey('Basket', on_delete=models.CASCADE)
    quantity = models.IntegerField()


class Brand(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    logo_url = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    content = models.TextField()
    rating = models.IntegerField()
    created_by = models.DateTimeField()


class Favorites(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Reply(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    content = models.TextField()
    created_by = models.DateTimeField()
