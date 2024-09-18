from helpers import (
    add_book, view_books, lend_book, return_book, view_borrowers, exit_program
)

def main():
    while True:
        menu()
        choice = input("> ")
        if choice == "0":
            exit_program()
        elif choice == "1":
            add_book()
        elif choice == "2":
            view_books()
        elif choice == "3":
            lend_book()
        elif choice == "4":
            return_book()
        elif choice == "5":
            view_borrowers()
        else:
            print("Invalid choice")

def menu():
    print("Please select an option:")
    print("0. Exit the program")
    print("1. Add a new book")
    print("2. View all books")
    print("3. Lend a book")
    print("4. Return a book")
    print("5. View borrowers")

if __name__ == "__main__":
    main()
