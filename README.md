# Datasync API

A Django REST API for managing data synchronization between systems.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Infrastructure Setup](#infrastructure-setup)
- [Running Tests](#running-tests)
- [API Documentation](#api-documentation)
- [Development](#development)

## Prerequisites
- Python 3.12+
- Git
- Redis (or Memurai for Windows)
- pip (Python package manager)

## Installation

1. Clone the repository

2. Install dependencies
```bash
pip install -r requirements.txt
```

## Infrastructure Setup

1. Database setup
```bash
python manage.py migrate
```

2. Create superuser
```bash
python manage.py createsuperuser
```

3. Install and start Memurai (Windows) or Redis (Linux/Mac)
```bash
# Windows: Download and install Memurai from https://www.memurai.com/
# Linux/Mac
sudo apt-get install redis-server
sudo service redis start
```

4. Start the development server
```bash
python manage.py runserver
```

## API Documentation

### Authentication Endpoints

1. User Signup
```bash
POST /api/auth/signup/
Content-Type: application/json

{
    "email": "user@example.com",
    "password": "secure_password"
}

Response:
{
    "message": "User created successfully"
}
```

2. User Login
```bash
POST /api/auth/login/
Content-Type: application/json

{
    "username": "user@example.com",
    "password": "secure_password"
}

Response:
{
    "token": "your-auth-token"
}
```

3. User Logout
```bash
POST /api/auth/logout/
Authorization: Token <your-token>

Response:
{
    "message": "Logged out successfully"
}
```

### Account Management

1. Create Account
```bash
POST /api/accounts/
Authorization: Token <your-token>
Content-Type: application/json

{
    "account_name": "Test Account",
    "website": "https://example.com"  # Optional
}

Response:
{
    "id": "uuid",
    "account_name": "Test Account",
    "app_secret_token": "generated-token",
    "website": "https://example.com",
    "created_at": "timestamp",
    "updated_at": "timestamp"
}
```

2. List Accounts
```bash
GET /api/accounts/
Authorization: Token <your-token>

Response:
[
    {
        "id": "uuid",
        "account_name": "Test Account",
        "app_secret_token": "token",
        "website": "https://example.com",
        "created_at": "timestamp",
        "updated_at": "timestamp"
    }
]
```

3. Get Account Details
```bash
GET /api/accounts/{id}/
Authorization: Token <your-token>

Response:
{
    "id": "uuid",
    "account_name": "Test Account",
    "app_secret_token": "token",
    "website": "https://example.com",
    "created_at": "timestamp",
    "updated_at": "timestamp"
}
```

4. Delete Account
```bash
DELETE /api/accounts/{id}/
Authorization: Token <your-token>

Response: 204 No Content
```

### Destination Management

1. Create Destination
```bash
POST /api/destinations/
Authorization: Token <your-token>
Content-Type: application/json

{
    "account": "account-uuid",
    "url": "https://example.com/webhook",
    "http_method": "POST",
    "headers": {
        "Custom-Header": "value"
    }
}

Response:
{
    "id": "uuid",
    "account": "account-uuid",
    "url": "https://example.com/webhook",
    "http_method": "POST",
    "headers": {
        "Custom-Header": "value"
    },
    "created_at": "timestamp",
    "updated_at": "timestamp"
}
```

2. List Destinations
```bash
GET /api/destinations/
Authorization: Token <your-token>

Response:
[
    {
        "id": "uuid",
        "account": "account-uuid",
        "url": "https://example.com/webhook",
        "http_method": "POST",
        "headers": {},
        "created_at": "timestamp",
        "updated_at": "timestamp"
    }
]
```

3. Get Destination Details
```bash
GET /api/destinations/{id}/
Authorization: Token <your-token>

Response:
{
    "id": "uuid",
    "account": "account-uuid",
    "url": "https://example.com/webhook",
    "http_method": "POST",
    "headers": {},
    "created_at": "timestamp",
    "updated_at": "timestamp"
}
```

4. Update Destination
```bash
PUT /api/destinations/{id}/
Authorization: Token <your-token>
Content-Type: application/json

{
    "url": "https://new-url.com/webhook",
    "http_method": "GET",
    "headers": {
        "New-Header": "value"
    }
}
```

5. Delete Destination
```bash
DELETE /api/destinations/{id}/
Authorization: Token <your-token>

Response: 204 No Content
```

### Account Members Management

1. Add Member to Account
```bash
POST /api/accounts/{account_id}/members/
Authorization: Token <your-token>
Content-Type: application/json

{
    "user": "user-id",
    "role": "role-id"
}

Response:
{
    "id": "uuid",
    "account": "account-id",
    "user": "user-id",
    "role": "role-id",
    "created_at": "timestamp",
    "updated_at": "timestamp"
}
```

2. List Account Members
```bash
GET /api/accounts/{account_id}/members/
Authorization: Token <your-token>

Response:
[
    {
        "id": "uuid",
        "account": "account-id",
        "user": {
            "id": "user-id",
            "email": "user@example.com"
        },
        "role": {
            "id": "role-id",
            "role_name": "Admin"
        }
    }
]
```

### Swagger Documentation
For interactive API documentation with request/response examples:
- Swagger UI: `http://localhost:8000/api/swagger/`
- ReDoc: `http://localhost:8000/api/redoc/`

## Running Tests

1. Run all tests
```bash
python manage.py test
```

2. Run tests with coverage
```bash
# Run tests and generate coverage data
python -m coverage run --source='.' manage.py test

# View coverage report in terminal
python -m coverage report

# Generate HTML coverage report
python -m coverage html
```

## Project Structure
```
datasync/
├── core/
│   ├── __init__.py
│   ├── admin.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views/
│       ├── __init__.py
│       ├── auth_views.py
│       └── api_views.py
├── datasync/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── requirements.txt
└── manage.py
```

## Development

### Making Changes
1. Create a new branch
```bash
git checkout -b feature/your-feature-name
```

2. Make your changes and run tests
```bash
python manage.py test
```

3. Check code coverage
```bash
python -m coverage run manage.py test
python -m coverage report
```

### Swagger Documentation
- Access the interactive API documentation at: `http://localhost:8000/api/swagger/`
- ReDoc alternative: `http://localhost:8000/api/redoc/`

## Troubleshooting

### Common Issues

1. Database migrations
```bash
# Reset migrations if needed
python manage.py migrate core zero
python manage.py makemigrations
python manage.py migrate
```

2. Redis/Memurai connection issues
- Check if Redis/Memurai is running
- Verify connection settings in settings.py
- Test connection using redis-cli or Memurai CLI

