import os
import sys
import random
import csv
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'roommate_recommend.settings')

import django
django.setup()

from django.contrib.auth.models import User
from recommender.models import UserProfile, RoommatePreference, Housing, LikeHousing


def populate_housing():
    index = 1
    with open('./address.csv', newline='') as csvfile:
        rows = csv.reader(csvfile)
        for row in rows:
            print(index)
            if index % 30 == 0:
                address = row[0]
                city = row[1]
                zipcode = int(row[2])
                lat = float(row[3])
                lon = float(row[4])
                Housing.objects.create(address=(address + ', ' + city), zipcode=zipcode,
                                       latitude=lat, longitude=lon)

            index += 1

def populate_like():
    allHouse = Housing.objects.all()
    allUser = User.objects.all()
    number = len(allUser)
    for house in allHouse:
        index_list = random.sample(range(0, number), 2)
        for index in index_list:
            LikeHousing.objects.create(house=house, user=allUser[index])

def deleteHouse():
    allHouse = Housing.objects.all()
    for house in allHouse:
        house.delete()

if __name__ == '__main__':
    print("Starting populating housing...")
    populate_housing()
    populate_like()
    #deleteHouse()
