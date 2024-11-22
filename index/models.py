from unittest.util import _MAX_LENGTH
from django.db import models

# Create your models here.


class Tokenlist(models.Model):
    uid = models.IntegerField(default=0)
    token = models.CharField(max_length=100)
    time = models.DecimalField(max_digits=20,decimal_places=9)

    def __str__(self) -> str:
        return str(self.uid)+" :: "+str(self.token)

class Ip_address(models.Model):
    ip = models.CharField(max_length=100)
    address = models.CharField(max_length=100)

class IpSpeed_a(models.Model):
    ip = models.CharField(max_length=100)
    time = models.DecimalField(max_digits=20,decimal_places=9)
    times = models.IntegerField(default=0)

class IpSpeed_g(models.Model):
    ip = models.CharField(max_length=100)
    time = models.DecimalField(max_digits=20,decimal_places=9)
    times = models.IntegerField(default=0)

# class Board(models.Model):
#     board=models.TextField(max_length=2000000)