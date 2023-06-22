def print_welcome():
    print("Welcome to WGUPS Package Delivery Service!\n")


def print_menu():
    menu = "1. View all packages at a given time period\n" \
           "2. Lookup a package by ID\n" \
           "3. TBD\n" \
           "4. Quit"
    print(menu)


def ui():
    print_welcome()
    user_input: str = ""
    while user_input != "4":
        print_menu()
        user_input = input("Enter a menu option: ")
        if user_input == '1':
            print("View all packages at a given time period")
        if user_input == "1":
            print("Available commands: help, quit")
        elif user_input == "4":
            print("See ya!")
            break
        else:
            print("\nUnknown command. Try again...\n")
