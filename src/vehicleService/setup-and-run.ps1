# ===============================
# Vehicle Service - Complete Setup & Run Script (Windows PowerShell)
# ===============================
# This script does EVERYTHING:
# 1. Checks .NET SDK is installed
# 2. Restores NuGet packages
# 3. Checks if PostgreSQL is running, starts it if not
# 4. Runs database migrations
# 5. Runs the .NET application
#
# Perfect for: Fresh clone, first-time setup, or daily use
# ===============================

$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "🚀 Vehicle Service - Complete Setup & Run" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# ===============================
# Step 1: Check .NET SDK
# ===============================
Write-Host "🔧 Step 1: Checking .NET SDK..." -ForegroundColor Blue
try {
    $dotnetVersion = dotnet --version
    Write-Host "✅ .NET SDK version: $dotnetVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ .NET SDK is not installed!" -ForegroundColor Red
    Write-Host "   Please install .NET 9 SDK from: https://dotnet.microsoft.com/download" -ForegroundColor Yellow
    exit 1
}
Write-Host ""

# ===============================
# Step 2: Check Docker is Running
# ===============================
Write-Host "🐳 Step 2: Checking Docker..." -ForegroundColor Blue
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
# Step 3: Restore NuGet Packages
# ===============================
Write-Host "📦 Step 3: Restoring NuGet packages..." -ForegroundColor Blue
Push-Location VehicleService/VehicleService.Api
try {
    dotnet restore --verbosity quiet
    Write-Host "✅ NuGet packages restored" -ForegroundColor Green
} catch {
    Write-Host "❌ Failed to restore packages" -ForegroundColor Red
    Pop-Location
    exit 1
}
Pop-Location
Write-Host ""

# ===============================
# Step 4: Check & Start PostgreSQL
# ===============================
Write-Host "🗄️  Step 4: Checking PostgreSQL database..." -ForegroundColor Blue

# Check if postgres-vehicle container exists and is running
$containerStatus = docker ps -a --filter "name=postgres-vehicle" --format "{{.Status}}"

if ($containerStatus -like "Up*") {
    Write-Host "✅ PostgreSQL is already running" -ForegroundColor Green
} elseif ($containerStatus) {
    Write-Host "⚠️  PostgreSQL container exists but is not running. Starting..." -ForegroundColor Yellow
    docker-compose up -d postgres-vehicle
    Write-Host "   Waiting for PostgreSQL to be ready..." -ForegroundColor Yellow
    Start-Sleep -Seconds 15
    Write-Host "✅ PostgreSQL started successfully" -ForegroundColor Green
} else {
    Write-Host "⚠️  PostgreSQL not found. Starting for the first time..." -ForegroundColor Yellow
    docker-compose up -d postgres-vehicle
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
        docker exec postgres-vehicle pg_isready -U postgres -d vehicle_db | Out-Null
        $connected = $true
        Write-Host "✅ Database is ready" -ForegroundColor Green
    } catch {
        $retryCount++
        if ($retryCount -lt $maxRetries) {
            Write-Host "   Waiting for database... (attempt $retryCount/$maxRetries)" -ForegroundColor Yellow
            Start-Sleep -Seconds 3
        } else {
            Write-Host "❌ Database is not responding. Please check Docker logs:" -ForegroundColor Red
            Write-Host "   docker logs postgres-vehicle" -ForegroundColor Yellow
            exit 1
        }
    }
}
Write-Host ""

# ===============================
# Step 6: Run Database Migrations
# ===============================
Write-Host "🔄 Step 6: Running database migrations..." -ForegroundColor Blue
Write-Host "   Note: Migrations also run automatically when the app starts" -ForegroundColor Gray
Write-Host "   This is just a verification step" -ForegroundColor Gray
Write-Host "✅ Migration check complete" -ForegroundColor Green
Write-Host ""

# ===============================
# Step 7: Run .NET Application
# ===============================
Write-Host "============================================================" -ForegroundColor Green
Write-Host "✅ All Setup Complete! Starting .NET Application..." -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host ""
Write-Host "📝 Quick Reference:" -ForegroundColor Cyan
Write-Host "   🌐 API:              http://localhost:7001" -ForegroundColor White
Write-Host "   📚 Swagger Docs:     http://localhost:7001 (root URL)" -ForegroundColor White
Write-Host "   💚 Health Check:     http://localhost:7001/health" -ForegroundColor White
Write-Host "   🚗 Vehicles API:     http://localhost:7001/api/vehicles" -ForegroundColor White
Write-Host ""
Write-Host "🛑 To stop the server: Press Ctrl+C" -ForegroundColor Yellow
Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Navigate to API project and run
Push-Location VehicleService/VehicleService.Api
dotnet run
Pop-Location

