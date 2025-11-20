# Vehicle Service (.NET 8 API)

Fleet Management Vehicle Service - Manages vehicle inventory, tracking, and service records.

## Quick Start

### 🚀 **Easiest Way** (One Command Does Everything!)

**Windows (PowerShell):**
```powershell
cd ..
.\setup-and-run.ps1
```

**Linux/Mac:**
```bash
cd ..
chmod +x setup-and-run.sh
./setup-and-run.sh
```

This automatically:
- Checks .NET SDK
- Restores NuGet packages
- Starts PostgreSQL (if not running)
- Runs database migrations
- Starts the .NET application

**Perfect for:** Fresh clone, first-time setup, or daily development!

**📚 For troubleshooting:** See `../LOCAL_DEVELOPMENT_GUIDE.md`

---





### Alternative: Docker Compose

```bash
# Start the service with Docker
docker-compose up -d

# Verify it's running
curl http://localhost:7001/health
```

**Service URL:** http://localhost:7001  
**Database:** PostgreSQL on port 5433  
**Swagger UI:** http://localhost:7001 (root URL)

---

## Features

- ✅ RESTful API for vehicle management
- ✅ Automatic database migrations with Entity Framework Core
- ✅ Automatic database seeding with sample data
- ✅ PostgreSQL database
- ✅ Docker containerization
- ✅ Health check endpoints
- ✅ Swagger/OpenAPI documentation
- ✅ CORS support

---

## Prerequisites

- Docker & Docker Compose
- .NET 8 SDK (for local development)

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
# Navigate to the API project
cd VehicleService/VehicleService.Api

# Restore dependencies
dotnet restore

# Run migrations
dotnet ef database update --project ../VehicleService.Infrastructure

# Run the service
dotnet run
```

---

## API Endpoints

### Vehicle Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| GET | `/api/vehicles` | List all vehicles |
| GET | `/api/vehicles/{id}` | Get specific vehicle |
| POST | `/api/vehicles` | Create new vehicle |
| PUT | `/api/vehicles/{id}` | Update vehicle |
| DELETE | `/api/vehicles/{id}` | Delete vehicle |
| GET | `/api/vehicles/{id}/status` | Get vehicle status |
| PATCH | `/api/vehicles/{id}/status` | Update vehicle status |

### Service Record Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/vehicles/{vehicleId}/services` | List service records for vehicle |
| GET | `/api/services/{id}` | Get specific service record |
| POST | `/api/services` | Create new service record |
| PUT | `/api/services/{id}` | Update service record |
| DELETE | `/api/services/{id}` | Delete service record |

### Documentation
- **Swagger UI:** http://localhost:7001 (configured at root URL)
- **OpenAPI JSON:** http://localhost:7001/swagger/v1/swagger.json

---

## Database

### Connection Info
- **Host:** localhost:5433
- **Database:** vehicle_db
- **User:** postgres
- **Password:** postgres

### Access Database

#### Command Line (psql)
```bash
docker exec -it postgres-vehicle psql -U postgres -d vehicle_db
```

#### Web Interface (pgAdmin)
For a graphical database management interface, see **[PGADMIN_GUIDE.md](./PGADMIN_GUIDE.md)** for detailed setup instructions.

Quick start:
```bash
docker-compose --profile admin up -d
```
Then open: **http://localhost:5050** (login: `admin@admin.com` / `admin123`)

### Sample Data
The database is automatically seeded with sample vehicles and service records:
- Multiple vehicles with various makes, models, and years
- Service records for maintenance tracking
- Realistic mileage and status information

---

## Configuration

### Environment Variables

Set in `../docker-compose.yml` or `.env`:

```env
ASPNETCORE_ENVIRONMENT=Development
ConnectionStrings__DefaultConnection=Host=postgres-vehicle;Port=5432;Database=vehicle_db;Username=postgres;Password=postgres
ASPNETCORE_URLS=http://+:8080
CORS_ORIGINS=*
```

### appsettings.json

Located in `VehicleService.Api/appsettings.json`:
```json
{
  "ConnectionStrings": {
    "DefaultConnection": "Host=localhost;Port=5433;Database=vehicle_db;Username=postgres;Password=postgres"
  },
  "Logging": {
    "LogLevel": {
      "Default": "Information",
      "Microsoft.AspNetCore": "Warning"
    }
  }
}
```

---

## Docker Services

| Service | Container | Port | Description |
|---------|-----------|------|-------------|
| vehicle-service | vehicle-service | 7001 | .NET 8 API |
| postgres-vehicle | postgres-vehicle | 5433 | PostgreSQL 16 |
| pgadmin-vehicle | pgadmin-vehicle | 5050 | DB Admin (optional) |

### Start with pgAdmin
```bash
docker-compose --profile admin up -d
```
Access at: http://localhost:5050
- Email: `admin@admin.com`
- Password: `admin123`

📚 **See [PGADMIN_GUIDE.md](./PGADMIN_GUIDE.md) for complete setup instructions**

---

## Project Structure

```
vehicleService/
├── VehicleService/
│   ├── VehicleService.Api/          # Web API layer
│   │   ├── Controllers/             # API endpoints
│   │   ├── Program.cs               # Application entry point
│   │   ├── appsettings.json         # Configuration
│   │   └── Dockerfile               # Docker image
│   ├── VehicleService.Application/  # Business logic layer
│   │   ├── Services/                # Application services
│   │   ├── DTOs/                    # Data transfer objects
│   │   └── Interfaces/              # Service contracts
│   ├── VehicleService.Domain/       # Domain layer
│   │   ├── Entities/                # Domain models
│   │   └── Interfaces/              # Repository contracts
│   └── VehicleService.Infrastructure/ # Data access layer
│       ├── Data/                    # DbContext & seeder
│       ├── Repositories/            # Repository implementations
│       └── Migrations/              # EF Core migrations
├── docs/                            # Documentation
│   ├── README.md
│   ├── PGADMIN_GUIDE.md
│   ├── SEEDER_IMPLEMENTATION.md
│   └── vehicle-service-db-schema.txt
├── docker-compose.yml               # Docker services
```

---

## Development

### Rebuild After Code Changes
```bash
docker-compose up --build
```

### Database Migrations

```bash
# Add new migration
cd VehicleService/VehicleService.Api
dotnet ef migrations add MigrationName --project ../VehicleService.Infrastructure

# Apply migrations
dotnet ef database update --project ../VehicleService.Infrastructure

# Remove last migration
dotnet ef migrations remove --project ../VehicleService.Infrastructure
```

### Run Tests
```bash
dotnet test
dotnet test --collect:"XPlat Code Coverage"
```

---

## Troubleshooting

### Port Already in Use
Edit `../docker-compose.yml` to use different ports.

### Database Connection Failed
```bash
# Check if PostgreSQL is running
docker ps

# View logs
docker-compose logs postgres-vehicle

# Wait for health check (~10 seconds)
docker-compose logs -f vehicle-service
```

### Migration Issues
```bash
# Reset database (removes all data!)
docker-compose down -v
docker-compose up -d

# Migrations will run automatically on startup
```

### Cannot Access Swagger
**Note:** Swagger UI is at the root URL: **http://localhost:7001** (not `/swagger`)

Ensure the service is running:
```bash
curl http://localhost:7001/
```

---

## Integration

This service works alongside the Maintenance Service:
- **Vehicle Service:** Port 7001, PostgreSQL 5433
- **Maintenance Service:** Port 5001, PostgreSQL 5434

Both services can run simultaneously without conflicts.

---

## Documentation

- **pgAdmin Setup & Connection Guide:** [PGADMIN_GUIDE.md](./PGADMIN_GUIDE.md)
- **API Documentation (Swagger):** Available at **http://localhost:7001** when running (opens at root URL)
- **Database Seeder:** See `VehicleService/VehicleService.Infrastructure/Data/DatabaseSeeder.cs`

---

## Production Deployment

### Security Checklist
- [ ] Change default PostgreSQL password
- [ ] Configure CORS_ORIGINS to specific domains
- [ ] Enable HTTPS
- [ ] Set up database backups
- [ ] Configure logging and monitoring
- [ ] Use user secrets or key vault for sensitive data
- [ ] Enable authentication/authorization

### Environment Variables
```env
ASPNETCORE_ENVIRONMENT=Production
ConnectionStrings__DefaultConnection=Host=<host>;Port=<port>;Database=vehicle_db;Username=<user>;Password=<secure-password>
ASPNETCORE_URLS=https://+:443;http://+:80
CORS_ORIGINS=https://yourdomain.com
```

### HTTPS Configuration
Update `VehicleService/VehicleService.Api/Dockerfile` and add SSL certificate:
```dockerfile
EXPOSE 443
```

---

## License

MIT License

