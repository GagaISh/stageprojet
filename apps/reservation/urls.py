from rest_framework import routers
from .api import CustomUserViewSet,RoomViewSet,BookingViewSet
from django.urls import path,include
from apps.reservation import views
from apps.reservation.views import *


router=routers.DefaultRouter()
router.register('user',CustomUserViewSet,basename='user')
router.register('room',RoomViewSet,basename='room')
router.register('booking',BookingViewSet,basename='booking')

urlpatterns = [
    path('api/',include(router.urls)),
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('addroom/', AddRoomView.as_view(), name='addroom'),
    path('booking/', BookingView.as_view(), name='booking'),
    path('', HomeView.as_view(), name='home'),
    path('admi/', views.dashboard, name='admin'),
    path('listroom/', ListRoomView.as_view(), name='listroom'),
    path('list-users/', ListUsersView.as_view(), name='list-users'),
    path('room-reserves/', ListReservesView.as_view(), name='room-reserves'),
    path('roomsavailable/', ListAvailableView.as_view(), name='roomsavailable'),
    
]   
    

