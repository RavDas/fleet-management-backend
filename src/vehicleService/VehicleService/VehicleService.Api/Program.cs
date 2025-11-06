using Microsoft.EntityFrameworkCore;
using Microsoft.OpenApi.Models;
using VehicleService.Infrastructure;
using VehicleService.Infrastructure.Data;

var builder = WebApplication.CreateBuilder(args);

// --------------------------------------------------
// 🔹 Add Services
// --------------------------------------------------

// Add controllers
builder.Services.AddControllers();

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

app.UseAuthorization();

// Map controllers
app.MapControllers();

// --------------------------------------------------
// 🔹 Health Check Endpoint
// --------------------------------------------------
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
// 🔹 Run the Application
// --------------------------------------------------
using (var scope = app.Services.CreateScope())
{
    var db = scope.ServiceProvider.GetRequiredService<VehicleDbContext>();
    db.Database.Migrate();
}
app.Run();
