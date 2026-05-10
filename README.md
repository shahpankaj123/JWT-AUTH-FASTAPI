# 🔐 FastAPI Backend — JWT Authentication

A secure REST API backend built with **FastAPI** featuring JWT authentication, async MySQL database integration via SQLAlchemy, and a clean MVC-style architecture.

---

## 🚀 Features

- JWT-based user authentication (register & login)
- Async database operations with SQLAlchemy 2.0
- MySQL database with auto table creation on startup
- User type / role management
- Pydantic v2 data validation
- Auto-generated Swagger UI & ReDoc documentation
- Clean layered architecture: Controller → Service → Selector → Model

---

## 🛠️ Tech Stack

| Technology | Version | Purpose |
|------------|---------|---------|
| [FastAPI](https://fastapi.tiangolo.com/) | 0.128.0 | Web framework |
| [SQLAlchemy](https://www.sqlalchemy.org/) | 2.0.45 | Async ORM |
| [PyMySQL](https://pymysql.readthedocs.io/) | 1.1.2 | MySQL driver |
| [Pydantic](https://docs.pydantic.dev/) | 2.12.5 | Data validation |
| [Uvicorn](https://www.uvicorn.org/) | 0.40.0 | ASGI server |
| [python-dotenv](https://pypi.org/project/python-dotenv/) | 1.2.1 | Environment config |
| [Sentry SDK](https://sentry.io/) | 2.48.0 | Error monitoring |

---

## 📁 Project Structure

```
FastApi-Backend/
├── config/
│   └── database_connection.py   # Async SQLAlchemy engine & session setup
├── controller/
│   ├── auth_controller.py       # Auth routes (register, login)
│   └── user_type.py             # User type/role routes
├── model/
│   └── mainapp_models.py        # SQLAlchemy ORM models
├── selector/                    # Database query layer (read operations)
├── services/                    # Business logic layer
├── main.py                      # App entry point, router registration
├── requiremnets.txt             # Python dependencies
├── schema.sql                   # SQL schema reference
└── .gitignore
```

---

## ⚙️ Setup & Installation

### Prerequisites

- Python 3.9+
- MySQL database server running

### 1. Clone the repository

```bash
git clone https://github.com/shahpankaj123/FastApi-Backend.git
cd FastApi-Backend
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requiremnets.txt
```

### 4. Configure environment variables

Create a `.env` file in the root directory:

```env
DATABASE_URL=mysql+aiomysql://username:password@localhost:3306/your_database
SECRET_KEY=your_super_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

> **Tip:** Generate a secure secret key with:
> ```bash
> openssl rand -hex 32
> ```

### 5. Set up the database

Create your MySQL database — the app auto-creates all tables on startup:

```sql
CREATE DATABASE your_database;
```

### 6. Run the development server

```bash
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`

---

## 📖 API Documentation

Once the server is running, visit:

- **Swagger UI** → [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc** → [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 🔑 API Endpoints

### Users — `/web/api/v1/users`

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|:---:|
| `POST` | `/web/api/v1/users/register` | Register a new user | ❌ |
| `POST` | `/web/api/v1/users/login` | Login and receive JWT token | ❌ |

### User Type — `/web/api/v1/user-type`

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|:---:|
| `GET` | `/web/api/v1/user-type/` | List all user types/roles | ✅ |
| `POST` | `/web/api/v1/user-type/` | Create a new user type | ✅ |

---

## 🔒 Authentication Flow

```
1. Register  →  POST /web/api/v1/users/register  →  User created in DB
2. Login     →  POST /web/api/v1/users/login     →  Returns JWT access token
3. Request   →  Any protected route              →  Pass token in Authorization header
```

### Example: Login Request

```bash
curl -X POST "http://127.0.0.1:8000/web/api/v1/users/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "john@example.com", "password": "yourpassword"}'
```

**Response:**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5...",
  "token_type": "bearer"
}
```

### Example: Accessing a Protected Route

```bash
curl -X GET "http://127.0.0.1:8000/web/api/v1/user-type/" \
  -H "Authorization: Bearer <your_access_token>"
```

---

## 🏗️ Architecture Overview

The project follows a clean layered MVC-inspired architecture:

```
Request → Controller (router) → Service (business logic) → Selector (DB queries) → Model (ORM)
```

- **Controller** — defines API routes and handles HTTP request/response
- **Services** — business logic, token generation, password hashing
- **Selector** — all database read queries
- **Model** — SQLAlchemy ORM table definitions
- **Config** — database connection and environment settings

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add some feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

## 👤 Author

**Pankaj Shah**
- GitHub: [@shahpankaj123](https://github.com/shahpankaj123)
