import os
import sys
import random
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'roommate_recommend.settings')

import django
django.setup()

from django.contrib.auth.models import User
from recommender.models import UserProfile, RoommatePreference, Housing, LikeHousing


def populate_housing():
    pass

def populate_like():
    allHouse = Housing.objects.all()
        


if __name__ == '__main__':
    print("Starting populating housing...")
    populate_housing()
    populate_like()