# Maintenance Service (Flask API)

Fleet Management Maintenance Service - Manages vehicle maintenance records, schedules, and tracking.

## Quick Start

```bash
# Start the service with Docker
docker-compose up -d

# Verify it's running
curl http://localhost:5001/health
```

**Service URL:** http://localhost:5001  
**Database:** PostgreSQL on port 5434

---

## Features

- ✅ RESTful API for maintenance management
- ✅ Automatic database initialization & seeding
- ✅ PostgreSQL database with sample data
- ✅ Docker containerization
- ✅ Health check endpoints
- ✅ CORS support

---

## Prerequisites

- Docker & Docker Compose
- Python 3.11+ (for local development)

---

## Running the Service

### With Docker (Recommended)

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Local Development

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# .\venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Run the service
python run.py
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| GET | `/` | Service info |
| GET | `/api/maintenance/` | List all maintenance items |
| GET | `/api/maintenance/:id` | Get specific item |
| POST | `/api/maintenance/` | Create new item |
| PUT | `/api/maintenance/:id` | Update item |
| DELETE | `/api/maintenance/:id` | Delete item |
| GET | `/api/maintenance/summary` | Get summary stats |
| GET | `/api/maintenance/vehicle/:vehicle_id/history` | Vehicle maintenance history |

---

## Database

### Connection Info
- **Host:** localhost:5434
- **Database:** maintenance_db
- **User:** postgres
- **Password:** postgres

### Access Database
```bash
docker exec -it postgres-maintenance psql -U postgres -d maintenance_db
```

### Sample Data
The database is automatically seeded with 5 maintenance items on first startup:
- M001: Oil Change (Overdue)
- M002: Brake Inspection (In Progress)
- M003: Tire Rotation (Scheduled)
- M004: Annual Inspection (Due Soon)
- M005: Engine Tune-up (Completed)

---

## Configuration

### Environment Variables (`.env`)
```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5434/maintenance_db
FLASK_ENV=development
PORT=5001
HOST=0.0.0.0
CORS_ORIGINS=*
```

---

## Docker Services

| Service | Container | Port | Description |
|---------|-----------|------|-------------|
| maintenance-service | maintenance-service | 5001 | Flask API |
| postgres-maintenance | postgres-maintenance | 5434 | PostgreSQL 16 |
| pgadmin-maintenance | pgadmin-maintenance | 5051 | DB Admin (optional) |

### Start with pgAdmin
```bash
docker-compose --profile admin up -d
```
Access at: http://localhost:5051
- Email: admin@maintenance.local
- Password: admin123

---

## Project Structure

```
maintenanceService/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── models/              # Database models
│   ├── routes/              # API routes
│   ├── services/            # Business logic
│   ├── schemas/             # Validation schemas
│   └── utils/               # Database seeder & utilities
├── config.py                # Configuration
├── run.py                   # Application entry point
├── requirements.txt         # Python dependencies
├── Dockerfile               # Docker image
├── docker-compose.yml       # Docker services
├── init-db.sql             # Database initialization (backup)
└── .env                     # Environment variables
```

---

## Development

### Rebuild After Code Changes
```bash
docker-compose up --build
```

### Run Tests
```bash
pytest
pytest --cov=app  # With coverage
```

### Database Migrations
```bash
# Initialize migrations (first time)
flask db init

# Create migration
flask db migrate -m "Description"

# Apply migration
flask db upgrade
```

---

## Troubleshooting

### Port Already in Use
Edit `docker-compose.yml` to use different ports.

### Database Connection Failed
```bash
# Check if PostgreSQL is running
docker ps

# View logs
docker-compose logs postgres-maintenance

# Wait for health check (~10 seconds)
```

### Reset Database
```bash
# Delete volumes and restart
docker-compose down -v
docker-compose up -d
```

---

## Integration

This service works alongside the Vehicle Service:
- **Vehicle Service:** Port 7001, PostgreSQL 5433
- **Maintenance Service:** Port 5001, PostgreSQL 5434

Both services can run simultaneously without conflicts.

---

## Documentation

- **Database Setup:** See `../../DATABASE_SETUP.md`
- **Seeder Implementation:** See `SEEDER_IMPLEMENTATION.md`

---

## Production Deployment

### Security Checklist
- [ ] Change default PostgreSQL password
- [ ] Set strong SECRET_KEY
- [ ] Configure CORS_ORIGINS to specific domains
- [ ] Enable HTTPS
- [ ] Set up database backups
- [ ] Configure logging and monitoring

### Environment Variables
```env
FLASK_ENV=production
SECRET_KEY=<strong-random-key>
DATABASE_URL=postgresql://<user>:<pass>@<host>:<port>/maintenance_db
CORS_ORIGINS=https://yourdomain.com
```

---

## License

MIT License
