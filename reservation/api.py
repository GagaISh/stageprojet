from  django.urls import path
from reservation.views import(
        CustomUserListView,CustomUserDetailView,CustomUserUpdateView,
        RoomListView,RoomDetailView,RoomUpdateView,BookingListView,
        BookingDetailView,BookingUpdateView)

urlpatterns = [
    path('api/custom-users/', CustomUserListView.as_view(), name='custom-users-list-api'),
    path('api/custom-users/<int:pk>/', CustomUserDetailView.as_view(), name='custom-users-detail-api'),
    path('api/custom-users/<int:pk>/update/', CustomUserUpdateView.as_view(), name='custom-users-update-api'),
    path('api/rooms/', RoomListView.as_view(), name='rooms-list-api'),
    path('api/rooms/<int:pk>/', RoomDetailView.as_view(), name='rooms-detail-api'),
    path('api/rooms/<int:pk>/update/', RoomUpdateView.as_view(), name='rooms-update-api'),
    path('api/bookings/', BookingListView.as_view(), name='bookings-list-api'),
    path('api/bookings/<int:pk>/', BookingDetailView.as_view(), name='bookings-detail-api'),
    path('api/bookings/<int:pk>/update/', BookingUpdateView.as_view(), name='bookings-update-api'),
]