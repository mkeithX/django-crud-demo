from django.db import models

# Create your models here.
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from datetime import date
from PIL import Image
from django.conf import settings
from apps.users.managers import UserManager
from django_countries.fields import CountryField
import uuid
from django.urls import reverse

def user_directory_path(instance, filename):
    return "uploads/user_{0}/1".format(instance.user.id, filename)

class User(AbstractUser):
    GENDER_CHOICES = (
        ("male", "Male"),
        ("female", "Female"),
        ("other", "Other"),
    )

    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    username = models.CharField(verbose_name="Username", max_length=30, unique=True)
    email = models.EmailField(verbose_name="Email", unique=True, null=True, db_index=True)
    date_of_birth = models.DateField(verbose_name="Birthday")
    gender = models.CharField(verbose_name="Gender", max_length=30, choices=GENDER_CHOICES, blank=True, null=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "date_of_birth", "gender"]

    objects = UserManager()

    def __str__(self) -> str:
        return self.email
    
    def age(self):
        today = date.today()
        age = today.year - self.date_of_birth.year
        if today.month < self.date_of_birth.month or (today.month == self.date_of_birth.month and today.day < self.date_of_birth.day):
            age -= 1
        return f"{age} yo"



class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True, related_name="user_profile")
    bio = models.TextField(blank=True, null=True, max_length=150)
    country = CountryField(null=True, blank=True)
    avatar = models.ImageField(default="default_avatar.png", blank=True, null=True, upload_to=user_directory_path, verbose_name="Avatar")

    def __str__(self) -> str:
        return self.user.username

    def get_absolute_url(self):
        return reverse('profile-detail-view', kwargs={"pk": self.user.pk})