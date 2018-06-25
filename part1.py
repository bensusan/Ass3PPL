import numpy as np
import csv

my_data = np.loadtxt(open("ratings.csv", "rb"), delimiter=',',skiprows=1)

user_ids = my_data[:,0]
unique_user_ids = np.unique(user_ids)
user_profiles_dict = {}
for user_id in np.nditer(unique_user_ids):
    mask = (user_ids == user_id)
    masked = my_data[mask]
    movie_ids = masked[:, 1].astype(int)
    ratings = masked[:, 2]
    user_profiles_dict[int(user_id)] = (movie_ids, ratings)


with open('names.csv', 'w') as csvfile:
    fieldnames = ['userid', 'movies','ratings']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for key in user_profiles_dict.keys():
        user_id = str(key)
        movie_ids = np.array_str(user_profiles_dict[key][0])
        ratings = user_profiles_dict[key][1]
        writer.writerow({'userid': user_id, 'movies': movie_ids,'ratings': ratings})


user_ids = my_data[:,1]
unique_user_ids = np.unique(user_ids)
user_profiles_dict = {}
for user_id in np.nditer(unique_user_ids):
    mask = (user_ids == user_id)
    masked = my_data[mask]
    movie_ids = masked[:, 0].astype(int)
    ratings = masked[:, 2]
    user_profiles_dict[int(user_id)] = (movie_ids, ratings)


with open('movies.csv', 'w') as csvfile:
    fieldnames = ['movie id', 'users','ratings']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for key in user_profiles_dict.keys():
        user_id = str(key)
        movie_ids = np.array_str(user_profiles_dict[key][0])
        ratings = user_profiles_dict[key][1]
        writer.writerow({'movie id': user_id, 'users': movie_ids,'ratings': ratings})