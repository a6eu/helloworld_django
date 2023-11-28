from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from . import views
urlpatterns = [
    path("users/login/", TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path("refresh/", TokenRefreshView.as_view(), name='token_refresh'),
    path("users/", views.RegisterUserView.as_view(), name='registration'),

    # path("users/<int:pk>/", views.UserUpdateAPIView.as_view(), name='update')
    path("users/profile/", views.UserUpdateAPIViews.as_view(), name='update')
]