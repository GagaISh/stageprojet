from django.http import HttpResponse
from django.shortcuts import render
from reservation.models import User

def accueil(request):
    return render(request, "accueil.html")

def login(request):
    return render(request, "login.html")

def signUp(request):
    User.objects.create()
    return render(request, "signup.html")

def Formulairereservation(request):
    return render(request, "reservation.html")

def dashboard(request):
    return render(request, "dashboard.html")

def salle(request):
    return render(request, "accueil.html")

def reservationSalle(request):
    return render(request, "accueil.html")

def ajouterSalle(request):
    return render(request, "ajoutsalle.html")

def utilisateurs(request):
    return render(request, "accueil.html")







