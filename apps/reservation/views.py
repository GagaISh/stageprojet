import os

from django.contrib.auth import authenticate, login
from django.core.files.storage import default_storage
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.utils import timezone
import zoneinfo

from apps.reservation.models import Booking, CustomUser, Room
from .api import CustomUsersListAPIView,RoomAvailableListAPIView,RoomReserveListAPIView

from .forms import SignUpForm

class SignupView(FormView):
    template_name = "signup.html"
    form_class = SignUpForm
    success_url = "/"

    def get_success_url(self):
        return reverse("home")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class LoginView(View):
    template_name = "login.html"

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("booking")

        context = {"page": "login"}
        return render(request, self.template_name, context)

    def post(self, request):
        email = request.POST.get("email")
        password = request.POST.get("password")
        if email is not None:
            email = email.lower()
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            user = None

        if user is None:
            user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            request.session["user_id"] = user.id

            if user.email == "ishimwegraciella@gmail.com":
                return redirect("admin")
            else:
                return redirect("booking")
        else:
            error_message = "Incorrect identifiers"
            print(f"Login failed: {error_message}")
            return render(request, "login.html", {"error": error_message})


class AddRoomView(View):
    template_name = "addroom.html"

    def post(self, request):
        room_name = request.POST.get("room_name")
        place = request.POST.get("place")
        capacity = request.POST.get("capacity")
        price = request.POST.get("price")
        image = request.FILES.get("image")

        if room_name:
            room = Room(
                room_name=room_name, place=place, capacity=capacity, price=price
            )
            if image:
                image_path = os.path.join("static", "images", image.name)
                Room.image = image_path
                with default_storage.open(image_path, "wb") as dest:
                    for chunk in image.chunks():
                        dest.write(chunk)
            room.save()
            return redirect("listroom")
        else:
            return HttpResponse("Le nom de la salle est requis.")

    def get(self, request):
        return render(request, self.template_name, {})


class BookingView(View):
    template_name = "booking.html"

    def post(self, request):
        id_user = request.session.get("user_id")
        id_room = request.POST.get("room_id")
        room_name = request.POST.get("room_name")
        start_date= request.POST.get("start_date")
        end_date = request.POST.get("end_date")

        try:
            room = Room.objects.get(room_name=room_name)
            id_room = room.id
        except Room.DoesNotExist:
            return HttpResponseBadRequest("Room name not found")
        
        print(f"Retrieved id_room: {id_room}")
        print(f"Retrieved id_user: {id_user }")

        custom_user = get_object_or_404(CustomUser, id=id_user)
        room = get_object_or_404(Room, id=id_room)
        response = Booking(
            id_user=custom_user,
            id_room=room,
            room_name=room_name,
            start_date=start_date,
            end_date=end_date,
            
        )
        response.save()

        room.availability = False
        room.save()

        return redirect("room-reserves")

    def get(self, request):
        return render(request, self.template_name, {"form": "form"})

class HomeView(View):
    def get(self, request):
        return render(request, "home.html")


def dashboard(request):
    return render(request, "dashboard.html")


class ListRoomView(TemplateView):
    template_name = "listroom.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["datas"] = Room.objects.all()
        return context


class ListUsersView(TemplateView):
    template_name = "listusers.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["datas"] = CustomUser.objects.order_by('id')
        return context


class ListReservesView(TemplateView):
    template_name = "listreserve.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["datas"] = Booking.objects.filter(id_room__availability=False).select_related('id_room', 'id_user')
        return context


class ListAvailableView(TemplateView):
    template_name = "listroomavailable.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["datas"] = Room.objects.filter(availability=True)
        return context
