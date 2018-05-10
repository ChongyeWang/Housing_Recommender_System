from django.contrib import admin
from recommender.models import UserProfile, RoommatePreference, Housing, LikeHousing, RecommendRoommate

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(RoommatePreference)
admin.site.register(Housing)
admin.site.register(LikeHousing)
admin.site.register(RecommendRoommate)
