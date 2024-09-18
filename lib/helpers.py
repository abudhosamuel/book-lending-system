from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import Book, User, Transaction
import datetime

engine = create_engine('sqlite:///book_lending.db')
Session = sessionmaker(bind=engine)

def validate_title_or_author(input_string):
    """
    Validates that the input contains at least one letter and is not purely numeric.
    Returns True if valid, False otherwise.
    """
    if any(char.isalpha() for char in input_string):
        return True
    return False

def get_valid_input(prompt):
    """
    Prompts the user for input and ensures the input is valid using the validate_title_or_author function.
    """
    while True:
        user_input = input(prompt)
        if validate_title_or_author(user_input):
            return user_input
        else:
            print("Invalid input. Please enter a valid string that contains letters (e.g., Red Dead Redemption 2).")

def add_book():
    """
    Adds a book to the system.
    """
    title = get_valid_input("Enter book title: ")
    author = get_valid_input("Enter book author: ")

    session = Session()
    book = Book(title=title, author=author)
    session.add(book)
    session.commit()
    session.close()
    print(f"Book '{title}' by {author} added successfully.")

def view_books():
    """
    Displays all books in the system.
    """
    session = Session()
    books = session.query(Book).all()
    if books:
        for book in books:
            print(f"{book.id}. {book.title} by {book.author}")
    else:
        print("No books found in the system.")
    session.close()

def lend_book():
    """
    Lends a book to a borrower.
    """
    session = Session()

    # Display available books
    view_books()
    book_id = int(input("Enter the book ID to lend: "))

    # Retrieve the book by ID, keeping it within the session
    book = session.query(Book).get(book_id)
    if not book:
        print(f"No book found with ID {book_id}.")
        session.close()
        return

    user_name = input("Enter borrower's name: ")
    user_contact = input("Enter borrower's contact info: ")

    # Retrieve or create the user
    user = session.query(User).filter_by(name=user_name).first()
    if not user:
        user = User(name=user_name, contact_info=user_contact)
        session.add(user)

    due_date_str = input("Enter due date (YYYY-MM-DD): ")
    try:
        due_date = datetime.datetime.strptime(due_date_str, "%Y-%m-%d")
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD.")
        session.close()
        return

    # Create a new transaction for lending the book
    transaction = Transaction(book=book, user=user, due_date=due_date, returned=0)
    session.add(transaction)

    # Access book title before closing the session
    book_title = book.title

    session.commit()
    session.close()

    # Print the success message after closing the session
    print(f"Book '{book_title}' lent to {user_name}.")

def return_book():
    """
    Marks a book as returned.
    """
    session = Session()

    # Display all active (unreturned) transactions
    transactions = session.query(Transaction).filter_by(returned=0).all()
    if not transactions:
        print("No active transactions found.")
        session.close()
        return

    # List all unreturned books
    for transaction in transactions:
        print(f"{transaction.id}. {transaction.book.title} lent to {transaction.user.name}, due on {transaction.due_date}")

    transaction_id = int(input("Enter the transaction ID to mark as returned: "))

    # Fetch the transaction by ID
    transaction = session.query(Transaction).get(transaction_id)
    if not transaction:
        print(f"No transaction found with ID {transaction_id}.")
        session.close()
        return

    # Mark the book as returned
    transaction.returned = 1

    # Access the book title and user name before closing the session
    book_title = transaction.book.title
    user_name = transaction.user.name

    # Commit the changes
    session.commit()
    session.close()

    # Display success message after closing the session
    print(f"Book '{book_title}' lent to {user_name} returned successfully.")

def view_borrowers():
    """
    Displays all borrowers and the books they have borrowed. 
    Removes borrowers who have returned all books.
    """
    session = Session()

    # Get all users
    users = session.query(User).all()

    for user in users:
        # Check if the user has any active (unreturned) transactions
        active_transactions = session.query(Transaction).filter_by(user_id=user.id, returned=0).all()

        if active_transactions:
            # Display user information and books they have borrowed
            print(f"Borrower: {user.name} - Contact: {user.contact_info}")
            for transaction in active_transactions:
                print(f"  Borrowed Book: {transaction.book.title}, Due Date: {transaction.due_date}")
        else:
            # If the user has no active transactions, delete the user from the system
            print(f"{user.name} has returned all books.")
            session.delete(user)

    # Commit the session to apply the deletion of users with no outstanding transactions
    session.commit()
    session.close()


def exit_program():
    """
    Exits the program.
    """
    print("Goodbye!")
    exit()
