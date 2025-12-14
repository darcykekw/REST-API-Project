# Library REST API

This project is a comprehensive RESTful API designed for a Library Management System. It serves as a backend service to manage a library's book collection, offering robust functionalities for adding, retrieving, updating, and deleting book records.

Built with **Flask** and **MySQL**, the API ensures secure access through **JWT (JSON Web Token)** authentication. It is designed to be flexible, supporting both **JSON** and **XML** response formats to accommodate different client requirements.

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

4.  Run the application:
    ```bash
    python app.py
    ```

## Usage

### API Usage

The application provides a RESTful API. You can interact with it using tools like Postman or curl.

#### Authentication

**Login**
*   **URL**: `/login`
*   **Method**: `POST`
*   **Auth**: Basic Auth (username: `admin`, password: `password123`)
*   **Response**: Returns a JWT token.

### Books

All endpoints below require the `token` query parameter. You must append the token you received from the login step to the URL.

**Important**: Do not include `<` or `>` characters around your token.
*   **Example**: `http://127.0.0.1:5000/books?token=eyJhbGci...`

**Get All Books**
*   **URL**: `/books`
*   **Example**: `http://127.0.0.1:5000/books?token=YOUR_TOKEN`
*   **Method**: `GET`
*   **Params**:
    *   `q`: Search query (optional).
    *   `format`: `xml` for XML output (optional).
*   **Response**: List of books.

**Get Single Book**
*   **URL**: `/books/<id>`
*   **Example**: `http://127.0.0.1:5000/books/1?token=YOUR_TOKEN`
*   **Method**: `GET`
*   **Response**: Book details.

**Add Book**
*   **URL**: `/books`
*   **Example**: `http://127.0.0.1:5000/books?token=YOUR_TOKEN`
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
*   **Example**: `http://127.0.0.1:5000/books/1?token=YOUR_TOKEN`
*   **Method**: `PUT`
*   **Body** (JSON): Fields to update.

**Delete Book**
*   **URL**: `/books/<id>`
*   **Example**: `http://127.0.0.1:5000/books/1?token=YOUR_TOKEN`
*   **Method**: `DELETE`

## Testing

The project includes a suite of unit tests to verify the API's functionality, including authentication, CRUD operations, and search.

**Prerequisites:**
*   Ensure your MySQL database (`library_db`) is running.
*   Ensure the database credentials in `app.py` match your local setup.

**Running the Tests:**
Execute the following command in your terminal:

```bash
python test_app.py
```
