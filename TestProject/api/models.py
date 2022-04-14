from django.contrib.auth.models import User
from django.db import models

class Message(models.Model):
    message_status = (
        ("review", "review"),
        ("blocked", "blocked"),
        ("correct", "correct"),
    )

    message = models.CharField(max_length=1000)
    status = models.CharField(choices=message_status, max_length=10, default="review")
    user_id = models.BigIntegerField()
