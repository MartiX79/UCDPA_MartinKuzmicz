import requests
import os


def api_results(_command, _param=None):
    """
    Return API results in json format

    Args:
        _command (str): GET command. Start with '/'
        _param (str, optional): Optional parameters, start with '&'

    Returns:
        json

    Notes:
        See more info about TMDB API
        https://developers.themoviedb.org/3/getting-started/introduction
    """
    api_key = os.environ['TMDB_API_KEY']
    url = 'https://api.themoviedb.org/3'
    if _param:
        response = requests.get(url + _command + '?api_key=' + api_key + _param)
    else:
        response = requests.get(url + _command + '?api_key=' + api_key)
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as error:
        print('API Error:')
        print(error)
    else:
        return response.json()