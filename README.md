# Library Management System (LMS)

> A production-grade, role-based web application built with **Python Django 6.0**, **PostgreSQL**, and **Jinja2** for automating academic and public library operations. Designed for MCA academic submission and real-world deployment.

---

## Overview

The Library Management System streamlines the complete lifecycle of library operations — including book cataloging, member lifecycle management, issue/return tracking, automated fine calculation, reservation handling, and analytical reporting.

The system enforces strict role-based access control (Admin, Librarian, Member), provides a responsive Bootstrap 5 frontend, and exposes a fully documented REST API secured with JWT tokens.

---

## Key Features

| Module                             | Capabilities                                                                                          |
| ---------------------------------- | ----------------------------------------------------------------------------------------------------- |
| **Authentication & Authorization** | Custom user model, role-based access (Admin / Librarian / Member), session login for web, JWT for API |
| **Book Management**                | CRUD operations, ISBN validation, category mapping, cover image upload, inventory tracking            |
| **Member Management**              | Registration, unique member code generation, membership status tracking, borrowing history            |
| **Issue & Return**                 | Eligibility validation, automatic due date calculation (14 days), real-time copy availability sync    |
| **Fine Management**                | Automatic overdue calculation (₹5/day), fine recording, payment collection workflow, waiver support   |
| **Reservation System**             | Queue management for unavailable books, expiry handling, availability notifications                   |
| **Reports & Dashboard**            | KPI cards, overdue tracking, fine collection metrics, CSV export, role-aware UI                       |
| **REST API**                       | DRF-powered endpoints, pagination, filtering, Swagger/OpenAPI docs, stateless JWT auth                |

---

## 🛠️ Technology Stack

| Layer                | Technology                                         | Version               |
| -------------------- | -------------------------------------------------- | --------------------- |
| **Backend**          | Python, Django, Django REST Framework              | 3.12 / 6.0.4 / 3.17.1 |
| **Authentication**   | `djangorestframework-simplejwt`                    | 5.5.1                 |
| **Database**         | PostgreSQL, `psycopg2-binary`                      | 14+ / 2.9.12          |
| **Templating**       | Jinja2 (Django backend), `django-jinja` extensions | 3.1.6                 |
| **Frontend**         | HTML5, CSS3, Bootstrap 5, Vanilla JS               | 5.3+                  |
| **API Docs**         | `drf-spectacular`                                  | 0.29.0                |
| **Admin UI**         | `django-unfold`                                    | Latest                |
| **Deployment Ready** | Gunicorn, Nginx, Docker, AWS/Heroku                | Configurable          |

---

## Project Structure

```
Library-management-System/
.
├── apps/                          # Django applications
│   ├── accounts/                  # User authentication & authorization
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── __init__.py
│   │   ├── migrations/
│   │   │   ├── 0001_initial.py
│   │   │   └── __init__.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── tests.py
│   │   ├── urls_api.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── library/                   # Book catalog management
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── __init__.py
│   │   ├── migrations/
│   │   │   ├── 0001_initial.py
│   │   │   └── __init__.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── tests.py
│   │   ├── urls_api.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── reports/                   # Analytics & KPI dashboard
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── __init__.py
│   │   ├── migrations/
│   │   │   └── __init__.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── tests.py
│   │   ├── urls_api.py
│   │   ├── urls.py
│   │   └── views.py
│   └── transactions/              # Book issue/return operations
│       ├── admin.py
│       ├── apps.py
│       ├── __init__.py
│       ├── migrations/
│       │   ├── 0001_initial.py
│       │   └── __init__.py
│       ├── models.py
│       ├── serializers.py
│       ├── tests.py
│       ├── urls_api.py
│       ├── urls.py
│       └── views.py
├── lms_core/                      # Django project settings
│   ├── asgi.py
│   ├── __init__.py
│   ├── jinja.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── templates/                     # Jinja2 templates
│   ├── accounts/
│   │   └── login.jinja
│   ├── base.jinja
│   ├── dashboard.jinja
│   ├── library/
│   │   └── book_list.jinja
│   ├── reports/
│   │   └── dashboard.jinja
│   └── transactions/
│       ├── history.jinja
│       └── issue.jinja
├── static/                        # Static assets (development)
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
├── staticfiles/                   # Collected static files (production)
│   ├── admin/
│   ├── css/
│   ├── js/
│   ├── rest_framework/
│   └── unfold/
├── media/                         # Uploaded files (book covers, etc.)
├── build.sh                       # Build script for deployment
├── create_superuser.sh            # Superuser creation script
├── start.sh                       # Application startup script
├── docker-compose.yml             # Docker Compose configuration
├── Dockerfile                     # Docker image definition
├── .dockerignore                  # Docker ignore patterns
├── .env                           # Environment variables (production)
├── .env.example                   # Environment variables template
├── .gitignore                     # Git ignore patterns
├── DOCKER_SETUP.md                # Docker setup guide
├── Procfile                       # Heroku/Render deployment config
├── render.yaml                    # Render.com deployment config
├── requirements.txt               # Python dependencies
├── runtime.txt                    # Python runtime version
├── manage.py                      # Django management command
└── README.md                      # This file
```

### Directory Guide

| Directory      | Purpose                                                                             |
| -------------- | ----------------------------------------------------------------------------------- |
| `apps/`        | Django applications organized by feature (Accounts, Library, Reports, Transactions) |
| `lms_core/`    | Django project configuration, URL routing, settings, and WSGI/ASGI servers          |
| `templates/`   | Jinja2 HTML templates for the web UI                                                |
| `static/`      | Development static assets (CSS, JS)                                                 |
| `staticfiles/` | Collected production static files (generated by `collectstatic`)                    |
| `media/`       | User-uploaded files (book covers, documents)                                        |

---

## ⚙️ Prerequisites

Before getting started, make sure you have the following installed:

- Python 3.10+ _(tested on 3.12.3)_
- PostgreSQL 14+
- `pip` & `virtualenv`
- Git

---

## Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/SharmaVaibhav976531/Library-management-System.git
cd Library-management-System
```

### 2. Create & Activate a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root and populate it with the following:

```env
DJANGO_SECRET_KEY=your-super-secure-random-key-here
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
DB_NAME=lms_db
DB_USER=postgres
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
```

### 5. Set Up the Database

Ensure your PostgreSQL service is running, then create the database:

```bash
createdb lms_db
```

### 6. Apply Migrations & Create a Superuser

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

---

## Running the Application

### Development Server

```bash
python manage.py runserver
```

Once running, the following interfaces are available:

| Interface         | URL                                |
| ----------------- | ---------------------------------- |
| Web Application   | http://127.0.0.1:8000/             |
| Admin Panel       | http://127.0.0.1:8000/admin/       |
| API Documentation | http://127.0.0.1:8000/api/v1/docs/ |
| Live URL          |https://library-management-system-tdp9.onrender.com  |
---

## API Endpoints Overview

| Method | Endpoint                       | Description                          | Auth              |
| ------ | ------------------------------ | ------------------------------------ | ----------------- |
| `POST` | `/api/v1/auth/login/`          | Obtain JWT access and refresh tokens | Public            |
| `GET`  | `/api/v1/library/books/`       | List books (paginated, searchable)   | Optional          |
| `POST` | `/api/v1/transactions/issue/`  | Issue a book to a member             | Librarian / Admin |
| `POST` | `/api/v1/transactions/return/` | Process return and calculate fine    | Librarian / Admin |
| `GET`  | `/api/v1/reports/dashboard/`   | KPI aggregation data                 | Admin             |

**Interactive API Documentation** is available at: `/api/v1/docs/`

---

## User Roles & Workflows

| Role          | Permissions                                                                | Typical Workflow                                                   |
| ------------- | -------------------------------------------------------------------------- | ------------------------------------------------------------------ |
| **Admin**     | Full system control, user management, fine waivers, global reports         | Configure system, manage roles, export analytics, override fines   |
| **Librarian** | Book catalog management, member onboarding, issue/return processing, fines | Search books, check eligibility, process returns, collect payments |
| **Member**    | View catalog, borrowing history, fine tracking, book reservations          | Browse books, view due dates, pay fines, check reservation status  |

---

## Testing

### Run Automated Tests

```bash
python manage.py test apps
```

### Manual Test Checklist

Work through the following scenarios to validate core functionality:

- [ ] Login with valid and invalid credentials
- [ ] Issue a book with an active membership and available copies
- [ ] Attempt to issue a book to an inactive or overdue member — validation should block the action
- [ ] Return an overdue book — verify fine calculation and status update
- [ ] Collect a fine — verify that dashboard KPI metrics update accordingly
- [ ] Search for books by title, author, and ISBN
- [ ] Export a CSV report from the dashboard
- [ ] Verify JWT authentication via Postman or Swagger

---

## License

This project was developed for academic purposes under the **Chandigarh University MCA Program**. Source code may be referenced for educational use with proper attribution.

---

## Acknowledgements

- **Django Software Foundation** & **PostgreSQL Global Development Group**
- **Bootstrap Team** & **Jinja2 / Pallets Projects**
- Academic mentors and CU Online faculty for SDLC and architecture guidance
- Open-source contributors to `drf-spectacular`, `simplejwt`, and `django-unfold`

---

## Need Help?

If you run into issues, here are a few good places to start:

- Run `python manage.py check` for system validation
- Review `lms_core/settings.py` for template and database configurations
- See `templates/base.jinja` for UI structure and static asset loading
- For API testing, import `http://127.0.0.1:8000/api/v1/schema/` into Postman
