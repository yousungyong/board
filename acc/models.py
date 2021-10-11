from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    nickname = models.CharField(max_length=100)
    comment = models.TextField(blank=True)
    age = models.IntegerField(default=0)
    pic = models.ImageField(upload_to="user/%y/%m")
    point = models.IntegerField(default = 0)