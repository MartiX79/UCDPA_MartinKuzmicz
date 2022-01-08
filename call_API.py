import requests
import os

def api_results(_command, _param=None):
    """
    Return API
    https://developers.themoviedb.org/3/getting-started/introduction
    """
    api_key = os.environ['TMDB_API_KEY']
    url = 'https://api.themoviedb.org/3/'
    if _param:
        response = requests.get(url + _command + '?api_key=' + api_key + _param)
    else:
        response = requests.get(url + _command + '?api_key=' + api_key)
    if response.status_code == 200:
        return response
    else:
        print("API Error")
