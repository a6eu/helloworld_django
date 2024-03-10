from django.urls import path
from . import views

urlpatterns = [
    path("basket/", views.BasketView.as_view()),
    path("basket/products/", views.ProductInBasketView.as_view()),
    path("basket/products/<int:pk>", views.RemoveOrPatchProductInBasketView.as_view()),

]