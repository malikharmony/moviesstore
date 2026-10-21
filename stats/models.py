from django.db import models
from django.contrib.auth.models import User
from movies.models import Movie

# Create your models here.
class UserStat(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    purchaseTotal = models.IntegerField()

class MovieStat(Movie):
    class Meta:
        proxy = True
        verbose_name = 'Movie statistics'
        verbose_name_plural = 'Movie statistics'