from django.urls import path
from . import views

urlpatterns = [
    path("my/orders/", views.OrderView.as_view(), name='view_orders'),
    path("admin/orders/", views.OrderListView.as_view(), name='view_orders_by_admin'),
    path("order/<int:pk>/", views.OrderDetailView.as_view(), name='update_order')

]