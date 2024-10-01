from django.db import models

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
     groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',  
        blank=True,
        help_text="The groups this user belongs to.",
    )
     user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',  
        blank=True,
        help_text="Specific permissions for this user.",
    )
     first_name = models.CharField(
        max_length=150,
        editable=False,
    )
     last_name = models.CharField(
        max_length=150,
        editable=False,
    )
     avatar = models.URLField(blank=True)
     name = models.CharField(
        max_length=150,
        default="",
    )
     def __str__(self):
        return self.username
