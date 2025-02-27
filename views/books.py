import datetime
import sqlite3
import json


class Books():

    def get_all(self):
        """Get all books from the database with their categories and reviews"""
        # Open a connection to the database
        with sqlite3.connect("./janesreviews.sqlite3") as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            # Write the SQL query to get the information you want
            db_cursor.execute("""
            SELECT
                b.id,
                b.title,
                b.author,
                b.isbn,
                b.publication_date,
                b.user_id,
                u.username
            FROM Book b
            JOIN User u ON b.user_id = u.id
            """)
            query_results = db_cursor.fetchall()

            # Initialize an empty list and then add each dictionary to it
            books = []
            for row in query_results:
                book = dict(row)

                # Get categories for this book
                db_cursor.execute("""
                SELECT
                    c.id,
                    c.category_name
                FROM Category c
                JOIN BookCategory bc ON c.id = bc.category_id
                WHERE bc.book_id = ?
                """, (book["id"],))

                categories = []
                category_results = db_cursor.fetchall()
                for category_row in category_results:
                    categories.append(dict(category_row))

                # Add categories to book
                book["categories"] = categories

                # Get reviews for this book
                db_cursor.execute("""
                SELECT
                    r.id,
                    r.rating,
                    r.review_text,
                    r.user_id,
                    u.username
                FROM Review r
                JOIN User u ON r.user_id = u.id
                WHERE r.book_id = ?
                """, (book["id"],))

                reviews = []
                review_results = db_cursor.fetchall()
                for review_row in review_results:
                    reviews.append(dict(review_row))

                # Add reviews to book
                book["reviews"] = reviews

                books.append(book)

            return json.dumps(books)

    def get_single(self, pk):
        """Get a single book by id with its categories and reviews"""
        # Open a connection to the database
        with sqlite3.connect("./janesreviews.sqlite3") as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            # Write the SQL query to get the information you want
            db_cursor.execute("""
            SELECT
                b.id,
                b.title,
                b.author,
                b.isbn,
                b.publication_date,
                b.user_id,
                u.username
            FROM Book b
            JOIN User u ON b.user_id = u.id
            WHERE b.id = ?
            """, (pk,))

            # Load the single result into memory
            data = db_cursor.fetchone()

            # Check if data was found
            if data is not None:
                # Create a dictionary from the database record
                book = dict(data)

                # Get categories for this book
                db_cursor.execute("""
                SELECT
                    c.id,
                    c.category_name
                FROM Category c
                JOIN BookCategory bc ON c.id = bc.category_id
                WHERE bc.book_id = ?
                """, (book["id"],))

                categories = []
                category_results = db_cursor.fetchall()
                for category_row in category_results:
                    categories.append(dict(category_row))

                # Add categories to book
                book["categories"] = categories

                # Get reviews for this book
                db_cursor.execute("""
                SELECT
                    r.id,
                    r.rating,
                    r.review_text,
                    r.user_id,
                    u.username
                FROM Review r
                JOIN User u ON r.user_id = u.id
                WHERE r.book_id = ?
                """, (book["id"],))

                reviews = []
                review_results = db_cursor.fetchall()
                for review_row in review_results:
                    reviews.append(dict(review_row))

                # Add reviews to book
                book["reviews"] = reviews

                return json.dumps(book)
            else:
                return None

    def create(self, book_data):
        """Create a new book in the database"""
        # Open a connection to the database
        with sqlite3.connect("./janesreviews.sqlite3") as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            # Write the SQL query to insert the new book
            db_cursor.execute("""
            INSERT INTO Book (title, author, isbn, publication_date, user_id)
            VALUES (?, ?, ?, ?, ?)
            """, (
                book_data["title"],
                book_data["author"],
                book_data["isbn"],
                book_data["publication_date"],
                book_data["user_id"]
            ))

            # Get the id of the new book
            id = db_cursor.lastrowid

            # Add the id to the book data
            book_data["id"] = id

            # If categories are provided, add them to the BookCategory table
            if "categories" in book_data and book_data["categories"]:
                for category_id in book_data["categories"]:
                    db_cursor.execute("""
                    INSERT INTO BookCategory (book_id, category_id)
                    VALUES (?, ?)
                    """, (id, category_id))

            return json.dumps(book_data)

    def update(self, pk, book_data):
        """Update a book in the database"""
        # Open a connection to the database
        with sqlite3.connect("./janesreviews.sqlite3") as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            # Write the SQL query to update the book
            db_cursor.execute("""
            UPDATE Book
            SET title = ?,
                author = ?,
                isbn = ?,
                publication_date = ?,
                user_id = ?
            WHERE id = ?
            """, (
                book_data["title"],
                book_data["author"],
                book_data["isbn"],
                book_data["publication_date"],
                book_data["user_id"],
                pk
            ))

            # Check if a row was updated
            rows_affected = db_cursor.rowcount

            # If categories are provided, update the BookCategory table
            if "categories" in book_data and book_data["categories"]:
                # First, delete existing category associations
                db_cursor.execute("""
                DELETE FROM BookCategory
                WHERE book_id = ?
                """, (pk,))

                # Then, add the new category associations
                for category_id in book_data["categories"]:
                    db_cursor.execute("""
                    INSERT INTO BookCategory (book_id, category_id)
                    VALUES (?, ?)
                    """, (pk, category_id))

            if rows_affected > 0:
                return True
            else:
                return False

    def delete(self, pk):
        """Delete a book from the database"""
        # Open a connection to the database
        with sqlite3.connect("./janesreviews.sqlite3") as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            # First, delete any category associations
            db_cursor.execute("""
            DELETE FROM BookCategory
            WHERE book_id = ?
            """, (pk,))

            # Then, delete any reviews associated with this book
            db_cursor.execute("""
            DELETE FROM Review
            WHERE book_id = ?
            """, (pk,))

            # Finally, delete the book
            db_cursor.execute("""
            DELETE FROM Book
            WHERE id = ?
            """, (pk,))

            # Check if a row was deleted
            rows_affected = db_cursor.rowcount

            if rows_affected > 0:
                return True
            else:
                return False