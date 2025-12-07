# Library REST API

This is a CRUD REST API for a Library Management System, built with Flask and MySQL. It supports JSON and XML output formats and is secured using JWT authentication.

## Features

*   **CRUD Operations**: Create, Read, Update, and Delete books.
*   **Authentication**: JWT-based authentication.
*   **Search**: Search books by title or author.
*   **Formatting**: Support for JSON (default) and XML output.

## Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/darcykekw/REST-API-Project.git
    cd REST-API-Project
    ```

2.  Create and activate a virtual environment:
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # Linux/Mac
    source venv/bin/activate
    ```

3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4.  Initialize the database:
    ```bash
    python init_db.py
    ```

5.  Run the application:
    ```bash
    python app.py
    ```

## API Usage

### Authentication

**Login**
*   **URL**: `/login`
*   **Method**: `POST`
*   **Auth**: Basic Auth (username: `admin`, password: `password123`)
*   **Response**: Returns a JWT token.

### Books

All endpoints below require the `token` query parameter (e.g., `?token=<your_token>`).

**Get All Books**
*   **URL**: `/books`
*   **Method**: `GET`
*   **Params**:
    *   `q`: Search query (optional).
    *   `format`: `xml` for XML output (optional).
*   **Response**: List of books.

**Get Single Book**
*   **URL**: `/books/<id>`
*   **Method**: `GET`
*   **Response**: Book details.

**Add Book**
*   **URL**: `/books`
*   **Method**: `POST`
*   **Body** (JSON):
    ```json
    {
        "title": "Book Title",
        "author": "Author Name",
        "published_year": 2023,
        "isbn": "1234567890"
    }
    ```

**Update Book**
*   **URL**: `/books/<id>`
*   **Method**: `PUT`
*   **Body** (JSON): Fields to update.

**Delete Book**
*   **URL**: `/books/<id>`
*   **Method**: `DELETE`

## Testing

Run the unit tests:
```bash
python test_app.py
```
