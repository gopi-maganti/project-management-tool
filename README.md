# 🛠️ Project Management Tool (PMT)

A web-based application to help users manage tasks, projects, and teams efficiently. Built using **Django**, **PostgreSQL**, and designed for scalability, developer productivity, and ease of use.

---

## 📁 Project Structure

```
project-management-tool/
├── .github/workflows/        # GitHub Actions for CI/CD
├── api/                      # Main app with business logic (models, views, etc.)
│   ├── constants/            # Constants used across the app
│   ├── migrations/           # Database migration files
│   ├── models/               # Database schema
│   ├── restful/              # Viewsets and serializers
│   ├── tests/                # Unit and integration tests
│   ├── utils/                # Helper functions
│   ├── apps.py               # App configuration
│   └── urls.py               # API-specific routing
├── pmt_backend/              # Project-level configuration
│   ├── settings.py           # Main Django settings
│   ├── urls.py               # Root URL configurations
│   ├── asgi.py / wsgi.py     # For deployment
│   └── custom_logger.py      # Project-wide logging setup
├── requirements/             # Python dependency files
│   ├── base.txt              # Main requirements
│   └── test.txt              # Testing dependencies
├── .env                      # Environment variables (not committed)
├── .gitignore                # Git ignored files
├── .isort.cfg                # Python import formatting config
├── docker-compose.yml        # Multi-container Docker setup
├── Dockerfile                # Backend Docker image
├── pytest.ini                # Pytest configuration
├── .coveragerc               # Code coverage config
└── README.md                 # This file
```

---

## 🚀 Features

✅ User registration and login (email or username)  
✅ Google Social Login  
✅ Token & JWT-based authentication  
✅ Admins can manage users  
✅ Clean REST API structure using Django REST Framework  
✅ Auto-generated API docs (Swagger/OpenAPI)  
✅ Containerized with Docker  
✅ CI with GitHub Actions  
✅ Full test coverage with Pytest  

---

## 🧑‍💻 Getting Started (For Developers)

### 🧰 Prerequisites

- Python 3.11+
- Docker & Docker Compose
- PostgreSQL
- (Optional) `pipenv` or `venv` for managing Python environments

---

### 🔧 Local Setup

#### 1. Clone the Repo

```bash
git clone https://github.com/your-username/project-management-tool.git
cd project-management-tool
```

#### 2. Setup Environment

Create a `.env` file at the root with:

```env
DEBUG=True
SECRET_KEY=your-secret-key
POSTGRES_DB=your_db_name
POSTGRES_USER=your_db_user
POSTGRES_PASSWORD=your_db_password
```

---

#### 3. Run with Docker

```bash
docker-compose up --build
```

The API will be available at `http://localhost:8000`.

---

#### 4. API Docs

Visit:

```url
http://localhost:8000/swagger/  # Swagger UI
http://localhost:8000/redoc/    # ReDoc UI
```

---

## 🧪 Running Tests

```bash
# Inside Docker container
pytest --cov=api
```

---

## 🛠 Technologies Used

| Tech            | Purpose                             |
|----------------|-------------------------------------|
| Django          | Web framework                      |
| Django REST     | API layer                          |
| PostgreSQL      | Database                           |
| Docker          | Containerization                   |
| Pytest          | Testing framework                  |
| GitHub Actions  | CI/CD automation                   |
| drf-yasg        | Swagger API documentation          |

---

## 🤝 Contributing

1. Fork the repo
2. Create your feature branch (`git checkout -b feature/foo`)
3. Commit changes (`git commit -m 'Add foo feature'`)
4. Push (`git push origin feature/foo`)
5. Open a Pull Request

---

## 🧠 For Non-Technical Users

- This tool helps you register, login, and manage users and tasks.
- Just like Trello or Asana, this is a backend server powering such apps.
- Your data is secured with token-based logins and passwords.
- You can view your profile or team lists using URLs like:

  - `http://localhost:8000/api/users/`
  - `http://localhost:8000/api/register/`

---

## 📬 Contact

Built by Gopi Krishna Maganti  
📧 Email: gopi.maganti1998@gmail.com

---
