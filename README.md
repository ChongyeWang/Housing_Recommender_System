# [CS410_Group_Project] Campus Roommate Recommender

### Si Chen(sichen12), Chongye Wang (chongye2), Wen-Chen Lo (wclo2)


## Description: 
Our project is a roommates recommendation system. Through our system, students can browse housing information in Champaign/Urbana which they can like or dislike. In addition, after filling out their roommates preference, students are able to look for recommended roommates based on their preference and needs for locations, all can be done easily through our web interface.

## Algorithm
### Recommendation Algorithm
We use both the combination of content based filtering and collaborative filtering.

Each user will be able to submit a form when they register. The form includes the prefered gender preference, whether the user smoke, whether the user likes party, whether the user sleeps late, whether the likes pet and a self description. Initially the user can select their target location for dorms so users that are not in the range will not be recommended to the user. For analyzing text similarity based on the description of the user, we use  word2vec - google pre-trained document GoogleNews-vectors-negative300.bin and get the similarity score using cosine function and sklearn library. For the content based filtering, from the information the user provided when they register, we can recommend potential roommate to the user after ranking other users based on their similarity. Also, each user will have a like list and dislike list, so they can choose if the users recommended to them is appropriate or not. The unliked users will not appear next time they search. Also,  from the user liked list, we can apply collaborative filtering since there is a higher probability that if a user from the liked list of the current user, users from the liked list of this user might also be appropriate for the current user as well. In addition, while searching, the user can also filter the recommended list based on the requirement such as remove users that smoke. When we acquire enough data, we can update our weight vector based on the users and their liked lists using linear regression.
### Parameters for API
```basic_info = {name : {gender : male, email : a1@illinois.edu, phone : 217}}```

```location_preference = {name : {lon : 80, lat : 80}}```

```roommate_preference = {name : {preference_gender : Male, smoke : No, party: No, sleep_late: No, pet: No, self_description : 'xxxxxxxxxxxxxx'}}```

```like_list = {name : [name, name, name, name], name2 : [name, name, name, name]}```

```dislike_list = {name : [name, name, name, name], name2 :  [name, name, name, name]}```

```feature_weight = [weight of feature1, weight of feature2, weight of feature3…….]```

## System Architecture
![image](https://github.com/ChongyeWang/CS410_Group_Project/blob/master/architecture.jpg)

### How to deploy
1. please install python3  and pip before deploying
2. Install and setup MySQL. Change DATABASES setting in ```roommate_recommend/roommate_recommend/settings.py```
3. Download pre-trained word2vec model from <https://drive.google.com/file/d/1dZbC1zw9RLvetsMqBlbG0G4Zzz6Bpbft/view?usp=sharing>, put it in ```roommate_recommend/static/model/```
4. Go to roommate_recommend directory, then ```pip install -r requirements.txt```
5. Database migration by ```python manage.py migrate```
6. Populate test clients by ```python populate_client.py```
7. Put dataset to database by ```python populate_house.py```
8. Run test server by ```python manage.py runserver```, use http://[host IP]:8000/ to access web server
9. For production deployment on Apache server, see <https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/modwsgi/>


## Dataset
The housing addresses within Urbana-Champaign City were retrieved from Champaign County GIS Consortium (<https://webstore.illinois.edu/shop/product.aspx?zpid=3194>). The addresses are displayed in US Dual Range Address style, with zipcode, longtitude and latitude. These addresses are provided to users to like/unlike.


## Motivations: 
Many students have the problems of looking for appropriate houses and roommates, so our houses finding system provide practical uses for these kinds of students. By providing the information of house locations they prefer and requirements for roommates, users can search the houses that match their location requirements and find recommended roommates for users based on their needs and habits, therefore increasing the possibilities of finding appropriate houses and roommates.
Initial Approach and Techniques:
First, we collected datasets for housing information nearby campus. Then, we built a web service so that users could register their personal profile, search and browse some rental housing, and make a list of their favorite houses. On the other hand, recommendation system will periodically generate and update a list of recommended roommates to users based on their personal profile, what houses they like, etc.
   
## Expected Outcomes: 
The two systems would be shown in a web interface. Users are able to choose their ideal houses on a google map window, and add to wish list. Then the interface would pop out reminder of created roommate recommendation list to users. 









