from django.db import models
from django.core.validators import RegexValidator


class Demand(models.Model):
    phone_number_regex = RegexValidator(
        regex=r'\d{10}$', message="Numbers without +7/8"
    )

    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(validators=[phone_number_regex],  max_length=10)
    email = models.EmailField(max_length=255, unique=True)
    description = models.TextField()




