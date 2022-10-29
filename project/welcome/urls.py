from django.urls import path
from . import views

app_name = "welcome"

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path("accounts/", views.accounts, name="accounts"),
    path("sessions/", views.sessions, name="sessions"),
]
