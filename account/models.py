from django.db import models
from django.contrib.auth.models import User

class UserHistory(models.Model):
	duration = models.CharField(max_length=100)
	trekking_type = models.CharField(max_length=100)
	destination_type = models.CharField(max_length=100)
	accomodation_type = models.CharField(max_length=100)
	temperature = models.FloatField(blank=False, default="1")
	difficulty = models.FloatField(blank=False, default="1")
	security = models.FloatField(blank=False, default="1")
	latitude = models.FloatField(blank = True, null=True, default="27.6817")
	longitude = models.FloatField(blank=True, null=True, default="85.3170")
	user = models.ForeignKey(User, on_delete=models.CASCADE)