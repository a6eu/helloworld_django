from django.urls import path
from . import views

urlpatterns = [
    path("/brands", views.BrandListView.as_view()),
    path("/brands/<int:pk>", views.BrandDetailView.as_view()),
]