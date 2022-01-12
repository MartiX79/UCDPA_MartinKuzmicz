from call_API import api_results
import pandas as pd
import time
from pandas.tseries.offsets import MonthEnd


def discoverMovies(_movies_year, _fileName):
    '''
    Getting list of movies and saving from API to csv file

    Args:
        _movies_year (int): Year to fetch the movies data
        _fileName (str): File name without extension

    Returns:
        csv file

    Notes:
        Warning! if the file already exist, it will be overwritten!
    '''

    # over 1000 pages in results
    # split data and call each month secretly
    # create reusable function
    def get_movies_list(_dateMin, _dateMax):
        _data = pd.DataFrame()
        _movies_list = api_results('/discover/movie', '&primary_release_date.gte=' + str(_dateMin) + '&primary_release_date.lte=' + str(_dateMax))
        _totalPages = _movies_list['total_pages']
        print("Date range: " + str(_dateMin) + " - " + str(_dateMax))
        print("Total pages: " + str(_totalPages))
        print("Number of results: " + str(_movies_list['total_results']))
        # loop trough all pages
        for p in range(_totalPages):
            _movies_list = api_results('/discover/movie', '&sort_by=release_date.desc&primary_release_date.gte=' + str(_dateMin) + '&primary_release_date.lte=' + str(_dateMax) + '&page=' + str(p + 1))
            # created dataframe from results
            _df = pd.json_normalize(_movies_list['results'])
            _data = _data.append(_df)
            print("Page " + str(p + 1) + " of " + str(_totalPages) + " scrapped")
        print(_data.shape)
        return _data

    # initialize empty dataframe
    df_movies_list = pd.DataFrame()

    # scrapping for each month
    for m in range(12):
        # get last day of the month
        _month_lastDay = pd.to_datetime(str(_movies_year) + '-' + str(format(m + 1, '02d')), format="%Y-%m") + MonthEnd(0)
        _movies_list = get_movies_list(str(_movies_year) + '-' + str(format(m + 1, '02d')) + '-01', str(format(_month_lastDay, "%Y-%m-%d")))
        df_movies_list = df_movies_list.append(_movies_list, ignore_index=True)
        print(df_movies_list.shape)
        # adding delay to prevent api calls limit
        time.sleep(10)

    df_movies_list.to_csv(_fileName + '.csv')
    print(df_movies_list.shape)


def get_move_details(source_file, destination_file):
    '''
    Function to get more moves details and save results into csv file.

    Parameters:
         source_file (str): CSV file with movies ID. Provide file name with extension
         destination_file (str): file name without extension

    Returns:
        Saving movies results into CSV file
    '''
    print("Getting list of movies...")
    df_movies_list = pd.read_csv(source_file)
    df_movies_list_details = pd.DataFrame()
    total_movies = df_movies_list['id'].count()
    m = 0

    # loop trough all movies from list and get details for each move
    for movie_id in df_movies_list['id']:
        m += 1
        print("Getting " + str(m) + " movie of " + str(total_movies))
        movie_details = api_results('/movie/' + str(movie_id))
        df_movie_details = pd.json_normalize(movie_details)
        df_movies_list_details = df_movies_list_details.append(df_movie_details, ignore_index=True)

    df_movies_list_details.to_csv(destination_file + '.csv')
    print(df_movies_list_details.shape)
