from django.shortcuts import render
from django import forms
from django.contrib.auth.models import User
from recommender.models import UserProfile, RoommatePreference, Housing, RecommendRoommate
from recommender.models import LikeHousing
from recommender.forms import UserForm, UserProfileForm, PreferenceForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from recommender.helper import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def index(request):
    context_dict = {'boldmessage': "you can browse housing info & get roommates we recommend to you!"}
    return render(request, 'recommender/index.html', context=context_dict)

@login_required
def roommate(request):
    current_user = request.user
    if request.method == 'POST':
        mate_name = request.POST.get('mate_name')
        try:
            r = RecommendRoommate.objects.get(user1=current_user, user2__username=mate_name)
            r.delete()
        except:
            pass
        user2 = User.objects.get(username=mate_name)
        if 'like' in request.POST:
            RecommendRoommate.objects.create(user1=current_user, user2=user2, like=True)
        elif 'dislike' in request.POST:
            RecommendRoommate.objects.create(user1=current_user, user2=user2, like=False)
        return HttpResponseRedirect(reverse('roommate'))
    else:
        context_dict = {}
        recomm_list = get_recommend_list(current_user)
        print("new recommend list: ", recomm_list)
        recomm_user = []
        for name in recomm_list:
            u = UserProfile.objects.get(user__username=name)
            recomm_user.append(u)
        context_dict['roommates'] = recomm_user
        try:
            preference = current_user.roommatepreference
            context_dict['gender_prefer'] = word_dic[preference.gender_prefer]
            context_dict['smoke'] = word_dic[preference.smoke]
            context_dict['party'] = word_dic[preference.party]
            context_dict['sleep_late'] = word_dic[preference.sleep_late]
            context_dict['pet'] = word_dic[preference.pet]
            context_dict['description'] = preference.description
        except:
            pass
        #r = RecommendRoomate.objects.filter(user1=current_user)
        #context_dict['roommates'] = r
        return render(request, 'recommender/roommate.html', context=context_dict)

@login_required
def show_like(request):
    current_user = request.user
    if request.method == 'POST':
        print(request.POST)
        mate_name = request.POST.get('mate_name')
        r = RecommendRoommate.objects.get(user1=current_user, user2__username=mate_name)
        r.delete()
        print(reverse('show_like'))
        return HttpResponseRedirect(reverse('show_like'))
    else:
        likes_list = RecommendRoommate.objects.filter(user1=current_user, like=True)
        mates = []
        for like in likes_list:
            mates.append(like.user2)
        return render(request, 'recommender/show_like.html',
                        {'mates': mates})

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
        if request.POST.get('zipcode') != None:
            zipCode = request.POST.get('zipcode')
            like_housing = LikeHousing.objects.filter(user=current_user)
            like_housing_list = []
            id_list = []
            for like in like_housing:
                like_housing_list.append(like.house)
                id_list.append(like.house.zid)

            housing_list = Housing.objects.filter(zipcode__startswith=zipCode).exclude(zid__in=id_list)
            return render(request, 'recommender/housing.html',
                          {'other_house': housing_list, 'like_housing_list': like_housing_list})
        else:
            house_id = request.POST.get('house_id')
            if 'unlike' in request.POST:
                LikeHousing.objects.get(user=current_user, house_id=house_id).delete()
                # model = cache.get('model_cache')
            elif 'like' in request.POST:
                LikeHousing.objects.create(user=current_user, house_id=house_id)

            #curr_user, distance_range, roommate_preference, location_preference, user_likes, user_dislikes,
            #feature_weight, no_diff_gender, no_smoke, no_party, no_sleep_late, no_pet, model):
            return HttpResponseRedirect(reverse('housing'))
    else:
        like_housing = LikeHousing.objects.filter(user=current_user)
        like_housing_list = []
        id_list = []
        for like in like_housing:
            like_housing_list.append(like.house)
            id_list.append(like.house.zid)

        housing_list = Housing.objects.all().exclude(zid__in=id_list)
        page = request.GET.get('page', 1)
        paginator = Paginator(housing_list, 30)
        try:
            houses = paginator.page(page)
        except PageNotAnInteger:
            houses = paginator.page(1)
        except EmptyPage:
            houses = paginator.page(paginator.num_pages)
        return render(request, 'recommender/housing.html',
                      {'other_house': houses, 'like_housing_list':like_housing_list})

def map(request):
    housing = Housing.objects.all()
    context_dict = {'housing': housing}
    return render(request, 'recommender/map.html', context_dict)


def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
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

