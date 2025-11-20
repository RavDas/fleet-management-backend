using Microsoft.EntityFrameworkCore;
using Microsoft.OpenApi.Models;
using VehicleService.Infrastructure;
using VehicleService.Infrastructure.Data;
using static VehicleService.Infrastructure.Data.DatabaseSeeder;

var builder = WebApplication.CreateBuilder(args);

// --------------------------------------------------
// 🔹 Add Services
// --------------------------------------------------

// Add controllers
builder.Services.AddControllers();

// Add CORS
builder.Services.AddCors(options =>
{
    options.AddDefaultPolicy(policy =>
    {
        var corsOrigins = builder.Configuration["CORS_ORIGINS"] ?? "*";
        if (corsOrigins == "*")
        {
            policy.AllowAnyOrigin()
                  .AllowAnyMethod()
                  .AllowAnyHeader();
        }
        else
        {
            policy.WithOrigins(corsOrigins.Split(','))
                  .AllowAnyMethod()
                  .AllowAnyHeader()
                  .AllowCredentials();
        }
    });
});

// Swagger (OpenAPI)
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen(c =>
{
    c.SwaggerDoc("v1", new OpenApiInfo
    {
        Title = "Vehicle Service API",
        Version = "v1",
        Description = "Fleet Management Vehicle Service API - manages vehicles, maintenance, and dispatch info."
    });
});

// Add PostgreSQL + Infrastructure Layer (DbContext + Repository)
builder.Services.AddInfrastructure(builder.Configuration);

// --------------------------------------------------
// 🔹 Build the App
// --------------------------------------------------
var app = builder.Build();

// --------------------------------------------------
// 🔹 Middleware Pipeline
// --------------------------------------------------
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI(c =>
    {
        c.SwaggerEndpoint("/swagger/v1/swagger.json", "Vehicle Service API v1");
        c.RoutePrefix = string.Empty; // Open Swagger at root URL
    });
}

app.UseHttpsRedirection();

// Enable CORS
app.UseCors();

app.UseAuthorization();

// Map controllers
app.MapControllers();

// --------------------------------------------------
// 🔹 Health Check Endpoints
// --------------------------------------------------
// Basic health check for Docker
app.MapGet("/health", () => Results.Ok(new { status = "healthy", service = "vehicle-service" }));

// Database health check
app.MapGet("/health/db", async (VehicleDbContext db) =>
{
    try
    {
        var canConnect = await db.Database.CanConnectAsync();
        return Results.Ok(new { database = "vehicle_db", connected = canConnect });
    }
    catch (Exception ex)
    {
        return Results.Problem(ex.Message);
    }
});

// Root endpoint
app.MapGet("/", () => "✅ Vehicle Service Running and Healthy!");

// --------------------------------------------------
// 🔹 Database Initialization (Migrations + Seeding)
// --------------------------------------------------
using (var scope = app.Services.CreateScope())
{
    var db = scope.ServiceProvider.GetRequiredService<VehicleDbContext>();
    var logger = scope.ServiceProvider.GetRequiredService<ILogger<Program>>();
    
    try
    {
        // Apply any pending migrations
        logger.LogInformation("🔄 Applying database migrations...");
        await db.Database.MigrateAsync();
        logger.LogInformation("✅ Database migrations applied successfully");
        
        // Seed sample data
        logger.LogInformation("🌱 Checking if database needs seeding...");
        await DatabaseSeeder.SeedAsync(db);
    }
    catch (Exception ex)
    {
        logger.LogError(ex, "❌ An error occurred while initializing the database");
        throw;
    }
}

// --------------------------------------------------
// 🔹 Run the Application
// --------------------------------------------------
app.Run();
