from training import*
from search import*
import geopy.distance
import operator


#Basic info:
#basic_info = {name : {gender : male, email : a1@illinois.edu, phone : 217}

#Location Preference:
#location_preference = {name : {lon : 80, lat : 80}}

#Roommate Preference:
#roommate_preference = {name : {preference_gender : Male, smoke : No, party: No, sleep_late: No, pet: No, self_description : 'xxx'}}


def get_satisfiedDistance_roommates(curr_user, location_preference, distance_range):
    """Get the potential users within the distance range"""
    satisfied_user_list = []
    for user in location_preference:
        if user == curr_user: continue
        distance = geopy.distance.vincenty((location_preference[curr_user][lat], location_preference[curr_user][lon]), (location_preference[user][lat], location_preference[user][lon])).m
        if distance <= distance_range: satisfied_user_list.append(user)
    return satisfied_user_list


def get_user_cosineScore(curr_user, roommate_preference, satisfied_user_list):
    """Get the cosine score for the current user and others and return a dictionary"""
    user_cosineScore = {}
    curr_user_description = roommate_preference[curr_user]['self_description']
    for user in satisfied_user_list:
        if user == curr_user: continue
        target_user_description = roommate_preference[user]['self_description']
        cosineScore = get_similarity(curr_user_description, target_user_description)
        if cosineScore == 0:
            user_cosineScore[user] = 0
        else:
            user_cosineScore[user] = cosineScore[0][0]
    return user_cosineScore


def get_userSimilarityRanking(user_cosineScore):
    """Get the ranking dictionary for the description of user"""
    user_tuple = sorted(user_cosineScore.items(), key=operator.itemgetter(1))
    user_description_ranking = {}
    rank = 1
    for pair in user_tuple:
        user_description_ranking[pair[0]] = rank
        rank += 1
    return user_description_ranking


def filter(curr_user, roommate_preference, satisfied_user_list, no_diff_gender, no_smoke, no_party, no_sleep_late, no_pet):
    """Filter the users based on the requirement of the current user"""
    if no_diff_gender:
        for user in satisfied_user_list:
            if roommate_preference[user]['preference_gender'] != roommate_preference[curr_user]['preference_gender']:
                satisfied_user_list.remove(user)
    if no_smoke:
        for user in satisfied_user_list:
            if roommate_preference[user]['smoke'] == True:
                satisfied_user_list.remove(user)
    if no_party:
        for user in satisfied_user_list:
            if roommate_preference[user]['party'] == True:
                satisfied_user_list.remove(user)
    if no_sleep_late:
        for user in satisfied_user_list:
            if roommate_preference[user]['sleep_late'] == True:
                satisfied_user_list.remove(user)
    if no_pet:
        for user in satisfied_user_list:
            if roommate_preference[user]['pet'] == True:
                satisfied_user_list.remove(user)



def overall_ranking(curr_user, roommate_preference, user_description_ranking, satisfied_user_list):
    """Get the overall ranking for users"""
    #roommate_preference = {name : {preference_gender : Male, smoke : No, party: No, sleep_late: No, self_description : 'xxx'}}
    #gender : 0.6
    #smoke : 0.1
    #party : 0.1
    #sleep : 0.1
    #pet : 0.05
    #self_description : 0.05
    user_overall_score = {}
    weight = np.array([0.6, 0.1, 0.1, 0.1, 0.05, 0.05])
    for user in satisfied_user_list:
        if user == curr_user: continue
        feature = np.zeros(6)
        feature[0] = (roommate_preference[user]['preference_gender'] == roommate_preference[curr_user]['preference_gender'])
        feature[1] = (roommate_preference[user]['smoke'] == roommate_preference[curr_user]['smoke'])
        feature[2] = (roommate_preference[user]['party'] == roommate_preference[curr_user]['party'])
        feature[3] = (roommate_preference[user]['sleep_late'] == roommate_preference[curr_user]['sleep_late'])
        feature[4] = (roommate_preference[user]['pet'] == roommate_preference[curr_user]['pet'])
        feature[5] = 1.0 / user_description_ranking[user]
        score = weight.dot(feature)
        user_overall_score[user] = score
    #Convert to user_ranking format
    user_overall_ranking = get_userSimilarityRanking(user_overall_score)
    return user_overall_ranking


def recommender():
    #Get satisfied position user list
    satisfied_user_list = get_satisfiedDistance_roommates(curr_user, location_preference, distance_range)

    #Filter the user list by requirements of the current user
    filter(curr_user, roommate_preference, satisfied_user_list, user_ranking, no_diff_gender, no_smoke, no_party, no_sleep_late, no_pet)

    #Get the cosine score
    user_cosineScore = get_user_cosineScore(curr_user, roommate_preference, satisfied_user_list)

    #Get the ranking of user list based on the user description
    user_description_ranking = get_userSimilarityRanking(user_cosineScore)

    #Get the overall ranking of users based on all features
    overall_user_ranking = overall_ranking(curr_user, roommate_preference, user_description_ranking, satisfied_user_list)



a = {}
a['wang'] = {}
a['wang1'] = {}
a['wang2'] = {}

a['wang']['preference_gender'] = 'Male'
a['wang']['smoke'] = False
a['wang']['party'] = True
a['wang']['sleep_late'] = True
a['wang']['pet'] = True
a['wang']['self_description'] = 'dog'

a['wang1']['preference_gender'] = 'Male'
a['wang1']['smoke'] = False
a['wang1']['party'] = True
a['wang1']['sleep_late'] = True
a['wang1']['pet'] = True
a['wang1']['self_description'] = 'I hate dog'

a['wang2']['preference_gender'] = 'Male'
a['wang2']['smoke'] = True
a['wang2']['party'] = True
a['wang2']['sleep_late'] = True
a['wang2']['pet'] = True
a['wang2']['self_description'] = 'cat'

satisfied_user_list = ['wang1', 'wang2']
filter('wang', a, satisfied_user_list, True, True, False, False, False)
print(satisfied_user_list)

b = get_user_cosineScore('wang', a, satisfied_user_list)
c = get_userSimilarityRanking(b)
overall = overall_ranking('wang', a, c, satisfied_user_list)
print(overall)
