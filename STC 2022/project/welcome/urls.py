from django.urls import path
from . import views

app_name = "welcome"

urlpatterns = [
    path("", views.login, name="login"),
    path("signup/", views.signup, name="signup"),
]
