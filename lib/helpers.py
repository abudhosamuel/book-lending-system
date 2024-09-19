from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import Book, User, Transaction
import datetime
from datetime import date  


engine = create_engine('sqlite:///book_lending.db')
Session = sessionmaker(bind=engine)

def validate_title_or_author(input_string):
    if any(char.isalpha() for char in input_string):
        return True
    return False

def get_valid_input(prompt):
    while True:
        user_input = input(prompt)
        if validate_title_or_author(user_input):
            return user_input
        else:
            print("Invalid input. Please enter a valid string that contains letters (e.g., Red Dead Redemption 2).")

def add_book():
    title = get_valid_input("Enter book title: ")
    author = get_valid_input("Enter book author: ")

    session = Session()
    book = Book(title=title, author=author)
    session.add(book)
    session.commit()
    session.close()
    print(f"Book '{title}' by {author} added successfully.")

def view_books():
    session = Session()
    books = session.query(Book).all()
    if books:
        for book in books:
            print(f"{book.id}. {book.title} by {book.author}")
    else:
        print("No books found in the system.")
    session.close()

def lend_book():
    session = Session()

    
    view_books()
    book_id = int(input("Enter the book ID to lend: "))

    
    book = session.query(Book).get(book_id)
    if not book:
        print(f"No book found with ID {book_id}.")
        session.close()
        return

    user_name = input("Enter borrower's name: ")
    user_contact = input("Enter borrower's contact info: ")

    
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

    
    transaction = Transaction(book=book, user=user, due_date=due_date, returned=0)
    session.add(transaction)

    
    book_title = book.title

    session.commit()
    session.close()

    
    print(f"Book '{book_title}' lent to {user_name}.")

def return_book():
    session = Session()

    
    transactions = session.query(Transaction).filter_by(returned=0).all()
    if not transactions:
        print("No active transactions found.")
        session.close()
        return

    
    for transaction in transactions:
        print(f"{transaction.id}. {transaction.book.title} lent to {transaction.user.name}, due on {transaction.due_date}")

    transaction_id = int(input("Enter the transaction ID to mark as returned: "))

    
    transaction = session.query(Transaction).get(transaction_id)
    if not transaction:
        print(f"No transaction found with ID {transaction_id}.")
        session.close()
        return

    
    transaction.returned = 1

  
    book_title = transaction.book.title
    user_name = transaction.user.name

    
    session.commit()
    session.close()

    
    print(f"Book '{book_title}' lent to {user_name} returned successfully.")

def view_borrowers():
    session = Session()

    
    users = session.query(User).all()

    for user in users:
        
        active_transactions = session.query(Transaction).filter_by(user_id=user.id, returned=0).all()

        if active_transactions:
           
            print(f"Borrower: {user.name} - Contact: {user.contact_info}")
            for transaction in active_transactions:
                print(f"  Borrowed Book: {transaction.book.title}, Due Date: {transaction.due_date}")
        else:
           
            print(f"{user.name} has returned all books.")
            session.delete(user)

    
    session.commit()
    session.close()


def edit_borrower():
    
    session = Session()
    
    users = session.query(User).all()
    if not users:
        print("No borrowers found in the system.")
        session.close()
        return

    print("Select a borrower to edit:")
    for user in users:
        print(f"{user.id}. {user.name} - Contact: {user.contact_info}")

    try:
        user_id = int(input("Enter the ID of the borrower you want to edit: "))
    except ValueError:
        print("Invalid ID. Please enter a valid borrower ID.")
        session.close()
        return

    user = session.query(User).get(user_id)
    if not user:
        print(f"No borrower found with ID {user_id}.")
        session.close()
        return

   
    print(f"Editing borrower: {user.name} - Contact: {user.contact_info}")
    print("1. Edit name")
    print("2. Edit contact information")
    print("3. Edit due date of borrowed books")
    choice = input("Enter the number corresponding to the detail you want to edit: ")

    if choice == "1":
        new_name = input("Enter new name: ").strip()
        if new_name:
            user.name = new_name
            print(f"Borrower name updated to: {new_name}")
        else:
            print("Invalid input. Name not updated.")
    elif choice == "2":
        new_contact = input("Enter new contact information: ").strip()
        if new_contact:
            user.contact_info = new_contact
            print(f"Borrower contact information updated to: {new_contact}")
        else:
            print("Invalid input. Contact information not updated.")
    elif choice == "3":
        
        active_transactions = session.query(Transaction).filter_by(user_id=user.id, returned=0).all()
        if not active_transactions:
            print(f"No active transactions found for borrower {user.name}.")
        else:
            print("Select a transaction to edit the due date:")
            for transaction in active_transactions:
                print(f"{transaction.id}. Book: {transaction.book.title}, Due Date: {transaction.due_date}")
            
            try:
                transaction_id = int(input("Enter the transaction ID to edit the due date: "))
            except ValueError:
                print("Invalid ID. Please enter a valid transaction ID.")
                session.close()
                return
            
            
            transaction = session.query(Transaction).get(transaction_id)
            if not transaction or transaction.user_id != user.id:
                print(f"No transaction found with ID {transaction_id} for borrower {user.name}.")
                session.close()
                return
            
            new_due_date_str = input("Enter new due date (YYYY-MM-DD): ")
            try:
                new_due_date = datetime.datetime.strptime(new_due_date_str, "%Y-%m-%d")
                transaction.due_date = new_due_date
                print(f"Due date updated to: {new_due_date}")
            except ValueError:
                print("Invalid date format. Due date not updated. Please use YYYY-MM-DD.")
    else:
        print("Invalid choice. No changes made.")
    
    
    session.commit()
    session.close()


def view_overdue_books():
    session = Session()

    
    transactions = session.query(Transaction).filter_by(returned=0).all()
    overdue_found = False

    for transaction in transactions:
        if transaction.due_date < date.today():
            overdue_found = True
            days_overdue = (date.today() - transaction.due_date).days
            fine = days_overdue * 10  # fine is $10
            transaction.fine = fine

            print(f"Overdue Book: {transaction.book.title} (ID: {transaction.book.id})")
            print(f"Borrower: {transaction.user.name} - Contact: {transaction.user.contact_info}")
            print(f"Due Date: {transaction.due_date}, Days Overdue: {days_overdue}, Fine: ${fine}")

    if not overdue_found:
        print("No overdue books found.")

    
    session.commit()
    session.close()


def search_books():
    session = Session()
    keyword = input("Enter keyword to search for books (title or author): ").strip()
    
    
    books = session.query(Book).filter(
        (Book.title.ilike(f'%{keyword}%')) | (Book.author.ilike(f'%{keyword}%'))
    ).all()
    
    if books:
        print(f"Books matching '{keyword}':")
        for book in books:
            print(f"{book.id}. {book.title} by {book.author}")
    else:
        print(f"No books found matching the keyword '{keyword}'.")
    
    session.close()


def search_borrowers():
    session = Session()
    keyword = input("Enter keyword to search for borrowers (name or contact info): ").strip()
    
   
    borrowers = session.query(User).filter(
        (User.name.ilike(f'%{keyword}%')) | (User.contact_info.ilike(f'%{keyword}%'))
    ).all()
    
    if borrowers:
        print(f"Borrowers matching '{keyword}':")
        for borrower in borrowers:
            print(f"{borrower.id}. {borrower.name} - Contact: {borrower.contact_info}")
    else:
        print(f"No borrowers found matching the keyword '{keyword}'.")
    
    session.close()


def exit_program():
    """
    Exits the program.
    """
    print("Goodbye!")
    exit()
