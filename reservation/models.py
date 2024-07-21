from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class CustomUserManager(BaseUserManager):
  def create_user(self, email, password, **extra_fields):
    if not email:
      raise ValueError("Email address is required.")
    user = self.model(email=self.normalize_email(email), **extra_fields)
    user.set_password(password)
    user.save(using=self._db)
    return user

  def create_superuser(self, email, password, **extra_fields):
    extra_fields.setdefault("is_staff", True)
    extra_fields.setdefault("is_superuser", True)

    if extra_fields.get("is_staff") is not True:
      raise ValueError("The superuser must have the status is_staff=True.")
    if extra_fields.get("is_superuser") is not True:
      raise ValueError("The superuser must have the status is_superuser=True.")

    return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser):
  last_name = models.CharField(max_length=255)
  first_name = models.CharField(max_length=255)
  birth_date = models.DateField()
  telephone = models.CharField(max_length=20)
  address = models.CharField(max_length=255)
  email = models.EmailField(unique=True)
  date_joined = models.DateTimeField(auto_now_add=True)
  last_login = models.DateTimeField(auto_now=True)
  is_active = models.BooleanField(default=True)
  is_staff = models.BooleanField(default=False)
  is_superuser = models.BooleanField(default=False)

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = [' last_name', 'first_name', 'birth_date', 'telephone', 'address', 'email']

  objects = CustomUserManager()

  def __str__(self):
    return f"{self.last_name} {self.first_name}"
  
class Room(models.Model):
    room_name = models.CharField(max_length=100)
    place = models.CharField(max_length=100)
    capacity = models.CharField(max_length=100)
    price = models.CharField(max_length=50)
    image = models.ImageField(upload_to='images', null=True, blank=True)
    availability=models.BooleanField(default=True)

class Booking(models.Model):
    id_salle = models.ForeignKey('reservation.Room', on_delete=models.CASCADE)
    id_user = models.ForeignKey('reservation.CustomUser', on_delete=models.CASCADE)
    room_name = models.CharField(max_length=100)
    Start_date = models.DateTimeField()
    end_date = models.DateTimeField()
   
