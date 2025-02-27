# Implementation Plan for Jane's Reviews API Extensions

## Overview
This plan outlines the steps needed to implement additional HTTP request handlers for books and categories in the Jane's Reviews application. The implementation will follow the existing pattern used for reviews.

## Current Project Structure
- **Database Schema**: Contains tables for Books, Users, Reviews, Categories, and BookCategory (junction table)
- **Handler Pattern**: Uses a base `HandleRequests` class with resource-specific classes (e.g., `Reviews`)
- **HTTP Methods**: Currently implements GET, POST, DELETE for reviews

## Requirements
1. Implement Book endpoints:
   - GET (all books)
   - GET (single book by ID)
   - POST (create new book)
   - PUT (update existing book)
   - DELETE (remove book)
2. Implement Category endpoints:
   - GET (all categories)
   - POST (create new category)
3. Include categories in book responses
4. Include all reviews as a list in book responses

## Implementation Steps

### 1. Create Book Handler Class

Create a new file `views/books.py` with a `Books` class that implements:

- `get_all()`: Fetch all books with their categories and reviews
- `get_single(pk)`: Fetch a single book by ID with its categories and reviews
- `create(book_data)`: Create a new book
- `update(pk, book_data)`: Update an existing book
- `delete(pk)`: Delete a book

The SQL queries for books will need to:
- Join with the BookCategory and Category tables to include category information
- Join with the Review table to include all reviews

### 2. Create Category Handler Class

Create a new file `views/categories.py` with a `Categories` class that implements:

- `get_all()`: Fetch all categories
- `create(category_data)`: Create a new category

### 3. Update JSON Server

Modify `json-server.py` to:

1. Import the new handler classes:
   ```python
   from views import Reviews, Books, Categories
   ```

2. Update `do_GET` to handle book and category requests:
   - Add logic for "books" resource (all and single)
   - Add logic for "categories" resource (all)

3. Update `do_POST` to handle book and category creation:
   - Add logic for "books" resource
   - Add logic for "categories" resource

4. Update `do_PUT` to handle book updates:
   - Add logic for "books" resource

5. Update `do_DELETE` to handle book deletion:
   - Add logic for "books" resource

### 4. Update __init__.py

Update `views/__init__.py` to expose the new classes:

```python
from .reviews import Reviews
from .books import Books
from .categories import Categories
```

## Detailed SQL Queries

### Books - Get All
```sql
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
```

### Books - Get Single with Categories and Reviews
```sql
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
```

Then for each book:
1. Get categories:
```sql
SELECT
    c.id,
    c.category_name
FROM Category c
JOIN BookCategory bc ON c.id = bc.category_id
WHERE bc.book_id = ?
```

2. Get reviews:
```sql
SELECT
    r.id,
    r.rating,
    r.review_text,
    r.user_id,
    u.username
FROM Review r
JOIN User u ON r.user_id = u.id
WHERE r.book_id = ?
```

### Categories - Get All
```sql
SELECT
    c.id,
    c.category_name
FROM Category c
```

## Data Processing Logic

For book responses, we'll need to:
1. Fetch the basic book information
2. Fetch related categories and add them as a list property
3. Fetch related reviews and add them as a list property

Example book response structure:
```json
{
  "id": 1,
  "title": "Book Title",
  "author": "Author Name",
  "isbn": "1234567890",
  "publication_date": "2023-01-01",
  "user_id": 1,
  "username": "user1",
  "categories": [
    {
      "id": 1,
      "category_name": "Fiction"
    },
    {
      "id": 2,
      "category_name": "Mystery"
    }
  ],
  "reviews": [
    {
      "id": 1,
      "rating": 5,
      "review_text": "Great book!",
      "user_id": 2,
      "username": "user2"
    }
  ]
}
```

## Testing Plan

1. Test each endpoint individually:
   - GET /books
   - GET /books/1
   - POST /books
   - PUT /books/1
   - DELETE /books/1
   - GET /categories
   - POST /categories

2. Verify that book responses include:
   - All book properties
   - List of categories
   - List of reviews

3. Test error handling:
   - Request non-existent resources
   - Provide invalid data in POST/PUT requests

## Implementation Timeline

1. Create Books class with all required methods
2. Create Categories class with all required methods
3. Update json-server.py to handle the new resources
4. Update views/__init__.py
5. Test all endpoints

## Next Steps After Implementation

1. Consider adding filtering capabilities (e.g., get books by category)
2. Consider adding pagination for large result sets
3. Add validation for input data
4. Add more robust error handling

## Code Templates

### views/books.py

```python
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
```

### views/categories.py

```python
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
```

### Updated views/__init__.py

```python
from .reviews import Reviews
from .books import Books
from .categories import Categories
```

### Updated json-server.py

The following changes need to be made to json-server.py:

1. Import the new handler classes:

```python
# Add your imports below this line
from views import Reviews, Books, Categories
```

2. Update do_GET to handle book and category requests:

```python
def do_GET(self):
    """Handle GET requests from a client"""

    response_body = ""
    url = self.parse_url(self.path)

    if url["requested_resource"] == "reviews":
        reviews = Reviews()
        if url["pk"] == 0:
            # Get all reviews
            response_body = reviews.get_all()
            return self.response(response_body, status.HTTP_200_SUCCESS)
        else:
            # Get single review
            response_body = reviews.get_single(url["pk"])
            if response_body is not None:
                return self.response(response_body, status.HTTP_200_SUCCESS)
            else:
                return self.response("Review not found", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND)
    elif url["requested_resource"] == "books":
        books = Books()
        if url["pk"] == 0:
            # Get all books
            response_body = books.get_all()
            return self.response(response_body, status.HTTP_200_SUCCESS)
        else:
            # Get single book
            response_body = books.get_single(url["pk"])
            if response_body is not None:
                return self.response(response_body, status.HTTP_200_SUCCESS)
            else:
                return self.response("Book not found", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND)
    elif url["requested_resource"] == "categories":
        categories = Categories()
        if url["pk"] == 0:
            # Get all categories
            response_body = categories.get_all()
            return self.response(response_body, status.HTTP_200_SUCCESS)
        else:
            return self.response("Individual category retrieval not implemented", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND)
    else:
        return self.response("", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND)
```

3. Update do_PUT to handle book updates:

```python
def do_PUT(self):
    """Handle PUT requests from a client"""

    # Parse the URL and get the primary key
    url = self.parse_url(self.path)
    pk = url["pk"]

    # Get the request body JSON for the new data
    content_len = int(self.headers.get('content-length', 0))
    request_body = self.rfile.read(content_len)
    request_body = json.loads(request_body)

    if url["requested_resource"] == "books":
        if pk != 0:
            books = Books()
            updated = books.update(pk, request_body)
            if updated:
                return self.response(None, status.HTTP_204_SUCCESS_NO_RESPONSE_BODY)
            else:
                return self.response("Book not found", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND)
    else:
        return self.response("Resource not found", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND)
```

4. Update do_DELETE to handle book deletion:

```python
def do_DELETE(self):
    """Handle DELETE requests from a client"""

    url = self.parse_url(self.path)
    pk = url["pk"]

    if url["requested_resource"] == "reviews":
        if pk != 0:
            reviews = Reviews()
            removed = reviews.delete(pk)
            if removed:
                return self.response(None, status.HTTP_204_SUCCESS_NO_RESPONSE_BODY)
            else:
                return self.response("Review not found", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND)
    elif url["requested_resource"] == "books":
        if pk != 0:
            books = Books()
            removed = books.delete(pk)
            if removed:
                return self.response(None, status.HTTP_204_SUCCESS_NO_RESPONSE_BODY)
            else:
                return self.response("Book not found", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND)
    else:
        return self.response("Resource not found", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND)
```

5. Update do_POST to handle book and category creation:

```python
def do_POST(self):
    """Handle POST requests from a client"""

    # Get the request body JSON for the new data
    content_len = int(self.headers.get('content-length', 0))
    request_body = self.rfile.read(content_len)
    request_body = json.loads(request_body)

    url = self.parse_url(self.path)

    if url["requested_resource"] == "reviews":
        reviews = Reviews()
        new_review = reviews.create(request_body)
        return self.response(new_review, status.HTTP_201_SUCCESS_CREATED)
    elif url["requested_resource"] == "books":
        books = Books()
        new_book = books.create(request_body)
        return self.response(new_book, status.HTTP_201_SUCCESS_CREATED)
    elif url["requested_resource"] == "categories":
        categories = Categories()
        new_category = categories.create(request_body)
        return self.response(new_category, status.HTTP_201_SUCCESS_CREATED)
    else:
        return self.response("Resource not found", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND)
```