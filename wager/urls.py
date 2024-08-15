from django.urls import path
from .views import (
    pick1View,
    placingPick1View,
    confirmingPick1View,
)


urlpatterns = [
    path("pick1/", pick1View.as_view(), name="pick1"),
    path("pick1/place/", placingPick1View.as_view(), name="placing-pick1"),
    path(
        "pick1/confirm/",
        confirmingPick1View.as_view(),
        name="confirm-pick1",
    ),
]
