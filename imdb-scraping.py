import time

from bs4 import BeautifulSoup

import pandas as pd
import requests

from constants import imdb_base_url, imdb_top_250_movies_url, user_agent, user_agent_2
from utils import removeIllegalCharacters, removeIllegalCharactersFromBudgetValues, findBudgetAndGrossUSA


request_header = {
    'user-agent': user_agent
}

################################# FOR FINDING THE LIST OF MOVIES ##############################################

imdb_web_page = requests.get(
    imdb_top_250_movies_url, headers=request_header
)

imdb_web_content = BeautifulSoup(imdb_web_page.content, 'html.parser')

movies_detailed_information = imdb_web_content.find(
    class_='lister-list')  # main class containing movie list

# This is for getting the movie list

movies_html_list = movies_detailed_information.find_all(class_='titleColumn')

movies_list = [
    removeIllegalCharacters(movie.get_text()) for movie in movies_html_list
]

############################# This is for getting urls of the movies in list #################################

movie_a_tags = movies_detailed_information.find_all(
    'a')  # URL information for movies

movies_url = [movie_url['href'] for movie_url in movie_a_tags]

# Deleting duplication movie urls from list
movies_url_duplicate_deleted = list(dict.fromkeys(movies_url))

total_no_of_ratings = []
rating_score = []
genre = []
budget = []
gross_usa = []

################################# Movie Detail for each of the url found in above section ####################

for url in movies_url_duplicate_deleted:

    index = movies_url_duplicate_deleted.index(url)

    movie_web_page = requests.get(  # GET request for individual movie
        imdb_base_url+url, headers=request_header
    )

    movie_soup_object = BeautifulSoup(movie_web_page.content, 'html.parser')

    movie_main_content = movie_soup_object.find(id='pagecontent')

    movie_genre_obj = movie_main_content.find(class_='subtext')

    movie_genres = movie_genre_obj.find_all('a')

    genres = [
        genre.get_text() for genre in movie_genres if 'genres' in genre.get('href')
    ]

    title_details = movie_main_content.find(id='titleDetails')

    budget_details = title_details.find_all(class_='txt-block')

    budget_details_text = [  # Fetching the budget details and removing corrupt data from the payload
        removeIllegalCharactersFromBudgetValues(budget.get_text()) for budget in budget_details
    ]

    # Method to find Budget and Gross USA from data
    budget_required = findBudgetAndGrossUSA(budget_details_text)

    total_no_of_ratings.append(movie_main_content.find(  # insertion of total no of ratings
        itemprop='ratingCount'
    ).get_text())

    rating_score.append(movie_main_content.find(  # inserting of individual rating score
        itemprop='ratingValue'
    ).get_text())

    genre.append(genres)  # insertion of genres

    budget.append(([
        budget for budget in budget_required if 'Budget' in budget
    ].pop(0)).replace('Budget:$', ''))  # to find Budget in Array or Budget and Gross USA

    gross_usa.append(([
        gross_usa for gross_usa in budget_required if 'Gross' in gross_usa
    ].pop(0)).replace('Gross USA: $', ''))  # to find Gross USA in Array or Budget and Gross USA

    if(index > 150):  # To avoid blocking, different user agent for requests will be used to avoid robot detection
        request_header['user-agent'] = user_agent_2
    # information logging to see if its working :)
    print('Done index:'+index.__str__())
    time.sleep(3)


movies_with_details = pd.DataFrame(
    {
        'Movie': movies_list,
        'Rating Score': rating_score,
        'Total No. of Ratings': total_no_of_ratings,
        'Genre': genre,
        'Budget': budget,
        'Gross USA': gross_usa
    }
)

movies_with_details.to_csv('Imdb_Top_250.csv')

print('Execution ended Successfully. Please Check your File')
