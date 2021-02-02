import json
import os
from tqdm import tqdm


def fill_data_points_currencies(data_symbol, options=None):
    if options is None:
        options = {}
    try:
        options['short_name'] = data_symbol['quoteType']['shortName']
    except (TypeError, KeyError):
        options['short_name'] = 'None'
    try:
        options['currency'] = data_symbol['price']['currency']
    except (TypeError, KeyError):
        options['currency'] = 'None'
    try:
        options['exchange'] = data_symbol['quoteType']['exchange']
    except (TypeError, KeyError):
        options['exchange'] = 'None'
    try:
        options['market'] = data_symbol['quoteType']['market']
    except (TypeError, KeyError):
        options['market'] = 'None'
    return options


def make_directories_and_fill_json_currencies(data, directory_name):
    try:
        os.mkdir(directory_name)
        currency_dictionaries = {}
        symbols_dictionaries = {}
        Errors = {}
    except FileExistsError:
        return print(directory_name + " already exists. Please delete or rename the directory "
                                      "before continuing")

    print("Creating folder structure")
    for symbol in tqdm(data):
        options = fill_data_points_currencies(data[symbol])
        symbols_dictionaries[symbol] = options

        try:
            currency = data[symbol]['summaryDetail']['currency']

            if currency not in currency_dictionaries and len(currency) > 0:
                currency_dictionaries[currency] = {}

            currency_dictionaries[currency][symbol] = options
        except (TypeError, KeyError) as e:
            Errors[symbol + ' Category'] = "Could not be categorized due to: " + str(e)

    print('Filling folders with data..')
    for category in tqdm(currency_dictionaries.keys()):
        category_new = category.replace('/', ' ')
        with open(directory_name + '/' + category_new + '.json', 'w') as handle:
            json.dump(currency_dictionaries[category], handle)
    with open(directory_name + '/_' + directory_name + ".json", 'w') as handle:
        json.dump(symbols_dictionaries, handle)

    if Errors:
        print("A couple of tickers were not able to be categorized. Please check the output of this function.")
        return Errors