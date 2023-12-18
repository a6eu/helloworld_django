from django.urls import path
from . import views

urlpatterns = [
    path("favorites/products", views.FavoritesListView.as_view()),
    path("favorites/products/<int:pk>", views.FavoritesAddDeleteView.as_view())

]