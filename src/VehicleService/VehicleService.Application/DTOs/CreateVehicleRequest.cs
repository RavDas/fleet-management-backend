namespace VehicleService.Application.DTOs
{
    public class CreateVehicleRequest
    {
        public string Make { get; set; } = string.Empty;
        public string Model { get; set; } = string.Empty;
        public int Year { get; set; }
        public string LicensePlate { get; set; } = string.Empty;
        public string Color { get; set; } = string.Empty;
        public string FuelType { get; set; } = string.Empty;
        public double CurrentMileage { get; set; }
    }
}
