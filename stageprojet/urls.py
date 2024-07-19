"""
URL configuration for StageProjet project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from reservation.views import *
from stageprojet import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns



urlpatterns = [
    path('admin/', admin.site.urls),
<<<<<<< HEAD
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', ConnexionView.as_view(), name='connexion'),
    path('ajout_salle/', AjoutSalleView.as_view(), name='ajout_salle'),
    path('reserver/', ReserverView.as_view(), name='reserver'),
    path('liste/', ListesView.as_view(), name='liste'),
    path('liste_reserve/', ListesReservesView.as_view(), name='liste_reserve'),
    path('', AccueilView.as_view(), name='accueil'),
    path('liste_salles_reserve/', ListesSallesReserveView.as_view(), name='liste_salles_reserve'),
    path('liste_salles_disponible/', ListesSallesDisponibleView.as_view(), name='liste_salles_disponible'),
    path('customusers/', CustomUserListView.as_view(), name='customuser_list'),
    path('customusers/<int:pk>/', CustomUserDetailView.as_view(), name='customuser_detail'),
    path('customusers/<int:pk>/update/', CustomUserUpdateView.as_view(), name='customuser_update'),
    path('salles/', SalleListView.as_view(), name='salle_list'),
    path('salles/<int:pk>/', SalleDetailView.as_view(), name='salle_detail'),
    path('salles/<int:pk>/update/', SalleUpdateView.as_view(), name='salle_update'),
    path('reservations/', ReservationListView.as_view(), name='reservation_list'),
    path('reservations/<int:pk>/', ReservationDetailView.as_view(), name='reservation_detail'),
    path('reservations/<int:pk>/update/', ReservationUpdateView.as_view(), name='reservation_update'),
    path('login/', LoginView.as_view(), name='login'),
    path('inscription/', InscriptionView.as_view(), name='inscription'),
    path('reservation/', ReservationView.as_view(), name='reservation'),
    path('admi/', DashboardView.as_view(), name='admin'),
    path('salle/', SalleView.as_view(), name='salle'),
    path('reservation_salle/', ReservationSalleView.as_view(), name='reservation_salle'),
    path('ajouter_salle/', AjouterSalleView.as_view(), name='ajouter_salle'),
    path('utilisateurs/', UtilisateursView.as_view(), name='utilisateurs'),
=======
    path('',views.accueil),
    path('login/',views.login),
    path('inscription/',views.inscription),
    path('formulaire/',views.Formulairereservation),
    path('admi/',views.dashboard),
    path('salle/',views.salle),
    path('ajout/',views.ajouterSalle),
    path('reservationSalle/',views.reservationSalle),
    path('utilisateurs/',views.utilisateurs),
>>>>>>> a5424556905dca1bbfacb3a2b88e4557ae7460f9
]
urlpatterns += staticfiles_urlpatterns()


