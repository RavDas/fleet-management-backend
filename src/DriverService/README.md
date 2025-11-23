# Driver Service (Spring Boot API)

Fleet Management Driver Service - Manages driver records, assignments, and schedules.

## Quick Start

### 🚀 **Easiest Way** (One Command Does Everything!)

**Bash (Linux/Mac/WSL):**
```bash
chmod +x setup-and-run.sh
./setup-and-run.sh
```

This automatically:
- Builds the Maven project
- Starts PostgreSQL (if not running)
- Runs the Spring Boot application

**📚 For troubleshooting:** See `docs/LOCAL_DEVELOPMENT_GUIDE.md`

---

### Alternative: Docker Compose

```bash
# Start the service with Docker
docker-compose up -d

# Verify it's running
curl http://localhost:6001/health
```

**Service URL:** http://localhost:6001
**Swagger UI:** http://localhost:6001/swagger-ui/index.html
**Database:** PostgreSQL on port 6433

---

## Features

- ✅ RESTful API for driver management
- ✅ **Interactive Swagger/OpenAPI documentation**
- ✅ Database migrations with Flyway
- ✅ PostgreSQL database
- ✅ Docker containerization
- ✅ Health check endpoints
- ✅ JPA/Hibernate ORM

---

## Database Communications

### Communication Details
*   **Database Engine:** PostgreSQL 16
*   **Communication Method:** **Spring Data JPA / Hibernate (ORM)**
    *   Uses Object-Relational Mapping (ORM) to map Java entities to database tables.
    *   **Library:** `spring-boot-starter-data-jpa` (uses Hibernate under the hood) and `postgresql` JDBC driver.
*   **Migration Tool:** **Flyway**
    *   `flyway-core` manages database schema changes automatically on application startup.
    *   Migration scripts are located in `src/main/resources/db/migration`.

### Connection Info
*   **External Host (Local):** `localhost:6433`
    *   Exposed to host machine for tools pgAdmin.
*   **Internal Host (Docker):** `postgres-driver`
    *   Used for inter-container communication.
*   **Database Name:** `driver_db`
*   **Username:** `postgres`
*   **Password:** `postgres`
*   **Port (Internal):** `5432`
*   **Port external:** `6433`

### Access Database

#### Command Line (psql)
```bash
docker exec -it postgres-driver psql -U postgres -d driver_db
```

#### Web Interface (pgAdmin)
For a graphical database management interface, see **[PGADMIN_GUIDE.md](docs/PGADMIN_GUIDE.md)** for detailed setup instructions.

Quick start:
```bash
docker-compose --profile admin up -d
```
Then open: **http://localhost:5055** (login: `admin@admin.com` / `admin123`)

---

## API Endpoints

### Interactive API Documentation
🚀 **Swagger UI:** http://localhost:6001/swagger-ui/index.html

Explore and test all API endpoints interactively!

### Main Resources
- `/api/drivers` - Manage driver profiles
- `/api/schedules` - Manage driver schedules
- `/api/forms` - Manage driver forms/logs

---

## Configuration

### Environment Variables
| Variable | Description | Default |
|----------|-------------|---------|
| `DB_HOST` | Database host address | `localhost` |
| `DB_PORT` | Database port | `6433` |
| `DB_NAME` | Database name | `driver_db` |
| `DB_USERNAME` | Database user | `postgres` |
| `DB_PASSWORD` | Database password | `postgres` |
| `SERVER_PORT` | Application port | `8080` |

Defined in `application.yml` and overridden in `docker-compose.yml`.

---

## Project Structure

```
DriverService/
├── src/
│   ├── main/
│   │   ├── java/com/fleetops/  # Source code
│   │   │   ├── controller/     # API Endpoints
│   │   │   ├── service/        # Business Logic
│   │   │   ├── repository/     # Data Access
│   │   │   ├── entity/         # DB Models
│   │   │   └── dto/            # Data Transfer Objects
│   │   └── resources/
│   │       ├── application.yml # Configuration
│   │       └── db/migration/   # Flyway SQL scripts
│   └── test/                   # Unit/Integration Tests
├── docs/
│   ├── LOCAL_DEVELOPMENT_GUIDE.md
│   └── PGADMIN_GUIDE.md
├── docker-compose.yml          # Docker services
├── Dockerfile                  # Docker image build
├── pom.xml                     # Maven dependencies
└── setup-and-run.sh            # Quick start script
```

---

## Development

### Rebuild After Code Changes
```bash
# If using Docker
docker-compose up --build

# If using local Maven
mvn clean install
mvn spring-boot:run
```

### Run Tests
```bash
mvn test
```

---

## License

MIT License
