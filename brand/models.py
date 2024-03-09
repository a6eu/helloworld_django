from django.db import models

# Create your models here.


class Brand(models.Model):
    name = models.CharField(unique=True, max_length=255)
    description = models.TextField(null=True, blank=True)
    logo_url = models.ImageField(upload_to="01it.group/brands/", null=True, blank= True)

    def __str__(self):
        return self.name
