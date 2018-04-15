"""
WSGI config for roommate_recommend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os
from django.core.cache import cache
from recommender.util.text_training import word2vec_training

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "roommate_recommend.settings")

#cache word2vec model
base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
path = os.path.join(base_path, 'static', 'model', 'GoogleNews-vectors-negative300.bin')
model = word2vec_training(path)
#cache.set('model_cache', model, None)

application = get_wsgi_application()
