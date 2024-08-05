from apps.reservation.serializers import CustomUserSerializer, RoomSerializer,BookingSerializer
from rest_framework import viewsets
from apps.reservation.models import CustomUser,Room,Booking
from rest_framework import generics

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset=CustomUser.objects.all()
    serializer_class=CustomUserSerializer

class RoomViewSet(viewsets.ModelViewSet):
    queryset=Room.objects.all()
    serializer_class=RoomSerializer

class BookingViewSet(viewsets.ModelViewSet):
    queryset=Booking.objects.all()
    serializer_class=BookingSerializer

class CustomUsersListAPIView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

class RoomReserveListAPIView(generics.ListCreateAPIView):
    queryset = Room.objects.filter(availability=False)
    serializer_class = RoomSerializer


class RoomAvailableListAPIView(generics.ListCreateAPIView):
    queryset = Room.objects.filter(availability=True)
    serializer_class = RoomSerializer