from django.db import models

# Create your models here.
class Shell(models.Model):
    pic = models.ImageField(upload_to='images/')

