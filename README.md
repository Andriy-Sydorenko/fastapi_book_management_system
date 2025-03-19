# Book Management System

This project is a FastAPI application that uses PostgreSQL for the database. It includes endpoints for user registration and login, along with CRUD operations for authors and books. The project uses asynchronous PostgreSQL access via asyncpg and secure password handling with argon2.

## Prerequisites

- Python 3.8+ installed
- PostgreSQL installed and running
- Git

## Setup Instructions

1. **Clone the repository**

   ```
   git clone https://github.com/Andriy-Sydorenko/fastapi_book_management_system.git
   ```
2. **Create and activate a virtual environment**
   - On macOS/Linux:
       ```bash
       python3 -m venv venv
       source venv/bin/activate
       ```
   - On Windows:
       ```bash
       python -m venv venv
       venv\Scripts\activate
       ```
3. **Install poetry if not installed yet**
    ```bash
    pip install poetry
    ```
4. **Install the project dependencies**
    ```bash
    poetry install
    ```
> For the next step, ensure you have a PostgreSQL database available.
5. **Create .env file in the root directory of the project and add the following environment variables:**
    ```
    DATABASE_HOST=
    DATABASE_PORT=
    DATABASE_NAME=
    DATABASE_USER=
    DATABASE_PASSWORD=
    ```
6. **For the next steps, make sure you're in the `app` directory, run the migrations to create the database tables and stored functions**
    ```bash
    python3 run_migrations.py
    ```
7. **Run the server**
    ```bash
    fastapi dev main.py
    ```


## Usage
1. **First, create user**
    ```bash
    curl -X POST http://localhost:8000/api/register/ \
      -H "Content-Type: application/json" \
      -d '{"email": "john.doe@example.com", "password": "strongpassword", "full_name": "John Doe"}'
    ```
2. **Get JWT token**
    ```bash
    curl -X POST http://localhost:8000/api/login/ \
      -H "Content-Type: application/json" \
      -d '{"email": "john.doe@example.com", "password": "strongpassword"}'
    ```
3. **Create author**
    ```bash
    curl -X POST http://localhost:8000/api/authors/ \
      -H "Content-Type: application/json" \
      -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJqb2huLmRvZUBleGFtcGxlLmNvbSIsImV4cCI6MTc0MjM3NTE4OX0.nJzaTVOZ5lUSRPCq3uU4RXhUbKUbMWRF3XBkbl1dBIg" \
      -d '{"name": "Test Author"}'
    ```
4. **Create book**
    ```bash
    curl -X POST http://localhost:8000/api/books/ \
      -H "Content-Type: application/json" \
      -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJqb2huLmRvZUBleGFtcGxlLmNvbSIsImV4cCI6MTc0MjM3NTE4OX0.nJzaTVOZ5lUSRPCq3uU4RXhUbKUbMWRF3XBkbl1dBIg" \
      -d '{"title": "Book Title", "isbn": "1234567890123", "published_year": 2023, "genre": "Fiction", "author_name": "Test Author"}'
    ```

5. **Get list of authors and books**
    ```bash
    curl -X GET http://localhost:8000/api/authors/
    ```
    ```bash
    curl -X GET http://localhost:8000/api/books/
   ```

## API Documentation
- The API is automatically documented using Swagger UI, available at:  
  `http://localhost:8000/docs`

## Recommendations for Improvement
- Add more tests to cover more scenarios
- Improve error handling and input validation, make error messages more user-friendly
- Add authentication for documentation to be able to test protected endpoints directly from Swagger UI
