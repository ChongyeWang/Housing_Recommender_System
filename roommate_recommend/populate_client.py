import os
import sys
import random
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'roommate_recommend.settings')

import django
django.setup()

from django.contrib.auth.models import User
from recommender.models import UserProfile, RoommatePreference

#nameList = ["AMELIA","OLIVIA","EMILY","AVA","ISLA","JESSICA","POPPY","ISABELLA","SOPHIE","MIA","RUBY","LILY","GRACE","EVIE","SOPHIA","ELLA","SCARLETT","CHLOE","ISABELLE","FREYA","CHARLOTTE","SIENNA","DAISY","PHOEBE","MILLIE","EVA","ALICE","LUCY","FLORENCE","SOFIA","LAYLA","LOLA","HOLLY","IMOGEN","MOLLY","MATILDA","LILLY","ROSIE","ELIZABETH","ERIN","MAISIE","LEXI","ELLIE","HANNAH","EVELYN","ABIGAIL","ELSIE","SUMMER","MEGAN","JASMINE","MAYA","AMELIE","LACEY","WILLOW","EMMA","BELLA","ELEANOR","ESME","ELIZA","GEORGIA","HARRIET","GRACIE","ANNABELLE","EMILIA","AMBER","IVY","BROOKE","ROSE","ANNA","ZARA","LEAH","MOLLIE","MARTHA","FAITH","HOLLIE","AMY","BETHANY","VIOLET","KATIE","MARYAM","FRANCESCA","JULIA","MARIA","DARCEY","ISABEL","TILLY","MADDISON","VICTORIA","ISOBEL","NIAMH","SKYE","MADISON","DARCY","AISHA","BEATRICE","SARAH","ZOE","PAIGE","HEIDI","LYDIA"]
pictureList = ['golden_bridge.jpg', 'matterhorn.jpg', 'golden.jpg', 'sun.jpg', '731.jpg', 'pyrenees_mountain.jpg', 'silicon.png', 'AiUl7xn.jpg', 'EhY3AHd.jpg']
textList = ['Hi I like to play basketball', 'Hello! I love to play tennis', 'Hi I want to find someone who love to sing',
            'I love to read', 'I love to cook, any one want to be roommate together', 'I love to sleep',
            'I like to watch TV', 'video game is fun', 'I love coding', 'work out work out!']

def deleteUsers():
    for i in range(100):
        name = 'user' + str(i + 1)
        u = User.objects.get(username=name)
        profile = UserProfile.objects.get(user=u)
        prefer = RoommatePreference.objects.get(user=u)
        prefer.delete()
        profile.delete()
        u.delete()


def populate():
    for i in range(100):
        name = 'user'+ str(i+1)
        user = User(username=name, email=(name + "@illinois.edu"))
        user.set_password(111)
        user.save()
        profile = UserProfile(gender = 'M' if random.randint(0, 1) == 1 else 'F')
        profile.user = user
        profile.picture = pictureList[random.randint(0, len(pictureList)-1)]
        profile.save()
        prefer = RoommatePreference()
        prefer.gender_prefer = "M" if random.randint(0, 1) == 1 else "F"
        prefer.smoke = True if random.randint(0, 1) == 1 else False
        prefer.party = True if random.randint(0, 1) == 1 else False
        prefer.sleep_late = True if random.randint(0, 1) == 1 else False
        prefer.pet = True if random.randint(0, 1) == 1 else False
        prefer.description = textList[random.randint(0, len(textList)-1)]
        prefer.user = user
        prefer.save()

if __name__ == '__main__':
    print("Starting populating client...")
    populate()
