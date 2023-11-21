from django.urls import path
from . import views

urlpatterns =[
    path("api/v1/catalog", views.ListCategoryView.as_view(), name='catalog')
]