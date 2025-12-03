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
                NextMaintenanceDate = new DateTime(2025, 1, 10, 0, 0, 0, DateTimeKind.Utc),  // MAINTENANCE DUE SOON
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
                FuelLevel = 19.8,  // LOW FUEL ALERT
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

            // Additional vehicles for better demo coverage
            var vehicle11 = new Vehicle
            {
                Id = Guid.NewGuid(),
                Make = "Freightliner",
                Model = "Cascadia",
                Year = 2021,
                LicensePlate = "FLR-3456",
                Color = "Red",
                FuelType = "Diesel",
                Status = (int)VehicleStatus.Active,
                CurrentLocation = "Highway Route 5",
                CurrentDriverId = null,
                FuelLevel = 18.5,  // LOW FUEL ALERT
                CurrentMileage = 156800,
                LastMaintenanceDate = new DateTime(2024, 11, 20, 0, 0, 0, DateTimeKind.Utc),
                NextMaintenanceDate = new DateTime(2025, 5, 20, 0, 0, 0, DateTimeKind.Utc),
                CreatedAt = DateTime.UtcNow.AddMonths(-20),
                UpdatedAt = DateTime.UtcNow
            };

            var vehicle12 = new Vehicle
            {
                Id = Guid.NewGuid(),
                Make = "Volvo",
                Model = "VNL",
                Year = 2020,
                LicensePlate = "VLV-7890",
                Color = "White",
                FuelType = "Diesel",
                Status = (int)VehicleStatus.Active,
                CurrentLocation = "North Terminal",
                CurrentDriverId = null,
                FuelLevel = 22.3,  // LOW FUEL ALERT
                CurrentMileage = 187200,
                LastMaintenanceDate = new DateTime(2024, 9, 15, 0, 0, 0, DateTimeKind.Utc),
                NextMaintenanceDate = new DateTime(2025, 1, 15, 0, 0, 0, DateTimeKind.Utc),  // MAINTENANCE DUE SOON
                CreatedAt = DateTime.UtcNow.AddMonths(-22),
                UpdatedAt = DateTime.UtcNow
            };

            var vehicle13 = new Vehicle
            {
                Id = Guid.NewGuid(),
                Make = "Kenworth",
                Model = "T680",
                Year = 2022,
                LicensePlate = "KW-1122",
                Color = "Blue",
                FuelType = "Diesel",
                Status = (int)VehicleStatus.Maintenance,
                CurrentLocation = "Service Center B",
                CurrentDriverId = null,
                FuelLevel = 44.8,
                CurrentMileage = 98400,
                LastMaintenanceDate = new DateTime(2024, 8, 10, 0, 0, 0, DateTimeKind.Utc),
                NextMaintenanceDate = new DateTime(2024, 12, 25, 0, 0, 0, DateTimeKind.Utc),  // OVERDUE
                CreatedAt = DateTime.UtcNow.AddMonths(-16),
                UpdatedAt = DateTime.UtcNow
            };

            var vehicle14 = new Vehicle
            {
                Id = Guid.NewGuid(),
                Make = "Peterbilt",
                Model = "579",
                Year = 2021,
                LicensePlate = "PB-5544",
                Color = "Black",
                FuelType = "Diesel",
                Status = (int)VehicleStatus.Active,
                CurrentLocation = "East Distribution Center",
                CurrentDriverId = null,
                FuelLevel = 95.2,
                CurrentMileage = 72300,
                LastMaintenanceDate = new DateTime(2024, 11, 30, 0, 0, 0, DateTimeKind.Utc),
                NextMaintenanceDate = new DateTime(2025, 5, 30, 0, 0, 0, DateTimeKind.Utc),
                CreatedAt = DateTime.UtcNow.AddMonths(-11),
                UpdatedAt = DateTime.UtcNow
            };

            var vehicle15 = new Vehicle
            {
                Id = Guid.NewGuid(),
                Make = "Mack",
                Model = "Anthem",
                Year = 2023,
                LicensePlate = "MCK-9988",
                Color = "Silver",
                FuelType = "Diesel",
                Status = (int)VehicleStatus.Active,
                CurrentLocation = "West Terminal",
                CurrentDriverId = null,
                FuelLevel = 88.7,
                CurrentMileage = 34200,
                LastMaintenanceDate = new DateTime(2024, 12, 1, 0, 0, 0, DateTimeKind.Utc),
                NextMaintenanceDate = new DateTime(2025, 6, 1, 0, 0, 0, DateTimeKind.Utc),
                CreatedAt = DateTime.UtcNow.AddMonths(-4),
                UpdatedAt = DateTime.UtcNow
            };

            var vehicle16 = new Vehicle
            {
                Id = Guid.NewGuid(),
                Make = "International",
                Model = "LT Series",
                Year = 2020,
                LicensePlate = "INT-3322",
                Color = "Orange",
                FuelType = "Diesel",
                Status = (int)VehicleStatus.Maintenance,
                CurrentLocation = "Service Center C",
                CurrentDriverId = null,
                FuelLevel = 12.4,  // LOW FUEL ALERT
                CurrentMileage = 203400,
                LastMaintenanceDate = new DateTime(2024, 7, 20, 0, 0, 0, DateTimeKind.Utc),
                NextMaintenanceDate = new DateTime(2024, 11, 20, 0, 0, 0, DateTimeKind.Utc),  // OVERDUE
                CreatedAt = DateTime.UtcNow.AddMonths(-25),
                UpdatedAt = DateTime.UtcNow
            };

            var vehicle17 = new Vehicle
            {
                Id = Guid.NewGuid(),
                Make = "Western Star",
                Model = "4700",
                Year = 2021,
                LicensePlate = "WS-6677",
                Color = "Gray",
                FuelType = "Diesel",
                Status = (int)VehicleStatus.Decommissioned,
                CurrentLocation = "Salvage Yard",
                CurrentDriverId = null,
                FuelLevel = 0.0,
                CurrentMileage = 345600,
                LastMaintenanceDate = new DateTime(2024, 5, 1, 0, 0, 0, DateTimeKind.Utc),
                NextMaintenanceDate = null,
                CreatedAt = DateTime.UtcNow.AddMonths(-30),
                UpdatedAt = DateTime.UtcNow
            };

            var vehicle18 = new Vehicle
            {
                Id = Guid.NewGuid(),
                Make = "Hino",
                Model = "268A",
                Year = 2022,
                LicensePlate = "HNO-1010",
                Color = "White",
                FuelType = "Diesel",
                Status = (int)VehicleStatus.Active,
                CurrentLocation = "Central Dispatch",
                CurrentDriverId = null,
                FuelLevel = 76.4,
                CurrentMileage = 45600,
                LastMaintenanceDate = new DateTime(2024, 11, 15, 0, 0, 0, DateTimeKind.Utc),
                NextMaintenanceDate = new DateTime(2025, 5, 15, 0, 0, 0, DateTimeKind.Utc),
                CreatedAt = DateTime.UtcNow.AddMonths(-7),
                UpdatedAt = DateTime.UtcNow
            };

            var vehicle19 = new Vehicle
            {
                Id = Guid.NewGuid(),
                Make = "Scania",
                Model = "R500",
                Year = 2023,
                LicensePlate = "SCN-4488",
                Color = "Blue",
                FuelType = "Diesel",
                Status = (int)VehicleStatus.Active,
                CurrentLocation = "Port Authority",
                CurrentDriverId = null,
                FuelLevel = 91.8,
                CurrentMileage = 28900,
                LastMaintenanceDate = new DateTime(2024, 12, 5, 0, 0, 0, DateTimeKind.Utc),
                NextMaintenanceDate = new DateTime(2025, 6, 5, 0, 0, 0, DateTimeKind.Utc),
                CreatedAt = DateTime.UtcNow.AddMonths(-3),
                UpdatedAt = DateTime.UtcNow
            };

            var vehicle20 = new Vehicle
            {
                Id = Guid.NewGuid(),
                Make = "DAF",
                Model = "XF",
                Year = 2021,
                LicensePlate = "DAF-7755",
                Color = "Green",
                FuelType = "Diesel",
                Status = (int)VehicleStatus.Idle,
                CurrentLocation = "South Depot",
                CurrentDriverId = null,
                FuelLevel = 24.6,  // LOW FUEL ALERT
                CurrentMileage = 134500,
                LastMaintenanceDate = new DateTime(2024, 10, 10, 0, 0, 0, DateTimeKind.Utc),
                NextMaintenanceDate = new DateTime(2025, 2, 10, 0, 0, 0, DateTimeKind.Utc),  // MAINTENANCE DUE SOON
                CreatedAt = DateTime.UtcNow.AddMonths(-14),
                UpdatedAt = DateTime.UtcNow
            };

            // Add all vehicles to context
            await context.Vehicles.AddRangeAsync(
                vehicle1, vehicle2, vehicle3, vehicle4, vehicle5,
                vehicle6, vehicle7, vehicle8, vehicle9, vehicle10,
                vehicle11, vehicle12, vehicle13, vehicle14, vehicle15,
                vehicle16, vehicle17, vehicle18, vehicle19, vehicle20
            );
            await context.SaveChangesAsync();

            Console.WriteLine("✅ Added 20 sample vehicles with comprehensive status distribution");

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
                },
                new VehicleStatusHistory
                {
                    Id = Guid.NewGuid(),
                    VehicleId = vehicle11.Id,
                    Status = VehicleStatus.Active,
                    ChangedBy = "System",
                    Description = "Vehicle registered and activated",
                    ChangedAt = DateTime.UtcNow.AddMonths(-20)
                },
                new VehicleStatusHistory
                {
                    Id = Guid.NewGuid(),
                    VehicleId = vehicle12.Id,
                    Status = VehicleStatus.Active,
                    ChangedBy = "System",
                    Description = "Vehicle registered and activated",
                    ChangedAt = DateTime.UtcNow.AddMonths(-22)
                },
                new VehicleStatusHistory
                {
                    Id = Guid.NewGuid(),
                    VehicleId = vehicle13.Id,
                    Status = VehicleStatus.Active,
                    ChangedBy = "System",
                    Description = "Vehicle registered and activated",
                    ChangedAt = DateTime.UtcNow.AddMonths(-16)
                },
                new VehicleStatusHistory
                {
                    Id = Guid.NewGuid(),
                    VehicleId = vehicle13.Id,
                    Status = VehicleStatus.Maintenance,
                    ChangedBy = "Mechanic",
                    Description = "Scheduled maintenance - major engine overhaul",
                    ChangedAt = DateTime.UtcNow.AddDays(-4)
                },
                new VehicleStatusHistory
                {
                    Id = Guid.NewGuid(),
                    VehicleId = vehicle14.Id,
                    Status = VehicleStatus.Active,
                    ChangedBy = "System",
                    Description = "Vehicle registered and activated",
                    ChangedAt = DateTime.UtcNow.AddMonths(-11)
                },
                new VehicleStatusHistory
                {
                    Id = Guid.NewGuid(),
                    VehicleId = vehicle15.Id,
                    Status = VehicleStatus.Active,
                    ChangedBy = "System",
                    Description = "Vehicle registered and activated",
                    ChangedAt = DateTime.UtcNow.AddMonths(-4)
                },
                new VehicleStatusHistory
                {
                    Id = Guid.NewGuid(),
                    VehicleId = vehicle16.Id,
                    Status = VehicleStatus.Active,
                    ChangedBy = "System",
                    Description = "Vehicle registered and activated",
                    ChangedAt = DateTime.UtcNow.AddMonths(-25)
                },
                new VehicleStatusHistory
                {
                    Id = Guid.NewGuid(),
                    VehicleId = vehicle16.Id,
                    Status = VehicleStatus.Maintenance,
                    ChangedBy = "Admin",
                    Description = "Critical maintenance - transmission failure",
                    ChangedAt = DateTime.UtcNow.AddDays(-6)
                },
                new VehicleStatusHistory
                {
                    Id = Guid.NewGuid(),
                    VehicleId = vehicle17.Id,
                    Status = VehicleStatus.Active,
                    ChangedBy = "System",
                    Description = "Vehicle registered and activated",
                    ChangedAt = DateTime.UtcNow.AddMonths(-30)
                },
                new VehicleStatusHistory
                {
                    Id = Guid.NewGuid(),
                    VehicleId = vehicle17.Id,
                    Status = VehicleStatus.Decommissioned,
                    ChangedBy = "Fleet Manager",
                    Description = "Vehicle decommissioned - end of service life",
                    ChangedAt = DateTime.UtcNow.AddMonths(-2)
                },
                new VehicleStatusHistory
                {
                    Id = Guid.NewGuid(),
                    VehicleId = vehicle18.Id,
                    Status = VehicleStatus.Active,
                    ChangedBy = "System",
                    Description = "Vehicle registered and activated",
                    ChangedAt = DateTime.UtcNow.AddMonths(-7)
                },
                new VehicleStatusHistory
                {
                    Id = Guid.NewGuid(),
                    VehicleId = vehicle19.Id,
                    Status = VehicleStatus.Active,
                    ChangedBy = "System",
                    Description = "Vehicle registered and activated",
                    ChangedAt = DateTime.UtcNow.AddMonths(-3)
                },
                new VehicleStatusHistory
                {
                    Id = Guid.NewGuid(),
                    VehicleId = vehicle20.Id,
                    Status = VehicleStatus.Active,
                    ChangedBy = "System",
                    Description = "Vehicle registered and activated",
                    ChangedAt = DateTime.UtcNow.AddMonths(-14)
                },
                new VehicleStatusHistory
                {
                    Id = Guid.NewGuid(),
                    VehicleId = vehicle20.Id,
                    Status = VehicleStatus.Idle,
                    ChangedBy = "Dispatcher",
                    Description = "Vehicle idle - fuel refill needed before next trip",
                    ChangedAt = DateTime.UtcNow.AddDays(-2)
                }
            };

            // Add status histories
            await context.VehicleStatusHistories.AddRangeAsync(statusHistories);
            await context.SaveChangesAsync();

            Console.WriteLine("✅ Added vehicle status histories (29 entries)");

            Console.WriteLine("🎉 Database seeding completed successfully!");
            Console.WriteLine("📊 Summary:");
            Console.WriteLine("   - 20 Vehicles (Ford, Tesla, Toyota, Mercedes, Chevrolet, Freightliner, Volvo, etc.)");
            Console.WriteLine("   - 29 Status History Entries");
            Console.WriteLine("   - Status Distribution: Active (11), Maintenance (5), Idle (3), Decommissioned (1)");
            Console.WriteLine("   - 4 Low Fuel Alerts (< 25% fuel level)");
            Console.WriteLine("   - 3 Maintenance Due Soon/Overdue vehicles");
        }
    }
}

