# pgAdmin Access Guide - Driver Service

## Overview
This guide explains how to access and configure pgAdmin for the Driver Service PostgreSQL database.

## Starting pgAdmin

To start the pgAdmin container along with the driver service:

```bash
docker-compose --profile admin up -d
```

This will start:
- `postgres-driver` - PostgreSQL database (port 6433 on host)
- `driver-service` - Driver API service (port 6001 on host)
- `pgadmin-driver` - pgAdmin web interface (port 5055 on host)

## Accessing pgAdmin

### Step 1: Open pgAdmin Web Interface

Open your web browser and navigate to:
```
http://localhost:5055
```

> **Note**: Wait 10-15 seconds after starting the container for pgAdmin to fully initialize.

### Step 2: Login to pgAdmin

Use the following credentials:

| Field | Value |
|-------|-------|
| **Email Address** | `admin@admin.com` |
| **Password** | `admin123` |

## Connecting to Driver Database

### Step 3: Register PostgreSQL Server

Once logged in to pgAdmin:

1. **Right-click** on "Servers" in the left sidebar
2. Select **"Register" → "Server..."**

### Step 4: General Tab Configuration

| Field | Value |
|-------|-------|
| **Name** | `Driver Database` (or any descriptive name) |
| **Server group** | Servers (default) |
| **Connect now?** | ✓ Checked |

### Step 5: Connection Tab Configuration

| Field | Value | Notes |
|-------|-------|-------|
| **Host name/address** | `postgres-driver` | ⚠️ Use container name, NOT `localhost` |
| **Port** | `5432` | Internal Docker port |
| **Maintenance database** | `driver_db` | The database name |
| **Username** | `postgres` | Database user |
| **Password** | `postgres` | Database password |
| **Save password?** | ✓ Checked | Remember credentials |

### Step 6: Save Configuration

Click **"Save"** to establish the connection.

## Database Structure

After connecting, you can explore:

### Tables
- **drivers** - Driver information
- **flyway_schema_history** - Migration history tracking

### Sample Data
The database is automatically seeded via the application on startup (if enabled) or you can manually insert data.

## Common Operations

### Viewing Data
1. Expand: **Servers → Driver Database → Databases → driver_db → Schemas → public → Tables**
2. Right-click on `drivers`
3. Select **"View/Edit Data" → "All Rows"**

### Running SQL Queries
1. Right-click on **driver_db**
2. Select **"Query Tool"**
3. Write your SQL query
4. Click the ▶️ (Execute) button or press F5

Example queries:
```sql
-- View all drivers
SELECT * FROM drivers;

-- Find active drivers
SELECT * FROM drivers WHERE status = 'ACTIVE';

-- Count drivers by license type
SELECT license_type, COUNT(*) as count 
FROM drivers 
GROUP BY license_type;
```

## Troubleshooting

### Issue: Cannot connect to localhost:5055
**Solution**: Wait 10-15 seconds for the container to fully start. Check container status:
```bash
docker ps | grep pgadmin-driver
```

### Issue: "Unable to connect to server" error
**Possible causes**:
1. **Wrong hostname**: Must use `postgres-driver`, not `localhost`
2. **Wrong port**: Use `5432` (internal), not `6433` (external)
3. **Wrong database name**: Must be `driver_db`
4. **PostgreSQL not ready**: Wait for the database container to be healthy

### Issue: Login credentials don't work
**Solution**: Verify you're using:
- Email: `admin@admin.com`
- Password: `admin123`

## Direct PostgreSQL Access (Alternative)

If you prefer command-line access instead of pgAdmin:

### From Host Machine
```bash
# Connect using host port 6433
psql -h localhost -p 6433 -U postgres -d driver_db
# OR via Docker
docker exec -it postgres-driver psql -U postgres -d driver_db
```

## Stopping pgAdmin

To stop the pgAdmin container:

```bash
docker stop pgadmin-driver
docker rm pgadmin-driver
```

To stop all services:
```bash
docker-compose down
```

## Port Reference

| Service | Container Port | Host Port | URL |
|---------|---------------|-----------|-----|
| Driver API | 8080 | 6001 | http://localhost:6001 |
| PostgreSQL | 5432 | 6433 | localhost:6433 |
| pgAdmin | 80 | 5055 | http://localhost:5055 |

## Support

For issues:
1. Check `docker logs driver-service` for API errors.
2. Check `docker logs postgres-driver` for DB errors.
3. Consult the [Local Development Guide](./LOCAL_DEVELOPMENT_GUIDE.md).

