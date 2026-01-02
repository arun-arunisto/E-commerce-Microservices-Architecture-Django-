# 🛒 E-Commerce Microservices Architecture (Django)

![Image](https://miro.medium.com/0%2AxuHRipbS0io0EYVl.png)

![Image](https://i.imgur.com/sZZgEwq.jpg)

![Image](https://hazelcast.com/wp-content/uploads/2024/04/glossary-eda.svg)

A **production-style e-commerce backend** built using **Django** and **Django REST Framework**, following **true microservices architecture principles**.

This project demonstrates:

* Clear service boundaries
* Independent deployments
* Event-driven communication
* API Gateway pattern
* No shared databases

> ⚠️ This is **not** a distributed monolith. Each service is isolated by design.

---

## 📌 Why This Project?

Most “microservices” demos:

* Share a database ❌
* Live inside one Django project ❌
* Use sync calls for everything ❌

This project exists to show **how microservices should actually be designed**, even at a small scale.

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

## 🔄 Communication Model

### Synchronous (HTTP)

* Token validation
* Product price checks

### Asynchronous (Events)

* Order creation
* Payment confirmation
* Notifications

Event-driven communication is handled via **RabbitMQ**.

---

## 🗂 Repository Structure

```
ecommerce-microservices/
├── api-gateway/
│   └── nginx.conf
│
├── auth-service/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── auth_service/
│
├── catalog-service/
│   ├── Dockerfile
│   └── catalog_service/
│
├── order-service/
│   ├── Dockerfile
│   └── order_service/
│
├── payment-service/
│   ├── Dockerfile
│   └── payment_service/
│
├── notification-service/
│   ├── Dockerfile
│   └── notification_service/
│
├── docker-compose.yml
└── README.md
```

Each service:

* Is a **separate Django project**
* Has its **own database**
* Can be deployed **independently**

---

## 🛠 Tech Stack

| Layer         | Technology                    |
| ------------- | ----------------------------- |
| Backend       | Django, Django REST Framework |
| Database      | PostgreSQL (per service)      |
| Messaging     | RabbitMQ                      |
| API Gateway   | NGINX                         |
| Containers    | Docker                        |
| Orchestration | Kubernetes (planned)          |

---

## 📦 Order Flow (Example)

```
Client
  ↓
API Gateway
  ↓
Order Service
  ├─ validates JWT (Auth Service)
  ├─ validates product (Catalog Service)
  └─ creates order (PENDING)
          ↓
     OrderCreated Event
          ↓
     Payment Service
          ↓
   PaymentSuccess Event
          ↓
     Order Service (CONFIRMED)
          ↓
 Notification Service
```

This flow avoids tight coupling and allows services to fail independently.

---

## 🧪 Local Development (Docker)

```bash
git clone https://github.com/your-username/ecommerce-microservices.git
cd ecommerce-microservices
docker-compose up --build
```

Services will be available via the API Gateway:

```
/auth/*
/catalog/*
/orders/*
/payments/*
```

---

## 🔐 Security Model

* JWT issued by Auth Service
* Gateway routes requests
* Services trust gateway
* No public DB access
* No shared secrets

---

## 🚀 Future Enhancements

* Kubernetes deployment
* Centralized logging
* Distributed tracing
* CI/CD pipelines
* Rate limiting at the gateway
* Circuit breakers

---

## 🎯 Learning Outcomes

By building this project, you will understand:

* Why microservices are expensive
* How async workflows work
* Event-driven system design
* Service isolation & ownership
* Real-world backend architecture

---

## ⚠️ Disclaimer (Honest One)

This architecture is **intentionally complex**.
If you’re building a startup MVP — **don’t use this**.
This project is for **learning, architecture practice, and senior-level interviews**.

---

## 👤 Author

**Arun Arunisto**
Senior Python Engineer
Focus: Backend Architecture, Django, Distributed Systems
