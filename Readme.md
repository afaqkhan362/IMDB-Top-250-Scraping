# Before moving on first install the libraries provided in requirements.txt file

User requirements.txt for installation of libraries used



# Scraping IMDB top 250 movie list

For scraping the file names "imdb-scrapping.py" should be loaded and run.


I have used two user agents to avoid blocking with a delay of 3 ms

First 150 requests will be done by user agent 1 and the other by user agent 2 (provided in constants.py)


## constants.py and utils.py files

constants.py contains the hard coded constants used in our project, to avoid errors.

utils.py provide us with simple methods that are used by our project like currency converter and removal of
illegal characters in data payload


# How to Run Imdb Scraper

please load the file name "imdb-scraping.py" and run it in vs code of any other editor (Spyder or Jupyter)

Upon successful completion of code in this file user will be shown a log that processing complete
and a relevant csv file will be generated in the workspace you are working with filename "Imdb_Top_250.csv"

Now that our file is created, now is the time to apply data analysis on our file

load another file in the repository named "data-analysis.py". Run this file or execute the code inside it 
this file will open the csv created in the first file and will start working on its data cleaning and sorting 
to give you the output results on the screen as shown in the Document "Assignment_Approach_and_Results.docx"

Upon successful completion of data-analysis.py file, you will have another file created named "Genre_Based_Gross_USA_Earning.csv". This file contains the total average earning gross USA for each genre.

## Additional Information

No such assumptions were made , everything is inside the code and also relevant commenting is added as well to 
help you understand the code well.

Apart from this 3 of the currencies were not present in the library i used to i have used the google currency 
exchange rate for USD. Those are included in constants.py file to help anyone use it in future.

Beautifier pep8 was also used in order to maintain and set the code if formatting or any other issue with alignment 
is missed. But the code was organized first, pep8 was the last resort.

Note that the csv files that will be created will be in the workspace you will be working and data-analysis file 
will pick it up from there to do analysis on that file.

An additional bar plot is made to help understand the graph for Average Gross USA earning to Each Genre.

## THE END

Tadaa you are done and you have your results :) 
