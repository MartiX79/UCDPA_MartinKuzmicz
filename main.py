from call_API import api_results
import API_to_CSV

# explore data
# get list of movies from 2021
movies_list = api_results('/discover/movie', '&primary_release_year=2021')

# check how many pages in result (max page parameter is 1000)
# https://developers.themoviedb.org/3/discover/movie-discover
total_pages = movies_list['total_pages']
print("Total pages for moves list: " + str(total_pages))

# save discovered movies results to csv file
#API_to_CSV.discoverMovies(2021, 'movies_list_2021')

# get more details about movies and save to csv
API_to_CSV.get_move_details('movies_list_2021.csv', 'movies_list_2021_details')