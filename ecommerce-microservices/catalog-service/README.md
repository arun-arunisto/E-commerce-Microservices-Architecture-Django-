# Catalog Service

The **Catalog Service** is responsible for managing **product data** in the e-commerce microservices system.

It exposes **read-only public APIs** and **JWT-protected write APIs**, and operates as a fully **independent microservice** behind an API Gateway.

This service **does not manage users** and **does not connect to the Auth Service database**.

---

## Responsibilities

The Catalog Service is responsible for:

* Creating products (authenticated)
* Updating products (authenticated)
* Deleting products (authenticated)
* Listing products (public)
* Retrieving product details (public)
* Persisting product data independently

It is **not** responsible for:

* User management
* Authentication logic
* Authorization rules beyond JWT validation
* Orders, payments, or inventory workflows

---

## Architecture Position

```
Client
  ↓
API Gateway (NGINX)
  ↓
Catalog Service (Django + DRF)
```

* All external traffic goes through the **API Gateway**
* Catalog Service is **not directly exposed**
* JWT is validated **locally and statelessly**

---

## Tech Stack

* Python 3.11
* Django
* Django REST Framework
* SimpleJWT (stateless mode)
* SQLite (Phase 1)
* Docker

---

## Authentication Strategy (Important)

### Stateless JWT Validation

Catalog Service uses **stateless JWT authentication**.

* JWTs are **issued by Auth Service**
* Catalog Service **verifies signature and expiry only**
* No user lookup is performed
* No user table is queried for authentication

### Why Stateless?

This ensures:

* No coupling to Auth Service database
* No duplicated user data
* Clean microservice boundaries

---

## JWT Configuration

Catalog Service uses:

```python
JWTStatelessUserAuthentication
```

This means:

* `request.user` is derived from the token
* No database lookup is performed
* Only the token payload is trusted

---

## Data Model

### Product

```text
Product
├── id
├── name
├── description
├── price
├── is_active
├── in_stock
├── created_at
└── updated_at
```

---

## API Endpoints

All endpoints are accessed **via the API Gateway**.

Base path:

```
/catalog/
```

---

### Health Check

```
GET /catalog/health/
```

Response:

```json
{
  "status": "catalog-service-up"
}
```

---

### List Products (Public)

```
GET /catalog/products/
```

Response:

```json
[
  {
    "id": 1,
    "name": "Phone",
    "description": "Flagship",
    "price": "999.99",
    "is_active": true,
    "created_at": "2026-01-16T12:30:00Z"
  }
]
```

---

### Retrieve Product (Public)

```
GET /catalog/products/{id}/
```

---

### Create Product (JWT Required)

```
POST /catalog/products/
```

Headers:

```
Authorization: Bearer <ACCESS_TOKEN>
Content-Type: application/json
```

Body:

```json
{
  "name": "Phone",
  "description": "Flagship",
  "price": "999.99"
}
```

Response:

```json
{
  "id": 1,
  "name": "Phone",
  "description": "Flagship",
  "price": "999.99",
  "is_active": true,
  "created_at": "2026-01-16T12:30:00Z"
}
```

---

### Update Product (JWT Required)

```
PUT /catalog/products/{id}/
```

---

### Delete Product (JWT Required)

```
DELETE /catalog/products/{id}/
```

---

## Docker & Persistence

### Database Persistence

* SQLite database is persisted using a **Docker volume**
* Data survives container restarts and rebuilds

Database path inside container:

```
/app/data/db.sqlite3
```

---

### Running Migrations

```bash
docker-compose exec catalog-service python manage.py migrate
```

---

## Service Isolation Rules

* Catalog Service **never queries user data**
* Catalog Service **never calls Auth Service**
* Authentication is **token-based only**
* Database is **owned exclusively by this service**

---

## Common Failure Modes (Already Solved)

| Issue                       | Solution                  |
| --------------------------- | ------------------------- |
| JWT invalid across services | Shared `SECRET_KEY`     |
| User lookup errors          | Stateless JWT auth        |
| DB lost on restart          | Docker volume             |
| Reverse proxy host errors   | Correct `ALLOWED_HOSTS` |
| Direct port access          | Gateway-only routing      |

---

## Phase 1 Status

✅ Product CRUD implemented
✅ Stateless JWT authentication
✅ API Gateway integration
✅ Database persistence
✅ Production-safe service boundaries

This service is **complete for Phase 1**.
