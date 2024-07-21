from reservation.models import CustomUser,Room,Booking
from .forms import SignUpForm
from django.contrib.auth import login, authenticate
import os
from django.core.files.storage import default_storage
from django.shortcuts import render, redirect
from rest_framework.response import Response
from reservation.serializers import CustomUserSerializer, RoomSerializer, BookingSerializer
from rest_framework import status
from rest_framework import viewsets, generics
from django.views.generic import TemplateView

class SignupViewSet(viewsets.ViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def list(self, request):
        form = SignUpForm()
        return render(request, 'signup.html', {'form': form})

    def create(self, request):
        form = SignUpForm(request.data)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            return render(request, 'signup.html', {'form': form})

class LoginViewSet(viewsets.ViewSet):
    def create(self, request):
        email = request.data.get('email').lower()
        password = request.data.get('password')
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            request.session['user_id'] = user.id
            if user.email == "ishimwegraciella@gmail.com":
                return redirect('admin')
            else:
                return redirect('booking')
        else:
            context = {'error': 'Incorrect identifiers'}
            return Response(context, status=status.HTTP_400_BAD_REQUEST)


class AddRoomViewSet(viewsets.ViewSet):
    def create(self, request):
        room_name = request.data.get('room_name')
        place = request.data.get('place')
        capacity = request.data.get('capacity')
        price = request.data.get('price')
        image = request.FILES.get('image')

        room = Room(room_name=room_name, place=place, capacity=capacity, price=price)
        if image:
            image_path = os.path.join('static', 'images', image.name)
            room.image = image_path
            with default_storage.open(image_path, 'wb') as dest:
                for chunk in image.chunks():
                    dest.write(chunk)
        room.save()
        return redirect('roomlist')

class BookViewSet(viewsets.ViewSet):
    def create(self, request):
        room_number = request.data.get('number')
        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date')
        id_user = request.session.get('user_id')
        try:
            room = Room.objects.get(room_Number=room_number)
        except Room.DoesNotExist:
            return Response({'error': 'Room not found'}, status=status.HTTP_404_NOT_FOUND)

        booking = Booking(room_Number=room, Start_date=start_date, end_date=end_date, id_user=id_user)
        booking.save()
        if not Booking.objects.filter(room_Number=room, Start_date__lte=start_date, end_date__gte=end_date).exists():
            room.availability = True
        else:
            room.availability = False

        room.save()

        return redirect('list_reserve')

class ListsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
class ListsReservesViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
class HomeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
class ListsRoomsBookViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Room.objects.filter(availability=False)
    serializer_class = RoomSerializer
class ListsRoomsAvailableViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Room.objects.filter(availability=True)
    serializer_class = RoomSerializer

class CustomUserListView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
class CustomUserDetailView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
class CustomUserUpdateView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

class RoomListView(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
class RoomDetailView(generics.RetrieveAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
class RoomUpdateView(generics.UpdateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

class BookingListView(generics.ListAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
class BookingDetailView(generics.RetrieveAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
class BookingUpdateView(generics.UpdateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

class LoginView(TemplateView):
    template_name = "login.html"

class SignUpView(TemplateView):
    template_name = "signup.html"

class BookingView(TemplateView):
    template_name = "booking.html"

class DashboardView(TemplateView):
    template_name = "dashboard.html"

class RoomView(TemplateView):
    template_name = "home.html"

class BookingRoomView(TemplateView):
    template_name = "home.html"

class AddRoomView(TemplateView):
    template_name = "addRoom.html"

class UsersView(TemplateView):
    template_name = "home.html"






