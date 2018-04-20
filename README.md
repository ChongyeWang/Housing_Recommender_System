# CS410_Group_Project

basic_info = {name : {gender : male, email : a1@illinois.edu, phone : 217}}

location_preference = {name : {lon : 80, lat : 80}}

roommate_preference = {name : {preference_gender : Male, smoke : No, party: No, sleep_late: No, pet: No, self_description : 'xxxxxxxxxxxxxx'}}


like_list = {name : [name, name, name, name], name2 : [name, name, name, name]}

dislike_list = {name : [name, name, name, name], name2 :  [name, name, name, name]}

feature_weight = [weight of feature1, weight of feature2, weight of feature3…….]








# Campus Roommate Recommender
Si Chen(sichen12), Chongye Wang (chongye2), Wen-Chen Lo (wclo2)

# Goal: 
Our goal is to build a houses finding system including a houses searching engine and a roommates recommendation system. Through our system, students looking for houses will be able to find the houses that satisfy their need for locations and the recommended roommates based on theirs needs and interests.

# Motivations: 
Many students have the problems of looking for appropriate houses and roommates, so our houses finding system provide practical uses for these kinds of students. By providing the information of house locations they prefer and requirements for roommates, users can search the houses that match their location requirements and find recommended roommates for users based on their needs and habits, therefore increasing the possibilities of finding appropriate houses and roommates.
Initial Approach and Techniques:
We have mainly two systems to build, namely a customized housing search engine and a roommate recommendation system. First, we will build a crawler using Zillow API to collect datasets for rental housing information nearby campus. We then build inverted indexes in order to develop the search engine. Besides, we will provide a web service so that users could register their personal profile, search and browse some rental housing, and make a list of their favorite houses. On the other hand, recommendation system will periodically generate and update a list of recommended roommates to users based on their personal profile, what houses they like, etc.
    We will possibly implement the crawler, search engine, and recommendation system by Python. Below are the tools and techniques we will possibly use:
MapReduce: build inverted index
HBase: store inverted index
Web Service: Django, a Python Web framework
MySQL: store user profile, recommendation list, etc.

# Expected Outcomes: 
The two systems would be shown in a web interface. Users are able to choose their ideal houses on a google map window, and add to wish list. Then the interface would pop out reminder of created roommate recommendation list to users. 
# Related Works: roommates.com

# Schedule:
3/25 - 3/31: Data cleaning and parsing. Survey recommendation algorithm.
4/1 - 4/7: Build index and search engine. 
4/8 - 4/14: Implementation for backend, frontend, and recommendation system.
4/15 - 4/21: Implementation for backend, frontend, and recommendation system.
4/22 - 4/28: System Integration.
4/29 - 5/5: Experiment setups and experimental evaluation.





