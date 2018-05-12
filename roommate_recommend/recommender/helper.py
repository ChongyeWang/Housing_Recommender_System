from recommender.models import UserProfile, RoommatePreference, LikeHousing, RecommendRoommate
from roommate_recommend.wsgi import model
from recommender.util.recommendation import recommender


word_dic = {'M':'Male', 'F':'Female', 'B':'Both', True:'Yes', False:'No'}

def get_recommend_list(current_user):
    basic_info = {}
    location_preference = {}
    roommate_preference = {}
    user_likes = {}
    user_dislikes = {}
    allusers = UserProfile.objects.all()
    if LikeHousing.objects.filter(user=current_user).count() == 0:
        return []
    for u in allusers:
        user_name = u.user.username
        preference = None
        try:
            preference = RoommatePreference.objects.get(user=u.user)
        except:
            continue
        lastLike = LikeHousing.objects.filter(user=u.user).last()
        if lastLike:
            location_preference[user_name] = {'lon': lastLike.house.longitude, 'lat': lastLike.house.latitude}
        else:
            continue
        basic_info[user_name] = {'gender': u.gender, 'email': u.user.email}
        roommate_preference[user_name] = {'preference_gender': word_dic[preference.gender_prefer],
                                          'smoke': word_dic[preference.smoke],
                                          'party': word_dic[preference.party],
                                          'sleep_late': word_dic[preference.sleep_late],
                                          'pet': word_dic[preference.pet],
                                          'self_description': preference.description}
        rr = RecommendRoommate.objects.filter(user1=u.user)
        user_likes[user_name] = []
        user_dislikes[user_name] = []
        for r in rr:
            if r.like:
                user_likes[user_name].append(r.user2.username)
            else:
                user_dislikes[user_name].append(r.user2.username)
        #print(user_name+ 'like: ' + str(user_likes[user_name]))
        #print(user_name + 'dislike: ' + str(user_dislikes[user_name]))
    feature_weight = [0.6, 0.1, 0.1, 0.1, 0.05, 0.05]
    recomm_list = recommender(current_user.username, 1000, roommate_preference, location_preference,
                              user_likes, user_dislikes, feature_weight,
                              False, False, False, False, False, model)
    return recomm_list