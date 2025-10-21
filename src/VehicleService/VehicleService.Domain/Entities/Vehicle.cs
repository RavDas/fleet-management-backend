using System;
using System.Collections.Generic;

namespace VehicleService.Domain.Entities
{
    public class Vehicle
    {
        public Guid Id { get; set; }

        // Basic Info
        public string VehicleCode { get; set; } = string.Empty;   
        public string LicensePlate { get; set; } = string.Empty;   
        public string Model { get; set; } = string.Empty;        
        public string Manufacturer { get; set; } = string.Empty;   
        public int Year { get; set; }
        public string Color { get; set; } = string.Empty;
        public string FuelType { get; set; } = string.Empty;       // Diesel / Petrol / Electric

        // Status and Condition
        public VehicleStatus Status { get; set; } = VehicleStatus.Active;
        public string CurrentLocation { get; set; } = string.Empty; 
        public string CurrentDriver { get; set; } = string.Empty;   
        public double FuelLevel { get; set; }                      
        public double Mileage { get; set; }                       

        // Maintenance
        public DateTime? LastMaintenanceDate { get; set; }
        public DateTime? NextMaintenanceDate { get; set; }

        // Timestamps
        public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
        public DateTime UpdatedAt { get; set; } = DateTime.UtcNow;

        // Relationships
        public ICollection<MaintenanceRecord> MaintenanceRecords { get; set; } = new List<MaintenanceRecord>();
        public ICollection<VehicleStatusHistory> StatusHistory { get; set; } = new List<VehicleStatusHistory>();
    }
}
