# Order Service

The **Order Service** is responsible for **order creation and management** in the e-commerce microservices system.

It coordinates between **authenticated users** and **product inventory**, while maintaining strict service boundaries.

This service **does not manage users** and **does not manage products**.

---

## Responsibilities

The Order Service is responsible for:

* Creating orders for authenticated users
* Validating product availability via Catalog Service
* Reserving (deducting) product stock atomically
* Calculating order totals server-side
* Persisting orders and order items
* Exposing order APIs behind the API Gateway

It is **not** responsible for:

* User authentication or identity storage
* Product creation or inventory ownership
* Payment processing (Phase 1)
* Notifications (Phase 1)

---

## Architecture Position

```
Client
  ↓
API Gateway (NGINX)
  ↓
Order Service
   ├── JWT validation (stateless)
   └── Sync calls to Catalog Service
```

All external traffic enters through the **API Gateway**.
Order Service is **never accessed directly**.

---

## Tech Stack

* Python 3.11
* Django
* Django REST Framework
* SimpleJWT (stateless authentication)
* SQLite (Phase 1, persisted via Docker volume)
* Docker

---

## Authentication Model

### Stateless JWT Authentication

Order Service uses **stateless JWT authentication**.

* JWTs are issued by **Auth Service**
* Order Service validates tokens locally
* No user database lookups are performed
* `request.user.id` is derived from the token

This ensures:

* No shared user database
* No tight coupling with Auth Service

---

## Data Model

### Order

```text
Order
├── id
├── user_id
├── total_amount
├── status (CREATED, PAID, CANCELLED)
└── created_at
```

### OrderItem

```text
OrderItem
├── id
├── order_id
├── product_id
├── quantity
└── price (snapshotted at order time)
```

Key design decisions:

* `user_id` is stored as an integer from JWT
* `product_id` is an external reference
* Product price is **snapshotted** to prevent price drift

---

## Cross-Service Interaction

### Catalog Service Integration

Order Service communicates with Catalog Service to:

1. Validate product existence
2. Retrieve product price
3. Reserve (deduct) product stock

Order Service **never updates product data directly**.

---

## API Endpoints

All endpoints are exposed **via the API Gateway**.

Base path:

```
/orders/
```

---

### Health Check

```
GET /orders/health/
```

Response:

```json
{
  "status": "order-service-up"
}
```

---

### Create Order (JWT Required)

```
POST /orders/orders/
```

Headers:

```
Authorization: Bearer <ACCESS_TOKEN>
Content-Type: application/json
```

Body:

```json
{
  "items": [
    { "product_id": 1, "quantity": 2 }
  ]
}
```

Processing steps:

1. Validate JWT
2. Validate product existence
3. Reserve stock in Catalog Service
4. Calculate total amount
5. Persist order and items

Response:

```json
{
  "id": 1,
  "total_amount": "1999.98",
  "status": "CREATED",
  "created_at": "2026-01-16T13:45:00Z"
}
```

---

## Error Scenarios

| Scenario           | Response             |
| ------------------ | -------------------- |
| Product not found  | `400 Bad Request`  |
| Insufficient stock | `409 Conflict`     |
| Missing JWT        | `401 Unauthorized` |
| Invalid request    | `400 Bad Request`  |

---

## Stock Consistency Strategy (Phase 1)

* Stock deduction is performed by **Catalog Service**
* Order Service requests stock reservation synchronously
* Database-level locking prevents race conditions
* No shared database access

This guarantees:

* Stock never goes negative
* Service ownership is preserved

---

## Docker & Persistence

### Database Persistence

* SQLite database is persisted using Docker volumes
* Data survives container restarts
* Database path:

  ```
  /app/data/db.sqlite3
  ```

---

### Running Migrations

```bash
docker-compose exec order-service python manage.py migrate
```

---

## Design Principles

* One service → one responsibility
* Stateless authentication
* No shared databases
* No trust in client-provided values
* Explicit cross-service contracts

---

## Phase 1 Status

✅ Order creation implemented
✅ JWT authentication enforced
✅ Cross-service stock deduction
✅ Database persistence
✅ API Gateway integration

Order listing, payment handling, and async workflows are **intentionally deferred**.

---

## Next Phase

Planned enhancements:

* List orders by user
* Order status transitions
* Payment service integration
* Event-driven notifications
* Idempotent order creation

These will be implemented incrementally.

---
