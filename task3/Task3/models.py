from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    # one to one realtionship : 1 user can only have 1 profile
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_picture = models.CharField(max_length=1000,null=True, blank=True)

    def __str__(self):
        return self.user.username
