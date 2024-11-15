from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager
)
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_("Email address is required."))
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("The superuser must have the status is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("The superuser must have the status is_superuser=True."))
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

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "last_name",
        "first_name",
        "birth_date",
        "telephone",
        "address",
    ]

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.last_name} {self.first_name}"
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
    
    def has_perms(self, perms, obj=None):
        return all(self.has_perm(perm, obj) for perm in perms)


class Room(models.Model):
    room_name = models.CharField(max_length=100)
    place = models.CharField(max_length=100)
    capacity = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    image = models.ImageField(upload_to="images", null=True, blank=False)
    availability = models.BooleanField(default=True)

    def is_available(self, start_date, end_date):
        bookings = Booking.objects.filter(
            id_room=self, start_date__lte=end_date, end_date__gte=start_date,is_cancelled=False
        )
        return bookings.exists()

    def delete(self, *args, **kwargs):
        Booking.objects.filter(id_room=self).delete()
        super().delete(*args, **kwargs)


class Booking(models.Model):
    id_user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="bookings"
    )
    id_room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="bookings")
    room_name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    is_cancelled = models.BooleanField(default=False)
