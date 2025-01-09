from django.urls import path

from .views import (
    SignupAPIView,
    ChangePassword,
    RequestOTPAPIView,
    VerifyOTPAndChangePasswordAPIView,
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path("signup/", SignupAPIView.as_view()),  # URL for signup API endpoint
    path("signin/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("old_to_new_pass/<int:pk>/", ChangePassword.as_view(), name="change_password"),  # URL for change password API endpoint
    path("password-reset/request-otp/", RequestOTPAPIView.as_view(), name="request_otp"),
    path("password-reset/verify/", VerifyOTPAndChangePasswordAPIView.as_view(), name="verify_otp_change_password"),
]
