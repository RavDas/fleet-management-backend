using Microsoft.EntityFrameworkCore;
using VehicleService.Domain.Entities;

namespace VehicleService.Infrastructure.Data
{
    /// <summary>
    /// Seeds the database with initial sample data for development/testing
    /// </summary>
    public static class DatabaseSeeder
    {
        /// <summary>
        /// Seeds sample vehicles, status histories, and maintenance records
        /// This method is idempotent - safe to run multiple times
        /// </summary>
        public static async Task SeedAsync(VehicleDbContext context)
        {
            // Check if data already exists
            if (await context.Vehicles.AnyAsync())
            {
                Console.WriteLine("ℹ️  Database already contains data. Skipping seed.");
                return;
            }

            Console.WriteLine("🌱 Seeding database with sample data...");

            // Create sample vehicles
            var vehicle1 = new Vehicle
            {
                Id = Guid.NewGuid(),
                Make = "Ford",
                Model = "Transit Van",
                Year = 2021,
                LicensePlate = "ABC-1234",
                Color = "White",
                FuelType = "Diesel",
                Status = (int)VehicleStatus.Active,
                CurrentLocation = "Depot A",
                CurrentDriver = "John Smith",
                FuelLevel = 85.5,
                CurrentMileage = 45200,
                LastMaintenanceDate = new DateTime(2024, 12, 1),
                NextMaintenanceDate = new DateTime(2025, 5, 1),
                CreatedAt = DateTime.UtcNow,
                UpdatedAt = DateTime.UtcNow
            };

            var vehicle2 = new Vehicle
            {
                Id = Guid.NewGuid(),
                Make = "Tesla",
                Model = "Model S",
                Year = 2023,
                LicensePlate = "XYZ-5678",
                Color = "Black",
                FuelType = "Electric",
                Status = (int)VehicleStatus.Active,
                CurrentLocation = "Depot B",
                CurrentDriver = "Sarah Lee",
                FuelLevel = 98.2,
                CurrentMileage = 13200,
                LastMaintenanceDate = new DateTime(2025, 1, 15),
                NextMaintenanceDate = new DateTime(2025, 7, 15),
                CreatedAt = DateTime.UtcNow,
                UpdatedAt = DateTime.UtcNow
            };

            var vehicle3 = new Vehicle
            {
                Id = Guid.NewGuid(),
                Make = "Toyota",
                Model = "Hilux",
                Year = 2020,
                LicensePlate = "JKL-9101",
                Color = "Silver",
                FuelType = "Diesel",
                Status = (int)VehicleStatus.Maintenance,
                CurrentLocation = "Warehouse 2",
                CurrentDriver = "Michael Brown",
                FuelLevel = 62.7,
                CurrentMileage = 88800,
                LastMaintenanceDate = new DateTime(2024, 11, 10),
                NextMaintenanceDate = new DateTime(2025, 4, 10),
                CreatedAt = DateTime.UtcNow,
                UpdatedAt = DateTime.UtcNow
            };

            // Add vehicles to context
            await context.Vehicles.AddRangeAsync(vehicle1, vehicle2, vehicle3);
            await context.SaveChangesAsync();

            Console.WriteLine("✅ Added 3 sample vehicles");

            // Create vehicle status histories
            var statusHistory1 = new VehicleStatusHistory
            {
                Id = Guid.NewGuid(),
                VehicleId = vehicle1.Id,
                Status = VehicleStatus.Active,
                ChangedBy = "System",
                Description = "Vehicle registered and active",
                ChangedAt = DateTime.UtcNow
            };

            var statusHistory2 = new VehicleStatusHistory
            {
                Id = Guid.NewGuid(),
                VehicleId = vehicle2.Id,
                Status = VehicleStatus.Active,
                ChangedBy = "System",
                Description = "Vehicle registered and active",
                ChangedAt = DateTime.UtcNow
            };

            var statusHistory3 = new VehicleStatusHistory
            {
                Id = Guid.NewGuid(),
                VehicleId = vehicle3.Id,
                Status = VehicleStatus.Maintenance,
                ChangedBy = "Admin",
                Description = "Vehicle under maintenance",
                ChangedAt = DateTime.UtcNow
            };

            // Add status histories
            await context.VehicleStatusHistories.AddRangeAsync(statusHistory1, statusHistory2, statusHistory3);
            await context.SaveChangesAsync();

            Console.WriteLine("✅ Added vehicle status histories");

            // Create maintenance records
            var maintenanceRecord1 = new MaintenanceRecord
            {
                Id = Guid.NewGuid(),
                VehicleId = vehicle1.Id,
                ServiceType = "Oil Change",
                Description = "Routine oil and filter change",
                ServiceDate = new DateTime(2024, 12, 1),
                Cost = 250.00,
                ServiceCenter = "AutoFix Center",
                PerformedBy = "Mark Taylor",
                CreatedAt = DateTime.UtcNow
            };

            var maintenanceRecord2 = new MaintenanceRecord
            {
                Id = Guid.NewGuid(),
                VehicleId = vehicle3.Id,
                ServiceType = "Brake Pad Replacement",
                Description = "Front brake pads replaced",
                ServiceDate = new DateTime(2024, 11, 10),
                Cost = 480.00,
                ServiceCenter = "SpeedServ Ltd",
                PerformedBy = "Luke Johnson",
                CreatedAt = DateTime.UtcNow
            };

            // Add maintenance records
            await context.MaintenanceRecords.AddRangeAsync(maintenanceRecord1, maintenanceRecord2);
            await context.SaveChangesAsync();

            Console.WriteLine("✅ Added maintenance records");
            Console.WriteLine("🎉 Database seeding completed successfully!");
            Console.WriteLine("📊 Summary:");
            Console.WriteLine("   - 3 Vehicles (VH-001: Ford Transit Van, VH-002: Tesla Model S, VH-003: Toyota Hilux)");
            Console.WriteLine("   - 3 Status History Entries");
            Console.WriteLine("   - 2 Maintenance Records");
        }
    }
}

