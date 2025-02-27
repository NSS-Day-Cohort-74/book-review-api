import datetime
import sqlite3
import json


class Reviews():

    def get_all(self):
        """Get all reviews from the database"""
        # Open a connection to the database
        with sqlite3.connect("./janesreviews.sqlite3") as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            # Write the SQL query to get the information you want
            db_cursor.execute("""
            SELECT
                r.id,
                r.rating,
                r.review_text,
                r.book_id,
                r.user_id,
                b.title
            FROM Review r
            JOIN Book b ON r.book_id = b.id
            """)
            query_results = db_cursor.fetchall()

            # Initialize an empty list and then add each dictionary to it
            reviews=[]
            for row in query_results:
                reviews.append(dict(row))

        return json.dumps(reviews)

    def get_single(self, pk):
        """Get a single review by id"""
        # Open a connection to the database
        with sqlite3.connect("./janesreviews.sqlite3") as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            # Write the SQL query to get the information you want
            db_cursor.execute("""
            SELECT
                r.id,
                r.rating,
                r.review_text,
                r.book_id,
                r.user_id,
                b.title
            FROM Review r
            JOIN Book b ON r.book_id = b.id
            WHERE r.id = ?
            """, (pk,))

            # Load the single result into memory
            data = db_cursor.fetchone()

            # Check if data was found
            if data is not None:
                # Create a dictionary from the database record
                review = dict(data)
                return json.dumps(review)
            else:
                return None

    def create(self, review_data):
        """Create a new review in the database"""
        # Open a connection to the database
        with sqlite3.connect("./janesreviews.sqlite3") as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            # Write the SQL query to insert the new review
            db_cursor.execute("""
            INSERT INTO Review (book_id, user_id, rating, review_text)
            VALUES (?, ?, ?, ?)
            """, (
                review_data["book_id"],
                review_data["user_id"],
                review_data["rating"],
                review_data["review_text"]
            ))

            # Get the id of the new review
            id = db_cursor.lastrowid

            # Add the id to the review data
            review_data["id"] = id

            return json.dumps(review_data)

    def delete(self, pk):
        """Delete a review from the database"""
        # Open a connection to the database
        with sqlite3.connect("./janesreviews.sqlite3") as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            # Write the SQL query to delete the review
            db_cursor.execute("""
            DELETE FROM Review
            WHERE id = ?
            """, (pk,))

            # Check if a row was deleted
            rows_affected = db_cursor.rowcount

            if rows_affected > 0:
                return True
            else:
                return False
