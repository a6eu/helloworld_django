from django.urls import path
from . import views

urlpatterns = [
    path("products/<int:pk>", views.ProductDetailView.as_view(), name='product_detail'),
    path("products/", views.ProductListCreateView.as_view(), name='product_list'),
]