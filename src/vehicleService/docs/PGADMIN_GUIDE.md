# pgAdmin Access Guide - Vehicle Service

## Overview
This guide explains how to access and configure pgAdmin for the Vehicle Service PostgreSQL database.

## Starting pgAdmin

To start the pgAdmin container along with the vehicle service:

```bash
docker-compose --profile admin up -d
```

This will start:
- `postgres-vehicle` - PostgreSQL database (port 5433 on host)
- `vehicle-service` - Vehicle API service (port 7001 on host)
- `pgadmin-vehicle` - pgAdmin web interface (port 5050 on host)

## Accessing pgAdmin

### Step 1: Open pgAdmin Web Interface

Open your web browser and navigate to:
```
http://localhost:5050
```

> **Note**: Wait 10-15 seconds after starting the container for pgAdmin to fully initialize.

### Step 2: Login to pgAdmin

Use the following credentials:

| Field | Value |
|-------|-------|
| **Email Address** | `admin@admin.com` |
| **Password** | `admin123` |

## Connecting to Vehicle Database

### Step 3: Register PostgreSQL Server

Once logged in to pgAdmin:

1. **Right-click** on "Servers" in the left sidebar
2. Select **"Register" → "Server..."**

### Step 4: General Tab Configuration

| Field | Value |
|-------|-------|
| **Name** | `Vehicle Database` (or any descriptive name) |
| **Server group** | Servers (default) |
| **Connect now?** | ✓ Checked |

### Step 5: Connection Tab Configuration

| Field | Value | Notes |
|-------|-------|-------|
| **Host name/address** | `postgres-vehicle` | ⚠️ Use container name, NOT `localhost` |
| **Port** | `5432` | Internal Docker port |
| **Maintenance database** | `vehicle_db` | The database name |
| **Username** | `postgres` | Database user |
| **Password** | `postgres` | Database password |
| **Save password?** | ✓ Checked | Remember credentials |

### Step 6: Save Configuration

Click **"Save"** to establish the connection.

## Database Structure

After connecting, you can explore:

### Tables
- **vehicles** - Main vehicle information
- **service_records** - Vehicle service history
- **__EFMigrationsHistory** - Entity Framework migration tracking

### Sample Data
The database is automatically seeded with sample data including:
- Multiple vehicle records with various makes, models, and years
- Associated service records for maintenance tracking
- Realistic mileage and status information

## Common Operations

### Viewing Data
1. Expand: **Servers → Vehicle Database → Databases → vehicle_db → Schemas → public → Tables**
2. Right-click on a table (e.g., `vehicles`)
3. Select **"View/Edit Data" → "All Rows"**

### Running SQL Queries
1. Right-click on **vehicle_db**
2. Select **"Query Tool"**
3. Write your SQL query
4. Click the ▶️ (Execute) button or press F5

Example queries:
```sql
-- View all vehicles
SELECT * FROM vehicles;

-- View all service records
SELECT * FROM service_records;

-- Count vehicles by status
SELECT status, COUNT(*) as count 
FROM vehicles 
GROUP BY status;

-- View vehicles with their service records
SELECT v.vin, v.make, v.model, v.year, s.service_type, s.service_date
FROM vehicles v
LEFT JOIN service_records s ON v.id = s.vehicle_id
ORDER BY s.service_date DESC;
```

## Troubleshooting

### Issue: Cannot connect to localhost:5050
**Solution**: Wait 10-15 seconds for the container to fully start. Check container status:
```bash
docker ps | grep pgadmin-vehicle
```

### Issue: "Unable to connect to server" error
**Possible causes**:
1. **Wrong hostname**: Must use `postgres-vehicle`, not `localhost` or `127.0.0.1`
2. **Wrong port**: Use `5432` (internal), not `5433` (external)
3. **Wrong database name**: Must be `vehicle_db`, not `postgres`
4. **PostgreSQL not ready**: Wait for the database container to be healthy

### Issue: Login credentials don't work
**Solution**: Verify you're using:
- Email: `admin@admin.com`
- Password: `admin123`

### Issue: Container keeps restarting
**Solution**: Check container logs:
```bash
docker logs pgadmin-vehicle
```

## Direct PostgreSQL Access (Alternative)

If you prefer command-line access instead of pgAdmin:

### From Host Machine (Windows)
```bash
# Connect using host port 5433
docker exec -it postgres-vehicle psql -U postgres -d vehicle_db
```

### Common psql Commands
```sql
\dt              -- List all tables
\d vehicles      -- Describe vehicles table
\l               -- List all databases
\q               -- Quit
```

## Stopping pgAdmin

To stop the pgAdmin container while keeping the database and service running:

```bash
docker stop pgadmin-vehicle
docker rm pgadmin-vehicle
```

To stop all services:
```bash
docker-compose down
```

To stop and remove volumes (⚠️ deletes all data):
```bash
docker-compose down -v
```

## Security Notes

⚠️ **Important**: The current configuration is for **development only**. For production:

1. **Change default passwords**:
   - pgAdmin: `PGADMIN_DEFAULT_PASSWORD`
   - PostgreSQL: `POSTGRES_PASSWORD`

2. **Use environment variables** instead of hardcoded credentials

3. **Enable SSL/TLS** for database connections

4. **Restrict network access** using Docker network policies

5. **Use secrets management** (Docker secrets, Kubernetes secrets, etc.)

## Port Reference

| Service | Container Port | Host Port | URL |
|---------|---------------|-----------|-----|
| Vehicle API | 8080 | 7001 | http://localhost:7001 |
| PostgreSQL | 5432 | 5433 | localhost:5433 |
| pgAdmin | 80 | 5050 | http://localhost:5050 |

## Related Documentation

- [Vehicle Service API Documentation](./README.md)
- [Docker Compose Configuration](../docker-compose.yml)
- [Entity Framework Migrations](./VehicleService/VehicleService.Infrastructure/Migrations/)
- [Database Seeder](./VehicleService/VehicleService.Infrastructure/Data/DatabaseSeeder.cs)

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review container logs: `docker logs <container-name>`
3. Verify all containers are healthy: `docker ps`
4. Consult the main project README

