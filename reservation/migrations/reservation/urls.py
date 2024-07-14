from django.urls import path
from reservation import views

urlpatterns = [
    path("", views.home, name="home"),
]