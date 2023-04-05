from load_data import load_data
from fuzzywuzzy import fuzz, process
import matplotlib.pyplot as plt
import numpy as np


ALL_DATA = load_data()


def main():
    create_speed_histogram()
    for data in ALL_DATA["data"]:
        print(data["SPEED"])
    """A command line interface"""
    print_starting_message()
    while True:
        user_input = input()
        data = execute_user_input(user_input)

        if data:
            print_data(data)


def search_ship_fuzzy_partial(search_ship_word: str):
    """
    Searching for partial fuzzy wuzzy highest match of ship names
    with search_ship_word and return list of info
    for matched ship in search
    :return: list['key: value', ....] info on matched ship in search
    """
    # creating list of shipnames from ALL_DATA
    list_of_ship_names = []
    for data in ALL_DATA["data"]:
        list_of_ship_names.append(data["SHIPNAME"].lower())

    # Find the best match of search_ship_word in list_of_ship_names
    best_match = process.extractOne(search_ship_word, list_of_ship_names, scorer=fuzz.token_set_ratio)

    # best_match is a tuple (matched_key, score)
    matched_ship_name, __ = best_match
    index = list_of_ship_names.index(matched_ship_name)

    info_list = [f"{key}: {value}" for key, value in ALL_DATA["data"][index].items()]
    return info_list


def print_data(data):
    """Regular for loot to print iterable data"""
    for info in data:
        print(info)


def execute_user_input(user_input: str):
    """
    Executing user input. if input right - return data
    if input wrong or cause an error - return None
    """
    user_input = user_input.split()
    try:
        command = user_input[0]
        if len(user_input) > 1:
            argument = (user_input[1])
            return MENU_DISPATCH[command](argument)

        return MENU_DISPATCH[user_input[0]]()
    except Exception:
        return None


def print_starting_message():
    """Printing starting message of a program"""
    print("Welcome to the Ships CLI! Enter 'help' to view available commands.")


def get_all_countries_no_duplicates():
    """ Returns list with countries, a,b,c order"""
    countries = set()
    for data in ALL_DATA["data"]:
        countries.add(data["COUNTRY"])

    countries = list(countries)
    countries.sort()
    return tuple(countries)


def get_top_countries(num_countries):
    """
    returns list of top num_countries by its ships
    'country: number_ships'
    """
    num_countries = int(num_countries)
    ship_per_country = {}
    # counting countries by it ships
    for data in ALL_DATA["data"]:
        country_from_data = data["COUNTRY"]
        if country_from_data not in ship_per_country:
            ship_per_country[country_from_data] = 0

        ship_per_country[country_from_data] += 1

    # sorting countries by number of ships
    sorted_dict = [f"{country}: {ships}" for country, ships
                   in sorted(
                        ship_per_country.items(),
                        key=lambda item: item[1],
                        reverse=True)
                   ]
    return sorted_dict[:num_countries]


def get_ships_by_types():
    """
    Returns list of how many ships of each type
    ['ship_type: number',...]
    """
    # counting ship types
    count_ship_types_dict = {}
    for data in ALL_DATA["data"]:
        ship_type = data["TYPE_SUMMARY"]
        if ship_type not in count_ship_types_dict:
            count_ship_types_dict[ship_type] = 0
        count_ship_types_dict[ship_type] += 1

    # making list of ship types from high to low
    list_of_ship_types = [
        f"{key}: {value}"
        for key, value in sorted(
            count_ship_types_dict.items(),
            key=lambda item: item[1],
            reverse=True
        )
    ]
    return list_of_ship_types


def create_speed_histogram():
    """
    Creates a histogram of ship speeds from a list of ship data.
    The histogram has bins with a width of 5 units each.

    The function reads the ship speeds from the ALL_DATA global variable,
    creates a histogram with matplotlib, saves it as a PNG file
    in the project folder, and then displays the histogram.
    """
    # creating list with ship speed floats
    ship_speeds = [float(data["SPEED"]) for data in ALL_DATA["data"]]

    # Define the bins for the histogram
    max_speed = max(ship_speeds)
    bins = np.arange(0, max_speed + 1, 5)

    # Create a histogram of the ship speeds
    plt.hist(ship_speeds, bins=bins, edgecolor='black', alpha=0.7)

    # Set the labels and title
    plt.xlabel('Speed')
    plt.ylabel('Frequency')
    plt.title('Histogram of Ship Speeds')

    # Save the histogram as a PNG file in the project folder
    plt.savefig('ship_speeds_histogram.png')

    # Show the histogram
    plt.show()


def get_menu_commands():
    """return all the menu options"""
    menu_list = ["Available commands:", "help", "show_countries",
                 "top_countries <num_countries>", "ships_by_types",
                 "search_ship <search_name>", "speed_histogram"]
    return menu_list


MENU_DISPATCH = {
    "help": get_menu_commands,
    "show_countries": get_all_countries_no_duplicates,
    "top_countries": get_top_countries,
    "ships_by_types": get_ships_by_types,
    "search_ship": search_ship_fuzzy_partial,
    "speed_histogram": create_speed_histogram
}
if __name__ == '__main__':
    main()
