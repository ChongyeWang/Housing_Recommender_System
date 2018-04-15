from django.conf.urls import include, url
from recommender import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^roommate/$', views.roommate, name='roommate'),
    url(r'^preference/$', views.preference, name='preference'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^housing/$', views.housing, name='housing'),
]