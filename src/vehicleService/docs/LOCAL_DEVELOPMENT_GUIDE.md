# Local Development Guide - Vehicle Service

Quick reference for local development tasks, troubleshooting, and advanced configuration for the .NET Vehicle Service.

---

## 🚀 Quick Start

**Just run this ONE command in your Bash terminal:**

```bash
chmod +x setup-and-run.sh
./setup-and-run.sh
```

The script automatically handles:
- ✅ .NET SDK verification
- ✅ NuGet package restoration
- ✅ Database startup
- ✅ Database migrations
- ✅ .NET application startup

---

## 🛑 Stopping the Service

Press `Ctrl+C` in the terminal running the script.

**Optionally stop the database:**
```bash
docker-compose down
```

---

## 🔍 Troubleshooting

### ❌ "Port 8479 is already in use"

**Cause:** Another process is using port 8479.

**Solution - Find and kill the process:**
```bash
# Find process using port 8479
lsof -i :8479

# Kill the process
kill -9 <PID_NUMBER>
```
---

### ❌ ".NET SDK is not installed"

**Cause:** .NET 9 SDK not installed or not in PATH.

**Solution:**

1. Download and install .NET 9 SDK from: https://dotnet.microsoft.com/download
2. Verify installation:
   ```bash
   dotnet --version
   ```
3. Restart your terminal
4. Run the script again

---

### ❌ NuGet restore fails

**Cause:** Network issues, NuGet cache corruption, or missing packages.

**Solution:**
```bash
# Clear NuGet cache
dotnet nuget locals all --clear

# Restore packages manually
cd VehicleService/VehicleService.Api
dotnet restore

# If still fails, check NuGet sources
dotnet nuget list source
```

---

### ❌ Database migration errors

**Cause:** Migration mismatch or database corruption.

**Solution 1 - Let the app handle it:**
The app automatically runs migrations on startup (see `Program.cs` line 116).

**Solution 2 - Reset database:**
```bash
# Stop and remove database (WARNING: deletes all data!)
docker-compose down -v

# Start fresh
./setup-and-run.sh
```

**Solution 3 - Run migrations manually:**
```bash
cd VehicleService/VehicleService.Api
dotnet ef database update --project ../VehicleService.Infrastructure
```

---

### ❌ "Hot reload not working" or changes not reflecting

**Cause:** .NET hot reload failed or need full rebuild.

**Solution:**

1. Press `Ctrl+C` to stop
2. Run `./setup-and-run.sh` again

Or rebuild explicitly:
```bash
cd VehicleService/VehicleService.Api
dotnet build
dotnet run
```

---

### ❌ Swagger UI not loading at http://localhost:8479

**Cause:** Application not running or wrong URL.

**Solutions:**

1. **Make sure app is running:**
   ```bash
   curl http://localhost:8479/health
   ```

2. **Check if running in Development mode:**
   Swagger only runs in Development environment.
   ```bash
   export ASPNETCORE_ENVIRONMENT="Development"
   ```

3. **Swagger is at root URL:**
   Visit http://localhost:8479 (not /swagger)

---

### ❌ Database connection fails after restart

**Cause:** Database container stopped or connection string issue.

**Solution:**
```bash
# Check container status
docker ps

# Check database logs
docker logs postgres-vehicle

# Restart database
docker-compose restart postgres-vehicle

# If corrupted, reset completely
docker-compose down -v
./setup-and-run.sh
```

---

## 🗄️ Database Access

### Option 1: Command Line (psql)

```bash
# Connect to PostgreSQL
docker exec -it postgres-vehicle psql -U postgres -d vehicle_db
```

**Useful SQL commands:**
```sql
-- List all tables
\dt

-- View all vehicles
SELECT * FROM "Vehicles";

-- Count vehicles by status
SELECT "Status", COUNT(*) FROM "Vehicles" GROUP BY "Status";

-- View vehicles with mileage
SELECT "Id", "Make", "Model", "Year", "VehicleIdentificationNumber", "CurrentMileage" 
FROM "Vehicles" 
ORDER BY "CurrentMileage" DESC 
LIMIT 10;

-- View maintenance records
SELECT * FROM "MaintenanceRecords";

-- Delete all data (WARNING!)
TRUNCATE TABLE "Vehicles", "MaintenanceRecords", "VehicleStatusHistory" CASCADE;

-- Exit
\q
```

### Option 2: pgAdmin (Web GUI)

```bash
# Start pgAdmin container
docker-compose --profile admin up -d

# Access at: http://localhost:5050
# Email: admin@admin.com
# Password: admin123
```

**First-time setup in pgAdmin:**
1. Click "Add New Server"
2. General tab → Name: `Vehicle DB`
3. Connection tab:
   - Host: `postgres-vehicle`
   - Port: `5432`
   - Database: `vehicle_db`
   - Username: `postgres`
   - Password: `postgres`
4. Click "Save"

See `docs/PGADMIN_GUIDE.md` for detailed instructions.

---

## ⚙️ Configuration

### Connection String

**Local Development** (edit `appsettings.Development.json`):
```json
{
  "ConnectionStrings": {
    "DefaultConnection": "Host=localhost;Port=7433;Database=vehicle_db;Username=postgres;Password=postgres"
  }
}
```

**Docker** (uses environment variable in `docker-compose.yml`):
```yaml
ConnectionStrings__DefaultConnection: "Host=postgres-vehicle;Port=5432;Database=vehicle_db;Username=postgres;Password=postgres"
```

### CORS Configuration

Edit `Program.cs` or set environment variable:
```bash
export CORS_ORIGINS="http://localhost:3000,http://localhost:5173"
```

### Logging Level

Edit `appsettings.Development.json`:
```json
{
  "Logging": {
    "LogLevel": {
      "Default": "Information",
      "Microsoft.AspNetCore": "Warning",
      "Microsoft.EntityFrameworkCore.Database.Command": "Information"
    }
  }
}
```

---

## 🔧 Manual Development (Without Script)

If you prefer manual control or the script isn't working:

### Terminal 1: Database
```bash
cd /path/to/vehicleService
docker-compose up postgres-vehicle
# Keep running
```

### Terminal 2: .NET App
```bash
cd /path/to/vehicleService/VehicleService/VehicleService.Api
dotnet restore
dotnet run
# Keep running
```

---

## 💡 Development Tips

### 1. Hot Reload is Enabled
.NET 9 has hot reload by default:
- Make changes to `.cs` files
- Save
- App automatically reloads (no restart needed!)

You'll see:
```
Hot reload of changes succeeded.
```

### 2. Use Swagger UI for API Testing
Visit http://localhost:8479
- Test all endpoints interactively
- See request/response schemas
- Automatically generated from your code

### 3. View Logs in Real-Time
```bash
# .NET app logs show in the terminal
# Shows requests, EF Core queries, errors

# Database logs
docker logs -f postgres-vehicle
```

### 4. Entity Framework Commands

```bash
cd VehicleService/VehicleService.Api

# Add new migration
dotnet ef migrations add MigrationName --project ../VehicleService.Infrastructure

# Apply migrations
dotnet ef database update --project ../VehicleService.Infrastructure

# Remove last migration
dotnet ef migrations remove --project ../VehicleService.Infrastructure

# View migration history
dotnet ef migrations list --project ../VehicleService.Infrastructure

# Generate SQL script
dotnet ef migrations script --project ../VehicleService.Infrastructure
```

### 5. Quick Database Reset
```bash
# Stop everything
docker-compose down -v

# Restart (recreates database with migrations and sample data)
./setup-and-run.sh
```

### 6. Test API Endpoints
```bash
# Health check
curl http://localhost:8479/health

# Get all vehicles
curl http://localhost:8479/api/vehicles

# Get specific vehicle
curl http://localhost:8479/api/vehicles/1

# Use Swagger UI for easier testing!
# http://localhost:8479
```

---

## 📊 Useful Commands

### Docker Commands
```bash
# Check running containers
docker ps

# View database logs
docker logs postgres-vehicle

# Stop all containers
docker-compose down

# Stop and remove database data
docker-compose down -v

# Restart just the database
docker-compose restart postgres-vehicle
```

### .NET Commands
```bash
# Restore packages
dotnet restore

# Build project
dotnet build

# Run project
dotnet run

# Run with specific environment
dotnet run --environment Production

# Clean build artifacts
dotnet clean

# Watch mode (auto-restart on changes)
dotnet watch run
```

### NuGet Commands
```bash
# List installed packages
dotnet list package

# Add new package
dotnet add package PackageName

# Update package
dotnet add package PackageName --version 1.2.3

# Remove package
dotnet remove package PackageName
```

---

## 🐛 Advanced Debugging

### Enable Verbose Logging

Edit `appsettings.Development.json`:
```json
{
  "Logging": {
    "LogLevel": {
      "Default": "Debug",
      "Microsoft": "Debug",
      "Microsoft.EntityFrameworkCore.Database.Command": "Information"
    }
  }
}
```

### Debug with Visual Studio / VS Code

**Visual Studio:**
1. Open `VehicleService.sln`
2. Press F5 to debug

**VS Code:**
1. Open `vehicleService` folder
2. Install C# Dev Kit extension
3. Press F5 to debug

### Breakpoints

Add breakpoints in your `.cs` files and use debugger to step through code.

### Check Database Connection
```csharp
// In your controller or service
var canConnect = await _context.Database.CanConnectAsync();
```

---

## 📝 Project Structure

```
vehicleService/
├── setup-and-run.sh            # Main script
├── docker-compose.yml          # Docker services
│
├── VehicleService/
│   ├── VehicleService.Api/     # Web API (entry point)
│   │   ├── Controllers/        # API endpoints
│   │   ├── Program.cs          # App configuration
│   │   ├── appsettings.json    # Configuration
│   │   └── Dockerfile
│   │
│   ├── VehicleService.Application/  # Business logic
│   │   ├── Services/
│   │   ├── DTOs/
│   │   └── Interfaces/
│   │
│   ├── VehicleService.Domain/       # Domain models
│   │   └── Entities/
│   │
│   └── VehicleService.Infrastructure/  # Data access
│       ├── Data/               # DbContext, Seeder
│       ├── Repositories/
│       └── Migrations/         # EF migrations
│
└── docs/                       # Documentation
    ├── README.md
    ├── PGADMIN_GUIDE.md
    └── SEEDER_IMPLEMENTATION.md
```

---

## 🚀 Quick Reference Card

| Task | Command |
|------|---------|
| **Start everything** | `./setup-and-run.sh` |
| **Stop .NET app** | `Ctrl+C` |
| **Stop database** | `docker-compose down` |
| **View logs** | Check terminal output |
| **Database CLI** | `docker exec -it postgres-vehicle psql -U postgres -d vehicle_db` |
| **Swagger docs** | http://localhost:8479 |
| **Health check** | http://localhost:8479/health |
| **Add migration** | `dotnet ef migrations add Name --project ../VehicleService.Infrastructure` |
| **Update database** | `dotnet ef database update --project ../VehicleService.Infrastructure` |
| **Reset database** | `docker-compose down -v` then restart script |
| **Watch mode** | `dotnet watch run` |

---

## 🆘 Still Having Issues?

1. **Check if Docker Desktop is running**
2. **Make sure .NET 9 SDK is installed** (`dotnet --version`)
3. **Make sure no other service is using port 8479 or 7433**
4. **Try running commands manually** (see Manual Development section)
5. **Check error messages carefully** - they usually indicate the problem
6. **Reset everything:**
   ```bash
   docker-compose down -v
   dotnet clean
   ./setup-and-run.sh
   ```

---

## 📚 Additional Resources

- **Main Documentation:** `docs/README.md`
- **Database GUI Setup:** `docs/PGADMIN_GUIDE.md`
- **Seeder Info:** `docs/SEEDER_IMPLEMENTATION.md`
- **Docker Compose Config:** `docker-compose.yml`
- **.NET Configuration:** `VehicleService/VehicleService.Api/appsettings.json`

---

**Happy coding!** 🎉
