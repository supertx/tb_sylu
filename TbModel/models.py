from django.db import models


# Create your models here.

class User(models.Model):
    uid = models.AutoField(primary_key=True)
    email = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    # province_name = models.CharField(max_length=255)
    # city_name = models.CharField(max_length=255)
    # county_name = models.CharField(max_length=255)
    # province_code = models.CharField(max_length=255)
    # city_code = models.CharField(max_length=255)
    # county_code = models.CharField(max_length=255)
    # flag = models.IntegerField()