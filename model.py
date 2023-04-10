import pymysql.cursors


class BookManagement:
    def __init__(self, db_host, db_user, db_password, db_name):
        self.db_host = db_host
        self.db_user = db_user
        self.db_password = db_password
        self.db_name = db_name
        self.create_table_and_insert_data()

    def _connect(self):
        '''
        Connects to the MySQL database using the provided credentials.

        Args:
            - None

        Returns:
            - pymysql.Connection: a connection object to the MySQL database
        '''
        return pymysql.connect(
            host=self.db_host,
            user=self.db_user,
            password=self.db_password,
            db=self.db_name,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )

    def create_table_and_insert_data(self):
        """
        Create a new database schema and insert initial data into the book table.

        Args:
            - None

        Returns:
            - None
        """
        conn = pymysql.connect(
            host=self.db_host,
            user=self.db_user,
            password=self.db_password,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        try:
            with conn.cursor() as cursor:
                cursor.execute(f'CREATE SCHEMA {self.db_name}')
            conn.commit()
        except:
            pass
        finally:
            conn.close()

        connection = self._connect()

        try:
            # Insert the new book record into the database
            with connection.cursor() as cursor:
                create_table_sql = '''CREATE TABLE book (
                    id INT NOT NULL AUTO_INCREMENT,
                    isbn VARCHAR(50),
                    title VARCHAR(255),
                    author VARCHAR(255),
                    publish_year INT,
                    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY (id)
                )'''
                cursor.execute(create_table_sql)

                insert_data_sql = '''INSERT INTO book (isbn, title, author, publish_year)
                VALUES 
                ('978-0201485677', 'Refactoring: Improving the Design of Existing Code', 'Martin Fowler', 1999),
                ('978-0596003302', 'Head First Design Patterns', 'Eric Freeman, Elisabeth Freeman, Kathy Sierra, Bert Bates', 2004),
                ('978-0596529321', 'JavaScript: The Good Parts', 'Douglas Crockford', 2008),
                ('978-0321356680', 'Effective Java', 'Joshua Bloch', 2008),
                ('978-0321573519', 'Programming Pearls', 'Jon Bentley', 1999),
                ('978-0596805524', 'Python Cookbook', 'Brian K. Jones, David Beazley', 2013),
                ('978-0201835953', 'The Pragmatic Programmer', 'Andrew Hunt, David Thomas', 1999),
                ('978-0132350884', 'Clean Code', 'Robert C. Martin', 2008),
                ('978-0321125217', 'Artificial Intelligence: A Modern Approach', 'Stuart Russell, Peter Norvig', 2002),
                ('978-0133591620', 'Database Systems: The Complete Book', 'Hector Garcia-Molina, Jeffrey D. Ullman, Jennifer Widom', 2008)'''
                cursor.execute(insert_data_sql)
                connection.commit()
        except:
            pass
        finally:
            connection.close()

    def add_book(self, title, author, publish_year, isbn):
        '''
        Add a book to the book management database.
        Args:
            title (str): The title of the book.
            author (str): The author of the book.
            publish_year (int): The year the book was published.
            isbn (str): The ISBN (International Standard Book Number) of the book.
        Returns:
            result (bool): True if the book was successfully added to the database, False otherwise.
        '''
        # Connect to the database
        connection = self._connect()
        result = False
        try:
            # Insert the new book record into the database
            with connection.cursor() as cursor:
                sql = "INSERT INTO `book` (`isbn`, `title`, `author`, `publish_year`) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql, (isbn, title, author, publish_year))
            connection.commit()
            result = True
        except:
            result = False
        finally:
            connection.close()
        return result

    def delete_book(self, isbn):
        '''
        Delete a book record from the database using its ISBN number

        Args:
            - isbn: the ISBN number of the book to be deleted

        Returns:
            - result: a boolean value indicating whether the deletion was successful or not
        '''
        # Connect to the database
        connection = self._connect()
        result = False

        try:
            # Delete the book record from the database
            with connection.cursor() as cursor:
                sql = "DELETE FROM `book` WHERE `isbn`=%s"
                cursor.execute(sql, (isbn,))
            connection.commit()
            result = True
        except:
            result = False
        finally:
            connection.close()
        return result

    def get_all_books(self):
        '''
        Retrieve all book records from the database
        Returns:
            - A list of book records, each represented as a dictionary with the following keys:
            - id: integer representing the book's ID in the database
            - isbn: string representing the book's ISBN number
            - title: string representing the book's title
            - author: string representing the book's author
            - publish_year: integer representing the year the book was published
            - create_time: timestamp representing the time the book record was created in the database
        '''
        # Connect to the database
        connection = self._connect()

        try:
            # Retrieve all book records from the database
            with connection.cursor() as cursor:
                sql = "SELECT * FROM `book`"
                cursor.execute(sql)
                results = cursor.fetchall()
            return results
        finally:
            connection.close()

    def search_books(self, keyword):
        '''
        Search for book records in the database based on the given keyword
        Args:
            - keyword: A string to search for in the book records. It will search for matches in the 'title'
            and 'author' fields.
        Returns:
            - A list of book records that match the keyword. Each book record is a dictionary with the following keys:
            'id', 'isbn', 'title', 'author', 'publish_year', 'create_time'.
        '''
        # Connect to the database
        connection = self._connect()

        try:
            # Search for book records in the database based on the given keyword
            with connection.cursor() as cursor:
                sql = "SELECT * FROM `book` WHERE `title` LIKE %s OR `author` LIKE %s"
                cursor.execute(sql, ('%' + keyword + '%', '%' + keyword + '%'))
                results = cursor.fetchall()
            return results
        finally:
            connection.close()
