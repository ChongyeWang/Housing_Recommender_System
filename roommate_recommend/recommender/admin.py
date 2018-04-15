from django.contrib import admin
from recommender.models import UserProfile, RoommatePreference, Housing

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(RoommatePreference)
admin.site.register(Housing)
