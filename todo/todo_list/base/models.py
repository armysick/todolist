from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser

import uuid


# Create your models here.

class CustomUser(AbstractUser):
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )

    # Add any additional fields you need here

    def __str__(self):
        return self.username


class Task(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    complete = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['complete']


class UserID:
    def __init__(self, user_id):
        self.user_id = user_id

    def __str__(self):
        return self.user_id
