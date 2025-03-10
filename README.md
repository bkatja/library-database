# Library Database Program

## Description
`my_library_db.py` is a simple command-line program for managing a library database. Users can add, view, and save books in a file. It is designed to be simple, using only built-in Python features with no extra dependencies.

## Features
- View all books in the database
- Add new books with title, author, ISBN, and year
- Store book data in a file
- Program validates data and prevents duplicate book entries based on title and ISBN
- Lightweight, menu-driven interface

## Requirements
- Python 3.x
- A text-based database file (plain text, formatted properly. See **File Format** for details.)

## Installation
- Clone or download this repository.
- Ensure you have Python installed (`python3 --version` to check).

## Usage
### Running the Program
Run the script with a database file as an argument:
```
python3 my_library_db.py library.txt
```

If the file doesn’t exist or is empty, an error will be displayed.
If the file contains corrupted entries, they will be extracted to a separate file `corrupted_data.txt`. User is able to use a cleaned up file.
For testing, you can use `library.txt`, `empty.txt`, `errors.txt`.

### Menu Options
1. Add a New Book: Allows to enter book details and stores them in the database.
2. Print Database: Displays all stored books with their details.
3. Quit Program: Exits the program.

### Adding a Book
- The program checks for duplicate titles and ISBN before adding a book.
- ISBN and year inputs are validated.
- Users can cancel the operation at any prompt by typing EXIT.

## File Format
The program reads and writes book data from a structured text file. The expected format is:
```
Idiot/Fyodor Dostoyevsky/9780850670356/1971
Moby Dick/Herman Melville/9781974305032/1981
```
Each book entry is on a new line, with fields separated by /.

## Example Run
```
python my_library_db.py library.txt
```

### Output:
```
==================================================
WELCOME TO THE LIBRARY DATABASE
==================================================

MAIN MENU
==================================================
[1]  ADD A NEW BOOK
[2]  PRINT DATABASE
[Q]  QUIT PROGRAM
==================================================
SELECT AN OPTION:
```
