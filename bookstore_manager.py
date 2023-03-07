from book_module import BookShop, Book


def integer_capture(request):
    """takes in a string which is the intended request message function continues to prompt user for input until the
    input can be interpreted as integer returns an integer"""
    while True:
        user_input = input(request)
        try:
            user_input = int(user_input)
        except ValueError:
            print("ERROR: enter an integer value")
        else:
            return user_input


def bool_capture(request):
    """takes in a string which is the intended request message function continues to prompt user for input until the
    input can be interpreted as 'y' or 'n'  then returns corresponding bool"""
    while True:
        user_input = input(request)
        if user_input == 'y' or user_input == 'n':
            if user_input == 'y':
                return True
            else:
                return False
        else:
            print("ERROR: please enter either y or n as a choice.")


def main():
    """main function manages a bookshop.
    A bookshop object is first created. This maintains a sql database of books with entries of
    (id, title, author, quantity)
    A few books are already populated into the database You may delete these either individually with
    delete book option or clear table option.
    USER CHOICE LOOP: user is presented with choice to manage the database
        1 - enter book
        2 - update book
        3 - delete book
        4 - search for id, title or author
        5 - view bookstore
        6 - clear bookstore table
        0 - exit
        the choices are managed by the methods with the bookshop object.
    User is repeatedly asked for input until they select 0 to exit
    """

    # initiate a BookShop object creating/using file alexandria_db with a SQL table named Alexandria
    phoenix_of_alexandria = BookShop("alexandria_db", "Alexandria")

    # the instructions asked that the database is to be populated with a certain number of books initially
    phoenix_of_alexandria.default_populate()

    # user choice loop
    while True:
        user_choice = input("""Please select from the following options:
        1 - enter book
        2 - update book
        3 - delete book
        4 - search for id, title or author
        5 - view bookstore
        6 - clear bookstore table
        0 - exit\n""")

        # add book to database
        if user_choice == "1":
            new_book_id = phoenix_of_alexandria.new_id_generator()
            new_book_title = input("Please enter the title of the book you would like to add \n").lower()
            new_book_author = input("Please enter the author of the book you would like to add \n").lower()
            new_book_quantity = integer_capture("Please enter the quantity of the book you would like to add \n")
            new_book = Book(new_book_id, new_book_title, new_book_author, new_book_quantity)
            phoenix_of_alexandria.add_book(new_book)

        # edit book in database
        elif user_choice == "2":
            id_to_edit = integer_capture("Please enter the id of the book you would like to edit\n")
            if not phoenix_of_alexandria.check_id_exists(id_to_edit):
                print("ERROR: id entered does not exist")
            else:
                # store old book data then store old book attribute only change this if user says yes to prompt
                old_book = phoenix_of_alexandria.search_book_by_id(id_to_edit)
                new_book_title = old_book.title
                change_title = bool_capture("Would you like to change the title. y/n\n")
                if change_title:
                    new_book_title = input("Please enter the title of the book\n").lower()
                new_book_author = old_book.author
                change_author = bool_capture("Would you like to change the author. y/n\n")
                if change_author:
                    new_book_author = input("Please enter the author of the book\n").lower()
                new_book_quantity = old_book.quantity
                change_quantity = bool_capture("Would you like to change the quantity. y/n\n")
                if change_quantity:
                    new_book_quantity = integer_capture("Please enter the quantity of the book\n")
                edited_book = Book(id_to_edit, new_book_title, new_book_author, new_book_quantity)
                phoenix_of_alexandria.edit_book(id_to_edit, edited_book)

        # delete book in database
        elif user_choice == "3":
            id_to_delete = integer_capture("Please enter the id of the book you would like to delete\n")
            phoenix_of_alexandria.delete_book(id_to_delete)

        # search database. Can either search for id, title or author. ID and title should return unique results, author
        # may return multiple books
        elif user_choice == "4":
            while True:
                query_type = input("Please enter the type of query you would like to make; "
                                   "id, title or author are valid options.\n").lower()
                if query_type == 'id' or query_type == 'title' or query_type == 'author':
                    break
                else:
                    print("ERROR: please select a query type of either: id, author or title")
            query = input("Please enter the query you would like to make.\n").lower()
            results = phoenix_of_alexandria.search_book(query_type, query)
            if results:
                [print(book) for book in results]
            else:
                print("No results found")

        # print books stores in database
        elif user_choice == "5":
            print(phoenix_of_alexandria)

        # clear all existing entries in the table
        elif user_choice == "6":
            phoenix_of_alexandria.clear_table_data()

        # exit the program
        elif user_choice == "0":
            exit()

        else:
            print("Error incorrect input. Please enter a numerical value to make a selection.\n")


if __name__ == '__main__':
    main()
