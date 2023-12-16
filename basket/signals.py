from django.db.models.signals import post_save, post_migrate
from django.dispatch import receiver
from custom_auth.models import UserProfile
from .models import Basket
from django.apps import AppConfig


@receiver(post_save, sender=UserProfile)
def create_user_cart(sender, instance, created, **kwargs):
    if created:
        Basket.objects.create(user=instance, total_price=0.00)

# @receiver(post_save, sender=Basket)
# def create_product_in_basket(sender, instance, created, **kwargs):
#     if created:
#         ProductsInBasket.objects.create(basket=instance)




