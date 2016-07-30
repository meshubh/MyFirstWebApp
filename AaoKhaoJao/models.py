from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.admin import User
from django.core.validators import RegexValidator


class Restaurants(models.Model):
    name = models.CharField(max_length=50)
    location=models.CharField(max_length=50)
    owner=models.ForeignKey(User)
    def __str__(self):
        return self.name

class Menu(models.Model):
    restaurant_id = models.ForeignKey(Restaurants)
    item = models.CharField(max_length=100)
    price = models.IntegerField()

    def __str__(self):
        return self.name

class UserProfile(models.Model):
        # This line is required. Links UserProfile to a User model instance.
        user = models.OneToOneField(User)

        # The additional attributes we wish to include.
        city=models.CharField(max_length=200)

        # Override the __unicode__() method to return out something meaningful!
        def __unicode__(self):
            return self.user.username

# Create your models here.
