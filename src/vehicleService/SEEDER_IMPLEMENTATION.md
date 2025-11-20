# Vehicle Service - Database Seeder Implementation

Complete guide for the automatic database seeding in the Vehicle Service.

---

## Overview

The Vehicle Service uses **automatic database seeding** via Entity Framework migrations and a C# DatabaseSeeder class. Seeding runs on every startup and is idempotent.

---

## ✅ Implementation

### 1. DatabaseSeeder.cs

**Location:** `VehicleService.Infrastructure/Data/DatabaseSeeder.cs`

**Features:**
- ✅ Idempotent - checks if data exists before seeding
- ✅ Seeds 3 sample vehicles with complete details
- ✅ Seeds 3 vehicle status history entries
- ✅ Seeds 2 maintenance records
- ✅ Detailed console logging
- ✅ Uses C# entities (type-safe)
- ✅ Async/await pattern

**Sample Data:**
```
3 Vehicles:
├─ Ford Transit Van (2021) - Active - Depot A - 45,200 mi
├─ Tesla Model S (2023) - Active - Depot B - 13,200 mi
└─ Toyota Hilux (2020) - Maintenance - Warehouse 2 - 88,800 mi

3 Status Histories:
├─ Ford: Active (System)
├─ Tesla: Active (System)
└─ Toyota: Maintenance (Admin)

2 Maintenance Records:
├─ Ford: Oil Change ($250) - AutoFix Center
└─ Toyota: Brake Pad Replacement ($480) - SpeedServ Ltd
```

### 2. Program.cs Integration

**Location:** `VehicleService.Api/Program.cs`

**Initialization Sequence:**
```csharp
using (var scope = app.Services.CreateScope())
{
    var db = scope.ServiceProvider.GetRequiredService<VehicleDbContext>();
    var logger = scope.ServiceProvider.GetRequiredService<ILogger<Program>>();
    
    // 1. Apply EF migrations
    await db.Database.MigrateAsync();
    
    // 2. Seed sample data
    await DatabaseSeeder.SeedAsync(db);
}
```

### 3. Docker Compose Configuration

**Enhanced Features:**
```yaml
services:
  vehicle-service:
    networks: [vehicle-network]         # Isolated network
    volumes: ["./VehicleService:/src"]  # Live code changes
    environment:
      CORS_ORIGINS: "*"                 # CORS support
    depends_on:
      postgres-vehicle:
        condition: service_healthy      # Wait for DB
    restart: always
```

---

## 🚀 How It Works

### Startup Sequence

```
1. docker-compose up
   └─ PostgreSQL container starts
      └─ Waits for health check (pg_isready)
      
2. Vehicle Service container starts
   └─ .NET application initializes
      
3. Program.cs runs database initialization:
   ├─ Apply EF Migrations
   │  └─ Creates tables: Vehicles, VehicleStatusHistories, MaintenanceRecords
   │
   └─ Call DatabaseSeeder.SeedAsync()
      ├─ Check: await context.Vehicles.AnyAsync()
      │  ├─ If data exists → Skip (log message)
      │  └─ If empty → Insert sample data
      │
      └─ Insert vehicles, histories, and records
         └─ Log success with summary

4. API server starts on port 7001
```

### Idempotency Check

```csharp
if (await context.Vehicles.AnyAsync())
{
    Console.WriteLine("ℹ️  Database already contains data. Skipping seed.");
    return;
}
```

**Benefits:**
- ✅ Safe to run multiple times
- ✅ Won't create duplicate data
- ✅ Fast check (immediate exit if data exists)
- ✅ No manual volume deletion needed

---

## 🎯 Usage

### First Time Setup

```bash
cd src/vehicleService
docker-compose up -d
```

**Expected Logs:**
```
🔄 Applying database migrations...
✅ Database migrations applied successfully
🌱 Checking if database needs seeding...
🌱 Seeding database with sample data...
✅ Added 3 sample vehicles
✅ Added vehicle status histories
✅ Added maintenance records
🎉 Database seeding completed successfully!
📊 Summary:
   - 3 Vehicles (Ford Transit Van, Tesla Model S, Toyota Hilux)
   - 3 Status History Entries
   - 2 Maintenance Records
```

### Subsequent Startups

```bash
docker-compose restart vehicle-service
```

**Expected Logs:**
```
🔄 Applying database migrations...
✅ Database migrations applied successfully
🌱 Checking if database needs seeding...
ℹ️  Database already contains data. Skipping seed.
```

### Fresh Database (Re-seed)

```bash
# Option 1: Delete volumes and restart
docker-compose down -v
docker-compose up -d

# Option 2: Delete data manually, then restart
docker exec -it postgres-vehicle psql -U postgres -d vehicle_db -c "DELETE FROM \"Vehicles\";"
docker-compose restart vehicle-service
```

---

## 🔍 Verification

### Check Logs

```bash
docker logs vehicle-service --tail 50
```

Look for seeding messages with 🌱 emoji.

### Query Database

```bash
docker exec -it postgres-vehicle psql -U postgres -d vehicle_db
```

**SQL Queries:**
```sql
-- Count vehicles
SELECT COUNT(*) FROM "Vehicles";
-- Expected: 3

-- View vehicle details
SELECT "LicensePlate", "Make", "Model", "Status", "CurrentDriver" 
FROM "Vehicles";

-- View status histories
SELECT "ChangedBy", "Status", "Description" 
FROM "VehicleStatusHistories";

-- View maintenance records
SELECT "ServiceType", "Cost", "ServiceCenter" 
FROM "MaintenanceRecords";
```

### API Health Check

```bash
# Basic health check
curl http://localhost:7001/health
# Expected: {"status":"healthy","service":"vehicle-service"}

# Database health check
curl http://localhost:7001/health/db
# Expected: {"database":"vehicle_db","connected":true}

# Get all vehicles
curl http://localhost:7001/api/vehicle
```

---

## 📊 Comparison with Maintenance Service

| Feature | Vehicle Service | Maintenance Service |
|---------|----------------|---------------------|
| **Language** | C# | Python |
| **ORM** | Entity Framework | SQLAlchemy |
| **Seeder** | DatabaseSeeder.cs | database_seeder.py |
| **Schema** | EF Migrations | db.create_all() |
| **Check** | AnyAsync() | query.count() |
| **When Runs** | Every startup | Every startup |
| **Backup Method** | None (migrations only) | init-db.sql |
| **Type Safety** | Yes (entities) | Yes (ORM models) |

**Both are production-ready and follow best practices!**

---

## 🛠️ Troubleshooting

### Seeder Not Running

**Check logs:**
```bash
docker logs vehicle-service
```

**Common Issues:**
1. **Database connection failed**
   - Ensure postgres-vehicle container is running: `docker ps`
   - Check health: `docker-compose logs postgres-vehicle`
   - Wait 10-15 seconds for PostgreSQL initialization

2. **Migrations failed**
   - Check migration logs for errors
   - Try: `docker-compose down -v && docker-compose up -d`

3. **Seeder exception**
   - Look for stack traces after "🌱 Seeding"
   - Check entity relationships and constraints

### Data Not Appearing

**Verify seeder executed:**
```bash
docker logs vehicle-service | grep "Seeding"
```

**Expected Output:**
- `🌱 Checking if database needs seeding...`
- Either: `🌱 Seeding database with sample data...` (first run)
- Or: `ℹ️  Database already contains data. Skipping seed.` (subsequent runs)

**If no seeding messages appear:**
1. Check Program.cs initialization code
2. Verify DatabaseSeeder.cs is in correct namespace
3. Check for compilation errors: `docker-compose logs vehicle-service`

### Port Conflicts

```bash
# Check what's using port 7001 or 5433
netstat -ano | findstr :7001
netstat -ano | findstr :5433

# Change ports in docker-compose.yml if needed
```

### Reset Everything

```bash
# Complete reset
cd src/vehicleService
docker-compose down -v --remove-orphans
docker-compose build --no-cache
docker-compose up -d
```

---

## 🎓 Benefits of This Approach

1. **Automatic Initialization**
   - No manual SQL scripts needed
   - Runs on every startup

2. **Type Safety**
   - Uses C# entities
   - Compile-time checking
   - IntelliSense support

3. **Maintainability**
   - Changes to entities automatically reflected
   - Easy to update sample data
   - Version controlled with code

4. **Idempotent**
   - Safe to run multiple times
   - No duplicate data
   - Fast startup when data exists

5. **Integration**
   - Works seamlessly with EF migrations
   - Consistent with .NET best practices
   - Easy to test

6. **Modern .NET Pattern**
   - Async/await throughout
   - Dependency injection
   - Structured logging

---

## 🔧 Customizing Sample Data

### Adding More Vehicles

Edit `DatabaseSeeder.cs`:

```csharp
var vehicle4 = new Vehicle
{
    Id = Guid.NewGuid(),
    Make = "Mercedes",
    Model = "Sprinter",
    Year = 2022,
    LicensePlate = "DEF-4567",
    Status = (int)VehicleStatus.Active,
    // ... more properties
};

await context.Vehicles.AddRangeAsync(vehicle1, vehicle2, vehicle3, vehicle4);
```

### Changing Idempotency Check

```csharp
// Check specific criteria instead of just Any()
if (await context.Vehicles.Where(v => v.Make == "Ford").AnyAsync())
{
    // Custom logic
}
```

### Disabling Seeder in Production

```csharp
// In Program.cs
if (app.Environment.IsDevelopment())
{
    await DatabaseSeeder.SeedAsync(db);
}
```

---

## 📝 Files Modified/Created

### Created
- ✅ `VehicleService.Infrastructure/Data/DatabaseSeeder.cs` (171 lines)
- ✅ `SEEDER_IMPLEMENTATION.md` (this file)

### Modified
- ✅ `VehicleService.Api/Program.cs` (added initialization section)
- ✅ `docker-compose.yml` (enhanced configuration)
- ✅ `Dockerfile` (added health check)

### Unchanged
- ✅ Entity classes (Vehicle, MaintenanceRecord, VehicleStatusHistory)
- ✅ VehicleDbContext
- ✅ Migrations

---

## ✅ Production Considerations

### Security
```csharp
// Use configuration for sensitive data
var adminPassword = configuration["AdminPassword"];

// Don't seed in production
if (!app.Environment.IsProduction())
{
    await DatabaseSeeder.SeedAsync(db);
}
```

### Performance
```csharp
// Bulk insert for large datasets
await context.BulkInsertAsync(vehicles);

// Use transactions
using var transaction = await context.Database.BeginTransactionAsync();
try
{
    // Seeding operations
    await transaction.CommitAsync();
}
catch
{
    await transaction.RollbackAsync();
    throw;
}
```

### Monitoring
```csharp
// Add metrics
logger.LogInformation("Seeded {Count} vehicles in {Duration}ms", 
    vehicleCount, stopwatch.ElapsedMilliseconds);
```

---

## 🚀 Next Steps

1. **Start the service:** `docker-compose up -d`
2. **Verify seeding:** `docker logs vehicle-service`
3. **Test API:** `curl http://localhost:7001/api/vehicle`
4. **Access database:** Via pgAdmin (port 5050) or psql
5. **Develop features:** Sample data is ready for testing!

---

## 📚 Additional Resources

- **Root Database Guide:** `../../DATABASE_SETUP.md`
- **Entity Framework Docs:** https://learn.microsoft.com/en-us/ef/core/
- **PostgreSQL with EF:** https://www.npgsql.org/efcore/

---

## Summary

The Vehicle Service now features:
- ✅ Automatic database seeding on every startup
- ✅ Idempotent operation (safe to run multiple times)
- ✅ Type-safe C# entities
- ✅ Comprehensive logging
- ✅ Docker integration with health checks
- ✅ CORS and network isolation
- ✅ Production-ready architecture

**The seeder ensures your database is always ready for development!** 🎉
