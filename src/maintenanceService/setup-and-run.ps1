# ===============================
# Maintenance Service - Complete Setup & Run Script (Windows PowerShell)
# ===============================
# This script does EVERYTHING:
# 1. Creates virtual environment (if needed)
# 2. Installs dependencies
# 3. Creates .env file (if needed)
# 4. Checks if PostgreSQL is running, starts it if not
# 5. Runs the Flask application
#
# Perfect for: Fresh clone, first-time setup, or daily use
# ===============================

$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "🚀 Maintenance Service - Complete Setup & Run" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# ===============================
# Step 1: Check Docker is Running
# ===============================
Write-Host "🐳 Step 1: Checking Docker..." -ForegroundColor Blue
try {
    docker ps | Out-Null
    Write-Host "✅ Docker is running" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker is not running. Please start Docker Desktop first!" -ForegroundColor Red
    Write-Host "   After starting Docker, run this script again." -ForegroundColor Yellow
    exit 1
}
Write-Host ""

# ===============================
# Step 2: Create .env file if needed
# ===============================
Write-Host "⚙️  Step 2: Checking configuration..." -ForegroundColor Blue
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
} else {
    Write-Host "✅ .env file already exists" -ForegroundColor Green
}
Write-Host ""

# ===============================
# Step 3: Setup Python Virtual Environment
# ===============================
Write-Host "🐍 Step 3: Setting up Python environment..." -ForegroundColor Blue
if (-not (Test-Path venv)) {
    Write-Host "   Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    Write-Host "✅ Virtual environment created" -ForegroundColor Green
} else {
    Write-Host "✅ Virtual environment already exists" -ForegroundColor Green
}

Write-Host "   Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

Write-Host "   Installing/updating dependencies..." -ForegroundColor Yellow
pip install --quiet -r requirements.txt
Write-Host "✅ Dependencies installed" -ForegroundColor Green
Write-Host ""

# ===============================
# Step 4: Check & Start PostgreSQL
# ===============================
Write-Host "🗄️  Step 4: Checking PostgreSQL database..." -ForegroundColor Blue

# Check if postgres-maintenance container exists and is running
$containerStatus = docker ps -a --filter "name=postgres-maintenance" --format "{{.Status}}"

if ($containerStatus -like "Up*") {
    Write-Host "✅ PostgreSQL is already running" -ForegroundColor Green
} elseif ($containerStatus) {
    Write-Host "⚠️  PostgreSQL container exists but is not running. Starting..." -ForegroundColor Yellow
    docker-compose up -d postgres-maintenance
    Write-Host "   Waiting for PostgreSQL to be ready..." -ForegroundColor Yellow
    Start-Sleep -Seconds 15
    Write-Host "✅ PostgreSQL started successfully" -ForegroundColor Green
} else {
    Write-Host "⚠️  PostgreSQL not found. Starting for the first time..." -ForegroundColor Yellow
    docker-compose up -d postgres-maintenance
    Write-Host "   Waiting for PostgreSQL to initialize (first-time setup)..." -ForegroundColor Yellow
    Start-Sleep -Seconds 20
    Write-Host "✅ PostgreSQL started successfully" -ForegroundColor Green
}
Write-Host ""

# ===============================
# Step 5: Verify Database Connection
# ===============================
Write-Host "🔍 Step 5: Verifying database connection..." -ForegroundColor Blue
$maxRetries = 5
$retryCount = 0
$connected = $false

while (-not $connected -and $retryCount -lt $maxRetries) {
    try {
        docker exec postgres-maintenance pg_isready -U postgres -d maintenance_db | Out-Null
        $connected = $true
        Write-Host "✅ Database is ready" -ForegroundColor Green
    } catch {
        $retryCount++
        if ($retryCount -lt $maxRetries) {
            Write-Host "   Waiting for database... (attempt $retryCount/$maxRetries)" -ForegroundColor Yellow
            Start-Sleep -Seconds 3
        } else {
            Write-Host "❌ Database is not responding. Please check Docker logs:" -ForegroundColor Red
            Write-Host "   docker logs postgres-maintenance" -ForegroundColor Yellow
            exit 1
        }
    }
}
Write-Host ""

# ===============================
# Step 6: Run Flask Application
# ===============================
Write-Host "============================================================" -ForegroundColor Green
Write-Host "✅ All Setup Complete! Starting Flask Application..." -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host ""
Write-Host "📝 Quick Reference:" -ForegroundColor Cyan
Write-Host "   🌐 API:              http://localhost:5001" -ForegroundColor White
Write-Host "   📚 Swagger Docs:     http://localhost:5001/docs" -ForegroundColor White
Write-Host "   💚 Health Check:     http://localhost:5001/health" -ForegroundColor White
Write-Host "   📋 Maintenance API:  http://localhost:5001/api/maintenance/" -ForegroundColor White
Write-Host ""
Write-Host "🛑 To stop the server: Press Ctrl+C" -ForegroundColor Yellow
Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Run the application
python run.py

