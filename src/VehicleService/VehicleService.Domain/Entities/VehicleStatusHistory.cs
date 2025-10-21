using System;

namespace VehicleService.Domain.Entities
{
    public class VehicleStatusHistory
    {
        public Guid Id { get; set; }
        public Guid VehicleId { get; set; }
        public VehicleStatus Status { get; set; }
        public string ChangedBy { get; set; } = string.Empty; // Admin or System user
        public string Description { get; set; } = string.Empty;
        public DateTime ChangedAt { get; set; } = DateTime.UtcNow;
    }
}
