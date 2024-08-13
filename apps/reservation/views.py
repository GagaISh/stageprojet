import os


from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest,HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.utils.dateparse import parse_date
from datetime import date, timedelta
from django.db.models import Q



from apps.reservation.models import Booking, CustomUser, Room

from .forms import SignUpForm
from .serializers import RoomSerializer

class SignupView(FormView):
    template_name = "signup.html"
    form_class=SignUpForm

    def get(self, request):
        form=self.form_class() 
        return render(request,self.template_name,{"form":form})
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
            
        else:
            return self.render_to_response(self.get_context_data(form=form))


class LoginView(TemplateView):
    template_name="login.html"

    def post(self,request):
        email=request.POST.get("email")
        password = request.POST.get("password")
        error_message = None
        if email is not None:
            email = email.lower()

        user = authenticate(request, username=email, password=password)
       
        if user is not None:
            login(request,user)
            request.session["user_id"] = user.id
            return redirect("home")
                
        else:
            error_message = "Incorrect identifiers"
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
                room_name=room_name, place=place, capacity=capacity, price=price,image=image
            )
            room.save()
            return redirect("listroom")
        else:
            return HttpResponse("Le nom de la salle est requis.")

    def get(self, request):
        return render(request, self.template_name, {})


class BookingView(View):
   
    template_name = "booking.html"

    def get(self, request,room_id):
        #user=self.request.user
        room = Room.objects.get(id= room_id)
        return render(request, self.template_name,{'room':room})
    
    def post(self, request,room_id):
            user=self.request.user
            room_name = request.POST.get("room_name")
            start_date = request.POST.get("start_date")
            end_date = request.POST.get("end_date")

            try:
                room = Room.objects.get(room_name=room_name)
                id_room = room.id
            except Room.DoesNotExist:
                error_message = "Room name not found."
                return render(request, "booking.html", {"error": error_message})

            room = get_object_or_404(Room, id=id_room)
            if not room.is_available(start_date, end_date):
                error_message = "Room is not available for the selected dates."
                return render(request, "booking.html", {"error": error_message})

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
            messages.success(request, "Reservation réussie")
            return redirect("home")



class HomeView(View):
    template_name= "home.html"
    def get(self, request):
        room=Room.objects.all()
        context = {
            "Room":room
        }
        return render(request,self.template_name, context)

def dashboard(request):
    return render(request, "dashboard.html")




class ListRoomView(TemplateView):
    template_name = "listroom.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["datas"] = Room.objects.all().order_by('id')
        return context
    
    def dispatch(self, request, *args, **kwargs):
        if "btn_filter" in request.GET:
            if request.GET.get("availability") != "Tous":
                if request.GET.get("availability") == "True":
                    avai = True
                else:
                    avai = False
                queryset = Room.objects.filter(availability=avai).order_by('id')
            else:
                queryset = Room.objects.all().order_by('id')
            return render(request,"listroom.html",{"datas":queryset})
        elif "btn_SearchRoom" in request.GET:
            name = request.GET.get('search')
            if name:
                queryset = Room.objects.filter(
                    Q(room_name__icontains=name) |
                    Q(place__icontains=name)
                )
                return render(request, "listroom.html", {"datas": queryset})
        return super().dispatch(request, *args, **kwargs)



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
        context["datas"]=Booking.objects.filter(id_room__availability=False).select_related('id_room', 'id_user')
        return context 

    def dispatch(self,request, *args, **kwargs):
            if "btn btn_filter" in request.GET:
                start_date = self.request.GET.get('start_date')
                end_date = self.request.GET.get('end_date')
                start_date = parse_date(start_date) if start_date else date.today()
                end_date = parse_date(end_date) if end_date else date.today() + timedelta(days=30)
                queryset = Booking.objects.filter(
                            id_room__availability=False,
                            start_date__gte=start_date,
                            end_date__lte=end_date
                        ).select_related('id_room', 'id_user')
                return render(request,"listreserve.html",{"datas":queryset})
                
            if "btn_SearchBooking" in request.GET:
                search_query = request.GET.get('search')
                if search_query:
                    queryset = Booking.objects.filter(
                        Q(id_user__email__icontains=search_query) |
                        Q(id_user__last_name__icontains=search_query) |
                        Q(id_user__first_name__icontains=search_query) |
                        Q(id_room__room_name__icontains=search_query)
                    ).select_related('id_room', 'id_user')
                    return render(request, "listreserve.html", {"datas": queryset})
            return super().dispatch(request, *args, **kwargs) 


class RoomView(TemplateView):
    template_name = "listroom.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["datas"] = Room.objects.all().order_by('id')
        return context

    def dispatch(self, request, *args, **kwargs):
        if "btn-delete" in request.GET:
            room_id = request.GET.get("btn-delete")
            return redirect(reverse('delete_room', args=[room_id]))
        elif "btn_update" in request.GET:
            room_id = request.GET.get("btn_update")
            return redirect(reverse('update_room', args=[room_id]))
        return super().dispatch(request, *args, **kwargs)

def delete_room(self, room_id):
        room = Room.objects.get(id=room_id)
        room.delete()


class UpdateRoomView(TemplateView):
    template_name = "update_room.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        room_id = kwargs.get('room_id')
        room = get_object_or_404(Room, id=room_id)
        context['room'] = room
        return context

    def post(self, request, *args, **kwargs):
        room_id = kwargs.get('room_id')
        room = get_object_or_404(Room, id=room_id)
        room.room_name = request.POST.get('room_name')
        room.place = request.POST.get('place')
        room.capacity = request.POST.get('capacity')
        room.price = request.POST.get('price')
        if 'image' in request.FILES:
            room.image = request.FILES['image']
        room.save()
        return redirect('listroom')

def delete_booking(request, booking_id):
    booking = Booking.objects.get(id=booking_id)
    room = booking.id_room
    room.availability = True
    room.save()
    booking.delete()
    return redirect(reverse('list-reserves'))

def delete_user(request,user_id):
    user=CustomUser.objects.get(id=user_id)
    user.delete()
    return redirect(reverse('list-users'))