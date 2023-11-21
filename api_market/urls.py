from django.urls import path
from . import views

urlpatterns =[
    path("catalog/", views.ListCategoryView.as_view(), name='catalog')
]