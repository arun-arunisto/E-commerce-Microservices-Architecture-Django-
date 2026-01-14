# Auth Service

The **Auth Service** is responsible for **authentication and identity management** in the e-commerce microservices system.

It issues and validates **JWT tokens** that are trusted by all other services (Catalog, Order, Payment, Notification).

This service is **self-contained**, **Dockerized**, and **does not share its database** with any other service.

---

## Responsibilities

The Auth Service is responsible for:

* User authentication using email & password
* Issuing JWT access and refresh tokens
* Validating JWT for protected endpoints
* Providing a health check endpoint
* Acting as the single source of truth for identity

It is **not** responsible for:

* Business logic (orders, products, payments)
* User profile management (beyond identity)
* Authorization rules of other services

---

## Architecture Overview

```
Client
  ↓
API Gateway (NGINX)
  ↓
Auth Service (Django + DRF + JWT)
```

* Public traffic never reaches the service directly
* All requests are routed through the API Gateway
* Other services validate JWT locally (no sync calls to Auth)

---

## Tech Stack

* Python 3.11
* Django
* Django REST Framework
* SimpleJWT
* Gunicorn
* Docker

---

## Authentication Model

### Custom User Model

This service uses a **custom Django user model**, not the default `auth_user` table.

Key characteristics:

* Email-based authentication
* Secure password hashing via Django
* Fully compatible with Django auth framework
* JWT tokens are issued against this custom table

This allows full control over the user schema without re-implementing security.

---

## API Endpoints

All endpoints are exposed **via the API Gateway**.

### Health Check

```
GET /auth/health/
```

Response:

```json
{
  "status": "auth-service-up"
}
```

---

### Obtain JWT Token

```
POST /auth/token/
```

Request:

```json
{
  "email": "user@example.com",
  "password": "password"
}
```

Response:

```json
{
  "access": "<jwt_access_token>",
  "refresh": "<jwt_refresh_token>"
}
```

---

### Refresh JWT Token

```
POST /auth/token/refresh/
```

Request:

```json
{
  "refresh": "<jwt_refresh_token>"
}
```

Response:

```json
{
  "access": "<new_access_token>"
}
```

---

### Protected Example Endpoint

```
GET /auth/me/
```

Headers:

```
Authorization: Bearer <access_token>
```

Response:

```json
{
  "id": 1,
  "email": "user@example.com"
}
```

---

## Docker Setup

### Dockerfile

The service runs using **Gunicorn**, not Django’s development server.

* Gunicorn binds to an internal service port
* Static files are not served (API-only service)
* Logs are written to stdout (Docker-friendly)

---

### Running Locally

From the project root:

```bash
docker-compose up --build auth-service
```

---

### Running Migrations

```bash
docker-compose exec auth-service python manage.py migrate
```

---

### Creating a User (Initial Setup)

```bash
docker-compose exec auth-service python manage.py createsuperuser
```

This user can be used to obtain JWT tokens for testing other services.

---

## Security Notes

* JWT tokens are signed using the service `SECRET_KEY`
* All downstream services must share the same JWT signing secret
* Passwords are never stored in plain text
* Authentication logic is not duplicated in other services

---

## Development Principles

* One service → one responsibility
* No shared databases
* Stateless authentication (JWT)
* API-first design
* Infrastructure concerns handled via Docker & Gateway

---

## Status

✅ Auth Service is **complete for Phase 1**
Future enhancements (roles, permissions, signup flows) will be added **only when required by downstream services**.
