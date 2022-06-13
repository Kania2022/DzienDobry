from django.db import models
from django.db.models import CASCADE, OneToOneField, EmailField, DO_NOTHING
from django.contrib.auth.models import User

# Create your models here.


class Profile(models.Model):
    user = OneToOneField(User, on_delete=CASCADE)
    email = EmailField()
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField(default='2000-01-01')


    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Services(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=500)


class ChosenServices(models.Model):
    user_id = models.ForeignKey(Profile, on_delete=DO_NOTHING)
    service_id = models.ForeignKey(Services, on_delete=DO_NOTHING)
