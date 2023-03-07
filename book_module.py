import sqlite3


class Book:
    """encapsulates the idea of the book as a list like object containing (id, title, author and quantity)
    has some additional methods to conveniently turn book back into tuple and to print the book in a user-friendly
    manner."""

    def __init__(self, book_id, title, author, quantity):
        self.id = book_id
        self.title = title
        self.author = author
        self.quantity = quantity

    def list_constructor(self, book_list):
        """alternative constructor for initialising book with a list instead of multiple arguments
        can initialise a book object alternatively by book_variable = Book.list_constructor(book_list)"""
        self.id = book_list[0]
        self.title = book_list[1]
        self.author = book_list[2]
        self.quantity = book_list[3]

    def convert_to_tuple(self):
        """returns tuple of book object data"""
        return self.id, self.title, self.author, self.quantity

    def __str__(self):
        return f"Book id: {self.id}\tTitle: {self.title}\tAuthor: {self.author}\tquantity: {self.quantity}"


class BookShop:
    """BookShop class.
    Creates a sqlite3 object with filename corresponding to datafile input. (instance level variable)
    then creates a table with name corresponding to table_name input (instance level variable)
    also creates a cursor object to manage the database (instance level variable)
    the class then has methods to manage the database. Since objects in the database are books the Book class is
    also used to help make management easier to read."""

    def __init__(self, datafile, table_name):
        """takes in the name of the file that stores the database and also a name for the table"""
        self.book_shop_datafile = datafile
        try:
            self.bookshop_database = sqlite3.connect(datafile)
        except Exception as e:
            print(e)
        else:
            self.bookshop_cursor = self.bookshop_database.cursor()
            self.table_name = table_name
            self.bookshop_cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS {self.table_name} (id INTEGER PRIMARY KEY, title TEXT, author TEXT,
                 quantity INTEGER)''')
            self.bookshop_database.commit()

    def __str__(self):
        """returns a string of all entries stored in the database"""
        self.bookshop_cursor.execute(f"""SELECT * FROM {self.table_name}""")
        return "\n".join([f"Book id: {row[0]}\tTitle: {row[1]}\tAuthor: {row[2]}\tquantity: {row[3]}" for row in
                          self.bookshop_cursor])

    def __repr__(self):
        return str(self)

    def check_id_exists(self, id_to_check):
        """bool return type. Checks if the id already is present in the table associated with the BookShelf object"""
        self.bookshop_cursor.execute(f"SELECT EXISTS(SELECT 1 FROM {self.table_name} WHERE id={id_to_check})")
        for row in self.bookshop_cursor:
            return bool(row[0])

    def new_id_generator(self):
        """returns (int) a new id which is one more than the current max id value"""
        self.bookshop_cursor.execute(f"SELECT id FROM {self.table_name}")
        return max([row[0] for row in self.bookshop_cursor]) + 1

    def search_book_by_id(self, target_id):
        """searches database for particular id and returns a book object with entries at that id"""
        if not self.check_id_exists(target_id):
            print("ERROR can't find id")
        else:
            self.bookshop_cursor.execute(f"SELECT title, author, quantity FROM {self.table_name} WHERE id=?",
                                         (target_id,))
            book = self.bookshop_cursor.fetchone()
            if book:
                return Book(target_id, book[0], book[1], book[2])
            else:
                print("No results found.")
                return False

    def search_book(self, query_type, query):
        """searches database for a given query type. Query type can be id, title or author. If id or title is chosen
        the return should be a unique book as the add_book/add_books methods screen for duplicate input of id or title
        If the query type is author, multiple books may be returned as the author may have multiple books in the
        database."""
        if query_type == 'id':
            self.bookshop_cursor.execute(f"SELECT id, title, author, quantity FROM {self.table_name} WHERE id=?",
                                         (int(query),))
        elif query_type == 'author':
            self.bookshop_cursor.execute(f"SELECT id, title, author, quantity FROM {self.table_name} WHERE author=?",
                                         (query,))
        elif query_type == 'title':
            self.bookshop_cursor.execute(f"SELECT id, title, author, quantity FROM {self.table_name} WHERE title=?",
                                         (query,))
        books = self.bookshop_cursor.fetchall()
        if books:
            return [Book(book[0], book[1], book[2], book[3]) for book in books]

    def title_exists(self, title_to_check):
        """bool return type. Checks if a given title already exists in the table associated with the BookShelf object"""
        if self.search_book('title', title_to_check):
            return True
        else:
            return False

    def add_book(self, book_to_add):
        """add a single book to the database. Also ensures that new book does not have an id already existing in
        database nor a title that already exists in the database"""
        if self.check_id_exists(book_to_add.id):
            print("Error book id already exists")
        elif self.title_exists(book_to_add.title):
            print("ERROR book title already exists")
        else:
            self.bookshop_cursor.execute(
                f'''INSERT INTO {self.table_name}(id, title, author, quantity) VALUES(?,?,?,?)''',
                book_to_add.convert_to_tuple())
            self.bookshop_database.commit()

    def add_books(self, books_to_add):
        """add multiple books to the database in one go. Ensures that new books don't have existing id nor title"""
        print("Hello")
        for book in books_to_add:
            if self.check_id_exists(book.id):
                print("ERROR book id already exists")
            elif self.title_exists(book.id):
                print("ERROR book title already exists")
            else:
                self.bookshop_cursor.execute(f'''INSERT INTO {self.table_name}(id, title, author, quantity) 
                VALUES(?,?,?,?)''', book.convert_to_tuple())
                self.bookshop_database.commit()

    def default_populate(self):
        """some initial books to populate the table with. Checks that the books have not already been added to the
        database"""
        books_to_add = [Book(3001, 'A Tale of Two Cities'.lower(), 'Charles Dickens'.lower(), 30),
                        Book(3002, 'Harry Potter and the Philosopher\'s Stone'.lower(), 'J.K. Rowling'.lower(), 40),
                        Book(3003, 'Harry Potter and the Chamber of Secrets'.lower(), 'J.K. Rowling'.lower(), 40),
                        Book(3004, 'The Lion, the Witch and the Wardrobe'.lower(), "C.S. Lewis".lower(), 25),
                        Book(3005, 'The Lord of the Rings'.lower(), 'J.R.R. Tolkien'.lower(), 37),
                        Book(3006, 'Alice in Wonderland'.lower(), 'Lewis Caroll'.lower(), 12)]
        # checks that none of the above books ids' and titles' exist
        # add_books does this as well but would be preferable not to always trigger the error messages
        for book in books_to_add:
            if (not self.check_id_exists(book.id)) and (not self.title_exists(book.title)):
                self.add_books(books_to_add)

    def edit_book(self, target_id, new_book):
        """edits a book with a given id and enters values contained within new book. Also ensures that the new book id
        matches the target id"""
        if new_book.id != target_id:
            print("ERROR: id mismatch\n")
        else:
            self.bookshop_cursor.execute(f"UPDATE {self.table_name} SET title=? WHERE id = ?",
                                         (new_book.title, target_id))
            self.bookshop_cursor.execute(f"UPDATE {self.table_name} SET author=? WHERE id = ?",
                                         (new_book.author, target_id))
            self.bookshop_cursor.execute(f"UPDATE {self.table_name} SET quantity=? WHERE id = ?",
                                         (new_book.quantity, target_id))
            self.bookshop_database.commit()

    def delete_book(self, target_id):
        """deletes book in database with given id"""
        if not self.check_id_exists(target_id):
            print("ERROR id entered does not exist.")
        else:
            self.bookshop_cursor.execute(f'''DELETE FROM {self.table_name} WHERE id = ? ''', (target_id,))
            self.bookshop_database.commit()

    def clear_table_data(self):
        """"deletes the data in the table associated with the current instance of the BookShelf object but does not
        delete the table"""
        self.bookshop_cursor.execute(f'''DELETE FROM {self.table_name}''')
        print(f"Table - {self.table_name} cleared.")

    def drop_table(self):
        """drops the table associated with the current instance of BookShelf object"""
        self.bookshop_cursor.execute(f'''DROP TABLE {self.table_name}''')
