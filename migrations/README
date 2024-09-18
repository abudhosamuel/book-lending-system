Python Application

# Book Lending System

The Book Lending System is a command-line interface (CLI) application that enables users to manage a small library or book-lending operation. The system keeps track of books, borrowers, and transactions (i.e., books lent out and returned). Users can add books, lend books to borrowers, return books, and view a list of current borrowers and their borrowed books.

The system is built using Python with SQLAlchemy ORM to manage interactions with an SQLite database. It is designed to simulate a simple library book-lending system, providing core functionality for managing books, borrowers, and transactions efficiently.

Features and Functionality
Add a Book
The system allows users to add a new book to the library by providing the book's title and author. The input is validated to ensure it contains alphabetic characters (so that invalid data is not entered).

View All Books
Users can view a list of all books in the library, along with the book IDs, titles, and authors. This helps in selecting the right book for lending.

Lend a Book
Users can lend books to borrowers. The system checks for the availability of the book (i.e., whether it's already lent out) and registers the borrowing transaction by linking a user with a book, setting a due date, and marking the transaction as active.

Return a Book
When a borrower returns a book, the system allows the user to mark the book as returned, updating the transaction status and ensuring that the book is available for lending again.

View Borrowers
Users can view a list of all current borrowers along with the books they have borrowed and the due dates. Borrowers who have returned all their books are automatically removed from the system.

Exit the Program
Users can exit the program at any time by selecting the exit option from the main menu.




## Authors

- [@abudhosamuel](https://www.github.com/abudhosamuel)




## Badges

Add badges from somewhere like: [shields.io](https://shields.io/)

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
[![GPLv3 License](https://img.shields.io/badge/License-GPL%20v3-yellow.svg)](https://opensource.org/licenses/)
[![AGPL License](https://img.shields.io/badge/license-AGPL-blue.svg)](http://www.gnu.org/licenses/agpl-3.0)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)Deployment

Pre-requisites
Ensure that Python 3.x is installed on your system.
Install Pipenv to manage the virtual environment and dependencies. You can install Pipenv using the following command:

pip install pipenv

Setting Up the Project
Clone or Download the Repository: Download or clone the project repository to your local machine.

git clone <https://github.com/abudhosamuel/book-lending-system>
cd book-lending-system
Install Dependencies: Use Pipenv to install the required dependencies (SQLAlchemy, etc.). Run the following command to install dependencies:

pipenv install

Activate the Virtual Environment: Start the virtual environment by running:

pipenv shell

Create the Database: The seed.py script initializes the database and adds some initial data. Run the following command to set up the database and insert sample records:

python lib/db/seed.py

Running the Program
Once the setup is complete, you can run the program using the following command:

python lib/cli.py

This will start the CLI-based Book Lending System. You can then interact with the menu to add books, lend books, return books, view borrowers, or exit the program.
## License

[MIT](https://choosealicense.com/licenses/mit/)


## Acknowledgements

Acknowledgements

Font Awesome
Feel free to contribute to the project by submitting a pull request or opening an issue.

