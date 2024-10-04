from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate

from .models import Booking, CustomUser, Room

from django.utils.translation import gettext_lazy as _


class CustomUserSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    last_name = serializers.CharField(max_length=255)
    first_name = serializers.CharField(max_length=255)
    birth_date = serializers.DateField()
    telephone = serializers.CharField(max_length=20)
    address = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    password = serializers.CharField()
    date_joined = serializers.DateTimeField(required=False)
    last_login = serializers.DateTimeField(required=False)
    is_active = serializers.BooleanField(required=False, default=True)
    is_staff = serializers.BooleanField(required=False,default=False)
    is_superuser = serializers.BooleanField(required=False,default=False)

    read_only_fields=["id","date_joined","last_login"]
   
    def create(self, validated_data):
        if CustomUser.objects.filter(email=validated_data['email']).exists():
            raise ValidationError({'email': 'A user with this email already exists.'})
    
        user = CustomUser(**validated_data)
        user.save()
        return user
        
class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ["id","room_name", "place", "capacity", "price", "image", "availability"]
        read_only_fields=["id","availability"]

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ["id","id_room", "id_user", "room_name", "start_date", "end_date","is_cancelled"]
        read_only_fields=["id","id_room","id_user","room_name","start_date","end_date","is_cancelled"]


