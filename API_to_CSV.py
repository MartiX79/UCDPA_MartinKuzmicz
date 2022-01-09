from call_API import api_results
import pandas as pd
import time

# get movies for whole 2021

# explore data
# get list of movies from 2021
movies_list = api_results('discover/movie', '&primary_release_year=2021')

# check how many pages in result (max page parameter is 1000)
# https://developers.themoviedb.org/3/discover/movie-discover
total_pages = movies_list['total_pages']
print("Total pages for moves list: " + str(total_pages))

# over 1000 pages in results
# split data into chunks

# create reusable function
def get_movies_list(_dateMin, _dateMax):
    _data = pd.DataFrame()
    _movies_list = api_results('discover/movie', '&primary_release_date.gte=' + str(_dateMin) + '&primary_release_date.lte=' + str(_dateMax))
    _totalPages = _movies_list['total_pages']
    print("Date range: " + str(_dateMin) + " - " + str(_dateMax))
    print("Total pages: " + str(_totalPages))
    print("Number of results: " + str(_movies_list['total_results']))
    # loop trough all pages
    for p in range(_totalPages):
        _movies_list = api_results('discover/movie', '&sort_by=release_date.desc&primary_release_date.gte=' + str(_dateMin) + '&primary_release_date.lte=' + str(_dateMax) + '&page=' + str(p + 1))
        # created dataframe from results
        _df = pd.json_normalize(_movies_list['results'])
        # drop unneeded columns
        _df = _df[['id', 'title', 'release_date', 'vote_average', 'vote_count']]
        _data = _data.append(_df)
        print("Page " + str(p+1) + " of " + str(_totalPages) + " scrapped")
        # adding delay to prevent api requests limit
        time.sleep(1)
    print(_data.shape)
    return _data

# initialize empty dataframe
movies_list = pd.DataFrame()

# get movies list for the specific date range
movies_list_1 = get_movies_list('2021-01-01', '2021-06-30')
movies_list = movies_list.append(movies_list_1)

movies_list_2 = get_movies_list('2021-07-01', '2021-12-31')
movies_list = movies_list.append(movies_list_2)

# reset index for whole data range
movies_list.reset_index(inplace=True, drop=True)
movies_list.to_csv('Movies_list.csv')
print(movies_list.shape)