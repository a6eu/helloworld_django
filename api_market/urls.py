from django.urls import path
from . import views

urlpatterns = [
    path("categories/", views.ListCategoryView.as_view(), name='categories'),
    path("products/<int:pk>", views.ProductDetailView.as_view(), name='product_detail'),
    path("products/", views.ProductListCreateView.as_view(), name='product_list'),
    path("product/<int:product_id>/comments/", views.CommentListCreateView.as_view(), name='comment_list'),
    path("product/<int:product_id>/comments/<int:pk>", views.CommentDetailView.as_view(), name="comment_update"),
    path("basket", views.BasketView.as_view()),
    path("basket/products", views.ProductInBasketView.as_view()),
    path("basket/products/<int:pk>", views.RemoveProductInBasketView.as_view()),
    path("favorites/products", views.FavoritesListView.as_view()),
    path("favorites/products/<int:pk>", views.FavoritesAddDeleteView.as_view())


]