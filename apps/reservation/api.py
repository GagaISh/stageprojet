from rest_framework import status,viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils.translation import gettext_lazy as _
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

from apps.reservation.models import Booking, CustomUser, Room
from apps.reservation.serializers import (
    BookingSerializer,
    CustomUserSerializer,
    RoomSerializer,
    AuthTokenSerializer,
)

class CustomUserViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
class RoomViewSet(viewsets.ModelViewSet):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = RoomSerializer

    def get_queryset(self):
        queryset=Room.objects.all()
        availability=self.request.query_params.get('availability')

        if availability is not None:
            queryset=queryset.filter(availability=availability)
        return queryset
        
    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

        
class BookingViewSet(viewsets.ModelViewSet):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = BookingSerializer

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

class CustomObtainAuthToken(ObtainAuthToken):
    serializer_class = AuthTokenSerializer

    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=authenticate(email=serializer.validated_data['email'],password=serializer.validated_data['password'])
        if user is not None:
            token,created=Token.objects.get_or_create(user=user)
            return Response({'token':token.key},status=status.HTTP_200_OK)
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        


