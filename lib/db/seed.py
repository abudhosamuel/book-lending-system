from models import Base, Book, User, Transaction
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime

# Create an engine and a session
engine = create_engine('sqlite:///book_lending.db')
Session = sessionmaker(bind=engine)
session = Session()

# Create all tables (Book, User, Transaction)
Base.metadata.create_all(engine)

# Seed data
book1 = Book(title="The Catcher in the Rye", author="J.D. Salinger")
user1 = User(name="John Doe", contact_info="john@example.com")
transaction1 = Transaction(book=book1, user=user1, due_date=datetime.date(2023, 12, 1), returned=0)

session.add_all([book1, user1, transaction1])
session.commit()
session.close()
