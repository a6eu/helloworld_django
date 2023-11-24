from django.urls import path
from . import views

urlpatterns = [
    path("categories/", views.ListCategoryView.as_view(), name='categories'),
    path("products/<int:pk>", views.ProductDetailView.as_view(), name='product_detail'),
    path("products/", views.ProductListView.as_view(), name='product_list')

]