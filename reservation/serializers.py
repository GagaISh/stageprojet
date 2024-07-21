from rest_framework import serializers
from .models import CustomUser, Room, Booking

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['last_name', 'first_name', 'birth_date', 'telephone', 'address', 'email', 'date_joined', 'last_login', 'is_active', 'is_staff', 'is_superuser']

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['room_name', 'place', 'capacity', 'price', 'image', 'availability']

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id_salle', 'id_user', 'room_name', 'Start_date', 'end_date']