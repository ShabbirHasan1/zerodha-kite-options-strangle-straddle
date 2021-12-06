from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
class KiteBroker(models.Model):
    user = models.OneToOneField(
        get_user_model(),
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='kite_broker'
    )
    kite_id = models.CharField(max_length=6)
    api_key = models.CharField(max_length=16)
    api_secret = models.CharField(max_length=32)
    access_token = models.CharField(max_length=32)

    def __str__(self):
        return f'{self.user}'