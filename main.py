from call_API import api_results

test = api_results('discover/movie', '&primary_release_year=2021').json()


# get list of movies from 2021
def discover_movies():
    _discover_movies = api_results('discover/movie', '&primary_release_year=2021').json()
    _totalPages = _discover_movies['total_pages']
    _page = _discover_movies['page']


print(test)

# discover_movies()
# show columns headers
# print(discoverMovies.keys())
#  print(req.text)
# df_discoverResults = pd.DataFrame.from_dict(discoverMovies['results'])
# movies = df_discoverResults[['id', 'title', 'vote_average', 'vote_count', 'release_date']]
# print(df_discover.head())
# print(df_discoverResults.info())
# print(df_discover[['id']])
# print(df_discoverResults)
print(' ---- ')
"""
for index, row in df_discoverResults.iterrows():
     m = '/movie/'+ str(row['id'])
     movieDetails = api_result(m)
     print(movieDetails)
     """
