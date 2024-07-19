from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import View
from reservation.models import CustomUser,Salle,Reservation
from .forms import InscriptionForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
import os
from django.core.files.storage import default_storage
from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from reservation.serializers import CustomUserSerializer, SalleSerializer, ReservationSerializer
from rest_framework import status


class SignupView(View):
    def get(self, request):
        form = InscriptionForm()
        return render(request, 'inscription.html', {'form': form})

    def post(self, request):
        form = InscriptionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accueil')
        else:
            return render(request, 'inscription.html', {'form': form})

class ConnexionView(View):
    def get(self, request):
        page = 'login'
        context = {'page': page}
        return render(request, 'login.html', context)

    def post(self, request):
        page = 'login'
        email = request.POST.get('email').lower()
        password = request.POST.get('password')
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
                return redirect('reservation')
        else:
            context = {'page': page, 'error': 'Identifiants incorrects'}
            return render(request, 'login.html', context)


class AjoutSalleView(View):
    def get(self, request):
        return render(request, 'ajoutsalle.html', {})

    def post(self, request):
        nom = request.POST.get('nom')
        lieu = request.POST.get('lieu')
        capacite = request.POST.get('capacite')
        prix = request.POST.get('prix')
        image = request.FILES.get('image')

        salle = Salle(nom_de_salle=nom, lieu=lieu, capacite=capacite, prix=prix)
        if image:
            image_path = os.path.join('static', 'images', image.name)
            salle.image = image_path
            with default_storage.open(image_path, 'wb') as dest:
                for chunk in image.chunks():
                    dest.write(chunk)
        salle.save()
        return redirect('listessalle')

class ReserverView(View):
    def get(self, request):
        return render(request, 'reservation.html', {'form': "form"})

    def post(self, request):
        numero_salle = request.POST.get('numero')
        datedebut = request.POST.get('datedebut')
        datefin = request.POST.get('datefin')
        id_user = request.session.get('user_id')
        try:
            salle = Salle.objects.get(numero_de_salle=numero_salle)
        except Salle.DoesNotExist:
            return render(request, 'reservation.html', {'error': 'Salle introuvable'})

        reservation = Reservation(numero_de_salle=salle, datedebut=datedebut, datefin=datefin, id_user=id_user)
        reservation.save()
        if not Reservation.objects.filter(numero_de_salle=salle, datedebut__lte=datedebut, datefin__gte=datefin).exists():
            salle.disponibilite = True
        else:
            salle.disponibilite = False

        salle.save()

        return redirect('listereserve')

class ListesView(View):
    def get(self, request):
        donnees = CustomUser.objects.all()
        return render(request, 'listedata.html', {'donnees': donnees})
class ListesReservesView(View):
    def get(self, request):
        donnees = Reservation.objects.all()
        return render(request, 'listeReserve.html', {'donnees': donnees})
class AccueilView(View):
    def get(self, request):
        donnees = Salle.objects.all()
        return render(request, "accueil.html", {'donnees': donnees})
class ListesSallesReserveView(View):
    def get(self, request):
        donnees = Salle.objects.filter(disponibilite=False)
        return render(request, 'listesalle.html', {'donnees': donnees})
class ListesSallesDisponibleView(View):
    def get(self, request):
        donnees = Salle.objects.filter(disponibilite=True)
        return render(request, 'listesalledisponible.html', {'donnees': donnees})

class CustomUserListView(APIView):
    def get(self, request):
        customusers = CustomUser.objects.all()
        serializer = CustomUserSerializer(customusers, many=True)
        return Response(serializer.data)

class CustomUserDetailView(APIView):
    def get(self, request, pk):
        customuser = CustomUser.objects.get(pk=pk)
        serializer = CustomUserSerializer(customuser)
        return Response(serializer.data)

class CustomUserUpdateView(APIView):
    def put(self, request, pk):
        customuser = CustomUser.objects.get(pk=pk)
        serializer = CustomUserSerializer(customuser, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SalleListView(APIView):
    def get(self, request):
        salles = Salle.objects.all()
        serializer = SalleSerializer(salles, many=True)
        return Response(serializer.data)

class SalleDetailView(APIView):
    def get(self, request, pk):
        salle = Salle.objects.get(pk=pk)
        serializer = SalleSerializer(salle)
        return Response(serializer.data)

class SalleUpdateView(APIView):
    def put(self, request, pk):
        salle = Salle.objects.get(pk=pk)
        serializer = SalleSerializer(salle, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReservationListView(APIView):
    def get(self, request):
        reservations = Reservation.objects.all()
        serializer = ReservationSerializer(reservations, many=True)
        return Response(serializer.data)

class ReservationDetailView(APIView):
    def get(self, request, pk):
        reservation = Reservation.objects.get(pk=pk)
        serializer = ReservationSerializer(reservation)
        return Response(serializer.data)

class ReservationUpdateView(APIView):
    def put(self, request, pk):
        reservation = Reservation.objects.get(pk=pk)
        serializer = ReservationSerializer(reservation, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(View):
    def get(self, request):
        return render(request, "login.html")

class InscriptionView(View):
    def get(self, request):
        return render(request, "inscription.html")

class ReservationView(View):
    def get(self, request):
        return render(request, "reservation.html")

class DashboardView(View):
    def get(self, request):
        return render(request, "dashboard.html")

class SalleView(View):
    def get(self, request):
        return render(request, "accueil.html")

class ReservationSalleView(View):
    def get(self, request):
        return render(request, "accueil.html")

class AjouterSalleView(View):
    def get(self, request):
        return render(request, "ajoutsalle.html")

class UtilisateursView(View):
    def get(self, request):
        return render(request, "accueil.html")







