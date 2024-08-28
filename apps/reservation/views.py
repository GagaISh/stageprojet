import os
import re
import logging
from datetime import date, datetime, timedelta

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.core.mail import send_mail
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.dateparse import parse_date
from django.utils.decorators import method_decorator
from django.views import View   
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.paginator import Paginator
from decimal import Decimal

from apps.reservation.models import Booking, CustomUser, Room

from .forms import SignUpForm

logger = logging.getLogger(__name__)

class SignupView(FormView):
    template_name = "signup.html"
    form_class = SignUpForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class LoginView(TemplateView):
    template_name = "login.html"
    redirect_authenticated_user = True
    redirect_field_name = "next"

    def post(self, request):
        email = request.POST.get("email")
        password = request.POST.get("password")
        error_message = None
        if email is not None:
            email = email.lower()

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            request.session["user_id"] = user.id
            next_url = request.GET.get(self.redirect_field_name)
            protected_paths = [
                "/admi/",
                "/addroom/",
                "/listroom/",
                "/list-users/",
                "/list-reserves/",
                "/delete_room/",
                "update_room",
                "/delete_booking/",
                "/delete_user/",
            ]
            if next_url:
                if (
                    next_url in protected_paths
                    or re.match(r"^/update_room/\d+/?$", next_url)
                    or re.match(r"^/delete_booking/\d+/?$", next_url)
                    or re.match(r"^/delete_user/\d+/?$", next_url)
                ):
                    if email != "ishimwegraciella17@gmail.com":
                        return HttpResponseRedirect(reverse("home"))
                    else:
                        return HttpResponseRedirect(next_url)
                else:
                    return HttpResponseRedirect(next_url)
            else:
                return HttpResponseRedirect(reverse("home"))

        else:
            error_message = _("Identifiants incorrects")
        return render(request, "login.html", {"error": error_message})


def logout_user(request):
    logout(request)
    return redirect("home")


@method_decorator(login_required, name="dispatch")
class AddRoomView(View):
    template_name = "addroom.html"
    redirect_field_name = "next"

    def get(self, request):
        return render(request, self.template_name, {})

    def post(self, request):
        room_name = request.POST.get("room_name")
        place = request.POST.get("place")
        capacity = request.POST.get("capacity")
        price = request.POST.get("price")
        image = request.FILES.get("image")

        if room_name:
            room = Room(
                room_name=room_name,
                place=place,
                capacity=capacity,
                price=price,
                image=image,
            )
            room.save()
            return redirect("listroom")
        else:
            return HttpResponse(_("Room name is required."))

@method_decorator(login_required, name="dispatch")
class BookingView(TemplateView):
    template_name = "booking.html"
    redirect_field_name = "next"

    def get(self, request, room_id):
        room = Room.objects.get(id=room_id)
        return render(request, self.template_name, {"room": room})

    def post(self, request, room_id):
        user = self.request.user
        room_name = request.POST.get("room_name")
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")

        try:
            room = Room.objects.get(room_name=room_name)
            id_room = room.id
        except Room.DoesNotExist:
            error_message =_("Room name not found.")
            return render(
                request, "booking.html", {"error": error_message, "room": room}
            )

        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

        if start_date < date.today():
            error_message =_("Start date must be greater than or equal to today's date.")
            return render(
                request, "booking.html", {"error": error_message, "room": room}
            )

        if end_date < start_date:
            error_message =_("End date must be greater than or equal to start date.")
            return render(
                request, "booking.html", {"error": error_message, "room": room}
            )

        room = get_object_or_404(Room, id=id_room)
        if room.is_available(start_date, end_date):
            error_message =_("Room is not available for the selected dates.")
            return render(
                request, "booking.html", {"error": error_message, "room": room}
            )

        room.availability = False
        room.save()

        booking = Booking(
            id_user=user,
            id_room=room,
            room_name=room_name,
            start_date=start_date,
            end_date=end_date,
        )
        booking.save()
        
        return redirect("home")


class HomeView(View):
    template_name = "home.html"

    def get(self, request):
        room = Room.objects.all()
        paginator = Paginator(room,3)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        context = {
            "page_obj": page_obj,
            "is_paginated": page_obj.has_other_pages(),
        }
        
        return render(request, self.template_name, context)
        
@login_required
def dashboard(request):
    return render(request, "dashboard.html")


@method_decorator(login_required, name="dispatch")
class ListRoomView(TemplateView):
    template_name = "listroom.html"
    redirect_field_name = "next"
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        rooms = Room.objects.all().order_by("id")
        paginator = Paginator(rooms, 5)
        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        context["rooms"] = page_obj.object_list
        context["page_obj"] = page_obj
        context["is_paginated"] = page_obj.has_other_pages()
        return context

    def dispatch(self, request, *args, **kwargs):
        if "btn_filter" in request.GET:
            if request.GET.get("availability") != "Tous":
                if request.GET.get("availability") == "True":
                    avai = True
                else:
                    avai = False
                queryset = Room.objects.filter(availability=avai).order_by("id")
            else:
                queryset = Room.objects.all().order_by("id")
            return render(request, "listroom.html", {"rooms": queryset})
        elif "btn_SearchRoom" in request.GET:
            name = request.GET.get("search")
            if name:
                queryset = Room.objects.filter(
                    Q(room_name__icontains=name) | Q(place__icontains=name)
                )
                return render(request, "listroom.html", {"rooms": queryset})
        return super().dispatch(request, *args, **kwargs)


@method_decorator(login_required, name="dispatch")
class ListUsersView(TemplateView):
    template_name = "listusers.html"
    redirect_field_name = "next"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        users= CustomUser.objects.all().order_by("id")
        paginator = Paginator(users,10)
        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        context["users"] = page_obj.object_list
        context["page_obj"] = page_obj
        context["is_paginated"] = page_obj.has_other_pages()
        return context


@method_decorator(login_required, name="dispatch")
class ListReservesView(TemplateView):
    template_name = "listreserve.html"
    redirect_field_name = "next"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        bookings = Booking.objects.all().order_by("is_cancelled")
        paginator = Paginator(bookings,8)
        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        context["bookings"] = page_obj.object_list
        context["page_obj"] = page_obj
        context["is_paginated"] =page_obj.has_other_pages()
        return context

    def dispatch(self, request, *args, **kwargs):
        if "btn_filter" in request.GET:
            start_date = self.request.GET.get("start_date")
            end_date = self.request.GET.get("end_date")
            start_date = parse_date(start_date) if start_date else date.today()
            end_date = (
                parse_date(end_date) if end_date else date.today() + timedelta(days=30)
            )
            queryset = Booking.objects.filter(
                id_room__availability=False,
                start_date__gte=start_date,
                end_date__lte=end_date,
            ).select_related("id_room", "id_user")
            return render(request, "listreserve.html", {"bookings": queryset})

        if "btn_SearchBooking" in request.GET:
            search_query = request.GET.get("search")
            if search_query:
                queryset = Booking.objects.filter(
                    Q(id_user__email__icontains=search_query)
                    | Q(id_user__last_name__icontains=search_query)
                    | Q(id_user__first_name__icontains=search_query)
                    | Q(id_room__room_name__icontains=search_query)
                ).select_related("id_room", "id_user")
                return render(request, "listreserve.html", {"bookings": queryset})
            
        return super().dispatch(request, *args, **kwargs)
    

@login_required
def delete_room(self, room_id):
    room = Room.objects.get(id=room_id)
    room.delete()
    return redirect(reverse("listroom"))


@method_decorator(login_required, name="dispatch")
class UpdateRoomView(TemplateView):
    template_name = "update_room.html"
    redirect_field_name = "next"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        room_id = kwargs.get("room_id")
        room = get_object_or_404(Room, id=room_id)
        context["room"] = room
        return context

    def post(self, request, room_id):
        room = get_object_or_404(Room, id=room_id)
        room.room_name = request.POST.get("room_name")
        room.place = request.POST.get("place")
        room.capacity = request.POST.get("capacity")
        room.price = Decimal(request.POST.get("price"))
        if "image" in request.FILES:
            room.image = request.FILES["image"]
        room.save()
        return redirect("listroom")


@login_required
def delete_booking(request, booking_id):
    booking = Booking.objects.get(id=booking_id)
    room = booking.id_room
    room.availability = True
    room.save()
    booking.delete()
    return redirect(reverse("list-reserves"))


class CancelBookingView(View):
      
      def post(self, request, booking_id):
        booking = Booking.objects.get(id=booking_id)
        room = booking.id_room
        booking.is_cancelled = True
        booking.save()

        has_other_reservations = Booking.objects.filter(
            id_room=room, 
            is_cancelled=False,
            start_date__gt=timezone.now()
        ) | Booking.objects.filter(
            id_room=room, 
            is_cancelled=False,
            start_date__lte=timezone.now(), 
            end_date__gte=timezone.now()
        )
    
        if  has_other_reservations.exists():
            room.availability = False
            logger.info(f"Booking cancelled. Room availability: {room.availability}")
        else:
            room.availability = True
            logger.info(f"Booking cancelled. Room availability: {room.availability}")
        room.save()
        return redirect('reservationclient')

   
@login_required
def delete_user(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    user.delete()
    return redirect(reverse("list-users"))


@method_decorator(login_required, name="dispatch")
class ContactView(TemplateView):
    template_name = "contact.html"
    redirect_field_name = "next"

    def get(self, request):
        user = request.user
        return render(request, self.template_name, {"user": user})

    def post(self, request):
        last_name = request.POST.get("last_name")
        first_name = request.POST.get("first_name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        subject = f"Message de {last_name}"
        body = f"""
        {_("Last Name:")} {last_name}
        {_("First Name:")} {first_name}
        {_("Email:")} {email}
        {_("Message:")} {message}
        """
        send_mail(subject, body, email, ["ishimwegraciella17@gmail.com"])

        return redirect(
            reverse("confirmation")
            + f"?last_name={last_name}&first_name={first_name}&email={email}"
        )


@method_decorator(login_required, name="dispatch")
class ConfirmationView(TemplateView):
    template_name = "confirmation.html"
    redirect_field_name = "next"

    def get(self, request, *args, **kwargs):
        last_name = request.GET.get("last_name")
        first_name = request.GET.get("first_name")
        email = request.GET.get("email")

        context = {"last_name": last_name, "first_name": first_name, "email": email}
        return render(request, self.template_name, context)



class ReservationClientView(TemplateView):
    template_name = "reservationclient.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["datas"] = Booking.objects.filter(
            id_user= self.request.user
        ).select_related("id_room", "id_user")
        return context

    def dispatch(self, request, *args, **kwargs):
        user = self.request.user

        if "btn_filter" in request.GET:
            
            start_date = self.request.GET.get("start_date")
            end_date = self.request.GET.get("end_date")
            start_date = parse_date(start_date) if start_date else date.today()
            end_date = (
                parse_date(end_date) if end_date else date.today() + timedelta(days=30)
            )
            queryset = Booking.objects.filter(
                id_user=user,
                id_room__availability=False,
                start_date__gte=start_date,
                end_date__lte=end_date,
            ).select_related("id_room", "id_user")
            return render(request, "reservationclient.html", {"datas": queryset})

        if "btn_SearchBooking" in request.GET:
            search_query = request.GET.get("search")
            if search_query:
                queryset = Booking.objects.filter(
                    id_user=user
                ).filter(
                    Q(id_room__room_name__icontains=search_query) |
                    Q(id_room__place__icontains=search_query)
                ).select_related("id_room", "id_user")
                return render(request, "reservationclient.html", {"datas": queryset})
            
        if "btn-cancel" in request.GET:
             return self.cancel_booking(request)
        return super().dispatch(request, *args, **kwargs)
