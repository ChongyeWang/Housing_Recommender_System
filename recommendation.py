from recommender.util.text_training import*
from recommender.util.search import*
import geopy.distance
import operator
import numpy as np

#Basic info:
#basic_info = {name : {gender : male, email : a1@illinois.edu, phone : 217}

#Location Preference:
#location_preference = {name : {lon : 80, lat : 80}}

#Roommate Preference:
#roommate_preference = {name : {preference_gender : Male, smoke : No, party: No, sleep_late: No, pet: No, self_description : 'xxx'}}

#user_likes:
#user_like = {name: [name1, name2]}

#user_dislikes
#user_dislikes = {name: [name1, name2]}

#feature_weight
#feature_weight = [weight of feature1, weight of feature2, weight of feature3]



def get_satisfiedDistance_roommates(curr_user, location_preference, distance_range):
    """Get the potential users within the distance range"""
    satisfied_user_list = []
    for user in location_preference:
        if user == curr_user: continue
        distance = geopy.distance.vincenty((location_preference[curr_user]['lat'], location_preference[curr_user]['lon']), (location_preference[user]['lat'], location_preference[user]['lon'])).m
        if distance <= distance_range: satisfied_user_list.append(user)
    return satisfied_user_list


def filter_by_require(curr_user, roommate_preference, satisfied_user_list, no_diff_gender, no_smoke, no_party, no_sleep_late, no_pet):
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


def remove_existing_users(curr_user, user_likes, user_dislikes, satisfied_user_list):
    """remove user that already exist in the user_likes and user_dislikes list"""
    return_list = list(satisfied_user_list)
    for user in satisfied_user_list:
        if user in user_likes[curr_user] or user in user_dislikes[curr_user]:
            return_list.remove(user)
    return return_list


def get_user_cosineScore(curr_user, roommate_preference, satisfied_user_list, model):
    """Get the cosine score for the current user and others and return a dictionary"""
    user_cosineScore = {}
    curr_user_description = roommate_preference[curr_user]['self_description']
    for user in satisfied_user_list:
        if user == curr_user: continue
        target_user_description = roommate_preference[user]['self_description']
        cosineScore = get_similarity(curr_user_description, target_user_description, model)
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


def overall_ranking(curr_user, roommate_preference, user_description_ranking, satisfied_user_list, feature_weight):
    """Get the overall ranking for users"""
    #roommate_preference = {name : {preference_gender : Male, smoke : No, party: No, sleep_late: No, self_description : 'xxx'}}
    #gender : 0.6
    #smoke : 0.1
    #party : 0.1
    #sleep : 0.1
    #pet : 0.05
    #self_description : 0.05
    user_overall_score = {}
    #weight = np.array([0.6, 0.1, 0.1, 0.1, 0.05, 0.05])
    for user in satisfied_user_list:
        if user == curr_user: continue
        feature = np.zeros(6)
        feature[0] = (roommate_preference[user]['preference_gender'] == roommate_preference[curr_user]['preference_gender'])
        feature[1] = (roommate_preference[user]['smoke'] == roommate_preference[curr_user]['smoke'])
        feature[2] = (roommate_preference[user]['party'] == roommate_preference[curr_user]['party'])
        feature[3] = (roommate_preference[user]['sleep_late'] == roommate_preference[curr_user]['sleep_late'])
        feature[4] = (roommate_preference[user]['pet'] == roommate_preference[curr_user]['pet'])
        feature[5] = 1.0 / user_description_ranking[user]
        score = np.array(feature_weight).dot(feature)
        user_overall_score[user] = score

    #Convert to user_ranking format
    user_overall_ranking = get_userSimilarityRanking(user_overall_score)
    #transfer to ranking - user
    ranking_user = {v: k for k, v in user_overall_ranking.items()}
    return ranking_user


def combine_recommendationMethod(overall_user_ranking_result, collaborative_filtering_result):
    """Combine the contenbased result and collaborative_filtering result"""
    result_list = []

    collaborative_filtering_num = 10
    content_based_num = 20

    for idx in range(1, min(content_based_num, len(overall_user_ranking_result)) + 1):
        user = overall_user_ranking_result[idx]
        result_list.append(user)
    for idx in range(0, min(collaborative_filtering_num, len(collaborative_filtering_result))):
        user = collaborative_filtering_result[idx]
        result_list.append(user)

    result_list = list(set(result_list))#remove duplicates
    return result_list


def collaborative_filtering(curr_user, roommate_preference, user_likes, feature_weight, model):
    #the result list of users we will recommend to the current user
    result_user_list = []

    satisfied_user_list = user_likes[curr_user]

    #Return if the liked list is empty
    if not satisfied_user_list: return result_user_list

    #Get the number of curr_user likes
    num_of_liked_user = len(satisfied_user_list)

    #Select the top 3 liked user based on similarity
    user_liked_list = []
    if num_of_liked_user == 1:
        user_liked_list = [user for user in satisfied_user_list]
    else:
        #Get the cosine score
        user_cosineScore = get_user_cosineScore(curr_user, roommate_preference, satisfied_user_list, model)

        #Get the ranking of user list based on the user description
        user_description_ranking = get_userSimilarityRanking(user_cosineScore)

        #Get the overall ranking of users based on all features
        overall_user_ranking = overall_ranking(curr_user, roommate_preference, user_description_ranking, satisfied_user_list, feature_weight)

        size = len(overall_user_ranking)
        user_liked_list = [None] * min(3, size)
        for ranking in overall_user_ranking:
            if ranking == 1:
                user_liked_list[0] = overall_user_ranking[ranking]
            elif ranking == 2:
                user_liked_list[1] = overall_user_ranking[ranking]
            elif ranking == 3:
                user_liked_list[2] = overall_user_ranking[ranking]

    for user_idx in range(0, len(user_liked_list)):
        user = user_liked_list[user_idx]
        user_list = user_likes[user]
        size = 10 / (user_idx + 1)
        if len(user_list) < size:
            result_user_list.extend(user_list)
        else:
            for i in range(0, size):
                result_user_list.append(user_list[i])

    result_user_list = list(set(result_user_list))#remove duplicates
    return result_user_list


def recommender(curr_user, distance_range, roommate_preference, location_preference, user_likes, user_dislikes, \
    feature_weight, no_diff_gender, no_smoke, no_party, no_sleep_late, no_pet, model):
    """Main recommender, recommend based on content based filtering and collaborative_filtering"""

    '''content based filtering'''
    #Get satisfied position user list
    satisfied_user_list = get_satisfiedDistance_roommates(curr_user, location_preference, distance_range)

    if not satisfied_user_list: return satisfied_user_list

    #remove user that already exist in the user_likes and user_dislikes list
    satisfied_user_list = remove_existing_users(curr_user, user_likes, user_dislikes, satisfied_user_list)

    if not satisfied_user_list: return satisfied_user_list

    #Filter the user list by requirements of the current user
    filter_by_require(curr_user, roommate_preference, satisfied_user_list, no_diff_gender, no_smoke, no_party, no_sleep_late, no_pet)

    if not satisfied_user_list: return satisfied_user_list

    #Get the cosine score
    user_cosineScore = get_user_cosineScore(curr_user, roommate_preference, satisfied_user_list, model)

    #Get the ranking of user list based on the user description
    user_description_ranking = get_userSimilarityRanking(user_cosineScore)

    #Get the overall ranking of users based on all features
    overall_user_ranking_result = overall_ranking(curr_user, roommate_preference, user_description_ranking, satisfied_user_list, feature_weight)

    '''collaborative_filtering'''
    collaborative_filtering_result = collaborative_filtering(curr_user, roommate_preference, user_likes, feature_weight, model)

    '''combine'''
    result_recommendation_list = combine_recommendationMethod(overall_user_ranking_result, collaborative_filtering_result)

    return result_recommendation_list

