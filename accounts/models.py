from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    followings = models.ManyToManyField('self', symmetrical=False, related_name='followers')
    name = models.CharField(max_length=50)
    profile_image = models.ImageField(blank=True, upload_to='origins/', default='default-image.jpg')
    is_private = models.BooleanField(default=False)