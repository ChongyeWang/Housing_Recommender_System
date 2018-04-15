from django.db import models
from django.contrib.auth.models import User
import uuid

class UserProfile(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    user = models.OneToOneField(User)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    def __str__(self):
        return self.user.username

class RoommatePreference(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('B', 'Both')
    )
    gender_prefer = models.CharField(max_length=1, choices=GENDER_CHOICES)
    smoke = models.BooleanField()
    party = models.BooleanField()
    sleep_late = models.BooleanField()
    pet = models.BooleanField()
    description = models.TextField(null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

"""
class Recommendation(models.Model):
    user = models.OneToOneField(UserProfile)
    recommend_to = models.ForeignKey(User, verbose_name='user', on_delete=models.CASCADE)
"""

"""
class Recommendation(models.Model):
    user1 = models.ForeignKey(User, verbose_name='user1', on_delete=models.CASCADE, related_name='user1')
    user2 = models.ForeignKey(User, verbose_name='user2', on_delete=models.CASCADE, related_name='user2')
    class Meta:
        unique_together = ('user1', 'user2',)
"""


class Housing(models.Model):
    zid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    address = models.CharField(max_length=128)
    zipcode = models.IntegerField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    description = models.CharField(max_length=500)
    user = models.ForeignKey(User, verbose_name='user_housing', on_delete=models.CASCADE)