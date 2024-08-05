from rest_framework import serializers

from .models import Booking, CustomUser, Room


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "last_name",
            "first_name",
            "birth_date",
            "telephone",
            "address",
            "email",
            "date_joined",
            "last_login",
            "is_active",
            "is_staff",
            "is_superuser",
        ]


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ["room_name", "place", "capacity", "price", "image", "availability"]


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ["id_room", "id_user", "room_name", "start_date", "end_date"]
