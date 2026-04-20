Homework assignment on **SQLAlchemy ORM + PostgreSQL**.

## Description

This project implements a university database with the following entities:

- Students
- Groups
- Teachers
- Subjects
- Grades

The project includes:

- SQLAlchemy ORM models
- database seeding with Faker
- database queries using SQLAlchemy Session
- an interactive console menu for CRUD operations

## Technologies

- Python 3
- PostgreSQL
- Docker Compose
- SQLAlchemy
- Faker
- python-dotenv
- tabulate

## Run PostgreSQL in Docker

```bash
docker compose up -d
```

## Create a .env file:

```bash
DB_USER=Admin
DB_PASSWORD=Password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=university_db
```

## Install Dependencies

```bash
poetry install
```

## Run

- Seed the database:

```bash
python seed.py
```

- Run the queries:

```bash
python my_select.py
```

- Run the interactive menu:

```bash
python main.py --menu
```
