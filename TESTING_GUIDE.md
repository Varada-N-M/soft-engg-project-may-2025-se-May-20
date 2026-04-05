# GrowWise Backend - Database Migration Testing Guide

## Quick Start

### Using Docker Compose (Recommended for PostgreSQL testing)

```bash
# Start all services
docker-compose up -d

# Initialize database with seed data
docker exec -it growwise_backend bash
python migrate.py

# Backend is now running on http://localhost:5000
# Frontend is now running on http://localhost:3000
```

### Using Local SQLite (No Setup Required)

```bash
cd backend
pip install -r requirements.txt
python run.py

# Backend now running on http://localhost:5000
# Database is SQLite at backend/database.db
```

---

## Verification Tests

### 1. Test Authentication Flow

```bash
# Test Admin Registration
curl -X POST http://localhost:5000/api/admin/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@test.com",
    "password": "Test123456",
    "first_name": "Admin",
    "last_name": "User"
  }'

# Test Child Registration
curl -X POST http://localhost:5000/api/child/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "child@test.com",
    "password": "Test123456",
    "first_name": "Child",
    "last_name": "User",
    "dob": "2015-05-20",
    "class": 5,
    "school_name": "Test School",
    "gender": "Male"
  }'

# Test Login
curl -X POST http://localhost:5000/api/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "child@test.com",
    "password": "Test123456"
  }'
```

### 2. Test CRUD Operations

#### Create Habit

```bash
# First get a valid token from login response
TOKEN="your_access_token_here"

curl -X POST http://localhost:5000/api/child/habit \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Morning Exercise",
    "description": "30 minutes of exercise",
    "category": "Health",
    "habit_xp": 25
  }'
```

#### Read Habits

```bash
curl -X GET http://localhost:5000/api/child/habit \
  -H "Authorization: Bearer $TOKEN"
```

#### Update Habit

```bash
curl -X PUT http://localhost:5000/api/child/habit/1 \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Morning Exercise Updated",
    "description": "45 minutes of exercise",
    "category": "Health",
    "habit_xp": 30
  }'
```

#### Delete Habit

```bash
curl -X DELETE http://localhost:5000/api/child/habit/1 \
  -H "Authorization: Bearer $TOKEN"
```

### 3. Test Gratitude Entries

```bash
# Create Gratitude Entry
curl -X POST http://localhost:5000/api/child/gratitude \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "gratitude_text": "I am grateful for my family"
  }'

# Get Gratitude Entries
curl -X GET http://localhost:5000/api/child/gratitude \
  -H "Authorization: Bearer $TOKEN"

# Get Entries from Specific Date
curl -X GET "http://localhost:5000/api/child/gratitude?date=05-04-25" \
  -H "Authorization: Bearer $TOKEN"

# Get Entries from Last N Days
curl -X GET "http://localhost:5000/api/child/gratitude?days=7" \
  -H "Authorization: Bearer $TOKEN"
```

### 4. Test Todo Lists

```bash
# Create Todo
curl -X POST http://localhost:5000/api/child/todo \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "to_do": "Complete homework",
    "description": "Math and Science homework",
    "is_daily": false
  }'

# Get Todos
curl -X GET http://localhost:5000/api/child/todo \
  -H "Authorization: Bearer $TOKEN"

# Update Todo
curl -X PUT http://localhost:5000/api/child/todo/1 \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "to_do": "Complete homework updated",
    "is_done": true
  }'

# Delete Todo
curl -X DELETE http://localhost:5000/api/child/todo/1 \
  -H "Authorization: Bearer $TOKEN"
```

### 5. Test Skills

```bash
# Create Skill
curl -X POST http://localhost:5000/api/child/skill \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "skill_name": "Basic Math",
    "skill_type": "Academic",
    "video_url": "https://example.com/video",
    "skill_xp": 50
  }'

# Get Skills
curl -X GET http://localhost:5000/api/child/skills \
  -H "Authorization: Bearer $TOKEN"

# Complete Skill
curl -X POST http://localhost:5000/api/child/skill/1/complete \
  -H "Authorization: Bearer $TOKEN"
```

### 6. Test Badges

```bash
# Get Badges
curl -X GET http://localhost:5000/api/child/badges \
  -H "Authorization: Bearer $TOKEN"
```

---

## Database Inspection

### View PostgreSQL Data (Docker Compose)

```bash
# Connect to PostgreSQL container
docker exec -it growwise_postgres psql -U growwise_user -d growwise_db

# List tables
\dt

# View users
SELECT * FROM users;

# View child records
SELECT * FROM child;

# View habits
SELECT * FROM habit;

# View gratitude entries
SELECT * FROM gratitude_entries;

# Exit
\q
```

### View SQLite Data (Local)

```bash
cd backend

# Using sqlite3 CLI
sqlite3 database.db

# List tables
.tables

# View users
SELECT * FROM users;

# View child records
SELECT * FROM child;

# View habits
SELECT * FROM habit;

# Exit
.quit
```

---

## Running Test Suite

```bash
cd backend

# Install test dependencies
pip install pytest pytest-flask

# Run all tests
pytest

# Run specific test file
pytest tests/test_login.py

# Run with verbose output
pytest -v

# Run with coverage
pytest --cov=api tests/

# Run specific test
pytest tests/test_gratitude.py::test_create_gratitude_entry
```

---

## Monitoring & Logging

### Check Backend Logs (Docker)

```bash
# Follow logs
docker logs -f growwise_backend

# View recent logs
docker logs --tail 100 growwise_backend
```

### Check PostgreSQL Status (Docker)

```bash
# Check container status
docker ps | grep postgres

# Check logs
docker logs growwise_postgres

# Connect and check database
docker exec growwise_postgres psql -U growwise_user -d growwise_db -c "SELECT now();"
```

---

## Common Issues & Solutions

### Issue 1: "Cannot connect to PostgreSQL"

**Solution:**
```bash
# Ensure containers are running
docker-compose up -d

# Check database health
docker exec growwise_postgres pg_isready -U growwise_user

# If container crashed, check logs
docker logs growwise_postgres
```

### Issue 2: "Database does not exist"

**Solution:**
```bash
# Recreate database
docker exec -it growwise_backend python migrate.py

# Or manually create
docker exec growwise_postgres psql -U growwise_user -c "CREATE DATABASE growwise_db;"
```

### Issue 3: "psycopg2 module not found"

**Solution:**
```bash
pip install -r backend/requirements.txt

# Or inside Docker
docker exec -it growwise_backend pip install -r requirements.txt
```

### Issue 4: Port already in use

**Solution:**
```bash
# Change port in docker-compose.yml
# Change port in .env
# Or stop conflicting service
docker ps  # Find conflicting container
docker stop <container_id>
```

### Issue 5: SQLAlchemy version conflicts

**Solution:**
```bash
pip install --upgrade SQLAlchemy
pip install --upgrade Flask-SQLAlchemy
```

---

## Performance Testing

### Test with Seed Data

```bash
cd backend
python migrate.py
# Application now has 50+ seed records for testing
```

### Monitor Query Performance

```python
# Add to app.py to log SQL queries
from flask_sqlalchemy import get_debug_queries

@app.after_request
def after_request(response):
    for query in get_debug_queries():
        if query.duration >= 0.5:
            app.logger.warning(f'SLOW QUERY: {query.statement}')
    return response
```

---

## Maintenance & Backups

### Backup PostgreSQL Database

```bash
# Backup to SQL file
docker exec growwise_postgres pg_dump -U growwise_user growwise_db > backup.sql

# Backup to custom format
docker exec growwise_postgres pg_dump -U growwise_user -Fc growwise_db > backup.dump

# Restore from backup
docker exec -i growwise_postgres psql -U growwise_user growwise_db < backup.sql
```

### Export Data

```bash
# Export to CSV
docker exec growwise_postgres psql -U growwise_user -d growwise_db \
  -c "COPY users TO STDOUT WITH (FORMAT csv);" > users.csv
```

---

## Next Steps

1. ✅ Backend database migrated from SQLite to PostgreSQL
2. ✅ All CRUD operations verified to work
3. ✅ Docker Compose configured with PostgreSQL service
4. ✅ Test suite updated for both SQLite and PostgreSQL
5. 📋 **Next: Deploy to Azure App Service with PostgreSQL Flexible Server**
6. 📋 **Next: Configure CI/CD pipeline for automated testing**
7. 📋 **Next: Set up monitoring and alerting**

---

## Reference Documentation

- [API Documentation](./backend/static/swagger.html)
- [PostgreSQL Migration Guide](./POSTGRESQL_MIGRATION.md)
- [Backend README](./backend/README.md)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)

---

**Status: ✅ Migration Complete and Tested**

All CRUD operations are functional with both SQLite and PostgreSQL databases.
