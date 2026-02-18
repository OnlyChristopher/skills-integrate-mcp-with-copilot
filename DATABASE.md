# Database Setup Guide

This document explains how to set up and use the database for the Mergington High School Management System.

## Overview

The application now uses **SQLAlchemy** ORM for database persistence, replacing the previous in-memory storage. This means:
- ✅ Data persists across server restarts
- ✅ Support for multiple database backends (SQLite, PostgreSQL, MySQL)
- ✅ Database migrations with Alembic
- ✅ Better scalability and concurrent access

## Quick Start (Development)

For local development, the application uses SQLite by default (no configuration needed):

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Seed the database with initial data
cd src
python seed_data.py

# 3. Run the application
uvicorn app:app --reload
```

The SQLite database will be created automatically at `mergington_school.db`.

## Database Configuration

### Environment Variables

Create a `.env` file in the project root (copy from `.env.example`):

```bash
cp .env.example .env
```

### SQLite (Default - Development)

No configuration needed! The application will use SQLite by default:

```env
DATABASE_URL=sqlite:///./mergington_school.db
```

### PostgreSQL (Recommended for Production)

1. Install PostgreSQL
2. Create a database:
   ```sql
   CREATE DATABASE mergington_school;
   ```
3. Update `.env`:
   ```env
   DATABASE_URL=postgresql://username:password@localhost:5432/mergington_school
   ```

### MySQL/MariaDB

1. Install MySQL/MariaDB
2. Create a database:
   ```sql
   CREATE DATABASE mergington_school;
   ```
3. Install additional dependency:
   ```bash
   pip install pymysql
   ```
4. Update `.env`:
   ```env
   DATABASE_URL=mysql+pymysql://username:password@localhost:3306/mergington_school
   ```

## Database Schema

### Tables

#### `activities`
- `id` (Primary Key)
- `name` (Unique)
- `description`
- `schedule`
- `max_participants`

#### `participants`
- `id` (Primary Key)
- `email` (Unique)

#### `activity_participants` (Association Table)
- `activity_id` (Foreign Key → activities.id)
- `participant_id` (Foreign Key → participants.id)

## Database Migrations with Alembic

### Initialize Database

```bash
# Create tables
python -m alembic upgrade head
```

### Create a New Migration

When you modify the models:

```bash
# Auto-generate migration
python -m alembic revision --autogenerate -m "Description of changes"

# Apply migration
python -m alembic upgrade head
```

### Migration Commands

```bash
# View current version
python -m alembic current

# View migration history
python -m alembic history

# Downgrade one version
python -m alembic downgrade -1

# Downgrade to base (empty database)
python -m alembic downgrade base
```

## Seeding the Database

To populate the database with initial activity data:

```bash
cd src
python seed_data.py
```

This will:
- Create all necessary tables
- Add 9 default activities (Chess Club, Programming Class, etc.)
- Add initial participants for each activity

**Note:** The seed script will skip if activities already exist.

## Database Management

### Viewing Data

For SQLite:
```bash
sqlite3 mergington_school.db
# Then run SQL queries like:
# SELECT * FROM activities;
# SELECT * FROM participants;
```

For PostgreSQL:
```bash
psql mergington_school
# Then run SQL queries
```

### Resetting the Database

To start fresh:

```bash
# For SQLite
rm mergington_school.db
python -m alembic upgrade head
cd src && python seed_data.py

# For PostgreSQL/MySQL
# Drop and recreate database, then:
python -m alembic upgrade head
cd src && python seed_data.py
```

## API Endpoints

The API endpoints remain the same:

- `GET /activities` - Get all activities
- `POST /activities/{activity_name}/signup?email=student@email.com` - Sign up
- `DELETE /activities/{activity_name}/unregister?email=student@email.com` - Unregister

## Troubleshooting

### "No module named 'src'"

Make sure you're running commands from the project root, not from within `src/`:

```bash
# Wrong
cd src
uvicorn app:app

# Correct
uvicorn src.app:app
```

### Database Connection Errors

1. Check your `.env` file has correct credentials
2. Verify database server is running
3. Ensure database exists
4. Check firewall/network settings

### Migration Conflicts

If you get Alembic conflicts:

```bash
# Check status
python -m alembic current

# If needed, stamp the current version
python -m alembic stamp head
```

## Production Deployment

### Recommendations

1. **Use PostgreSQL** for production (better concurrency, reliability)
2. **Set environment variables** via your hosting platform (don't commit `.env`)
3. **Run migrations** as part of deployment:
   ```bash
   python -m alembic upgrade head
   ```
4. **Connection Pooling**: Already configured in `database.py`
5. **Backups**: Set up regular database backups
6. **Monitoring**: Monitor database performance and connections

### Example Production Setup

```bash
# Set environment variable
export DATABASE_URL="postgresql://user:pass@db.example.com:5432/prod_db"

# Run migrations
python -m alembic upgrade head

# Start application
uvicorn src.app:app --host 0.0.0.0 --port 8000 --workers 4
```

## Next Steps

This database implementation is foundational for future features:
- ✅ Issue #18 - Database Persistence (✓ COMPLETED)
- → Issue #19 - User Authentication (requires database)
- → Issue #17 - User Profiles (requires database)
- → Issue #8 - Results & Scoring (requires database)

See the [project issues](https://github.com/OnlyChristopher/skills-integrate-mcp-with-copilot/issues) for the full feature roadmap.
