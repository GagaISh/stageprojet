from rest_framework import routers
from .api import CustomUserViewSet,RoomViewSet,BookingViewSet
from django.urls import path,include
from apps.reservation import views
from apps.reservation.views import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView 


router=routers.DefaultRouter()
router.register('user',CustomUserViewSet,basename='user')
router.register('room',RoomViewSet,basename='room')
router.register('booking',BookingViewSet,basename='booking')

urlpatterns = [
    path('api/',include(router.urls)),
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('addroom/', AddRoomView.as_view(), name='addroom'),
    path('booking/<int:room_id>', BookingView.as_view(), name='booking'),
    path('listroom/',ListRoomView.as_view(),name='listroom'),
    path('', HomeView.as_view(), name='home'),
    path('admi/', views.dashboard, name='admin'),
    path('list-users/', ListUsersView.as_view(), name='list-users'),
    path('list-reserves/', ListReservesView.as_view(), name='list-reserves'),
    path('delete_room/<int:room_id>/', views.delete_room, name='delete_room'),
    path('update_room/<int:room_id>/', views.UpdateRoomView.as_view(), name='update_room'),
    path('delete_booking/<int:booking_id>/', views.delete_booking, name='delete_booking'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
]
    
  

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

