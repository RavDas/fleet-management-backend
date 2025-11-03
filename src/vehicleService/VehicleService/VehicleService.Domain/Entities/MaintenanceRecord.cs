using System;

namespace VehicleService.Domain.Entities
{
    public class MaintenanceRecord
    {
        public Guid Id { get; set; }
        public Guid VehicleId { get; set; }
        public string ServiceType { get; set; } = string.Empty;   // Oil Change, Brake Replacement
        public string Description { get; set; } = string.Empty;
        public DateTime ServiceDate { get; set; }
        public double Cost { get; set; }
        public string ServiceCenter { get; set; } = string.Empty;
        public string PerformedBy { get; set; } = string.Empty;   // Mechanic name
        public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
    }
}
