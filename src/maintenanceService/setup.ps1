# ===============================
# Maintenance Service Setup Script (Windows PowerShell)
# ===============================

$ErrorActionPreference = "Stop"

Write-Host "======================================" -ForegroundColor Cyan
Write-Host "🚀 Maintenance Service Setup" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# Check if .env exists
if (-not (Test-Path .env)) {
    Write-Host "⚠️  .env file not found. Creating from template..." -ForegroundColor Yellow
    
    $envContent = @"
# Flask Configuration
FLASK_ENV=development
FLASK_APP=run.py
SECRET_KEY=dev-secret-key-change-in-production-f89a7d6c8b4e3a2d

# Database Configuration (PostgreSQL)
DATABASE_URL=postgresql://postgres:postgres@localhost:5434/maintenance_db

# Server Configuration
PORT=5001
HOST=0.0.0.0

# CORS Configuration
CORS_ORIGINS=*

# Pagination
ITEMS_PER_PAGE=10

# Logging
LOG_LEVEL=DEBUG
"@
    
    $envContent | Out-File -FilePath .env -Encoding utf8
    Write-Host "✅ .env file created" -ForegroundColor Green
}

Write-Host "📦 Step 1: Checking Python dependencies..." -ForegroundColor Blue
if (-not (Test-Path venv)) {
    Write-Host "Creating virtual environment..."
    python -m venv venv
}

Write-Host "Activating virtual environment..."
.\venv\Scripts\Activate.ps1

Write-Host "Installing dependencies..."
pip install -r requirements.txt
Write-Host "✅ Dependencies installed" -ForegroundColor Green
Write-Host ""

Write-Host "🐳 Step 2: Starting Docker containers..." -ForegroundColor Blue
docker-compose up -d postgres-maintenance
Write-Host "Waiting for PostgreSQL to be ready..."
Start-Sleep -Seconds 10
Write-Host "✅ PostgreSQL is running" -ForegroundColor Green
Write-Host ""

Write-Host "🗄️  Step 3: Database is initialized via init-db.sql" -ForegroundColor Blue
Write-Host "✅ Database schema created and sample data inserted" -ForegroundColor Green
Write-Host ""

Write-Host "🔧 Step 4: Setting up Flask-Migrate (if needed)..." -ForegroundColor Blue
if (-not (Test-Path migrations)) {
    $env:FLASK_APP = "run.py"
    flask db init
    Write-Host "✅ Flask-Migrate initialized" -ForegroundColor Green
}
Write-Host ""

Write-Host "======================================" -ForegroundColor Green
Write-Host "✅ Setup Complete!" -ForegroundColor Green
Write-Host "======================================" -ForegroundColor Green
Write-Host ""
Write-Host "📝 Next steps:"
Write-Host "   1. Start the service:" -ForegroundColor Cyan
Write-Host "      docker-compose up"
Write-Host "      or run locally:"
Write-Host "      python run.py"
Write-Host ""
Write-Host "   2. Access the API:" -ForegroundColor Cyan
Write-Host "      http://localhost:5001"
Write-Host ""
Write-Host "   3. Health check:" -ForegroundColor Cyan
Write-Host "      http://localhost:5001/health"
Write-Host ""
Write-Host "   4. API endpoints:" -ForegroundColor Cyan
Write-Host "      http://localhost:5001/api/maintenance"
Write-Host ""
Write-Host "   5. Database management (optional):" -ForegroundColor Cyan
Write-Host "      docker-compose --profile admin up pgadmin-maintenance"
Write-Host "      http://localhost:5051"
Write-Host "      Email: admin@maintenance.local"
Write-Host "      Password: admin123"
Write-Host ""


