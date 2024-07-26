from django.urls import path
from .views import (
    UserMobileRegistrationView,
    OTPVerificationView,
    PersonalDetailRegistrationView,
    ActivateUserRegistrationView,
)

urlpatterns = [
    path("mobile", UserMobileRegistrationView.as_view(), name="mobile"),
    path("otp-verify/<str:token>", OTPVerificationView.as_view(), name="otp-verify"),
    path(
        "personal-detail/<str:token>",
        PersonalDetailRegistrationView.as_view(),
        name="personal-detail",
    ),
    path(
        "user-activate/<str:token>",
        ActivateUserRegistrationView.as_view(),
        name="user-activate",
    ),
]
