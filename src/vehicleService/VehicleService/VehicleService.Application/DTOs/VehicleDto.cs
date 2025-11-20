namespace VehicleService.Application.DTOs
{
    public class VehicleDto
    {
        public Guid Id { get; set; }
        public string Make { get; set; } = string.Empty;
        public string Model { get; set; } = string.Empty;
        public int Year { get; set; }
        public string LicensePlate { get; set; } = string.Empty;
        public string Color { get; set; } = string.Empty;
        public string FuelType { get; set; } = string.Empty;
        public double CurrentMileage { get; set; }
        public double FuelLevel { get; set; }
        public string? CurrentLocation { get; set; }
        public string? CurrentDriver { get; set; }
        public int Status { get; set; }
        public DateTime? LastMaintenanceDate { get; set; }
        public DateTime? NextMaintenanceDate { get; set; }
        public DateTime CreatedAt { get; set; }
        public DateTime UpdatedAt { get; set; }
    }

    public class UpdateVehicleRequest
    {
        public string? Make { get; set; }
        public string? Model { get; set; }
        public int? Year { get; set; }
        public string? LicensePlate { get; set; }
        public string? Color { get; set; }
        public string? FuelType { get; set; }
        public double? CurrentMileage { get; set; }
        public double? FuelLevel { get; set; }
        public string? CurrentLocation { get; set; }
        public string? CurrentDriver { get; set; }
        public int? Status { get; set; }
        public DateTime? LastMaintenanceDate { get; set; }
        public DateTime? NextMaintenanceDate { get; set; }
    }

    public class VehicleStatistics
    {
        public int TotalVehicles { get; set; }
        public int ActiveVehicles { get; set; }
        public int IdleVehicles { get; set; }
        public int MaintenanceVehicles { get; set; }
        public int OfflineVehicles { get; set; }
        public double AverageFuelLevel { get; set; }
        public double AverageMileage { get; set; }
        public int LowFuelCount { get; set; }
        public int MaintenanceDueCount { get; set; }
    }

    public class FuelData
    {
        public Guid VehicleId { get; set; }
        public string VehicleIdentifier { get; set; } = string.Empty;
        public string Make { get; set; } = string.Empty;
        public string Model { get; set; } = string.Empty;
        public double FuelLevel { get; set; }
        public string FuelType { get; set; } = string.Empty;
        public string? CurrentDriver { get; set; }
        public string Status { get; set; } = string.Empty;
    }
}
