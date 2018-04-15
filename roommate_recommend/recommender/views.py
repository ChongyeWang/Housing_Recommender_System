from django.shortcuts import render
from django import forms
from django.contrib.auth.models import User
from recommender.models import UserProfile, RoommatePreference
from recommender.forms import UserForm, UserProfileForm, PreferenceForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from recommender.util.recommendation import recommender
from django.core.cache import cache

word_dic = {'M':'Male', 'F':'Female', 'B':'Both', True:'Yes', False:'No'}


def index(request):
    context_dict = {'boldmessage': "you can search for housing & get roommates we recommend to you!"}
    return render(request, 'recommender/index.html', context=context_dict)

@login_required
def roommate(request):
    current_user = request.user
    context_dict = {}
    try:
        preference = current_user.roommatepreference
        context_dict = {'gender_prefer': word_dic[preference.gender_prefer],
                        'smoke': word_dic[preference.smoke],
                        'party': word_dic[preference.party],
                        'sleep_late': word_dic[preference.sleep_late],
                        'pet': word_dic[preference.pet],
                        'description': preference.description}
    except:
        pass
    return render(request, 'recommender/roommate.html', context=context_dict)

@login_required
def preference(request):
    current_user = request.user
    edit_success = False
    preference_form = None
    if request.method == 'POST':
        try:
            r = RoommatePreference.objects.get(user=current_user)
            preference_form = PreferenceForm(data=request.POST, instance=r)
        except:
            preference_form = PreferenceForm(data=request.POST)
        if preference_form.is_valid():
            prefer = preference_form.save()
            prefer.user = current_user
            prefer.save()
            edit_success = True
        else:
            print(preference_form.errors)
    else:
        try:
            r = RoommatePreference.objects.get(user=current_user)
            preference_form = PreferenceForm(instance=r)
        except:
            preference_form = PreferenceForm()
    return render(request, 'recommender/preference.html',
                  {'preference_form': preference_form, 'edit_success':edit_success})

@login_required
def housing(request):
    current_user = request.user
    if request.method == 'POST':
        model = cache.get('model_cache')
        basic_info = {}
        location_preference = {}
        roommate_preference = {}
        user_likes = {}
        user_dislikes = {}
        allusers = UserProfile.objects.all()
        for u in allusers:
            user_name = u.user.username
            basic_info[user_name] = {'gender':u.gender, 'email':u.user.email}
            location_preference[user_name] = {'lon' : -88.0, 'lat' : 40.0}
            preference = None
            try:
                preference = RoommatePreference.objects.get(user=u.user)
            except:
                pass
            roommate_preference[user_name] = {'preference_gender' : word_dic[preference.gender_prefer],
                                               'smoke' : word_dic[preference.smoke],
                                               'party': word_dic[preference.party],
                                               'sleep_late': word_dic[preference.sleep_late],
                                               'pet': word_dic[preference.pet],
                                               'self_description': preference.description}
            user_likes[user_name] = {'alice'}
            user_dislikes[user_name] = {'bob'}

        feature_weight = [1, 1, 1, 1, 1, 1]
        recomm_list = recommender(current_user.username, 50, roommate_preference, location_preference,
                                  user_likes, user_dislikes, feature_weight,
                                  False, False, False, False, False, model)
        print(recomm_list)
        #curr_user, distance_range, roommate_preference, location_preference, user_likes, user_dislikes,
        #feature_weight, no_diff_gender, no_smoke, no_party, no_sleep_late, no_pet, model):
        return HttpResponseRedirect(reverse('housing'))
    else:
        housing_list = ['house1', 'house2', 'house3', 'house4', 'house5']
        return render(request, 'recommender/housing.html', {'housing_info': housing_list})


def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'recommender/register.html',
        {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Invalid user")
        else:
            print("Invalid login details: {0}, {1}".format(username, password))
            #return HttpResponse("Invalid login details supplied.")
            return render(request, 'recommender/login.html', {'fail': True})
    else:
        return render(request, 'recommender/login.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

