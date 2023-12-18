from django.urls import path
from . import views

urlpatterns = [
    path("product/<int:product_id>/comments/", views.CommentListCreateView.as_view(), name='comment_list'),
    path("product/<int:product_id>/comments/<int:pk>", views.CommentDetailView.as_view(), name="comment_update"),

]