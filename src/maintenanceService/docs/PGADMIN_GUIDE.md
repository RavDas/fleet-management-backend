# pgAdmin Access Guide - Maintenance Service

## Overview
This guide explains how to access and configure pgAdmin for the Maintenance Service PostgreSQL database.

## Starting pgAdmin

To start the pgAdmin container along with the maintenance service:

```bash
docker-compose --profile admin up -d
```

This will start:
- `postgres-maintenance` - PostgreSQL database (port 5433 on host)
- `maintenance-service` - Maintenance API service (port 5001 on host)
- `pgadmin-maintenance` - pgAdmin web interface (port 5051 on host)

## Accessing pgAdmin

### Step 1: Open pgAdmin Web Interface

Open your web browser and navigate to:
```
http://localhost:5051
```

> **Note**: Wait 10-15 seconds after starting the container for pgAdmin to fully initialize.

### Step 2: Login to pgAdmin

Use the following credentials:

| Field | Value |
|-------|-------|
| **Email Address** | `admin@admin.com` |
| **Password** | `admin123` |

## Connecting to Maintenance Database

### Step 3: Register PostgreSQL Server

Once logged in to pgAdmin:

1. **Right-click** on "Servers" in the left sidebar
2. Select **"Register" → "Server..."**

### Step 4: General Tab Configuration

| Field | Value |
|-------|-------|
| **Name** | `Maintenance Database` (or any descriptive name) |
| **Server group** | Servers (default) |
| **Connect now?** | ✓ Checked |

### Step 5: Connection Tab Configuration

| Field | Value | Notes |
|-------|-------|-------|
| **Host name/address** | `postgres-maintenance` | ⚠️ Use container name, NOT `localhost` |
| **Port** | `5432` | Internal Docker port |
| **Maintenance database** | `maintenance_db` | The database name |
| **Username** | `postgres` | Database user |
| **Password** | `postgres` | Database password |
| **Save password?** | ✓ Checked | Remember credentials |

### Step 6: Save Configuration

Click **"Save"** to establish the connection.

## Database Structure

After connecting, you can explore:

### Tables
- **maintenance_items** - Main maintenance records and scheduling

### Sample Data
The database is automatically seeded with sample data including:
- Maintenance items with various statuses (overdue, due_soon, scheduled, in_progress, completed)
- Different priority levels (low, medium, high, critical)
- Associated vehicle IDs, cost estimates, and technician assignments
- Realistic due dates and mileage information

### Indexes
- `idx_vehicle_id` - Fast lookups by vehicle
- `idx_status` - Fast filtering by status
- `idx_priority` - Fast filtering by priority
- `idx_due_date` - Fast date-based queries
- `idx_created_at` - Chronological sorting

### Triggers
- **update_maintenance_items_updated_at** - Automatically updates `updated_at` timestamp on record modification

## Common Operations

### Viewing Data
1. Expand: **Servers → Maintenance Database → Databases → maintenance_db → Schemas → public → Tables**
2. Right-click on `maintenance_items`
3. Select **"View/Edit Data" → "All Rows"**

### Running SQL Queries
1. Right-click on **maintenance_db**
2. Select **"Query Tool"**
3. Write your SQL query
4. Click the ▶️ (Execute) button or press F5

Example queries:
```sql
-- View all maintenance items
SELECT * FROM maintenance_items;

-- View overdue maintenance
SELECT * FROM maintenance_items 
WHERE status = 'overdue' 
ORDER BY priority DESC, due_date ASC;

-- Count maintenance by status
SELECT status, COUNT(*) as count 
FROM maintenance_items 
GROUP BY status;

-- View high priority items
SELECT id, vehicle_id, type, status, priority, due_date, estimated_cost
FROM maintenance_items 
WHERE priority IN ('high', 'critical')
ORDER BY due_date ASC;

-- Calculate total costs by vehicle
SELECT vehicle_id, 
       SUM(estimated_cost) as total_estimated,
       SUM(actual_cost) as total_actual,
       COUNT(*) as maintenance_count
FROM maintenance_items
GROUP BY vehicle_id;

-- Upcoming maintenance (next 7 days)
SELECT * FROM maintenance_items
WHERE due_date BETWEEN CURRENT_DATE AND CURRENT_DATE + INTERVAL '7 days'
  AND status NOT IN ('completed', 'cancelled')
ORDER BY due_date ASC;
```

## Troubleshooting

### Issue: Cannot connect to localhost:5051
**Solution**: Wait 10-15 seconds for the container to fully start. Check container status:
```bash
docker ps | grep pgadmin-maintenance
```

### Issue: "Unable to connect to server" error
**Possible causes**:
1. **Wrong hostname**: Must use `postgres-maintenance`, not `localhost` or `127.0.0.1`
2. **Wrong port**: Use `5432` (internal), not `5433` (external)
3. **Wrong database name**: Must be `maintenance_db`, not `postgres`
4. **PostgreSQL not ready**: Wait for the database container to be healthy

### Issue: Login credentials don't work
**Solution**: Verify you're using:
- Email: `admin@admin.com`
- Password: `admin123`

### Issue: Container keeps restarting
**Solution**: Check container logs:
```bash
docker logs pgadmin-maintenance
```

## Direct PostgreSQL Access (Alternative)

If you prefer command-line access instead of pgAdmin:

### From Host Machine (Windows)
```bash
# Connect using host port 5433
docker exec -it postgres-maintenance psql -U postgres -d maintenance_db
```

### Common psql Commands
```sql
\dt              -- List all tables
\d maintenance_items  -- Describe maintenance_items table
\di              -- List all indexes
\l               -- List all databases
\df              -- List all functions
\q               -- Quit
```

## Stopping pgAdmin

To stop the pgAdmin container while keeping the database and service running:

```bash
docker stop pgadmin-maintenance
docker rm pgadmin-maintenance
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

6. **Implement proper authentication** for the API endpoints

## Port Reference

| Service | Container Port | Host Port | URL |
|---------|---------------|-----------|-----|
| Maintenance API | 5001 | 5001 | http://localhost:5001 |
| PostgreSQL | 5432 | 5433 | localhost:5433 |
| pgAdmin | 80 | 5051 | http://localhost:5051 |

## API Endpoints

With the service running, you can access:
- **Swagger UI**: http://localhost:5001/docs
- **API Base**: http://localhost:5001/api/maintenance

## Related Documentation

- [Maintenance Service API Documentation](./README.md)
- [Docker Compose Configuration](../docker-compose.yml)
- [Database Schema](./init-db.sql)
- [Database Seeder](./app/utils/database_seeder.py)
- [Migration Script](./migrate-sqlite-to-postgres.py)

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review container logs: `docker logs <container-name>`
3. Verify all containers are healthy: `docker ps`
4. Check Flask application logs: `docker logs maintenance-service`
5. Consult the main project README

