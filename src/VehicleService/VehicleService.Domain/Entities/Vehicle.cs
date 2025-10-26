using System;
using System.Collections.Generic;

namespace VehicleService.Domain.Entities
{
    public class Vehicle
    {
        public Guid Id { get; set; }

        // Basic info
        public string Make { get; set; } = string.Empty;        // 🔹 Add this
        public string Model { get; set; } = string.Empty;
        public int Year { get; set; }
        public string LicensePlate { get; set; } = string.Empty;
        public string Color { get; set; } = string.Empty;
        public string FuelType { get; set; } = string.Empty;

        // Vehicle metrics
        public double CurrentMileage { get; set; }              // 🔹 Add this
        public double FuelLevel { get; set; }

        // Status info
        public string? CurrentLocation { get; set; }
        public string? CurrentDriver { get; set; }
        public int Status { get; set; }

        // Maintenance dates
        public DateTime? LastMaintenanceDate { get; set; }
        public DateTime? NextMaintenanceDate { get; set; }

        // System tracking
        public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
        public DateTime UpdatedAt { get; set; } = DateTime.UtcNow;

        // Navigation properties
        public ICollection<MaintenanceRecord>? MaintenanceRecords { get; set; }
        public ICollection<VehicleStatusHistory>? StatusHistory { get; set; }
    }
}
