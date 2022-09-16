from django.db import models
from django.contrib.auth.models import User


class UserAPISession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    expired_at = models.DateTimeField()
    token = models.CharField(max_length=64)
