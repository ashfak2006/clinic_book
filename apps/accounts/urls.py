from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    LoginView,
    SignUpView,
    UsernameLoginView,
    VerifyOTPView,
)

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("verify-otp/", VerifyOTPView.as_view(), name="verify_otp"),
    path("login/", LoginView.as_view(), name="login"),
    path("username-login/", UsernameLoginView.as_view(), name="username_login"),
]
