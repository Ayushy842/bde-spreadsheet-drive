from django.db import models
from django.contrib.auth.validators import ASCIIUsernameValidator

class User(models.Model):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30,validators=[ASCIIUsernameValidator()])
    password = models.CharField(max_length=100,help_text="your password must contain at least 8 character and a mix of letters,numbers and symbols")



class Meter(models.Model):
    serial_number = models.IntegerField(primary_key=True)
    inc_name = models.CharField(max_length=255)
    proprietor_name = models.CharField(max_length=255)
    meter_measurement = models.FloatField()
    diff_units = models.FloatField()
    avg_unit = models.FloatField()
    power_utility_index = models.IntegerField()
    power_station_name = models.CharField(max_length=255)
    usage_type = models.CharField(max_length=255)
    csi_index = models.IntegerField(default=0)
    
        