from rest_framework import status,viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.reservation.models import Booking, CustomUser, Room
from apps.reservation.serializers import (
    BookingSerializer,
    CustomUserSerializer,
    RoomSerializer,
)

class CustomUserViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
class RoomViewSet(viewsets.ModelViewSet):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = RoomSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        response_data = []
        for room in serializer.data:
            room['image'] = {'image': room['image']}  
            response_data.append(room)
        return Response({"data": response_data})
    
    def get_queryset(self):
        queryset=Room.objects.all()
        availability=self.request.query_params.get('availability')

        if availability is not None:
            queryset=queryset.filter(availability=availability)
        return queryset
        
    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

        
class BookingViewSet(viewsets.ModelViewSet):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = BookingSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    def get_queryset(self):
        queryset = Booking.objects.all()
        is_cancelled=self.request.query_params.get('is_cancelled')
        start_date=self.request.query_params.get('start_date')
        end_date=self.request.query_params.get('end_date')
        if is_cancelled is not None:
            queryset=queryset.filter(is_cancelled=is_cancelled)
        if start_date is not None and end_date is not None:
            queryset=queryset.filter(start_date__gte=start_date,end_date__lte=end_date)

        return queryset
        
    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)



        


