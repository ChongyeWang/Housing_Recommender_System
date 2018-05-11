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
    picture = models.ImageField(upload_to='profile_images', blank=True,
                                default='profile_images/profile_default.jpg')

    def __str__(self):
        return self.user.username

class RoommatePreference(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender_prefer = models.CharField(max_length=1, choices=GENDER_CHOICES)
    smoke = models.BooleanField()
    party = models.BooleanField()
    sleep_late = models.BooleanField()
    pet = models.BooleanField()
    description = models.TextField(null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.user.username


class RecommendRoommate(models.Model):
    user1 = models.ForeignKey(User, verbose_name='user1', on_delete=models.CASCADE, related_name='user1')
    user2 = models.ForeignKey(User, verbose_name='user2', on_delete=models.CASCADE, related_name='user2')
    like = models.BooleanField()

    class Meta:
        unique_together = ('user1', 'user2',)

    def __str__(self):
        return self.user1.username + '_' + self.user2.username


class Housing(models.Model):
    zid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    address = models.CharField(max_length=128)
    zipcode = models.IntegerField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    #description = models.CharField(max_length=500)

    def __str__(self):
        return self.address


class LikeHousing(models.Model):
    user = models.ForeignKey(User, verbose_name='housing_like', on_delete=models.CASCADE)
    house = models.ForeignKey(Housing, verbose_name='housing_liked', on_delete=models.CASCADE)
    class Meta:
        unique_together = ('user', 'house',)

    def __str__(self):
        return self.user.username + '_' + self.house.address


"""
class Recommendation(models.Model):
    user = models.OneToOneField(UserProfile)
    recommend_to = models.ForeignKey(User, verbose_name='user', on_delete=models.CASCADE)
"""

