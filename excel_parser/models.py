
from django.db import models
from django.utils.timezone import now


class Data(models.Model):
    company = models.CharField(verbose_name='Компания', max_length=128)
    data1 = models.IntegerField()
    data2 = models.IntegerField()
    qliq = models.BooleanField(default=0)
    qoil = models.BooleanField(default=0)
    fact = models.BooleanField(default=0)
    forecast = models.BooleanField(default=0)
    date = models.DateField(default=now)
