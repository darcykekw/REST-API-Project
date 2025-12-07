import MySQLdb

def init_db():
    # Connect to MySQL server first to create DB if not exists
    db = MySQLdb.connect(
        host="localhost",
        user="root",
        passwd=""
    )
    cursor = db.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS library_db")
    db.select_db("library_db")


    # Create books table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS books (
        id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        author VARCHAR(255) NOT NULL,
        published_year INT,
        isbn VARCHAR(20)
    )
    """)

    # Create users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(50) NOT NULL UNIQUE,
        password VARCHAR(255) NOT NULL
    )
    """)

    # Check if books exist, if not add some
    cursor.execute("SELECT COUNT(*) FROM books")
    count = cursor.fetchone()[0]
    if count == 0:
        books = [
            ('The Great Gatsby', 'F. Scott Fitzgerald', 1925, '9780743273565'),
            ('To Kill a Mockingbird', 'Harper Lee', 1960, '9780061120084'),
            ('1984', 'George Orwell', 1949, '9780451524935'),
            ('Pride and Prejudice', 'Jane Austen', 1813, '9780141439518'),
            ('The Catcher in the Rye', 'J.D. Salinger', 1951, '9780316769488'),
            ('The Hobbit', 'J.R.R. Tolkien', 1937, '9780547928227'),
            ('Fahrenheit 451', 'Ray Bradbury', 1953, '9781451673319'),
            ('Jane Eyre', 'Charlotte Bronte', 1847, '9780141441146'),
            ('Animal Farm', 'George Orwell', 1945, '9780451526342'),
            ('Wuthering Heights', 'Emily Bronte', 1847, '9780141439556'),
            ('Brave New World', 'Aldous Huxley', 1932, '9780060850524'),
            ('The Lord of the Rings', 'J.R.R. Tolkien', 1954, '9780544003415'),
            ('Harry Potter and the Sorcerer\'s Stone', 'J.K. Rowling', 1997, '9780590353427'),
            ('The Da Vinci Code', 'Dan Brown', 2003, '9780307474278'),
            ('The Alchemist', 'Paulo Coelho', 1988, '9780062315007'),
            ('The Hunger Games', 'Suzanne Collins', 2008, '9780439023481'),
            ('The Kite Runner', 'Khaled Hosseini', 2003, '9781594631931'),
            ('The Book Thief', 'Markus Zusak', 2005, '9780375842207'),
            ('The Chronicles of Narnia', 'C.S. Lewis', 1950, '9780066238500'),
            ('Gone with the Wind', 'Margaret Mitchell', 1936, '9781451635621')
        ]
        cursor.executemany("INSERT INTO books (title, author, published_year, isbn) VALUES (%s, %s, %s, %s)", books)
        print("Added 20 sample books.")

    # Check if admin user exists
    cursor.execute("SELECT * FROM users WHERE username = 'admin'")
    if not cursor.fetchone():
        cursor.execute("INSERT INTO users (username, password) VALUES ('admin', 'password123')")
        print("Added admin user.")

    db.commit()
    db.close()
    print("Database initialized.")

if __name__ == "__main__":
    init_db()
