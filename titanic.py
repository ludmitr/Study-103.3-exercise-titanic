from load_data import load_data
ALL_DATA = load_data()


def main():
    """A command line interface"""
    # print("\n".join(get_all_countries_no_duplicates()))
    # check = get_menu_dispatch_keys()
    print_starting_message()
    while True:
        user_input = input()
        data = execute_user_input(user_input)

        if data:
            print_data(data)



def print_data(data):
    """Regular for loot to print iterable data"""
    for info in data:
        print(info)


def execute_user_input(user_input: str):
    """
    Executing user input. if input right - return data
    if input wrong or cause a error - return None
    """
    user_input = user_input.split()
    try:
        command = user_input[0]
        if len(user_input) > 1:
            argument = int(user_input[1])
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


def get_menu_dispatch_keys():
    """return all the menu options"""
    menu_list = ["Available commands:", "help", "show_countries", "top_countries <num_countries>"]
    return menu_list


MENU_DISPATCH = {
    "help": get_menu_dispatch_keys,
    "show_countries": get_all_countries_no_duplicates,
    "top_countries": get_top_countries
}
if __name__ == '__main__':
    main()
