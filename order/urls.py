from django.urls import path
from . import views

urlpatterns = [
    path("order/", views.OrderView.as_view(), name='view_order'),
    path("order/<int:pk>", views.OrderDetailView.as_view(), name='update_order')

]