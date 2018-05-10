from recommender.util.text_training import*
import numpy as np
import numpy.linalg as la

def generate_feature_array(feature_array, roommate_preference, model):
    """Generate the feature array based on the roommate_preference of the user"""
    feature_array[0] = roommate_preference[curr_user]['preference_gender'] == roommate_preference[other_user]['preference_gender']
    feature_array[1] = roommate_preference[curr_user]['smoke'] == roommate_preference[other_user]['smoke']
    feature_array[2] = roommate_preference[curr_user]['party'] == roommate_preference[other_user]['party']
    feature_array[3] = roommate_preference[curr_user]['sleep_late'] == roommate_preference[other_user]['sleep_late']
    feature_array[4] = roommate_preference[curr_user]['pet'] == roommate_preference[other_user]['pet']

    curr_user_description = roommate_preference[curr_user]['self_description']
    target_user_description = roommate_preference[other_user]['self_description']
    cosineScore = get_similarity(curr_user_description, target_user_description, model)
    similarity_score = 0
    if cosineScore == 0:
        similarity_score = 0
    else:
        similarity_score = cosineScore[0][0]
    if similarity_score >= 0.5:
        feature_array[5] = 1
    else:
        feature_array[5] = 0


def update_feature_weight(user_list, roommate_preference, user_likes, user_dislikes, feature_weight, model):
    """Update the feature weight based on the user feedbacks"""
    feature_matrix = []
    feedback_matrix = []
    for curr_user in user_list:
        #Add likes
        for other_user in user_likes[curr_user]:
            feature_array = np.zeros(6)
            generate_feature_array(feature_array, roommate_preference, model)
            feature_matrix.append(feature_matrix)
            feedback_matrix.append(1)
        #Add dislikes
        for other_user in user_dislikes[curr_user]:
            feature_array = np.zeros(6)
            generate_feature_array(feature_array, roommate_preference, model)
            feature_matrix.append(feature_matrix)
            feedback_matrix.append(0)
    feature_matrix = np.array(feature_matrix)
    feedback_matrix = np.array(feedback_matrix)
    feature_weight = la.solve(feature_matrix, feedback_matrix)
