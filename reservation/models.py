from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class CustomUserManager(BaseUserManager):
  def create_user(self, email, password, **extra_fields):
    if not email:
      raise ValueError("L'adresse e-mail est requise.")
    user = self.model(email=self.normalize_email(email), **extra_fields)
    user.set_password(password)
    user.save(using=self._db)
    return user

  def create_superuser(self, email, password, **extra_fields):
    extra_fields.setdefault("is_staff", True)
    extra_fields.setdefault("is_superuser", True)

    if extra_fields.get("is_staff") is not True:
      raise ValueError("Le superutilisateur doit avoir le statut is_staff=True.")
    if extra_fields.get("is_superuser") is not True:
      raise ValueError("Le superutilisateur doit avoir le statut is_superuser=True.")

    return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser):
  nom = models.CharField(max_length=255)
  prenom = models.CharField(max_length=255)
  date_naissance = models.DateField()
  telephone = models.CharField(max_length=20)
  adresse = models.CharField(max_length=255)
  email = models.EmailField(unique=True)
  date_joined = models.DateTimeField(auto_now_add=True)
  last_login = models.DateTimeField(auto_now=True)
  is_active = models.BooleanField(default=True)
  is_staff = models.BooleanField(default=False)
  is_superuser = models.BooleanField(default=False)

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['nom', 'prenom', 'date_naissance', 'telephone', 'adresse', 'email']

  objects = CustomUserManager()

  def __str__(self):
    return f"{self.nom} {self.prenom}"
