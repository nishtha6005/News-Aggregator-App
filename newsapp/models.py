from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    category = models.CharField(max_length=20, unique = 'True')

class Source(models.Model):
    source = models.CharField(max_length=50, unique = 'True')

class UserSource(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    source = models.ForeignKey(Source, on_delete = models.CASCADE)
    subscription = models.BooleanField(default=False)

class UserCategory(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    category = models.ForeignKey(Category, on_delete = models.CASCADE)
    selection = models.BooleanField(default=False)