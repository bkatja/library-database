import sys
import time

def read_books(file_path):
    """Reads book data from the file, verifying correct format. Extracts corrupted lines in a separate file."""
    books = []
    corrupted_lines = []

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line_number, line in enumerate(file, start=1):
                line = line.strip()
                if not line:
                    continue

                parts = line.split('/')
                if len(parts) != 4:
                    print(f"[WARNING] Skipping malformed line {line_number}: {line}")
                    corrupted_lines.append(line)
                    continue

                title, author, isbn, year = parts

                # To avoid issues while reading a file and accept books that have '/' in Title or Author fields 
                # '/' is encoded to '|' for storing. Decode '|' back to '/' 
                title = title.replace("|", "/")
                author = author.replace("|", "/")

                # Validate ISBN and Year
                if not isbn.isdigit() or len(isbn) not in (10, 13):
                    print(f"[WARNING] Skipping line {line_number}: Invalid ISBN format → {line}")
                    corrupted_lines.append(line)
                    continue

                if not year.isdigit() or not (1000 <= int(year) <= time.localtime().tm_year):
                    print(f"[WARNING] Skipping line {line_number}: Invalid year → {line}")
                    corrupted_lines.append(line)
                    continue

                books.append({
                    'Title': title.strip(),
                    'Author': author.strip(),
                    'ISBN': isbn.strip(),
                    'Year': int(year.strip())
                })
    
    except FileNotFoundError:
        print(f"[ERROR] File '{file_path}' not found.")
        sys.exit(1)

    # Extract corrupted lines (if any) to a separate file
    if corrupted_lines:
        corrupted_file = "corrupted_data.txt"
        with open(corrupted_file, 'w', encoding='utf-8') as file:
            for bad_line in corrupted_lines:
                file.write(bad_line + "\n")

        print(f"\n[INFO] Corrupted entries have been saved in '{corrupted_file}'. Please review and fix them.\n")

    return sorted(books, key=lambda x: x['Year'])

def write_books(file_path, books):
    """Writes books to file, keeping them sorted by year, then alphabetically by title."""
    books.sort(key=lambda x: (x['Year'], x['Title'].lower()))

    with open(file_path, 'w', encoding='utf-8') as file:
        for book in books:
            # Encode '/' before saving to avoid issues when reading a file.
            title = book['Title'].replace("/", "|")
            author = book['Author'].replace("/", "|")
            
            file.write(f"{title}/{author}/{book['ISBN']}/{book['Year']}\n")

def confirm_action(prompt):
    """Ensures user provides a valid Y/N response before continuing."""
    while True:
        choice = input(prompt).strip().upper()
        if choice in ("Y", "N"):
            return choice
        print("\n[ERROR] Invalid input! Please enter 'Y' for Yes or 'N' for No.")

def is_valid_isbn(isbn):
    """Check if the given ISBN is valid (10 or 13 digits) using checksum rules."""
    if len(isbn) == 10:
        total = sum((i + 1) * int(digit) for i, digit in enumerate(isbn))
        if total % 11 != 0:
            print(f"[ERROR] Invalid ISBN-10! Checksum failed for {isbn}. ISBN-10 must satisfy the modulus 11 rule.")
            return False
        return True

    elif len(isbn) == 13:
        total = sum((3 if i % 2 else 1) * int(digit) for i, digit in enumerate(isbn))
        if total % 10 != 0:
            print(f"[ERROR] Invalid ISBN-13! Checksum failed for {isbn}. ISBN-13 must satisfy the modulus 10 rule.")
            return False
        return True

    print("[ERROR] ISBN must be exactly 10 or 13 digits.")
    return False

def get_valid_input(prompt, error_message="Invalid input! Try again."):
    """Generic function to get a valid non-empty input."""
    while True:
        value = input(prompt).strip()
        if value.upper() == "EXIT":
            print("\n[INFO] Operation canceled.\n")
            return None
        if value:
            return value.replace("/", "|")
        print(f"[ERROR] {error_message}")

def get_valid_year():
    """Gets a valid publishing year from user."""
    current_year = time.localtime().tm_year
    while True:
        year = input(f"Enter publishing year (between 1000 and {current_year}): ").strip()
        if year.upper() == "EXIT":
            print("\n[INFO] Operation canceled.\n")
            return None
        if year.isdigit() and 1000 <= int(year) <= current_year:
            return int(year)
        print(f"[ERROR] Invalid year! Enter a valid year between 1000 and {current_year}.")

def get_valid_isbn(books):
    """Gets a valid ISBN and checks for duplicates."""
    while True:
        isbn = input("Enter book ISBN (10 or 13 digits, numbers only): ").strip()
        if isbn.upper() == "EXIT":
            print("\n[INFO] Operation canceled.\n")
            return None
        if isbn in ("0000000000", "0000000000000"):
            print("\n[ERROR] Incorrect ISBN. Please enter a valid ISBN.")
            continue
        if isbn.isdigit() and len(isbn) in (10, 13):
            # Check for duplicate ISBN
            if any(book['ISBN'] == isbn for book in books):
                print("\n[WARNING] A book with this ISBN already exists:")
                for book in books:
                    if book['ISBN'] == isbn:
                        print(f"{book['Title']} | {book['Author']} | {book['ISBN']} | {book['Year']}")
                if confirm_action("\nProceed with adding this book anyway? (Y/N): ") == "N":
                    print("\n[INFO] Operation canceled.\n")
                    return None
            return isbn
        print("[ERROR] Invalid ISBN! It must be a valid 10 or 13-digit number.")
