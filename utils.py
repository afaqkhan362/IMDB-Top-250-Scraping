# imported to convert the currencies to USD
from currency_converter import CurrencyConverter

from constants import French_Currency, German_Currency, Russian_Currency

def removeIllegalCharacters(self):

    # Below replacement is done after inspecting the data fetched from Web. It can be different
    # in different scenarios
    moviesListsWithYearAndIndex = self.replace('\n', '').replace('      ', '')

    movieListSplitted = moviesListsWithYearAndIndex.split(".", 1)

    moviesList = movieListSplitted[1].split("(", 1)

    return moviesList[0]


def removeIllegalCharactersFromBudgetValues(self):
    # Removing spacing and different text in budget and gross usa values
    return self.replace('\n', '').replace('            (estimated)', '').replace('        ', '')


def findBudgetAndGrossUSA(self):

    required_budget = []
    # For some movies on IMDB the Budget or Gross USA can be empty, Check to avoid code breakage
    if any('Budget' in element for element in self):
        required_budget.append(([
            gross_usa_budget for gross_usa_budget in self if 'Budget' in gross_usa_budget
        ]).pop(0))
    else:
        required_budget.append('Budget:$N/A')

    if any('Gross USA:' in element for element in self):
        required_budget.append(([
            gross_usa_budget for gross_usa_budget in self if 'Gross USA:' in gross_usa_budget
        ]).pop(0))
    else:
        required_budget.append('Gross USA: $N/A')

    return required_budget


def cleanAndConvertCurrencyToUSD(self):
    convert_currency = CurrencyConverter()

    self = self.replace('Budget:', '')

    currency = self[0:3]
    amount = self[3:]
    # Values for different currencies taken from web on Date: 08th of August 2020
    if (currency == French_Currency):  # Currency Converter does not support French Currency
        amount = amount.replace(',', '')
        return (float(amount)*(1/5.5236))

    if (currency == German_Currency):  # Currency Converter does not Support German Currency
        amount = amount.replace(',', '')
        return (float(amount)*0.6028)

    if (currency == Russian_Currency):  # Also the russian currency
        amount = amount.replace(',', '')
        return (float(amount)*0.014)

    amount = convert_currency.convert(amount.replace(',', ''), currency, 'USD')

    return str(amount)  # to keep consistency of string in data frame
