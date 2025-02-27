import sqlite3
import json


class Categories():

    def get_all(self):
        """Get all categories from the database"""
        # Open a connection to the database
        with sqlite3.connect("./janesreviews.sqlite3") as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            # Write the SQL query to get the information you want
            db_cursor.execute("""
            SELECT
                c.id,
                c.category_name
            FROM Category c
            """)
            query_results = db_cursor.fetchall()

            # Initialize an empty list and then add each dictionary to it
            categories = []
            for row in query_results:
                categories.append(dict(row))

            return json.dumps(categories)

    def create(self, category_data):
        """Create a new category in the database"""
        # Open a connection to the database
        with sqlite3.connect("./janesreviews.sqlite3") as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            # Write the SQL query to insert the new category
            db_cursor.execute("""
            INSERT INTO Category (category_name)
            VALUES (?)
            """, (category_data["category_name"],))

            # Get the id of the new category
            id = db_cursor.lastrowid

            # Add the id to the category data
            category_data["id"] = id

            return json.dumps(category_data)