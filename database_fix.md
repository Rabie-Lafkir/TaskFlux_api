# TaskFlux - Database Fixes and Setup Notes

This file documents all the steps and fixes applied on the PostgreSQL database for TaskFlux.

---

## 1. Create the database and user

```sql
CREATE DATABASE taskflux;
CREATE USER taskflux_user WITH PASSWORD 'supersecret';
GRANT ALL PRIVILEGES ON DATABASE taskflux TO taskflux_user;
````

---

## 2. Connect to taskflux database

```sql
CREATE DATABASE taskflux;
CREATE USER taskflux_user WITH PASSWORD 'supersecret';
GRANT ALL PRIVILEGES ON DATABASE taskflux TO taskflux_user;
```

---

## 3. Create the tables

```sql
-- users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    profile_pic VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- projects table
CREATE TABLE projects (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    start_date DATE,
    end_date DATE,
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- tasks table
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    due_date DATE,
    status VARCHAR(20) DEFAULT 'pending',
    priority VARCHAR(20) DEFAULT 'medium',
    completed_at TIMESTAMP,
    project_id INTEGER REFERENCES projects(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 4. Grant table privileges

```sql
GRANT ALL PRIVILEGES ON TABLE users TO taskflux_user;
GRANT ALL PRIVILEGES ON TABLE projects TO taskflux_user;
GRANT ALL PRIVILEGES ON TABLE tasks TO taskflux_user;
```

---

## 5. Grant privileges on sequences (for SERIAL columns)

```sql
GRANT USAGE, SELECT ON SEQUENCE users_id_seq TO taskflux_user;
GRANT USAGE, SELECT ON SEQUENCE projects_id_seq TO taskflux_user;
GRANT USAGE, SELECT ON SEQUENCE tasks_id_seq TO taskflux_user;
```

---

## 6. Optional - allow default privileges for future tables/sequences

```sql
ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT ALL ON TABLES TO taskflux_user;

ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT USAGE, SELECT ON SEQUENCES TO taskflux_user;
```

---

## 7. .env configuration

```env
DB_HOST=localhost
DB_NAME=taskflux
DB_USER=taskflux_user
DB_PASSWORD=supersecret
DB_PORT=5432
FLASK_SECRET_KEY=supersecretkey
```

---

## 8. Troubleshooting log

* Fixed `permission denied for table users` by granting table privileges
* Fixed `permission denied for sequence users_id_seq` by granting sequence usage
* Fixed `connection pool closed` by avoiding early shutdown from exceptions
* Fixed `ModuleNotFoundError: bcrypt` by installing missing package

---

## 9. How to connect with pgAdmin

* connect as `postgres`
* manage roles and databases visually
* connect to `taskflux` as `taskflux_user` for testing

---

---

## 10. Project table privileges

When testing the `projects` CRUD, the following privileges were required:

```sql
GRANT ALL PRIVILEGES ON TABLE projects TO taskflux_user;
GRANT USAGE, SELECT ON SEQUENCE projects_id_seq TO taskflux_user;




