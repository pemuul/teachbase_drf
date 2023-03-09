from django.db import models
from django.contrib.auth.models import User
 

class Users(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, primary_key = True)
    user_id_teachbase = models.IntegerField(blank=True, null=True)
    email = models.CharField(max_length=255)
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True)
    description = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=100, blank=True)
    role_id = models.IntegerField(default=1)
    auth_type = models.IntegerField(default=0)
    password = models.CharField(max_length=100)
    lang = models.CharField(max_length=30, default='ru')

    def __str__(self):
        return str([self.user_id_teachbase, self.user])


if __name__ == '__main__':
    pass