from django.db import models

# Create your models here.
class User(models.Model):
    nom=models.fields.CharField(max_length=100)
    prenom=models.fields.CharField(max_length=100)
    datenaissance=models.fields.DateField()
    adresse=models.fields.CharField(max_length=50)
    telephone=models.fields.IntegerField()
    email=models.fields.EmailField()
    password=models.fields.CharField(max_length=20)
    

class salles(models.Model):
    nom=models.fields.CharField(max_length=50)
    lieu=models.fields.CharField(max_length=20)
    capacite=models.fields.IntegerField()
    prix=models.fields.IntegerField()