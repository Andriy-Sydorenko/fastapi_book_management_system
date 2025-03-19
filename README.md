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
