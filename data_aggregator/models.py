from django.db import models

# Create your models here.


class Health(models.Model):
    next_token = models.CharField(max_length=10, default="")


class ApiKey(models.Model):
    api_key = models.CharField(max_length=100, primary_key=True)
