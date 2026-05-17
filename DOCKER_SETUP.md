# Docker Setup for Library Management System

## Quick Start

### 1. Clone or navigate to the project directory

```bash
cd /home/vaibhavsharma/Desktop/Library-management-System
```

### 2. Create a `.env` file (optional)

Copy from `.env.example` if you want to customize settings:

```bash
cp .env.example .env
```

### 3. Build and run with Docker Compose

```bash
docker-compose up -d
```

This will:

- Build the Django application image
- Start a PostgreSQL database container
- Run database migrations automatically
- Collect static files
- Start the application on http://localhost:8000

### 4. View logs

```bash
docker-compose logs -f web
```

## Available Commands

### Stop the containers

```bash
docker-compose down
```

### Stop and remove volumes (clears database)

```bash
docker-compose down -v
```

### Run migrations manually

```bash
docker-compose exec web python manage.py migrate
```

### Create a superuser

```bash
docker-compose exec web python manage.py createsuperuser
```

### Access Django shell

```bash
docker-compose exec web python manage.py shell
```

### Restart services

```bash
docker-compose restart
```

### Rebuild the image

```bash
docker-compose up -d --build
```

## Environment Variables

The application uses environment variables from `.env` file. Key variables:

- `DEBUG`: Set to `True` for development, `False` for production
- `DJANGO_SECRET_KEY`: Django secret key
- `DB_NAME`: PostgreSQL database name
- `DB_USER`: PostgreSQL username
- `DB_PASSWORD`: PostgreSQL password
- `DB_HOST`: Database host (use `db` for Docker)
- `DB_PORT`: Database port

## Accessing the Application

- **Web Application**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin
- **API Documentation**: http://localhost:8000/api/schema/swagger-ui

## Troubleshooting

### Port already in use

If port 8000 is already in use, you can change it in `docker-compose.yml`:

```yaml
ports:
  - "8001:8000" # Maps container port 8000 to host port 8001
```

### Database connection issues

Ensure the database container is healthy:

```bash
docker-compose ps
```

If `db` service shows unhealthy, restart it:

```bash
docker-compose restart db
```

### Rebuild everything from scratch

```bash
docker-compose down -v
docker-compose up -d --build
```
