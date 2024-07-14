from django.http import HttpResponse
from django.shortcuts import render
from reservation.models import User

def accueil(request):
    #return HttpResponse("<h1>Bienvenue sur notre page</h1>")
    #a = User.objects.get(id=1)
    return render(request, "accueil.html")

def login(request):
    #return HttpResponse("<h1>Se connecter</h1> <p>Merci</p>")
    return render(request, "login.html")

def signUp(request):
    #return HttpResponse("<h1>S'inscrire</h1>")
    User.objects.create()
    return render(request, "signup.html")

def Formulairereservation(request):
    #return HttpResponse("<h1>Reservez des maintenant</h1>")
    return render(request, "reservation.html")

def dashboard(request):
    #return HttpResponse("<h1>Bienvenue cher administrateur")
    return render(request, "dashboard.html")

def salle(request):
    #return HttpResponse("<h1>Liste des salles</h1>")
    return render(request, "accueil.html")

def reservationSalle(request):
    #return HttpResponse("<h1>Les salles deja reservees</h1>")
    return render(request, "accueil.html")

def ajouterSalle(request):
    #return HttpResponse("<h1>Ajouter une salle</h1>")
    return render(request, "ajoutsalle.html")

def utilisateurs(request):
    #return HttpResponse("<h1>Liste des utilisateurs</h1>")
    return render(request, "accueil.html")







