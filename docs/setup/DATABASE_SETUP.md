# Database Setup Guide

Complete guide for initializing and managing databases for both microservices.

---

## Overview

| Service | Technology | Port | Database | Schema Setup | Data Seeding |
|---------|-----------|------|----------|--------------|--------------|
| **Maintenance Service** | Python/Flask | 5001 | maintenance_db (5433) | SQLAlchemy | Python Seeder + SQL Backup |
| **Vehicle Service** | .NET/C# | 7001 | vehicle_db (7433) | EF Migrations | C# DatabaseSeeder |

Both services use **PostgreSQL 16** with automatic initialization and seeding.

---

## 🔧 Maintenance Service (Python/Flask)

### Database Initialization: Dual Approach

1. **Primary:** Python Seeder (`app/utils/database_seeder.py`) - Runs on every startup
2. **Backup:** PostgreSQL Init Script (`init-db.sql`) - Runs on first container creation

### How It Works

```
Container Startup
├─ PostgreSQL starts → init-db.sql creates schema + sample data (backup)
├─ Flask app starts → run.py
│  ├─ initialize_database() is called
│  │  ├─ db.create_all() - Ensures tables exist
│  │  └─ seed_database() - Checks if data exists
│  │     ├─ If empty → Insert 5 sample maintenance items
│  │     └─ If data exists → Skip (idempotent)
│  └─ Start Flask server on port 5001
```

### Features

- ✅ **Idempotent:** Checks `MaintenanceItem.query.count()` before seeding
- ✅ **Automatic:** Runs every startup, no manual steps
- ✅ **Flexible:** No volume deletion needed to re-seed
- ✅ **Type-Safe:** Uses Python ORM models
- ✅ **Dual Redundancy:** SQL + Python seeder

### Sample Data (5 Items)

- **M001:** Oil Change - VH-001 (Overdue, HIGH)
- **M002:** Brake Inspection - VH-002 (In Progress, MEDIUM)
- **M003:** Tire Rotation - VH-003 (Scheduled, LOW)
- **M004:** Annual Inspection - VH-001 (Due Soon, HIGH)
- **M005:** Engine Tune-up - VH-002 (Completed, MEDIUM)

### Docker Compose Features

```yaml
services:
  maintenance-service:
    networks: [maintenance-network]    # Isolated network
    volumes: ["./:/app"]               # Live code reload
    environment:
      CORS_ORIGINS: "*"                # CORS support
    depends_on:
      postgres-maintenance:
        condition: service_healthy     # Wait for DB health
```

---

## 🚀 Vehicle Service (.NET/C#)

### Database Initialization: EF Migrations + C# Seeder

**Location:** `VehicleService.Infrastructure/Data/DatabaseSeeder.cs`

### How It Works

```
Container Startup
├─ PostgreSQL starts → Creates empty vehicle_db
├─ .NET app starts → Program.cs
│  ├─ Apply EF Migrations (creates schema)
│  └─ DatabaseSeeder.SeedAsync()
│     ├─ Check: await context.Vehicles.AnyAsync()
│     ├─ If empty → Insert 3 vehicles + histories + records
│     └─ If data exists → Skip (idempotent)
└─ Start API server on port 7001
```

### Features

- ✅ **Idempotent:** Checks `AnyAsync()` before seeding
- ✅ **Automatic:** Runs every startup
- ✅ **Type-Safe:** Uses C# entities
- ✅ **Migration-Based:** Schema managed by EF migrations

### Sample Data (3 Vehicles + Related Data)

- **VH-001:** Ford Transit Van (Active, 45,200 mi)
- **VH-002:** Tesla Model S (Active, 13,200 mi)
- **VH-003:** Toyota Hilux (Maintenance, 88,800 mi)
- Plus: 3 status histories, 2 maintenance records

### Docker Compose Features

```yaml
services:
  vehicle-service:
    networks: [vehicle-network]        # Isolated network
    volumes: ["./VehicleService:/src"] # Live code reload
    environment:
      CORS_ORIGINS: "*"                # CORS support
    depends_on:
      postgres-vehicle:
        condition: service_healthy     # Wait for DB health
```

---

## 🎯 Quick Start

### Start Both Services

```bash
# Maintenance Service
cd src/maintenanceService
docker-compose up -d

# Vehicle Service
cd src/vehicleService
docker-compose up -d
```

### Verify Database Seeding

**Maintenance Service:**
```bash
docker logs maintenance-service | grep "Seeding"
# Expected: "✅ Successfully seeded 5 maintenance items"

docker exec -it postgres-maintenance psql -U postgres -d maintenance_db -c "SELECT COUNT(*) FROM maintenance_items;"
# Expected: 5
```

**Vehicle Service:**
```bash
docker logs vehicle-service | grep "Seeding"
# Expected: "✅ Added 3 sample vehicles"

docker exec -it postgres-vehicle psql -U postgres -d vehicle_db -c "SELECT COUNT(*) FROM \"Vehicles\";"
# Expected: 3
```

### Access Services

- **Maintenance Service:** http://localhost:5001/health
- **Vehicle Service:** http://localhost:7001/health

---

## 🔄 Common Tasks

### Restart Services (Re-seed automatically)

```bash
# Maintenance Service
docker-compose restart maintenance-service

# Vehicle Service
docker-compose restart vehicle-service
```

Both seeders run on every startup and skip if data exists.

### Fresh Database (Delete volumes)

```bash
# Maintenance Service
cd src/maintenanceService
docker-compose down -v
docker-compose up -d

# Vehicle Service
cd src/vehicleService
docker-compose down -v
docker-compose up -d
```

### Access Databases Directly

```bash
# Maintenance DB
docker exec -it postgres-maintenance psql -U postgres -d maintenance_db

# Vehicle DB
docker exec -it postgres-vehicle psql -U postgres -d vehicle_db
```

### Use pgAdmin (Optional)

```bash
# Maintenance Service
cd src/maintenanceService
docker-compose --profile admin up -d
# Access: http://localhost:5051

# Vehicle Service
cd src/vehicleService
docker-compose --profile admin up -d
# Access: http://localhost:5050
```

---

## 📊 Database Credentials

### Maintenance Service
- **Host:** localhost
- **Port:** 5433
- **Database:** maintenance_db
- **Username:** postgres
- **Password:** postgres

### Vehicle Service
- **Host:** localhost
- **Port:** 7433
- **Database:** vehicle_db
- **Username:** postgres
- **Password:** postgres

---

## 🔍 Key Differences

| Aspect | Maintenance Service | Vehicle Service |
|--------|-------------------|-----------------|
| **Language** | Python | C# |
| **ORM** | SQLAlchemy | Entity Framework |
| **Schema Creation** | db.create_all() | EF Migrations |
| **Seeder** | Python function | C# static class |
| **Backup Method** | init-db.sql | None (migrations only) |
| **Check Method** | query.count() | AnyAsync() |

**Both approaches are production-ready and follow best practices!**

---

## 🛠️ Troubleshooting

### "Sample data not inserted"

**Maintenance Service:**
```bash
# Seeder runs on every startup
docker-compose restart maintenance-service
docker logs maintenance-service

# Look for: 🌱 Seeding database...
# Fresh start if needed:
docker-compose down -v && docker-compose up -d
```

**Vehicle Service:**
```bash
# Seeder runs on every startup
docker-compose restart vehicle-service
docker logs vehicle-service

# Look for: 🌱 Seeding database...
# Fresh start if needed:
docker-compose down -v && docker-compose up -d
```

### Port Conflicts (7433 in use)

```bash
# Check what's using the ports
netstat -ano | findstr :7433

# Stop conflicting PostgreSQL services
# Windows:
Stop-Service postgresql-x64-*

# Linux/Mac:
sudo systemctl stop postgresql
```

### Database Won't Start

```bash
# Check logs
docker-compose logs postgres-maintenance
docker-compose logs postgres-vehicle

# Common issues:
# - Port already in use → Change ports in docker-compose.yml
# - Corrupted volume → docker-compose down -v
# - Insufficient memory → Check Docker resources
```

### Health Check Never Passes

```bash
# Wait 10-15 seconds for PostgreSQL initialization
docker-compose logs postgres-maintenance

# If still failing, restart:
docker-compose restart postgres-maintenance
```

---

## ✅ Health Checks

**Maintenance Service:**
```bash
curl http://localhost:5001/health
# Expected: {"status":"healthy","service":"maintenance-service"}

curl http://localhost:5001/api/maintenance/
# Expected: Array of 5 maintenance items
```

**Vehicle Service:**
```bash
curl http://localhost:7001/health
# Expected: {"status":"healthy","service":"vehicle-service"}

curl http://localhost:7001/health/db
# Expected: {"database":"vehicle_db","connected":true}
```

---

## 🎓 Best Practices

1. **Always use idempotent seeders** - Check for existing data first
2. **Run seeders on every startup** - Ensures database is always ready
3. **Use ORM models for seeding** - Type-safe and maintainable
4. **Implement proper logging** - Makes debugging easier
5. **Keep sample data realistic** - Helps with development and testing
6. **Use health checks** - Monitor database connectivity
7. **Separate databases per service** - Microservice isolation
8. **Document seeding behavior** - Clear for team members

---

## 📝 Implementation Details

### Maintenance Service Seeder

**File:** `src/maintenanceService/app/utils/database_seeder.py`

```python
def seed_database():
    existing_count = MaintenanceItem.query.count()
    if existing_count > 0:
        logger.info(f"ℹ️  Database already contains {existing_count} items. Skipping seed.")
        return False
    
    # Insert 5 sample items...
    db.session.bulk_insert_mappings(MaintenanceItem, sample_data)
    db.session.commit()
    return True
```

### Vehicle Service Seeder

**File:** `src/vehicleService/VehicleService.Infrastructure/Data/DatabaseSeeder.cs`

```csharp
public static async Task SeedAsync(VehicleDbContext context)
{
    if (await context.Vehicles.AnyAsync())
    {
        Console.WriteLine("ℹ️  Database already contains data. Skipping seed.");
        return;
    }
    
    // Create and insert 3 vehicles + related data...
    await context.Vehicles.AddRangeAsync(vehicle1, vehicle2, vehicle3);
    await context.SaveChangesAsync();
}
```

---

## 🚀 Production Deployment

### Pre-Deployment Checklist

- [ ] Change default database passwords
- [ ] Update connection strings in `.env` or configuration
- [ ] Configure backup strategy
- [ ] Set up monitoring and alerts
- [ ] Review and adjust seeder data (or disable for production)
- [ ] Enable SSL/TLS for database connections
- [ ] Configure proper CORS origins
- [ ] Set up database migrations in CI/CD

### Seeder in Production

**Option 1:** Keep seeder but use production-appropriate data  
**Option 2:** Disable seeder in production environment  
**Option 3:** Use seeder only for staging/test environments

---

## 📚 Additional Documentation

- **Maintenance Service Details:** `src/maintenanceService/README.md`
- **Maintenance Seeder Implementation:** `src/maintenanceService/SEEDER_IMPLEMENTATION.md`
- **Vehicle Service Details:** `src/vehicleService/README.md` (if exists)
- **Vehicle Seeder Implementation:** `src/vehicleService/SEEDER_IMPLEMENTATION.md`

---

## Summary

Both services feature:
- ✅ **Automatic database initialization**
- ✅ **Idempotent data seeding**
- ✅ **Docker-based deployment**
- ✅ **Health checks and monitoring**
- ✅ **Isolated networks and volumes**
- ✅ **CORS support**
- ✅ **Production-ready architecture**

Just run `docker-compose up -d` in each service directory and you're ready to develop! 🎉
