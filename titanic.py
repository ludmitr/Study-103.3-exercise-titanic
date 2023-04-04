from load_data import load_data
ALL_DATA = load_data()



def main():
    # print("\n".join(get_all_countries_no_duplicates()))
    # check = get_menu_dispatch_keys()
    print_starting_message()
    while True:
        user_input = input("input: ")
        data = execute_user_input(user_input)
        if data:
            print(data)
        else:
            print("Wrong command, try again")


def execute_user_input(user_input: str):
    user_input = user_input.split()
    command = user_input[0]
    try:
        if len(user_input) > 1:
            argument = user_input[1]
            return MENU_DISPATCH[command](argument)
        else:
            return MENU_DISPATCH[user_input[0]]()
    except:
        return None


def get_menu_dispatch_keys():
    """return all the menu options"""
    return MENU_DISPATCH.keys()


def print_starting_message():
    print("Welcome to the Ships CLI! Enter 'help' to view available commands.")


def get_all_countries_no_duplicates():
    """ Returns list with countries, a,b,c order"""
    countries = set()
    for data in ALL_DATA["data"]:
        countries.add(data["COUNTRY"])

    countries = list(countries)
    countries.sort()
    return tuple(countries)

def get_top_counrties():
    pass


MENU_DISPATCH = {
    "help": get_menu_dispatch_keys,
    "show_countries": get_all_countries_no_duplicates,
    "top_countries": get_top_counrties
}
if __name__ == '__main__':
    main()
