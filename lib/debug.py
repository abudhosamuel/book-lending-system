from db.models import Book, User, Transaction
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///book_lending.db')
Session = sessionmaker(bind=engine)

# Run debugging functions here if necessary
session = Session()
books = session.query(Book).all()
for book in books:
    print(f"Book: {book.title}, Author: {book.author}")
