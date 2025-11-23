# Fleet Management Backend - Project Structure

This document describes the organized structure of the fleet management backend project.

## 📁 Root Directory Structure

```
fleet-management-backend/
├── docs/                          # Project-wide documentation
│   ├── setup/
│   │   └── DATABASE_SETUP.md     # Database setup guide
│   └── services/
│       └── VEHICLE_SERVICE_INTEGRATION.md
│
├── infrastructure/                # Infrastructure as Code
│   ├── ansible/                   # Ansible configurations
│   │   ├── README.md             # Ansible documentation
│   │   ├── hosts.ini
│   │   └── k8-cluster-setup.yaml
│   └── terraform/                 # Terraform modules
│       ├── README.md             # Terraform documentation
│       ├── environments/
│       │   └── dev/
│       │       ├── main.tf
│       │       ├── outputs.tf
│       │       └── variables.tf
│       ├── modules/
│       │   ├── compute/
│       │   ├── networking/
│       │   └── security/
│       └── README.md
│
├── src/                           # Source code for all services
│   ├── maintenanceService/        # Python Flask service
│   └── vehicleService/            # C# .NET service
│
└── FleetManagementSystem.sln      # .NET solution file
```

## 🔧 Maintenance Service Structure

Each service is self-contained with its own documentation, scripts, and Docker configurations.

```
src/maintenanceService/
├── docs/                          # Service-specific documentation
│   ├── README.md                  # Main service documentation
│   ├── LOCAL_DEVELOPMENT_GUIDE.md # Development setup guide
│   ├── PGADMIN_GUIDE.md          # Database admin guide
│   └── SEEDER_IMPLEMENTATION.md  # Data seeding documentation
│
├── app/                           # Application code
│   ├── controllers/               # API controllers
│   ├── models/                    # Database models
│   ├── routes/                    # API routes
│   ├── schemas/                   # Request/response schemas
│   ├── services/                  # Business logic
│   └── utils/                     # Utility functions
│
├── setup-and-run.sh               # Setup script
├── setup-and-run.sh               # Linux/Mac setup script
│
├── docker-compose.yml             # Docker services configuration
├── Dockerfile                     # Docker image definition
│
├── run.py                         # Flask application entry point
├── config.py                      # Application configuration
├── requirements.txt               # Python dependencies
└── init-db.sql                    # Database initialization
```

## 🚗 Vehicle Service Structure

```
src/vehicleService/
├── docs/                          # Service-specific documentation
│   ├── README.md                  # Main service documentation
│   ├── PGADMIN_GUIDE.md          # Database admin guide
│   ├── SEEDER_IMPLEMENTATION.md  # Data seeding documentation
│   └── vehicle-service-db-schema.txt
│
├── docker-compose.yml             # Docker services configuration
│
└── VehicleService/                # .NET solution
    ├── VehicleService.Api/        # API layer
    │   ├── Controllers/
    │   ├── Dockerfile            # Docker image definition
    │   ├── Program.cs
    │   └── appsettings.json
    ├── VehicleService.Application/ # Application layer
    │   ├── DTOs/
    │   └── Interfaces/
    ├── VehicleService.Domain/     # Domain layer
    │   └── Entities/
    └── VehicleService.Infrastructure/ # Infrastructure layer
        ├── Data/
        ├── Migrations/
        └── Repositories/
```

## 🌐 Frontend Structure

```
fleet-management-group8-final-assignment/
└── fleet-management-app/
    ├── docs/                      # Documentation
    │   ├── AUTHENTICATION.md
    │   ├── README.AUTH.md
    │   └── CONTRIBUTING.md
    │
    ├── src/
    │   ├── app/                   # Next.js app directory
    │   │   ├── (auth)/           # Auth routes
    │   │   └── (dashboard)/      # Dashboard routes
    │   ├── components/            # React components
    │   │   ├── analytics/
    │   │   ├── auth/
    │   │   ├── shared/
    │   │   ├── ui/               # UI components
    │   │   └── user/
    │   ├── contexts/              # React contexts
    │   ├── hooks/                 # Custom hooks
    │   ├── services/              # API services
    │   │   └── api/
    │   ├── types/                 # TypeScript types
    │   └── utils/                 # Utility functions
    │
    ├── public/                    # Static assets
    └── package.json
```

## 🎯 Organization Principles

### 1. **Service Independence**
- Each service contains its own documentation, scripts, and Docker configurations
- No shared scripts or configurations between services
- Easy to understand and work with each service independently

### 2. **Clear Documentation Hierarchy**
- Project-wide docs in root `/docs` folder
- Service-specific docs in each service's `/docs` folder
- All documentation is organized by category (setup, services, infrastructure)

### 3. **Infrastructure Separation**
- All infrastructure code (Ansible, Terraform) in `/infrastructure` folder
- Organized by tool type and environment
- Easy to manage and version control infrastructure changes

### 4. **Self-Contained Services**
- Each service has everything needed to run independently
- Scripts, Docker files, and configs stay with their service
- No need to navigate to root directory for service-specific operations

## 🚀 Quick Start Locations

### Maintenance Service
- **Documentation**: `src/maintenanceService/docs/README.md`
- **Setup Script**: `src/maintenanceService/setup-and-run.sh`
- **Docker**: `src/maintenanceService/docker-compose.yml`

### Vehicle Service
- **Documentation**: `src/vehicleService/docs/README.md`
- **Docker**: `src/vehicleService/docker-compose.yml`

### Frontend
- **Documentation**: `fleet-management-group8-final-assignment/fleet-management-app/docs/`
- **Main README**: `fleet-management-group8-final-assignment/fleet-management-app/README.md`

### Infrastructure
- **Ansible Documentation**: `infrastructure/ansible/README.md`
- **Ansible Playbooks**: `infrastructure/ansible/`
- **Terraform Documentation**: `infrastructure/terraform/README.md`
- **Terraform Modules**: `infrastructure/terraform/`
- **Database Setup**: `docs/setup/DATABASE_SETUP.md`

## 📝 Notes

- All documentation files have been updated with correct relative paths
- Scripts reference files using relative paths from their service directory
- Docker configurations use service-specific naming
- Frontend documentation is consolidated in the `docs/` folder

