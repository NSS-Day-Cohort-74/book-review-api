import datetime
import sqlite3
import json


class Reviews():

    def update(self, pk):
        # Open a connection to the database
        with sqlite3.connect("./bookreviews.sqlite3") as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            # Write the SQL query to get the information you want
            db_cursor.execute("""

                """,
                (

                )
            )

            rows_modified = db_cursor.rowcount

            if rows_modified != 0:
                return True

            return False

    def get_all(self):
        # Open a connection to the database
        with sqlite3.connect("./janesreviews.sqlite3") as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            # Write the SQL query to get the information you want
            db_cursor.execute("""
            SELECT
                rating,
                review_text,
                book_id,
                b.title
            FROM Review
            JOIN Book b ON book_id = b.id
            """)
            query_results = db_cursor.fetchall()

            # Initialize an empty list and then add each dictionary to it
            reviews=[]
            for row in query_results:
                reviews.append(dict(row))


        return json.dumps(reviews)

