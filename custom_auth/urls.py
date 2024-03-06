from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from . import views

urlpatterns = [
    path("users/login/", views.UserLoginView.as_view(), name='token_obtain_pair'),
    path("refresh/", TokenRefreshView.as_view(), name='token_refresh'),
    path("users/", views.RegisterUserView.as_view(), name='registration'),
    # path("users/<int:pk>/", views.UserUpdateAPIView.as_view(), name='update'),
    path("users/profile/", views.UserUpdateAPIView.as_view(), name='profile'),
    path("users/profile/all", views.UserListView.as_view(), name='profile'),
    path('password-reset-request/', views.PasswordResetRequestAPIView.as_view(), name='password_reset_request'),
    path('password-reset-confirm/', views.PasswordResetCompleteAPIView.as_view(), name='password_reset_confirm'),
]
