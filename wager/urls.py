from django.urls import path
from .views import pick1View


urlpatterns = [
    path("pick1/", pick1View.as_view(), name="pick1"),
]
