from django.urls import path
from . import views

urlpatterns = [
    path("brands/", views.BrandListView.as_view()),
    path("brands/<str:name>", views.BrandDetailView.as_view()),
    path('brands/<int:id>/', views.BrandUpdateAPIView.as_view(), name='brand-update'),
    path('brands/create/', views.BrandCreateAPIView.as_view(), name='brand-create'),
]