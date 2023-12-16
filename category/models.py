from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
# Create your models here.


class Category(MPTTModel):
    name = models.CharField(max_length=255)
    img_url = models.ImageField(upload_to="01it.group/categories/", null=True)
    parent = TreeForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name="children")

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name


class ParentCategory(models.Model):
    child = models.ForeignKey(Category, related_name='child_categories', on_delete=models.CASCADE)
    parent = models.ForeignKey(Category, related_name='parent_categories', on_delete=models.CASCADE)