from django.db import models

class example1(models.Model):
	name = models.CharField(max_length=200, default='')

class example2(models.Model):
	flagged = models.BooleanField(default=False)