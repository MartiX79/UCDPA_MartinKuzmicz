import pandas as pd
import numpy as np
import seaborn as sn
import matplotlib.pyplot as plt

from call_API import api_results
import API_to_CSV


# explore data
# get list of movies from 2021 from API
_, movies_list_results = api_results('/discover/movie', '&primary_release_year=2021')

# check how many pages in result (max page parameter is 1000)
# https://developers.themoviedb.org/3/discover/movie-discover
total_pages = movies_list_results['total_pages']
print("Total pages for moves list: " + str(total_pages))

# save discovered movies results to csv file
#API_to_CSV.discoverMovies(2021, 'movies_list_2021')

# get details for all mivies from the list and save to csv
API_to_CSV.get_move_details('movies_list_2021.csv', 'movies_list_2021_details')


# get list of columns
movies_df = pd.read_csv('movies_list_2021_details.csv')
print(movies_df.columns)

# keep only needed columns
movies_df = movies_df[['id','genres','budget','revenue','vote_average','vote_count']]
print(movies_df.columns)

# analise data
print(movies_df.info())
print(movies_df.head())

# change default display columns limit to see data from all columns
pd.set_option('max_columns', None)
print(movies_df.head())

#replace 0 with NaN to indicate missing value and not the 0 revenue
movies_df['revenue'] = movies_df['revenue'].replace(0, np.nan)
movies_df['budget'] = movies_df['budget'].replace(0, np.nan)

print(movies_df.info())

# rating score weight (no. of vote_average / vote_count)
movies_df['rating_score'] = movies_df['vote_average']/movies_df['vote_count']

movies_df_vote = movies_df.loc[(movies_df != 0).all(axis=1), :]

sn.histplot(data=movies_df_vote['vote_average'], bins=10)
plt.show()

