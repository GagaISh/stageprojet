from django.urls import path,include
from rest_framework import routers
from reservation.views import (
    SignupViewSet, LoginViewSet, AddRoomViewSet, BookViewSet,
    ListsViewSet, ListsReservesViewSet, HomeViewSet,
    ListsRoomsBookViewSet, ListsRoomsAvailableViewSet,LoginView, BookingView, DashboardView,
    RoomView, BookingRoomView, AddRoomView, UsersView,SignupView
)

router = routers.DefaultRouter()
router.register(r'signup', SignupViewSet, basename='signup')
router.register(r'login', LoginViewSet, basename='login')
router.register(r'addroom', AddRoomViewSet, basename='addroom')
router.register(r'book', BookViewSet, basename='book')
router.register(r'lists', ListsViewSet, basename='lists')
router.register(r'listsreserves', ListsReservesViewSet, basename='listsreserves')
router.register(r'home', HomeViewSet, basename='home')
router.register(r'listsroomsbook', ListsRoomsBookViewSet, basename='listsroomsbook')
router.register(r'listsroomsavailable', ListsRoomsAvailableViewSet, basename='listsroomsavailable')

urlpatterns = [
    path('api/', include(router.urls)),
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('booking/', BookingView.as_view(), name='booking'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('room/', RoomView.as_view(), name='room'),
    path('booking-room/', BookingRoomView.as_view(), name='booking-room'),
    path('add-room/', AddRoomView.as_view(), name='add-room'),
    path('users/', UsersView.as_view(), name='users'),
  
   
]