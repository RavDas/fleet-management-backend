# Maintenance Service - Database Seeder Implementation

Complete guide for the automatic database seeding in the Maintenance Service.

---

## Overview

The Maintenance Service uses **automatic database seeding** with a dual approach: Python ORM seeder (primary) + PostgreSQL init script (backup). Seeding runs on every startup and is idempotent.

---

## ✅ Implementation

### 1. database_seeder.py

**Location:** `app/utils/database_seeder.py`

**Features:**
- ✅ Idempotent - checks if data exists before seeding
- ✅ Seeds 5 sample maintenance items
- ✅ Uses SQLAlchemy ORM models (type-safe)
- ✅ Detailed logging with emoji indicators
- ✅ Proper error handling and rollback
- ✅ Two main functions:
  - `seed_database()` - Inserts sample data
  - `initialize_database()` - Main entry point

**Sample Data:**
```
5 Maintenance Items:
├─ M001: Oil Change - VH-001 (Overdue, HIGH priority)
├─ M002: Brake Inspection - VH-002 (In Progress, MEDIUM priority)
├─ M003: Tire Rotation - VH-003 (Scheduled, LOW priority)
├─ M004: Annual Inspection - VH-001 (Due Soon, HIGH priority)
└─ M005: Engine Tune-up - VH-002 (Completed, MEDIUM priority)

Covers:
- Vehicles: VH-001, VH-002, VH-003
- All statuses: overdue, in_progress, scheduled, due_soon, completed
- All priorities: low, medium, high
```

### 2. run.py Integration

**Location:** `run.py`

**Initialization Sequence:**
```python
if __name__ == '__main__':
    with app.app_context():
        try:
            logger.info("=" * 60)
            logger.info("🚀 Starting Maintenance Service")
            logger.info("=" * 60)
            initialize_database()  # Calls seeder
            logger.info("=" * 60)
        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")
            raise
    
    # Start Flask server
    app.run(host=host, port=port, debug=True)
```

### 3. Dual Approach (Redundancy)

**Primary:** Python Seeder (runs every startup)
**Backup:** `init-db.sql` (runs on first PostgreSQL container creation)

This dual approach ensures database initialization even if one method fails.

### 4. Docker Compose Configuration

**Enhanced Features:**
```yaml
services:
  maintenance-service:
    networks: [maintenance-network]    # Isolated network
    volumes: ["./:/app"]               # Live code reload
    environment:
      CORS_ORIGINS: "*"                # CORS support
      DATABASE_URL: "postgresql://..." # DB connection
    depends_on:
      postgres-maintenance:
        condition: service_healthy     # Wait for DB
    restart: always

  postgres-maintenance:
    volumes:
      - maintenance_pg_data:/var/lib/postgresql/data
      - ./init-db.sql:/docker-entrypoint-initdb.d/init-db.sql
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres -d maintenance_db"]
      interval: 5s
```

---

## 🚀 How It Works

### Startup Sequence

```
1. docker-compose up
   └─ PostgreSQL container starts
      ├─ init-db.sql runs (creates schema + sample data)
      └─ Health check passes (pg_isready)
      
2. Flask container starts
   └─ Python application initializes
   
3. run.py execution:
   ├─ Initialize database:
   │  ├─ db.create_all() - Ensure tables exist
   │  └─ seed_database() - Check and seed data
   │     ├─ Check: MaintenanceItem.query.count() > 0?
   │     │  ├─ Yes → Skip (log existing count)
   │     │  └─ No → Insert 5 sample items
   │     └─ Log success with summary
   │
   └─ Start Flask server on port 5001
```

### Idempotency Check

```python
existing_count = MaintenanceItem.query.count()
if existing_count > 0:
    logger.info(f"ℹ️  Database already contains {existing_count} maintenance items. Skipping seed.")
    return False
```

**Benefits:**
- ✅ Safe to run multiple times
- ✅ Won't create duplicate data
- ✅ Fast check (immediate exit if data exists)
- ✅ Shows existing record count

---

## 🎯 Usage

### First Time Setup

```bash
cd src/maintenanceService
docker-compose up -d
```

**Expected Logs:**
```
============================================================
🚀 Starting Maintenance Service
============================================================
🔄 Initializing database...
✅ Database tables ready
🌱 Seeding database with sample maintenance data...
✅ Successfully seeded 5 maintenance items
📊 Sample data summary:
   - 5 maintenance items (M001-M005)
   - Vehicles: VH-001, VH-002, VH-003
   - Various statuses: overdue, in_progress, scheduled, due_soon, completed
🎉 Database seeding completed successfully!
✅ Database initialization complete
============================================================
🌐 Starting server on 0.0.0.0:5001
```

### Subsequent Startups

```bash
docker-compose restart maintenance-service
```

**Expected Logs:**
```
============================================================
🚀 Starting Maintenance Service
============================================================
🔄 Initializing database...
✅ Database tables ready
ℹ️  Database already contains 5 maintenance items. Skipping seed.
✅ Database initialization complete
============================================================
🌐 Starting server on 0.0.0.0:5001
```

### Re-seed Data

**Option 1: Delete data, then restart**
```bash
docker exec -it postgres-maintenance psql -U postgres -d maintenance_db -c "DELETE FROM maintenance_items;"
docker-compose restart maintenance-service
```

**Option 2: Fresh start (deletes volumes)**
```bash
docker-compose down -v
docker-compose up -d
```

---

## 🔍 Verification

### Check Logs

```bash
docker logs maintenance-service --tail 50
```

Look for seeding messages starting with 🌱

### Query Database

```bash
docker exec -it postgres-maintenance psql -U postgres -d maintenance_db
```

**SQL Queries:**
```sql
-- Count maintenance items
SELECT COUNT(*) FROM maintenance_items;
-- Expected: 5

-- View all items
SELECT id, vehicle_id, type, status, priority 
FROM maintenance_items;

-- Check specific statuses
SELECT status, COUNT(*) 
FROM maintenance_items 
GROUP BY status;
```

### API Health Check

```bash
# Basic health check
curl http://localhost:5001/health
# Expected: {"status":"healthy","service":"maintenance-service"}

# Get all maintenance items
curl http://localhost:5001/api/maintenance/
# Expected: Array of 5 maintenance items
```

---

## 📊 Advantages Over SQL-Only Approach

| Feature | Python Seeder | SQL Init Script |
|---------|--------------|-----------------|
| **When Runs** | Every startup | Container creation only |
| **Re-seeding** | Just restart | Must delete volumes |
| **Flexibility** | High | Low |
| **Type Safety** | Yes (ORM models) | No (raw SQL) |
| **Logging** | Python logging | PostgreSQL notices |
| **Error Handling** | Comprehensive | Limited |
| **Maintenance** | Alongside code | Separate file |
| **Debugging** | Easy | Harder |

**The Maintenance Service uses BOTH for redundancy!**

---

## 🛠️ Troubleshooting

### Seeder Not Running

**Check logs:**
```bash
docker logs maintenance-service
```

**Common Issues:**
1. **Database connection failed**
   - Ensure postgres-maintenance is running: `docker ps`
   - Check logs: `docker-compose logs postgres-maintenance`
   - Wait 10-15 seconds for initialization

2. **Table creation failed**
   - Check SQLAlchemy errors in logs
   - Verify model definitions

3. **Seeder exception**
   - Look for stack traces after "🌱 Seeding"
   - Check database constraints

### Data Not Appearing

**Verify seeder executed:**
```bash
docker logs maintenance-service | grep "Seeding"
```

**Expected Output:**
- `🌱 Seeding database with sample maintenance data...`
- Either: `✅ Successfully seeded 5 maintenance items` (first run)
- Or: `ℹ️  Database already contains X items. Skipping seed.` (subsequent runs)

**If no seeding messages:**
1. Check `run.py` initialization code
2. Verify `database_seeder.py` is imported correctly
3. Look for Python errors before seeding

### Port Conflicts

```bash
# Check what's using port 5001 or 5434
netstat -ano | findstr :5001
netstat -ano | findstr :5434

# Stop conflicting services
# Windows:
Stop-Service postgresql-x64-*

# Linux/Mac:
sudo systemctl stop postgresql
```

### Reset Everything

```bash
# Complete reset
cd src/maintenanceService
docker-compose down -v --remove-orphans
docker-compose build --no-cache
docker-compose up -d
```

---

## 🎓 Benefits of This Approach

1. **Automatic & Flexible**
   - Runs on every startup
   - No manual SQL scripts needed
   - No volume deletion required to re-seed

2. **Idempotent & Safe**
   - Checks for existing data
   - Won't create duplicates
   - Safe to run multiple times

3. **Type-Safe & Maintainable**
   - Uses Python ORM models
   - Changes to models automatically reflected
   - Version controlled with code

4. **Well-Logged**
   - Clear console output
   - Emoji-enhanced messages
   - Easy to debug

5. **Dual Redundancy**
   - Python seeder (primary)
   - SQL init script (backup)
   - Maximum reliability

6. **Modern Pattern**
   - Matches Vehicle Service approach
   - Follows Flask best practices
   - Production-ready

---

## 🔄 Comparison with Vehicle Service

| Aspect | Maintenance Service | Vehicle Service |
|--------|-------------------|-----------------|
| **Language** | Python | C# |
| **ORM** | SQLAlchemy | Entity Framework |
| **Seeder** | database_seeder.py | DatabaseSeeder.cs |
| **Schema** | db.create_all() | EF Migrations |
| **Check** | query.count() > 0 | AnyAsync() |
| **When Runs** | Every startup | Every startup |
| **Backup Method** | init-db.sql | None |
| **Logging** | Python logging | .NET logging |

**Both are production-ready and follow best practices!**

---

## 🔧 Customizing Sample Data

### Adding More Items

Edit `database_seeder.py`:

```python
sample_data = [
    # ... existing items ...
    {
        'id': 'M006',
        'vehicle_id': 'VH-004',
        'type': 'Battery Replacement',
        'status': 'scheduled',
        'priority': 'medium',
        'due_date': date.today() + timedelta(days=7),
        'current_mileage': 32000,
        'due_mileage': 33000,
        'estimated_cost': 200.0,
        'assigned_to': 'Service Center D'
    }
]
```

### Changing Idempotency Check

```python
# Check specific criteria
existing_high_priority = MaintenanceItem.query.filter_by(priority='high').count()
if existing_high_priority > 0:
    # Custom logic
```

### Disabling Seeder in Production

```python
# In run.py or seeder
if os.environ.get('FLASK_ENV') != 'production':
    initialize_database()
```

---

## 📝 Files Modified/Created

### Created
- ✅ `app/utils/database_seeder.py` (147 lines)
- ✅ `SEEDER_IMPLEMENTATION.md` (this file)

### Modified
- ✅ `run.py` (added initialization call and logging)
- ✅ `../docker-compose.yml` (enhanced configuration)
- ✅ `Dockerfile` (added health check)

### Unchanged
- ✅ `app/models/maintainance.py` (models unchanged)
- ✅ `init-db.sql` (kept as backup)
- ✅ `config.py` (no changes needed)

---

## ✅ Production Considerations

### Security
```python
# Don't seed in production
if not app.config.get('TESTING') and os.environ.get('FLASK_ENV') != 'production':
    initialize_database()

# Use environment variables for sensitive data
admin_email = os.environ.get('ADMIN_EMAIL')
```

### Performance
```python
# Bulk insert for large datasets
db.session.bulk_insert_mappings(MaintenanceItem, sample_data)

# Use transactions
try:
    db.session.begin_nested()
    # Seeding operations
    db.session.commit()
except:
    db.session.rollback()
    raise
```

### Monitoring
```python
import time
start_time = time.time()
# Seeding operations
duration = time.time() - start_time
logger.info(f"Seeded {count} items in {duration:.2f}s")
```

---

## 🚀 Next Steps

1. **Start the service:** `docker-compose up -d`
2. **Verify seeding:** `docker logs maintenance-service`
3. **Test API:** `curl http://localhost:5001/api/maintenance/`
4. **Access database:** Via pgAdmin (port 5051) or psql
5. **Develop features:** Sample data is ready!

---

## 📚 Additional Resources

- **Root Database Guide:** `../../DATABASE_SETUP.md`
- **Service README:** `README.md`
- **Flask-SQLAlchemy Docs:** https://flask-sqlalchemy.palletsprojects.com/
- **PostgreSQL Docs:** https://www.postgresql.org/docs/

---

## Summary

The Maintenance Service now features:
- ✅ Automatic database seeding on every startup
- ✅ Idempotent operation (safe to run multiple times)
- ✅ Type-safe Python ORM models
- ✅ Comprehensive logging
- ✅ Dual redundancy (Python + SQL)
- ✅ Docker integration with health checks
- ✅ CORS and network isolation
- ✅ Production-ready architecture

**The seeder ensures your database is always ready for development!** 🎉
