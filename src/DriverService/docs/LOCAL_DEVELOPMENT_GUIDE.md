# Local Development Guide - Driver Service

Quick reference for local development tasks, troubleshooting, and advanced configuration.

---

## 🚀 Quick Start

**Just run this ONE command:**

### All Platforms (Windows/Linux/Mac):
```bash
./setup-and-run.sh
```

For Git Bash on Windows or Linux/Mac, you might need to make it executable first:
```bash
chmod +x ./setup-and-run.sh
./setup-and-run.sh
```

The script automatically handles:
- ✅ Maven build (clean install)
- ✅ Database startup (PostgreSQL container)
- ✅ Waiting for database readiness
- ✅ Spring Boot application startup

---

## 🛑 Stopping the Service

Press `Ctrl+C` in the terminal running the script.

**Optionally stop the database:**
```powershell
docker-compose down
```

---

## 🔍 Troubleshooting

### ❌ "Port 8080 or 6001 is already in use"

**Cause:** Another process is using the required ports.
- **8080:** Default Spring Boot port (internal/local).
- **6001:** Docker mapped port.

**Solution 1 - Find and kill the process:**
```powershell
# Windows
netstat -ano | findstr :8080
taskkill /PID <PID_NUMBER> /F

# Linux/Mac
lsof -i :8080
kill -9 <PID_NUMBER>
```

**Solution 2 - Use a different port:**
Edit `application.yml` or set environment variable:
```bash
export SERVER_PORT=8081
./setup-and-run.sh
```

---

### ❌ "Connection refused" to Database

**Cause:** PostgreSQL container is not running or not ready.

**Solution:**
1. Check if the container is running:
   ```bash
   docker ps
   ```
2. View database logs:
   ```bash
   docker logs postgres-driver
   ```
3. Ensure `DB_HOST` is correctly set (use `localhost` for running outside Docker, `postgres-driver` for inside Docker).

---

### ❌ Maven Build Fails

**Cause:** Missing dependencies or Java version mismatch.

**Solution:**
1. Ensure you have **Java 21** installed:
   ```bash
   java -version
   ```
2. Try cleaning dependencies:
   ```bash
   mvn clean install -U
   ```

---

## 🗄️ Database Access

### Option 1: Command Line (psql)

```powershell
# Connect to PostgreSQL
docker exec -it postgres-driver psql -U postgres -d driver_db
```

**Useful SQL commands:**
```sql
-- List all tables
\dt

-- View all drivers
SELECT * FROM drivers;

-- Count drivers by status
SELECT status, COUNT(*) FROM drivers GROUP BY status;

-- Exit
\q
```

### Option 2: pgAdmin (Web GUI)

```powershell
# Start pgAdmin container
docker-compose --profile admin up -d

# Access at: http://localhost:5055
# Email: admin@admin.com
# Password: admin123
```

**First-time setup in pgAdmin:**
1. Click "Add New Server"
2. General tab → Name: `Driver DB`
3. Connection tab:
   - Host: `postgres-driver`
   - Port: `5432`
   - Database: `driver_db`
   - Username: `postgres`
   - Password: `postgres`
4. Click "Save"

See `PGADMIN_GUIDE.md` for detailed instructions.

---

## ⚙️ Environment Variables

### Default Configuration (application.yml)
```yaml
server:
  port: 8080

spring:
  datasource:
    url: jdbc:postgresql://${DB_HOST:localhost}:${DB_PORT:5432}/${DB_NAME:driver_db}
    username: ${DB_USERNAME:postgres}
    password: ${DB_PASSWORD:postgres}
```

### Customizing for Local Run
You can set these environment variables before running the jar:

```bash
export DB_HOST=localhost
export DB_PORT=6433  # Connect to Docker DB from host
export SERVER_PORT=8081
java -jar target/driver-service-1.0-SNAPSHOT.jar
```

---

## 🔧 Manual Development (Without Script)

If you prefer manual control:

### Terminal 1: Database
```powershell
docker-compose up postgres-driver
# Keep running
```

### Terminal 2: Spring Boot App
```bash
# Run with Maven wrapper (if available) or installed Maven
mvn spring-boot:run
```

---

## 💡 Development Tips

### 1. Hot Reloading
If you have `spring-boot-devtools` enabled (check pom.xml), recompiling a file in your IDE (IntelliJ/Eclipse) will trigger a fast restart.

### 2. API Documentation (Swagger UI)
Visit http://localhost:8080/swagger-ui/index.html (or port 6001 if using Docker)
- Test endpoints interactively.
- View schemas for Driver, Vehicle, and Schedule.

### 3. Database Migrations (Flyway)
- SQL scripts are in `src/main/resources/db/migration`.
- To add a change, create a new file: `V2__Description.sql`.
- Flyway automatically applies pending migrations on startup.

### 4. Quick Database Reset
```powershell
# Stop everything and remove volumes
docker-compose down -v

# Restart
./setup-and-run.sh
```

---

## 🚀 Quick Reference Card

| Task | Command |
|------|---------|
| **Start everything** | `./setup-and-run.sh` |
| **Stop App** | `Ctrl+C` |
| **Stop database** | `docker-compose down` |
| **Database CLI** | `docker exec -it postgres-driver psql -U postgres -d driver_db` |
| **API docs (Local)** | http://localhost:8080/swagger-ui/index.html |
| **API docs (Docker)**| http://localhost:6001/swagger-ui/index.html |
| **Health check** | http://localhost:8080/health |

---

## 🆘 Still Having Issues?

1. **Check Docker:** Ensure Docker Desktop is running.
2. **Check Ports:** Ensure ports 6001, 6433, and 5055 are free.
3. **Check Java:** Ensure `JAVA_HOME` is set to JDK 21.
4. **Logs:** Read the error stack trace in the terminal.

---

