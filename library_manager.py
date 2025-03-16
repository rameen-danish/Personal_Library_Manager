import json

class PersonalLibraryManager:
    def __init__(self, filename="library.json"):   #self represents the instance of the class and allows access to its attributes and methods.
        """
        Initialize the library manager.
        Loads the library data from a JSON file if it exists.
        Creates a backup file for safety.
        """
        self.filename = filename                       # Stores the filename in the instance
        self.backup_filename = "library_backup.json"  # Stores the backup filename in the instance
        self.library = self.load_library()              # Loads book data when an instance is created
    
    def load_library(self):
        """
        Load the library from a JSON file.
        Returns an empty list if the file does not exist or has invalid JSON.
        """
        try:                                              # (with open(...)) Used to read/write data from a JSON file (library.json).
            with open(self.filename, "r") as file:         #"r" (read mode): Loads the library data from the file.
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def save_library(self):
        """
        Save the library data to a JSON file and create a backup.
        """
        with open(self.filename, "w") as file:              #"w" (write mode): Saves the updated book list back to the file
            json.dump(self.library, file, indent=4)         #converts a Python list into JSON and writes it to the file.
        with open(self.backup_filename, "w") as backup_file:
            json.dump(self.library, backup_file, indent=4)        # A copy is saved in "library_backup.json" to prevent data loss.
    
    def add_book(self):
        """
        Prompt the user to enter book details and add it to the library.
        Handles invalid year input gracefully.
        """
        title = input("Enter the book title: ")
        author = input("Enter the author: ")
        while True:                                             #Uses a while True loop to keep asking until a valid input is provided.
            try:
                year = int(input("Enter the publication year: "))
                if 1000 <= year <= 9999:
                    break
                else:
                    print("Invalid year! Please enter a 4-digit year.")
            except ValueError:
                print("Invalid input! Please enter a valid 4-digit year.")
        genre = input("Enter the genre: ")
        read_status = input("Have you read this book? (yes/no): ").strip().lower() == "yes"
        
        self.library.append({"title": title, "author": author, "year": year, "genre": genre, "read": read_status})
        self.save_library()
        print("Book added successfully!\n")
    
    def remove_book(self):
        """
        Remove a book from the library based on the title with confirmation.
        """
        title = input("Enter the title of the book to remove: ")
        matching_books = [book for book in self.library if book["title"].lower() == title.lower()]
        
        if not matching_books:
            print("Book not found!\n")
            return
        
        confirm = input(f"Are you sure you want to remove '{title}'? (yes/no): ").strip().lower()
        if confirm == "yes":
            self.library = [book for book in self.library if book["title"].lower() != title.lower()]
            self.save_library()
            print("Book removed successfully!\n")
        else:
            print("Book removal cancelled.\n")
    
    def search_book(self):
        """
        Search for a book by title or author and display matching results.
        Allows case-insensitive searches.
        """
        choice = input("Search by:\n1. Title\n2. Author\nEnter your choice: ")
        query = input("Enter your search query: ").lower()
        results = [book for book in self.library if query in book["title"].lower() or query in book["author"].lower()]
        
        if results:
            for book in results:
                self.display_book(book)
        else:
            print("No matching books found.\n")
    
    def display_books(self):
        """
        Display all books in the library in a formatted list.
        """
        if not self.library:
            print("Your library is empty.\n")
        else:
            for idx, book in enumerate(self.library, start=1):
                print(f"{idx}.", end=" ")
                self.display_book(book)
    
    def display_statistics(self):
        """
        Display statistics including total number of books and percentage read.
        """
        total_books = len(self.library)
        read_books = sum(book["read"] for book in self.library)
        percentage_read = (read_books / total_books * 100) if total_books else 0
        print(f"Total books: {total_books}\nPercentage read: {percentage_read:.1f}%\n")
    
    def display_book(self, book):
        """
        Display the details of a single book in a readable format.
        """
        status = "Read" if book["read"] else "Unread"
        print(f"{book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {status}")
    
    def mark_as_read_unread(self):
        """
        Allows users to mark a book as read or unread.
        """
        title = input("Enter the title of the book to update: ")
        for book in self.library:
            if book["title"].lower() == title.lower():
                book["read"] = not book["read"]                 #Flips the read status (True → False or False → True).
                self.save_library()
                print(f"Updated '{book['title']}' to {'Read' if book['read'] else 'Unread'}.\n")
                return
        print("Book not found!\n")
    
    def menu(self):
        """
        Display a menu system for the user to interact with the library manager.
        """
        while True:
            print("\nMenu\n1. Add a book\n2. Remove a book\n3. Search for a book\n4. Display all books\n5. Display statistics\n6. Mark book as Read/Unread\n7. Exit")
            choice = input("Enter your choice: ")
            
            if choice == "1":
                self.add_book()
            elif choice == "2":
                self.remove_book()
            elif choice == "3":
                self.search_book()
            elif choice == "4":
                self.display_books()
            elif choice == "5":
                self.display_statistics()
            elif choice == "6":
                self.mark_as_read_unread()
            elif choice == "7":
                self.save_library()
                print("Library saved to file. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.\n")

if __name__ == "__main__":
    manager = PersonalLibraryManager()
    manager.menu()
"""
__name__ is a special variable in Python that holds the name of the script.
When a script is executed directly (not imported as a module), __name__ is set to "__main__".
This condition ensures that the program only runs when executed directly, not when imported into another script.
"""