from django.db import models

# Create your models here.
class RegionData(models.Model):
    region = models.CharField(max_length=100)
    date = models.DateField()
    interest = models.FloatField()
    vacancy = models.FloatField()
    cpi = models.FloatField()
    price = models.FloatField()
    value = models.FloatField()
    adj_price = models.FloatField()
    adj_value = models.FloatField()
    next_quarter = models.FloatField()