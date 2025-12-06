# FastAPI Blog & Product System

A robust, scalable backend API built with **FastAPI** and **Python**, designed to power modern web applications. This project features a complete user management system, content creation workflows (blogs/articles), product handling, and real-time communication capabilities.

It is designed to serve as a solid foundation for backend engineering, with a focus on clean architecture, authentication, and database relationships.

## 🚀 Tech Stack

### Backend
- **Framework**: [FastAPI](https://fastapi.tiangolo.com/) - High performance, easy to learn, fast to code, ready for production.
- **Language**: Python 3.9+
- **Database**: SQLite (Development) with **SQLAlchemy** ORM.
- **Authentication**: OAuth2 with Password (and Hashing) + JWT Tokens.
- **Real-time**: WebSockets.
- **Validation**: Pydantic models.

### Frontend
- **React**: The project structure includes a `React App` folder for the frontend application. The backend is pre-configured with **CORS** to allow requests from a React app running on `http://localhost:3000`.
- **Demo Client**: A lightweight HTML/JS client (`client.py`) is included to demonstrate real-time WebSocket chat functionality.

## ✨ Key Features

### 🔐 Authentication & Security
- **User Registration & Login**: Secure user creation with password hashing (bcrypt).
- **JWT Tokens**: API endpoints are secured using JSON Web Tokens.
- **Permissions**: Resource access control (e.g., only authors can delete their posts).

### 📝 Content Management
- **Articles & Blogs**: logic for creating, reading, updating, and deleting (CRUD) textual content.
- **Database Relationships**: One-to-Many relationship between **Users** and **Articles** (Users can own multiple articles).
- **Image Uploads**: Dedicated endpoint (`/upload`) to handle file uploads, serving them statically from the `/files` directory.

### 💬 Real-Time Chat
- **WebSockets**: Implemented a two-way interactive chat endpoint (`/chat`) that broadcasts messages to all connected clients.
- **Middleware**: Custom middleware to track and log process duration for every request.

### 🛒 Products
- **Product API**: Endpoints to handle product data, demonstrating validation and complex query parameters.

## 📂 Project Structure

```
.
├── Get Method/
│   ├── main.py             # Application entry point
│   ├── auth/               # Authentication logic (JWT, OAuth2)
│   ├── db/                 # Database models and session handling
│   │   ├── models.py       # SQLAlchemy Database Tables (Users, Articles)
│   │   └── database.py     # Database connection
│   ├── Routers/            # API Route handlers (clean separation of concerns)
│   │   ├── blog_get.py     # Blog retrieval logic
│   │   ├── blog_post.py    # Blog creation logic
│   │   ├── user.py         # User management endpoints
│   │   ├── article.py      # Article management endpoints
│   │   └── ...
│   ├── templates/          # Jinja2 templates for server-side rendering
│   └── client.py           # WebSocket client demo
├── React App/              # Frontend React Application (Placeholder/Repository)
├── .gitignore              # Git configuration
└── requirements.txt        # Python dependencies
```

## 🗄️ Database Schema

The application uses a relational database model:

- **Users Table** (`users`)
  - `id`: Integer, Primary Key
  - `username`: String
  - `email`: String
  - `password`: String (Hashed)
  - `items`: Relationship to Articles

- **Items/Articles Table** (`items`)
  - `id`: Integer, Primary Key
  - `title`: String
  - `content`: String
  - `published`: Boolean
  - `user_id`: Foreign Key to Users table

## 🔧 Setup & Running

1.  **Clone the repository**
2.  **Create a virtual environment**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
3.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Run the Backend**
    Navigate to the source directory:
    ```bash
    cd "Get Method"
    uvicorn main:app --reload
    ```
    The API will be available at `http://localhost:8000`.

5.  **Explore the API**
    Open your browser and navigate to `http://localhost:8000/docs` to see the interactive **Swagger UI** documentation. You can test all endpoints directly from there.

6.  **Run WebSocket Demo**
    Open `http://localhost:8000/` or the specific chat endpoint to test real-time messaging.

## 🔮 Future Improvements
- Complete the **React** frontend implementation in the `React App` directory.
- Migrate database to PostgreSQL for production.
- Add Unit Tests using `pytest` (some structure already exists in `test_main.py`).
