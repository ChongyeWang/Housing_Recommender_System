from text_training import*
from recommendation import*

def collaborative_filtering(curr_user, roommate_preference, user_likes, feature_weight):
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
        user_cosineScore = get_user_cosineScore(curr_user, roommate_preference, satisfied_user_list)

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
