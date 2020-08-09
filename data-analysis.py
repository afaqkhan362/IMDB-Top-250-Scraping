import matplotlib.pyplot as plt  # plotting library

import numpy as np

import pandas as pd


from utils import cleanAndConvertCurrencyToUSD  # helper function

imdb_top_250 = pd.read_csv("Imdb_Top_250.csv")

# remove the first column dataframe creates
imdb_top_cleaned = imdb_top_250.drop(columns='Unnamed: 0')


for index in range(len(imdb_top_cleaned['Budget'])):

    budget = imdb_top_cleaned['Budget'][index]

    # if budget has values other than numbers then this function will change it to USD
    if not np.isreal(budget) and 'Budget' in imdb_top_cleaned['Budget'][index]:
        imdb_top_cleaned['Budget'][index] = cleanAndConvertCurrencyToUSD(
            budget
        )

# removing commas from numeric values for below three dataframe columns
imdb_top_cleaned['Total No. of Ratings'] = imdb_top_cleaned['Total No. of Ratings'].str.replace(
    ',', ''
)

imdb_top_cleaned['Budget'] = imdb_top_cleaned['Budget'].str.replace(',', '')

imdb_top_cleaned['Gross USA'] = imdb_top_cleaned['Gross USA'].str.replace(
    ',', ''
)

# first plot for values rating score and total no. of ratings
plt.bar(
    imdb_top_cleaned['Total No. of Ratings'],
    imdb_top_cleaned['Rating Score']
)
plt.xlabel('Total No. of Ratings')
plt.ylabel('Rating Score')
plt.show()

# dropped nan values in dataframe to ease use dataframe for analysis in making plots
imdb_top_cleaned.dropna(inplace=True)

# second plot for budget against rating score
plt.bar(
    imdb_top_cleaned['Budget'],
    imdb_top_cleaned['Rating Score']
)
plt.xlabel('Budget')
plt.ylabel('Rating Score')
plt.show()

# if genre has any nan values, safety check for genres
imdb_top_cleaned = imdb_top_cleaned.dropna(
    subset=['Genre']).reset_index(
        drop=True
)

# removing ' from string to further use it for concatenation
imdb_top_cleaned['Genre'] = imdb_top_cleaned['Genre'].str.replace("'", "")

genre_splitted = imdb_top_cleaned['Genre'].str.split(',')

genre_character_length = genre_splitted.str.len()

# changing the datatype from str to float
imdb_top_cleaned['Gross USA'] = imdb_top_cleaned['Gross USA'].astype(float)
imdb_top_cleaned['Budget'] = imdb_top_cleaned['Budget'].astype(float)

# average earning gross usa
average_earning_usa = imdb_top_cleaned['Gross USA'] / \
    imdb_top_cleaned['Budget']

# genre earning separtely
genre_earning = pd.DataFrame(
    {
        'Average Earning Gross USA': np.repeat(average_earning_usa, genre_character_length),
        'Genre': np.concatenate(genre_splitted)
    }
)
genre_earning.sort_values(by='Genre', ascending=False, inplace=True)

genre_earning = genre_earning.reset_index(
    drop=True
)

# Below replaces are used to remove illegal characters that was corrupting the sorting
genre_earning['Genre'] = genre_earning['Genre'].str.replace(
    '[', ''
)
genre_earning['Genre'] = genre_earning['Genre'].str.replace(
    ']', ''
)

genre_earning['Genre'] = genre_earning['Genre'].str.replace(
    ' ', ''
)

genre_based_earning = genre_earning.groupby(
    'Genre')['Average Earning Gross USA'].mean().reset_index(name="Average Earning Gross USA")

genre_based_earning = genre_based_earning.reset_index(
    drop=True
)

genre_based_earning.sort_values(
    by='Genre', ascending=False, inplace=True)

genre_based_earning = genre_based_earning.reset_index(
    drop=True
)

# bar plot to see earnings and genre
plt.bar(
    genre_based_earning['Genre'],
    genre_based_earning['Average Earning Gross USA']
)
plt.xlabel('Genre')
plt.ylabel('Average Earning Gross USA in $')
plt.show()

# saving to csv file 
genre_based_earning.to_csv('Genre_Based_Gross_USA_Earning.csv')
