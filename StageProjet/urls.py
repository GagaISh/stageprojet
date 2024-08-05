from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path

from apps.reservation import views
from apps.reservation.views import *
from StageProjet import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("signup/", SignupView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    path("addroom/", AddRoomView.as_view(), name="addroom"),
    path("booking/", BookingView.as_view(), name="booking"),
    path("", HomeView.as_view(), name="home"),
    path("admi/", views.dashboard, name="admin"),
    path("listroom/", ListRoomView.as_view(), name="listroom"),
    path("api/users/", UsersListAPIView.as_view(), name="users"),
    path(
        "api/RoomReserveList/",
        RoomReserveListAPIView.as_view(),
        name="api/RoomReserveList/",
    ),
    path(
        "api/RoomAvailableList/",
        RoomAvailableListAPIView.as_view(),
        name="api/RoomAvailableList/",
    ),
    path("list-users/", ListUsersView.as_view(), name="list-users"),
    path("room-reserves/", ListReservesView.as_view(), name="room-reserves"),
    path("roomsavailable/", ListAvailableView.as_view(), name="roomsavailable"),
]
urlpatterns += staticfiles_urlpatterns()
