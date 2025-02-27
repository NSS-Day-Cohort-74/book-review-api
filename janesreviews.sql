-- Jane's Reviews SQLite Database Schema and Sample Data
-- Generated based on janesreviews.dbml

-- Drop tables if they exist to ensure clean setup
DROP TABLE IF EXISTS BookCategory;
DROP TABLE IF EXISTS Review;
DROP TABLE IF EXISTS Category;
DROP TABLE IF EXISTS Book;
DROP TABLE IF EXISTS User;

-- Create User table
CREATE TABLE User (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE
);

-- Create Book table
CREATE TABLE Book (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    isbn TEXT UNIQUE,
    publication_date DATETIME,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES User(id)
);

-- Create Review table
CREATE TABLE Review (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    rating INTEGER NOT NULL,
    review_text TEXT,
    FOREIGN KEY (book_id) REFERENCES Book(id),
    FOREIGN KEY (user_id) REFERENCES User(id)
);

-- Create Category table
CREATE TABLE Category (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_name TEXT NOT NULL
);

-- Create BookCategory junction table
CREATE TABLE BookCategory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    FOREIGN KEY (book_id) REFERENCES Book(id),
    FOREIGN KEY (category_id) REFERENCES Category(id)
);

-- Insert sample data

-- Insert Users (4)
INSERT INTO User (username, email) VALUES
    ('jane_doe', 'jane@example.com'),
    ('john_smith', 'john@example.com'),
    ('alice_wonder', 'alice@example.com'),
    ('bob_reader', 'bob@example.com');

-- Insert Categories (7)
INSERT INTO Category (category_name) VALUES
    ('Fiction'),
    ('Non-Fiction'),
    ('Mystery'),
    ('Science Fiction'),
    ('Romance'),
    ('Biography'),
    ('History');

-- Insert Books (10, distributed among users)
INSERT INTO Book (title, author, isbn, publication_date, user_id) VALUES
    ('The Silent Patient', 'Alex Michaelides', '978-1250301697', '2019-02-05', 1),
    ('Educated', 'Tara Westover', '978-0399590504', '2018-02-20', 1),
    ('Where the Crawdads Sing', 'Delia Owens', '978-0735219090', '2018-08-14', 2),
    ('Becoming', 'Michelle Obama', '978-1524763138', '2018-11-13', 2),
    ('The Midnight Library', 'Matt Haig', '978-0525559474', '2020-09-29', 3),
    ('Project Hail Mary', 'Andy Weir', '978-0593135204', '2021-05-04', 3),
    ('The Four Winds', 'Kristin Hannah', '978-1250178602', '2021-02-02', 4),
    ('The Invisible Life of Addie LaRue', 'V.E. Schwab', '978-0765387561', '2020-10-06', 4),
    ('Klara and the Sun', 'Kazuo Ishiguro', '978-0593318171', '2021-03-02', 1),
    ('The Lincoln Highway', 'Amor Towles', '978-0735222359', '2021-10-05', 2);

-- Insert BookCategory associations (2 categories per book, 20 total)
INSERT INTO BookCategory (book_id, category_id) VALUES
    (1, 1), -- The Silent Patient: Fiction
    (1, 3), -- The Silent Patient: Mystery
    (2, 2), -- Educated: Non-Fiction
    (2, 6), -- Educated: Biography
    (3, 1), -- Where the Crawdads Sing: Fiction
    (3, 3), -- Where the Crawdads Sing: Mystery
    (4, 2), -- Becoming: Non-Fiction
    (4, 6), -- Becoming: Biography
    (5, 1), -- The Midnight Library: Fiction
    (5, 4), -- The Midnight Library: Science Fiction
    (6, 1), -- Project Hail Mary: Fiction
    (6, 4), -- Project Hail Mary: Science Fiction
    (7, 1), -- The Four Winds: Fiction
    (7, 7), -- The Four Winds: History
    (8, 1), -- The Invisible Life of Addie LaRue: Fiction
    (8, 4), -- The Invisible Life of Addie LaRue: Science Fiction
    (9, 1), -- Klara and the Sun: Fiction
    (9, 4), -- Klara and the Sun: Science Fiction
    (10, 1), -- The Lincoln Highway: Fiction
    (10, 7); -- The Lincoln Highway: History

-- Insert Reviews (each user reviews one book)
INSERT INTO Review (book_id, user_id, rating, review_text) VALUES
    (3, 1, 5, 'A beautifully written story that captivated me from beginning to end. The character development is exceptional.'),
    (5, 2, 4, 'An intriguing concept that makes you think about the choices we make in life. I found the ending particularly moving.'),
    (7, 3, 4, 'A powerful historical novel that shows the resilience of the human spirit. The descriptions of the Dust Bowl era are vivid and haunting.'),
    (1, 4, 5, 'One of the best psychological thrillers I''ve read in years. The twist at the end completely caught me by surprise.');










SELECT
    rating,
    review_text,
    book_id,
    b.title
FROM Review
JOIN Book b ON book_id = b.id
;