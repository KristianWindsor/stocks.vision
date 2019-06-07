from django.conf import settings
from django.db import models


class Example(models.Model):
	name = models.CharField(max_length=200, default='')

class Example2(models.Model):
	flagged = models.BooleanField(default=False)