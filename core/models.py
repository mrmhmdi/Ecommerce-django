from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse

# Create your models here.


class CustomeUser(AbstractUser):

    def get_absolute_url(self):
        return reverse("edit_myaccount", kwargs={"pk": self.username})
