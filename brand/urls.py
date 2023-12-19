from django.urls import path
from . import views

urlpatterns = [
    path("brands/", views.BrandListView.as_view()),
    path("brands/<str:name>", views.BrandDetailView.as_view()),
]