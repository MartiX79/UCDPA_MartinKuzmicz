import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from ast import literal_eval
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from call_API import api_results
import API_to_CSV

# if no new dada needed and working on existing csv files, comment lines from 10 - 26
# get list of movies from 2021 from API
_, movies_list_results = api_results('/discover/movie', '&primary_release_year=2021')

# check how many pages in result (max page parameter is 1000)
# https://developers.themoviedb.org/3/discover/movie-discover
total_pages = movies_list_results['total_pages']
print("Total pages for moves list: " + str(total_pages))

# save discovered movies results to csv file
#API_to_CSV.discoverMovies(2021, 'movies_list_2021')

# get details for all movies from the list and save to csv
API_to_CSV.get_move_details('movies_list_2021.csv', 'movies_list_2021_details')

# get keywords for movies from list and save to csv file
API_to_CSV.get_addition_details('movies_list_2021.csv', 'keywords', 'keywords')


def convert_categories(x):
    return ','.join([x['name'] for x in x])

# get list of columns
movies_df = pd.read_csv('movies_list_2021_details.csv')
print(movies_df.columns)
print(movies_df.shape)

# drop unnecessary columns
movies_df = movies_df[['id','title','genres','budget','revenue','vote_average','vote_count']]
print(movies_df.columns)

# change default display columns limit to see data from all columns
pd.set_option('max_columns', None)
print(movies_df.head())

# replace 0 with NaN to indicate missing value and not the 0 revenue
movies_df['revenue'] = movies_df['revenue'].replace(0, np.nan)
movies_df['budget'] = movies_df['budget'].replace(0, np.nan)
movies_df['vote_average'] = movies_df['vote_average'].replace(0, np.nan)
movies_df['vote_count'] = movies_df['vote_count'].replace(0, np.nan)
movies_df.drop_duplicates(keep=False, inplace=True)         # remove duplicates

# access genres data
movies_df['genres'] = movies_df['genres'].apply(literal_eval)
movies_df['genres'] = movies_df['genres'].apply(convert_categories)

# analise data source
print(movies_df.shape)
print(movies_df.info())
print(movies_df.head())


# get keywords data
keywords_df = pd.read_csv('keywords.csv')

print(keywords_df.head())
print(keywords_df.columns)
print(keywords_df.shape)

# clean Keywords df data
keywords_df['keywords'] = keywords_df['keywords'].apply(literal_eval)
keywords_df['keywords'] = keywords_df['keywords'].apply(convert_categories)
keywords_df['keywords'] = keywords_df['keywords'].replace('', np.nan)
keywords_df = keywords_df.dropna()

print(keywords_df.head())
print(keywords_df.shape)

# merge two dataframes
movies_df = movies_df.merge(keywords_df, how='left', on='id')
movies_df = movies_df[['id','title','genres','budget','revenue','vote_average','vote_count','keywords']]
print(movies_df.shape)
print(movies_df.head())

# analise content - keywords, check occurrence
keyword_occurrence = keywords_df.apply(lambda x: pd.Series(x['keywords']), axis=1).stack().reset_index(level=1, drop=True)
keyword_occurrence = keyword_occurrence.value_counts()
keywords_top10 = keyword_occurrence.head(10)
print(keywords_top10)

# check for nulls
print(movies_df[['id','title','genres','keywords']].isnull().sum())

plt.bar(keywords_top10.keys().tolist(), keywords_top10.tolist())
plt.subplots_adjust(bottom=0.4)
plt.xticks(rotation=60, horizontalalignment="center")
plt.xlabel("Keywords")
plt.ylabel("Occurrence")
plt.title("Occurrence of top 10 keywords")
plt.show()


# rating score weight (no. of vote_average / vote_count)
movies_df['rating_score'] = movies_df['vote_average']/movies_df['vote_count']

# analise votes
vote_mean = movies_df['vote_average'].mean()
print("vote mean -> " + str(vote_mean))

minimum_vote = movies_df['vote_count'].quantile(0.85)
print(minimum_vote)

movies_voted = movies_df.copy().loc[movies_df['vote_count'] >= minimum_vote]
movies_voted = movies_voted[['id','title','vote_average','vote_count']]
print(movies_voted.shape)


# calculating weighted average rating (IMDB formula)
def weighted_rating (x, min_vote = minimum_vote, mean_vote = vote_mean):
    no_votes = x['vote_count']
    avg_vote = x['vote_average']
    return (no_votes/(no_votes+minimum_vote) * avg_vote) + (min_vote / (min_vote + no_votes) * mean_vote)

movies_voted['score'] = movies_voted.apply(weighted_rating, axis=1)

movies_voted = movies_voted.sort_values('score', ascending=False)
# top 10 movies
movies_voted['score'] = movies_voted['score'].map("{:,.1f}".format)
print(movies_voted.head(10))

# graph of ratings
plt.figure(figsize=(10, 4))
movies_voted['vote_average'].hist(bins=20)
plt.xlabel("Rating")
plt.ylabel("Votes")
plt.title("Average votes")
plt.show()

# recommendation

# crate new column by combining keywords and genres
movies_df['features'] = movies_df['keywords'] + ',' + movies_df['genres']
movies_df['features'] = movies_df['features'].fillna('')

print(movies_df['features'])

# remove comma(,) and make all lowercase letters
movies_df['features'] = movies_df['features'].str.lower().str.replace(","," ")

print(movies_df['features'])

# F-IDF Remove all stop words
tfidf = TfidfVectorizer(stop_words='english')

# TF-IDF matrix
tfidf_matrix = tfidf.fit_transform(movies_df['features'])

# similarity matrix
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
m_index = pd.Series(movies_df.index, index=movies_df['title'])

print(m_index[:5])

def recommended_movies(title):
    movie_index = m_index[title]
    recom_movies_list = list(enumerate(cosine_sim[movie_index]))
    recom_movies_list = sorted(recom_movies_list, key=lambda x: x[1], reverse=True)
    recom_movies_list = recom_movies_list[1:6]
    movie_indices = [i[0] for i in recom_movies_list]
    return movies_df['title'].iloc[movie_indices]

print("==================")
print(recommended_movies('Spider-Man: No Way Home'))
print("")
print(recommended_movies('Black Widow'))
