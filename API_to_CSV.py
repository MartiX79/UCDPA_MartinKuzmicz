from call_API import api_results
import pandas as pd

movies_list = api_results('discover/movie', '&primary_release_year=2021').json()

df = pd.json_normalize(movies_list['results'])
print(df.shape)

df = df[['id', 'title', 'vote_average', 'vote_count']]
# df.to_csv('Movies_list.csv')
print(df.shape)
print(df)
