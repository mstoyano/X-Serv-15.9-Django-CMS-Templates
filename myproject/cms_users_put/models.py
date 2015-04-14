from django.db import models

# Create your models here.

class Birthday(models.Model):
	nombre = models.CharField(max_length=32)
	fecha = models.DateField()
	regalo = models.CharField(max_length=32)