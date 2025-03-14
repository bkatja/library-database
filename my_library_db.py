import os
import sys
import time
from helpers import confirm_action, get_valid_input, get_valid_year, get_valid_isbn, read_books, write_books

def print_header():
    print("=" * 50)
    print("WELCOME TO THE LIBRARY DATABASE")
    print("=" * 50)

def display_books(books):
    print("\n" + "=" * 50)
    print("LIBRARY DATABASE - BOOK LIST")
    print("=" * 50)
    
    if not books:
        print("  [NO BOOKS FOUND IN DATABASE]")
    else:
        for idx, book in enumerate(books, start=1):
            print(f"{idx}.  Title  : {book['Title'].replace('|', '/')}")
            print(f"    Author : {book['Author'].replace('|', '/')}")
            print(f"    ISBN   : {book['ISBN']}")
            print(f"    Year   : {book['Year']}")
            print("-" * 50)

    print("BOOK LIST COMPLETE")

def add_book(file_path, books):
    print("\n" + "=" * 50)
    print("ADDING A NEW BOOK TO THE DATABASE")
    print("=" * 50)
    print("Type 'EXIT' at any prompt to cancel adding a book.\n")

    title = get_valid_input("Enter book title: ", "Title cannot be empty.")
    if title is None:
        return

    existing_books = [book for book in books if book['Title'].lower() == title.lower()]
    if existing_books:
        print("\n[WARNING] A book with this title already exists:")
        for book in existing_books:
            print(f"{book['Title'].replace('|', '/')} | {book['Author'].replace('|', '/')} | {book['ISBN']} | {book['Year']}")
        if confirm_action("\nProceed with adding this book? (Y/N): ") == "N":
            print("\n[INFO] Book addition canceled.\n")
            return

    author = get_valid_input("Enter author name: ", "Author name cannot be empty.")
    if author is None:
        return

    isbn = get_valid_isbn(books)
    if isbn is None:
        return

    year = get_valid_year()
    if year is None:
        return

    print("\nYou entered the following book:")
    print("=" * 50)
    print(f"Title  : {title.replace('|', '/')}")
    print(f"Author : {author.replace('|', '/')}")
    print(f"ISBN   : {isbn}")
    print(f"Year   : {year}")
    print("=" * 50)

    if confirm_action("\nDo you want to update the database with this book? (Y/N): ") == "N":
        print("\n[INFO] Book addition canceled.\n")
        return

    books.append({'Title': title, 'Author': author, 'ISBN': isbn, 'Year': year})
    write_books(file_path, books)
    print("\nBook added successfully!")
    time.sleep(1)

def show_menu(file_path, books):
    while True:
        print("\n" + "=" * 50)
        print("MAIN MENU")
        print("=" * 50)
        print("[1]  ADD A NEW BOOK")
        print("[2]  PRINT DATABASE")
        print("[Q]  QUIT PROGRAM")
        print("=" * 50)

        choice = input("SELECT AN OPTION: ").strip().upper()
        if choice == "1":
            add_book(file_path, books)
        elif choice == "2":
            display_books(books)
        elif choice == "Q":
            print("\nShutting down library database... Goodbye!")
            time.sleep(1)
            break
        else:
            print("\n[ERROR] Invalid choice! Please select a valid option.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("\n[ERROR] Usage: python my_library_db.py <file_path>\n")
        sys.exit(1)
    
    file_path = sys.argv[1]
    if not os.path.exists(file_path):
        print(f"\n[ERROR] File '{file_path}' not found.\n")
        sys.exit(1)
    
    books = read_books(file_path)
    
    print_header()
    show_menu(file_path, books)
