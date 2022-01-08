from call_API import api_results
import pandas as pd

# get list of movies from 2021
movies_list = api_results('discover/movie', '&primary_release_year=2021')

# check how many pages in result (max page parameter is 1000)
# https://developers.themoviedb.org/3/discover/movie-discover
total_pages = movies_list['total_pages']
print("Total pages for moves list: " + str(total_pages))

# over 1000 pages in results
# get list of all genres
genres = api_results('/genre/movie/list')
df_genre = pd.json_normalize(genres['genres'])
print("Total number of genres: " + str(len(df_genre)))

# call movies for each genres - this will limit number of pages in each result
# check how many pages
genre_movies = api_results('discover/movie', '&primary_release_year=2021&with_genres=' + str(37))
print(genre_movies['total_pages'])

# get result for each page
_page = 1
while _page <= genre_movies['total_pages']:
    genre_movies_page = api_results('discover/movie', '&primary_release_year=2021&with_genres=' + str(37) + '&page=' + str(_page))
    df_genre_movies_page = pd.json_normalize(genre_movies_page['results'])
    print(df_genre_movies_page[['id', 'title', 'vote_average', 'vote_count']])
    _page += 1



print('-----')


'''
for g in df_movies_genre['id']:
    genre_movies = api_results('discover/movie', '&primary_release_year=2021&with_genres=' + str(28)).json()
    print(genre_movies['results'])
    print(genre_movies['total_results'])
    print('-----')

df = pd.json_normalize(movies_list['results'])
print(df.shape)


df = df[['id', 'title', 'vote_average', 'vote_count']]
# df.to_csv('Movies_list.csv')
print(df.shape)
# print(df)
'''