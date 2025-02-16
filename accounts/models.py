from django.db import models
from django.contrib.auth.models import User


# extending user model in order to add extra fields
class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


    # you can add extra fields as you need

    def __str__(self):
        return self.user.username