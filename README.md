# TaskFlux API

TaskFlux is a modern, container‑ready backend service for task and project management.  
It is built with **Flask** (Python 3.12) and **PostgreSQL**, packaged with **Docker Compose** for an effortless setup in any environment.

---

## 🌟 Key Features

- **RESTful API** organised with Flask Blueprints  
- **JWT authentication** with secure password hashing (bcrypt)  
- **Pydantic v2** request/response validation  
- **PostgreSQL 17** database with a named volume for persistent data  
- **Dockerised development workflow** – one command to build & run  
- Ready for future **React + TypeScript (Vite) frontend** integration  

---

## 📁 Project Structure

```
TaskFlux_api/
├── app/                    # Main application package
│   ├── api/
│   │   ├── routes/         # Blueprints: users, projects, tasks
│   │   ├── schemas/        # Pydantic models
│   │   └── utils/          # JWT helpers, error handlers
│   ├── __init__.py         # App factory
│   └── ...
├── Dockerfile              # Multi‑stage build (python:3.12‑slim)
├── docker-compose.yml      # web + db services
├── requirements.txt
├── run.py                  # Entry‑point for `flask run`
└── .env.example            # Environment variable template
```

---

## ⚙️ Requirements

| Tool | Minimum Version |
|------|-----------------|
| Docker | 24 + |
| Docker Compose | bundled with Docker Desktop ≥ 2.20 |
| (Optional) Python | 3.12 for local execution |

---

## 🚀 Quick Start

1. **Clone the repo**

```bash
git clone https://github.com/Rabie-Lafkir/TaskFlux_api.git
cd TaskFlux_api
```

2. **Configure secrets**

```bash
cp .env.example .env
# edit .env and fill in strong passwords / keys
```

3. **Build & run the stack**

```bash
docker compose up --build -d
```

> On first run, the Flask image is built; afterwards `docker compose up -d` is instant.  
> The API is available at **http://localhost:5000**.

4. **Stop / reset**

```bash
docker compose down          # stop containers (keeps DB volume)
docker compose down -v --rmi all   # stop & remove everything
```

---

## 🌐 Environment Variables

| Variable | Description | Default (dev) |
|----------|-------------|---------------|
| `DB_HOST` | Database host (service name) | `db` |
| `DB_PORT` | Database port | `5432` |
| `DB_NAME` | PostgreSQL database | `taskflux` |
| `DB_USER` | DB user | `taskflux_user` |
| `DB_PASSWORD` | DB user password | `taskflux2025` |
| `FLASK_SECRET_KEY` | Flask/JWT secret key | _secret key_ |


---

## 🛣️ API Reference (v 1)

All routes are prefixed with **`/api`**.  
Authentication uses the `Authorization: Bearer <token>` header.

### Users

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/users/register` | Create a new account |
| POST | `/users/login` | Authenticate & receive JWT |
| GET | `/users/<id>` | Get user profile (auth) |
| PUT | `/users/<id>` | Update profile (auth) |
| DELETE | `/users/<id>` | Delete account (auth) |

### Projects

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/projects` | Create project |
| GET | `/projects/<id>` | Get single project |
| GET | `/projects/user/<user_id>` | List a user’s projects |
| PUT | `/projects/<id>` | Update project |
| DELETE | `/projects/<id>` | Delete project |

### Tasks

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/tasks` | Create task |
| GET | `/tasks/<id>` | Get single task |
| GET | `/tasks/project/<project_id>` | List tasks in project |
| PUT | `/tasks/<id>` | Update task |
| DELETE | `/tasks/<id>` | Delete task |

---

## 🗄️ Database Management

This repo currently ships with raw SQL in **`database_fix.md`** for the initial schema.  
You can migrate to **Flask‑Migrate (Alembic)** by running:

```bash
docker compose exec web flask db init      # once
docker compose exec web flask db migrate -m "initial"
docker compose exec web flask db upgrade
```

---

## 🧪 Testing

Planned:

```bash
pytest
```

A separate `docker-compose.test.yml` will spin up a disposable database for integration tests.

---

## 📈 Roadmap

- [x] Dockerised Flask + Postgres stack  
- [x] JWT‑secured CRUD for Users / Projects / Tasks  
- [ ] Automatic migrations with Alembic  
- [ ] CI workflow (lint → test → build → push image)  
- [ ] Swagger / OpenAPI docs  
- [ ] Vite + React TS front‑end  
- [ ] Seed & fixtures for demo data  

---

## 🤝 Contributing

1. Fork the repo & create a branch from `dev`.  
2. Install *pre‑commit* and run `pre-commit install`.  
3. Write tests for your feature or fix.  
4. Open a pull request with a clear description.

We appreciate small, focused PRs!

---

## 🪪 License

This project is released under the MIT License — see `LICENSE` for details.

---

Happy coding! 🎉
