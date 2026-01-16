# 🛒 E-Commerce Microservices (Django + Docker)

A **production-oriented e-commerce backend** built using **Django** and **Django REST Framework**, following **true microservices architecture principles**.

Each service is:

* Independently deployable
* Owns its own database
* Isolated behind an API Gateway
* Authenticated using **stateless JWT**

This project focuses on **correct architecture, service isolation, and real-world failure handling**, not shortcuts.

---

## 📌 Purpose of This Project

Most “microservices” examples online:

* Share databases ❌
* Depend on Django’s monolith assumptions ❌
* Skip real auth boundaries ❌

This repository exists to demonstrate:

* Proper service boundaries
* Centralized authentication with distributed trust
* Stateless JWT in microservices
* Dockerized services that survive restarts
* How things actually break and how to fix them

---

## 🧱 Architecture Overview

### Core Services

| Service                  | Responsibility                  |
| ------------------------ | ------------------------------- |
| **Auth Service**         | User authentication, JWT tokens |
| **Catalog Service**      | Product catalog & pricing       |
| **Order Service**        | Order creation & lifecycle      |
| **Payment Service**      | Payment processing              |
| **Notification Service** | Email/SMS notifications (async) |
| **API Gateway**          | Single public entry point       |

---

All external traffic flows through the **API Gateway**.
Internal services are **never accessed directly**.

---

## 🧩 Services (What Exists Today)

### 🔐 Auth Service

Responsible for **authentication and identity**.

* Custom Django user model
* Email/password authentication
* Issues JWT access & refresh tokens
* Single source of truth for identity

📁 `auth-service/`
📄 `auth-service/README.md`

---

### 🛒 Catalog Service

Responsible for **product management**.

* Product CRUD APIs
* Public read endpoints
* JWT-protected write endpoints
* Stateless JWT validation (no user DB access)

📁 `catalog-service/`
📄 `catalog-service/README.md`

---

### 📦 Order Service

Responsible for **order management (Phase 1 bootstrap)**.

* Independent Django service
* Health check endpoint implemented
* Service isolation validated
* No business logic yet (by design)

📁 `order-service/`

---

### 💳 Payment Service

Responsible for **payment processing (Phase 1 bootstrap)**.

* Independent Django service
* Health check endpoint implemented
* No payment provider integration yet
* Exists to validate service lifecycle & routing

📁 `payment-service/`

---

### 🔔 Notification Service

Responsible for **notifications (Phase 1 bootstrap)**.

* Independent Django service
* Health check endpoint implemented
* Future home for email / SMS / async events

📁 `notification-service/`

---

### 🌐 API Gateway

Single public entry point for all services.

* NGINX reverse proxy
* Path-based routing:

  * `/auth/`
  * `/catalog/`
  * `/orders/`
  * `/payments/`
  * `/notifications/`
* No business logic
* No authentication logic

📁 `api-gateway/`

---

## 🔐 Authentication Model

* **Auth Service** issues JWTs
* All other services validate JWT **statelessly**
* No service (except Auth) touches user tables
* Trust is established via a shared signing secret

This prevents:

* Shared databases
* User duplication
* Tight coupling

---

## 🗂 Repository Structure (Updated)

```
ecommerce-microservices/
├── api-gateway/
│   └── nginx/
│       └── nginx.conf
│
├── auth-service/
│   ├── app/
│   ├── Dockerfile
│   └── README.md
│
├── catalog-service/
│   ├── app/
│   ├── Dockerfile
│   └── README.md
│
├── order-service/
│   ├── app/
│   ├── README.md
│   └── Dockerfile
│
├── payment-service/
│   ├── app/
│   ├── README.md
│   └── Dockerfile
│
├── notification-service/
│   ├── app/
│   ├── README.md
│   └── Dockerfile
│
├── docker-compose.yml
└── README.md
```

Each service:

* Is a **separate Django project**
* Has its **own database**
* Can be started, stopped, or rebuilt independently

---

## 🛠 Tech Stack (Current)

| Layer      | Technology                                  |
| ---------- | ------------------------------------------- |
| Backend    | Django, Django REST Framework               |
| Auth       | SimpleJWT (stateless)                       |
| Gateway    | NGINX                                       |
| Containers | Docker, Docker Compose                      |
| Database   | SQLite (per service, persisted via volumes) |

---

## 🧪 Running the System

```bash
docker-compose up --build
```

All APIs are accessed **only via the API Gateway**.

Stopping services:

```bash
docker-compose down
```

Removing all persisted data (destructive):

```bash
docker-compose down -v
```

---

## 🩺 Health Checks

Each service exposes a health endpoint to validate:

* Service startup
* Routing via gateway
* Independent lifecycle

Example:

```
GET /catalog/health/
GET /orders/health/
GET /payments/health/
GET /notifications/health/
```

---

## 🧠 Design Principles

This project enforces:

* One service → one responsibility
* Stateless authentication
* Explicit configuration
* No shared databases
* Incremental complexity

---

## 🚧 What’s Next (Planned)

The following **will be implemented next**, not yet:

* Order business logic
* Product-to-order validation
* Payment workflows
* Event-driven notifications
* PostgreSQL per service
* Observability & metrics

---

## ⚠️ Honest Disclaimer

This architecture is **intentionally not beginner-friendly**.

* ❌ Not an MVP template
* ❌ Not a CRUD tutorial
* ✅ A serious learning project
* ✅ Suitable for backend architecture interviews
* ✅ Suitable for senior-level discussion

---

## 👤 Author

**Arun Arunisto**

Senior Python Engineer

Focus: Backend Architecture, Django, Distributed Systems
