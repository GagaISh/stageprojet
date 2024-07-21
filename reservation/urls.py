from django.urls import path,include
from rest_framework import routers
from reservation.views import (
    SignupViewSet, LoginViewSet, AddRoomViewSet, BookViewSet,
    ListsViewSet, ListsReservesViewSet, HomeViewSet,
    ListsRoomsBookViewSet, ListsRoomsAvailableViewSet,
    CustomUserListView, CustomUserDetailView, CustomUserUpdateView,
    RoomListView, RoomDetailView, RoomUpdateView,
    BookingListView, BookingDetailView, BookingUpdateView,
    LoginView, SignUpView, BookingView, DashboardView,
    RoomView, BookingRoomView, AddRoomView, UsersView
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
    path('api/custom-users/', CustomUserListView.as_view(), name='custom-users-list-api'),
    path('api/custom-users/<int:pk>/', CustomUserDetailView.as_view(), name='custom-users-detail-api'),
    path('api/custom-users/<int:pk>/update/', CustomUserUpdateView.as_view(), name='custom-users-update-api'),
    path('api/rooms/', RoomListView.as_view(), name='rooms-list-api'),
    path('api/rooms/<int:pk>/', RoomDetailView.as_view(), name='rooms-detail-api'),
    path('api/rooms/<int:pk>/update/', RoomUpdateView.as_view(), name='rooms-update-api'),
    path('api/bookings/', BookingListView.as_view(), name='bookings-list-api'),
    path('api/bookings/<int:pk>/', BookingDetailView.as_view(), name='bookings-detail-api'),
    path('api/bookings/<int:pk>/update/', BookingUpdateView.as_view(), name='bookings-update-api'),
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('booking/', BookingView.as_view(), name='booking'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('room/', RoomView.as_view(), name='room'),
    path('booking-room/', BookingRoomView.as_view(), name='booking-room'),
    path('add-room/', AddRoomView.as_view(), name='add-room'),
    path('users/', UsersView.as_view(), name='users'),
]