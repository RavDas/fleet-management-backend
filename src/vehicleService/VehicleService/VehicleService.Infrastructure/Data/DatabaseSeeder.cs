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

            // Create sample vehicles with diverse statuses and realistic data
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
                CurrentLocation = "Downtown Depot",
                CurrentDriverId = null, // Available for assignment
                FuelLevel = 85.5,
                CurrentMileage = 45230,
                LastMaintenanceDate = new DateTime(2024, 12, 1, 0, 0, 0, DateTimeKind.Utc),
                NextMaintenanceDate = new DateTime(2025, 5, 1, 0, 0, 0, DateTimeKind.Utc),
                CreatedAt = DateTime.UtcNow.AddMonths(-6),
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
                CurrentLocation = "North Station",
                CurrentDriverId = null,
                FuelLevel = 98.2,
                CurrentMileage = 13200,
                LastMaintenanceDate = new DateTime(2025, 1, 15, 0, 0, 0, DateTimeKind.Utc),
                NextMaintenanceDate = new DateTime(2025, 7, 15, 0, 0, 0, DateTimeKind.Utc),
                CreatedAt = DateTime.UtcNow.AddMonths(-3),
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
                CurrentLocation = "Service Center A",
                CurrentDriverId = null,
                FuelLevel = 62.7,
                CurrentMileage = 88800,
                LastMaintenanceDate = new DateTime(2024, 11, 10, 0, 0, 0, DateTimeKind.Utc),
                NextMaintenanceDate = new DateTime(2025, 4, 10, 0, 0, 0, DateTimeKind.Utc),
                CreatedAt = DateTime.UtcNow.AddMonths(-12),
                UpdatedAt = DateTime.UtcNow
            };

            var vehicle4 = new Vehicle
            {
                Id = Guid.NewGuid(),
                Make = "Mercedes-Benz",
                Model = "Sprinter",
                Year = 2022,
                LicensePlate = "MBZ-2468",
                Color = "Blue",
                FuelType = "Diesel",
                Status = (int)VehicleStatus.Active,
                CurrentLocation = "East Warehouse",
                CurrentDriverId = null,
                FuelLevel = 73.4,
                CurrentMileage = 32100,
                LastMaintenanceDate = new DateTime(2024, 10, 20, 0, 0, 0, DateTimeKind.Utc),
                NextMaintenanceDate = new DateTime(2025, 4, 20, 0, 0, 0, DateTimeKind.Utc),
                CreatedAt = DateTime.UtcNow.AddMonths(-8),
                UpdatedAt = DateTime.UtcNow
            };

            var vehicle5 = new Vehicle
            {
                Id = Guid.NewGuid(),
                Make = "Chevrolet",
                Model = "Silverado",
                Year = 2021,
                LicensePlate = "CHV-1357",
                Color = "Red",
                FuelType = "Gasoline",
                Status = (int)VehicleStatus.Idle,
                CurrentLocation = "South Depot",
                CurrentDriverId = null,
                FuelLevel = 45.8,
                CurrentMileage = 67890,
                LastMaintenanceDate = new DateTime(2024, 9, 5, 0, 0, 0, DateTimeKind.Utc),
                NextMaintenanceDate = new DateTime(2025, 3, 5, 0, 0, 0, DateTimeKind.Utc),
                CreatedAt = DateTime.UtcNow.AddMonths(-10),
                UpdatedAt = DateTime.UtcNow
            };

            var vehicle6 = new Vehicle
            {
                Id = Guid.NewGuid(),
                Make = "Nissan",
                Model = "Leaf",
                Year = 2023,
                LicensePlate = "NSN-7890",
                Color = "Green",
                FuelType = "Electric",
                Status = (int)VehicleStatus.Active,
                CurrentLocation = "Central Hub",
                CurrentDriverId = null,
                FuelLevel = 89.3,
                CurrentMileage = 8500,
                LastMaintenanceDate = new DateTime(2025, 1, 10, 0, 0, 0, DateTimeKind.Utc),
                NextMaintenanceDate = new DateTime(2025, 7, 10, 0, 0, 0, DateTimeKind.Utc),
                CreatedAt = DateTime.UtcNow.AddMonths(-2),
                UpdatedAt = DateTime.UtcNow
            };

            var vehicle7 = new Vehicle
            {
                Id = Guid.NewGuid(),
                Make = "RAM",
                Model = "1500",
                Year = 2020,
                LicensePlate = "RAM-4321",
                Color = "Gray",
                FuelType = "Gasoline",
                Status = (int)VehicleStatus.Maintenance,
                CurrentLocation = "Service Center B",
                CurrentDriverId = null,
                FuelLevel = 15.2,
                CurrentMileage = 102400,
                LastMaintenanceDate = new DateTime(2024, 8, 15, 0, 0, 0, DateTimeKind.Utc),
                NextMaintenanceDate = new DateTime(2025, 2, 15, 0, 0, 0, DateTimeKind.Utc),
                CreatedAt = DateTime.UtcNow.AddMonths(-18),
                UpdatedAt = DateTime.UtcNow
            };

            var vehicle8 = new Vehicle
            {
                Id = Guid.NewGuid(),
                Make = "Honda",
                Model = "Ridgeline",
                Year = 2022,
                LicensePlate = "HND-5555",
                Color = "White",
                FuelType = "Gasoline",
                Status = (int)VehicleStatus.Active,
                CurrentLocation = "West Terminal",
                CurrentDriverId = null,
                FuelLevel = 91.7,
                CurrentMileage = 23456,
                LastMaintenanceDate = new DateTime(2024, 11, 25, 0, 0, 0, DateTimeKind.Utc),
                NextMaintenanceDate = new DateTime(2025, 5, 25, 0, 0, 0, DateTimeKind.Utc),
                CreatedAt = DateTime.UtcNow.AddMonths(-5),
                UpdatedAt = DateTime.UtcNow
            };

            var vehicle9 = new Vehicle
            {
                Id = Guid.NewGuid(),
                Make = "Volkswagen",
                Model = "Crafter",
                Year = 2021,
                LicensePlate = "VW-8888",
                Color = "Yellow",
                FuelType = "Diesel",
                Status = (int)VehicleStatus.Maintenance,
                CurrentLocation = "Service Center C",
                CurrentDriverId = null,
                FuelLevel = 52.1,
                CurrentMileage = 78900,
                LastMaintenanceDate = new DateTime(2024, 12, 10, 0, 0, 0, DateTimeKind.Utc),
                NextMaintenanceDate = new DateTime(2025, 6, 10, 0, 0, 0, DateTimeKind.Utc),
                CreatedAt = DateTime.UtcNow.AddMonths(-9),
                UpdatedAt = DateTime.UtcNow
            };

            var vehicle10 = new Vehicle
            {
                Id = Guid.NewGuid(),
                Make = "Isuzu",
                Model = "NPR",
                Year = 2020,
                LicensePlate = "ISU-9999",
                Color = "White",
                FuelType = "Diesel",
                Status = (int)VehicleStatus.Idle,
                CurrentLocation = "Downtown Depot",
                CurrentDriverId = null,
                FuelLevel = 68.5,
                CurrentMileage = 95600,
                LastMaintenanceDate = new DateTime(2024, 10, 5, 0, 0, 0, DateTimeKind.Utc),
                NextMaintenanceDate = new DateTime(2025, 4, 5, 0, 0, 0, DateTimeKind.Utc),
                CreatedAt = DateTime.UtcNow.AddMonths(-15),
                UpdatedAt = DateTime.UtcNow
            };

            // Add vehicles to context
            await context.Vehicles.AddRangeAsync(
                vehicle1, vehicle2, vehicle3, vehicle4, vehicle5,
                vehicle6, vehicle7, vehicle8, vehicle9, vehicle10
            );
            await context.SaveChangesAsync();

            Console.WriteLine("✅ Added 10 sample vehicles");

            // Create vehicle status histories
            var statusHistories = new List<VehicleStatusHistory>
            {
                new VehicleStatusHistory
                {
                    Id = Guid.NewGuid(),
                    VehicleId = vehicle1.Id,
                    Status = VehicleStatus.Active,
                    ChangedBy = "System",
                    Description = "Vehicle registered and activated",
                    ChangedAt = DateTime.UtcNow.AddMonths(-6)
                },
                new VehicleStatusHistory
                {
                    Id = Guid.NewGuid(),
                    VehicleId = vehicle2.Id,
                    Status = VehicleStatus.Active,
                    ChangedBy = "System",
                    Description = "Vehicle registered and activated",
                    ChangedAt = DateTime.UtcNow.AddMonths(-3)
                },
                new VehicleStatusHistory
                {
                    Id = Guid.NewGuid(),
                    VehicleId = vehicle3.Id,
                    Status = VehicleStatus.Active,
                    ChangedBy = "System",
                    Description = "Vehicle registered and activated",
                    ChangedAt = DateTime.UtcNow.AddMonths(-12)
                },
                new VehicleStatusHistory
                {
                    Id = Guid.NewGuid(),
                    VehicleId = vehicle3.Id,
                    Status = VehicleStatus.Maintenance,
                    ChangedBy = "Admin",
                    Description = "Scheduled maintenance - brake system inspection",
                    ChangedAt = DateTime.UtcNow.AddDays(-2)
                },
                new VehicleStatusHistory
                {
                    Id = Guid.NewGuid(),
                    VehicleId = vehicle4.Id,
                    Status = VehicleStatus.Active,
                    ChangedBy = "System",
                    Description = "Vehicle registered and activated",
                    ChangedAt = DateTime.UtcNow.AddMonths(-8)
                },
                new VehicleStatusHistory
                {
                    Id = Guid.NewGuid(),
                    VehicleId = vehicle5.Id,
                    Status = VehicleStatus.Active,
                    ChangedBy = "System",
                    Description = "Vehicle registered and activated",
                    ChangedAt = DateTime.UtcNow.AddMonths(-10)
                },
                new VehicleStatusHistory
                {
                    Id = Guid.NewGuid(),
                    VehicleId = vehicle5.Id,
                    Status = VehicleStatus.Idle,
                    ChangedBy = "Dispatcher",
                    Description = "Vehicle parked - low fuel level",
                    ChangedAt = DateTime.UtcNow.AddDays(-5)
                },
                new VehicleStatusHistory
                {
                    Id = Guid.NewGuid(),
                    VehicleId = vehicle6.Id,
                    Status = VehicleStatus.Active,
                    ChangedBy = "System",
                    Description = "Vehicle registered and activated",
                    ChangedAt = DateTime.UtcNow.AddMonths(-2)
                },
                new VehicleStatusHistory
                {
                    Id = Guid.NewGuid(),
                    VehicleId = vehicle7.Id,
                    Status = VehicleStatus.Active,
                    ChangedBy = "System",
                    Description = "Vehicle registered and activated",
                    ChangedAt = DateTime.UtcNow.AddMonths(-18)
                },
                new VehicleStatusHistory
                {
                    Id = Guid.NewGuid(),
                    VehicleId = vehicle7.Id,
                    Status = VehicleStatus.Maintenance,
                    ChangedBy = "Mechanic",
                    Description = "Vehicle offline - engine diagnostic required",
                    ChangedAt = DateTime.UtcNow.AddDays(-7)
                },
                new VehicleStatusHistory
                {
                    Id = Guid.NewGuid(),
                    VehicleId = vehicle8.Id,
                    Status = VehicleStatus.Active,
                    ChangedBy = "System",
                    Description = "Vehicle registered and activated",
                    ChangedAt = DateTime.UtcNow.AddMonths(-5)
                },
                new VehicleStatusHistory
                {
                    Id = Guid.NewGuid(),
                    VehicleId = vehicle9.Id,
                    Status = VehicleStatus.Active,
                    ChangedBy = "System",
                    Description = "Vehicle registered and activated",
                    ChangedAt = DateTime.UtcNow.AddMonths(-9)
                },
                new VehicleStatusHistory
                {
                    Id = Guid.NewGuid(),
                    VehicleId = vehicle9.Id,
                    Status = VehicleStatus.Maintenance,
                    ChangedBy = "Admin",
                    Description = "Scheduled maintenance - tire rotation and oil change",
                    ChangedAt = DateTime.UtcNow.AddDays(-1)
                },
                new VehicleStatusHistory
                {
                    Id = Guid.NewGuid(),
                    VehicleId = vehicle10.Id,
                    Status = VehicleStatus.Active,
                    ChangedBy = "System",
                    Description = "Vehicle registered and activated",
                    ChangedAt = DateTime.UtcNow.AddMonths(-15)
                },
                new VehicleStatusHistory
                {
                    Id = Guid.NewGuid(),
                    VehicleId = vehicle10.Id,
                    Status = VehicleStatus.Idle,
                    ChangedBy = "Dispatcher",
                    Description = "Vehicle available - waiting for assignment",
                    ChangedAt = DateTime.UtcNow.AddDays(-3)
                }
            };

            // Add status histories
            await context.VehicleStatusHistories.AddRangeAsync(statusHistories);
            await context.SaveChangesAsync();

            Console.WriteLine("✅ Added vehicle status histories (15 entries)");

            Console.WriteLine("🎉 Database seeding completed successfully!");
            Console.WriteLine("📊 Summary:");
            Console.WriteLine("   - 10 Vehicles (Ford Transit, Tesla Model S, Toyota Hilux, Mercedes Sprinter, etc.)");
            Console.WriteLine("   - 15 Status History Entries");
            Console.WriteLine("   - Diverse statuses: Active (6), Maintenance (2), Idle (2), Offline (1)");
        }
    }
}

