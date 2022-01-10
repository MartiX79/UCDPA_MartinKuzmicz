from call_API import api_results
import pandas as pd
import time
from pandas.tseries.offsets import MonthEnd


def discoverMovies(_movies_year, _fileName):
    # over 1000 pages in results
    # split data and call each month secretly
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
        print(_data.shape)
        return _data

    # initialize empty dataframe
    df_movies_list = pd.DataFrame()

    # scrapping for each month
    for m in range(1):
        # get last day of the month
        _month_lastDay = pd.to_datetime(str(_movies_year) + '-' + str(format(m + 1, '02d')), format="%Y-%m") + MonthEnd(0)
        _movies_list = get_movies_list(str(_movies_year) + '-' + str(format(m + 1, '02d')) + '-01', str(format(_month_lastDay, "%Y-%m-%d")))
        df_movies_list = df_movies_list.append(_movies_list)
        print(df_movies_list.shape)
        # adding delay to prevent api calls limit
        time.sleep(10)

    # reset index for whole data range
    df_movies_list.reset_index(inplace=True, drop=True)
    df_movies_list.to_csv(_fileName)
    print(df_movies_list.shape)