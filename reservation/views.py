from django.http import HttpResponse
from django.shortcuts import render, redirect
from reservation.models import CustomUser
from .forms import InscriptionForm
from django.contrib.auth import login, authenticate


def inscription(request):
  if request.method == 'POST':
    form = InscriptionForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request)
      return redirect('accueil') 
  else:
    form = InscriptionForm()
  return render(request, 'inscription.html', {'form': form})


def accueil(request):
    return render(request, "accueil.html")

def login(request):
    return render(request, "login.html")

def signUp(request):
    return render(request, "inscription.html")

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







