from django.db import models

# Create your models here.

class Admin( models.Model ):
    username = models.CharField( max_length=11 )
    password = models.CharField( max_length=20 )

class Student( models.Model ):
    username = models.CharField( max_length=11 )
    password = models.CharField( max_length=20 )
    name = models.CharField( max_length=100 )
    queue = models.CharField( max_length=1000 )
    memory = models.CharField( max_length=500 )

class Group( models.Model ):
    name = models.CharField( max_length=10 )
    post = models.CharField( max_length=179 )
    visible = models.BooleanField()
