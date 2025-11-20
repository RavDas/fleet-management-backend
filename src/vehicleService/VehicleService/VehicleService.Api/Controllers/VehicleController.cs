using Microsoft.AspNetCore.Mvc;
using VehicleService.Application.Interfaces;
using VehicleService.Application.DTOs;
using VehicleService.Domain.Entities;

namespace VehicleService.Api.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class VehiclesController : ControllerBase
    {
        private readonly IVehicleRepository _repo;

        public VehiclesController(IVehicleRepository repo)
        {
            _repo = repo;
        }

        // GET: api/vehicles
        [HttpGet]
        public async Task<IActionResult> GetAll([FromQuery] int? status)
        {
            IEnumerable<Vehicle> vehicles;
            
            if (status.HasValue)
            {
                vehicles = await _repo.GetByStatusAsync(status.Value);
            }
            else
            {
                vehicles = await _repo.GetAllAsync();
            }

            var vehicleDtos = vehicles.Select(v => MapToDto(v));
            return Ok(vehicleDtos);
        }

        // GET: api/vehicles/{id}
        [HttpGet("{id}")]
        public async Task<IActionResult> GetVehicleById(Guid id)
        {
            var vehicle = await _repo.GetByIdAsync(id);
            if (vehicle == null)
                return NotFound(new { message = $"Vehicle with ID {id} not found" });
            
            return Ok(MapToDto(vehicle));
        }

        // POST: api/vehicles
        [HttpPost]
        public async Task<IActionResult> AddVehicle([FromBody] CreateVehicleRequest request)
        {
            if (request == null)
                return BadRequest("Invalid vehicle data.");

            var vehicle = new Vehicle
            {
                Id = Guid.NewGuid(),
                Make = request.Make,
                Model = request.Model,
                Year = request.Year,
                LicensePlate = request.LicensePlate,
                Color = request.Color,
                FuelType = request.FuelType,
                CurrentMileage = request.CurrentMileage,
                FuelLevel = 100, // Default to full tank
                Status = 0, // Default to idle
                CreatedAt = DateTime.UtcNow,
                UpdatedAt = DateTime.UtcNow
            };

            await _repo.AddAsync(vehicle);
            await _repo.SaveChangesAsync();

            return CreatedAtAction(nameof(GetVehicleById), new { id = vehicle.Id }, MapToDto(vehicle));
        }

        // PUT: api/vehicles/{id}
        [HttpPut("{id}")]
        public async Task<IActionResult> UpdateVehicle(Guid id, [FromBody] UpdateVehicleRequest request)
        {
            var vehicle = await _repo.GetByIdAsync(id);
            if (vehicle == null)
                return NotFound(new { message = $"Vehicle with ID {id} not found" });

            // Update only provided fields
            if (!string.IsNullOrEmpty(request.Make)) vehicle.Make = request.Make;
            if (!string.IsNullOrEmpty(request.Model)) vehicle.Model = request.Model;
            if (request.Year.HasValue) vehicle.Year = request.Year.Value;
            if (!string.IsNullOrEmpty(request.LicensePlate)) vehicle.LicensePlate = request.LicensePlate;
            if (!string.IsNullOrEmpty(request.Color)) vehicle.Color = request.Color;
            if (!string.IsNullOrEmpty(request.FuelType)) vehicle.FuelType = request.FuelType;
            if (request.CurrentMileage.HasValue) vehicle.CurrentMileage = request.CurrentMileage.Value;
            if (request.FuelLevel.HasValue) vehicle.FuelLevel = request.FuelLevel.Value;
            if (request.CurrentLocation != null) vehicle.CurrentLocation = request.CurrentLocation;
            if (request.CurrentDriver != null) vehicle.CurrentDriver = request.CurrentDriver;
            if (request.Status.HasValue) vehicle.Status = request.Status.Value;
            if (request.LastMaintenanceDate.HasValue) vehicle.LastMaintenanceDate = request.LastMaintenanceDate;
            if (request.NextMaintenanceDate.HasValue) vehicle.NextMaintenanceDate = request.NextMaintenanceDate;
            
            vehicle.UpdatedAt = DateTime.UtcNow;

            await _repo.UpdateAsync(vehicle);
            await _repo.SaveChangesAsync();

            return Ok(MapToDto(vehicle));
        }

        // DELETE: api/vehicles/{id}
        [HttpDelete("{id}")]
        public async Task<IActionResult> DeleteVehicle(Guid id)
        {
            var vehicle = await _repo.GetByIdAsync(id);
            if (vehicle == null)
                return NotFound(new { message = $"Vehicle with ID {id} not found" });

            await _repo.DeleteAsync(vehicle);
            await _repo.SaveChangesAsync();

            return Ok(new { message = "Vehicle deleted successfully", id = id });
        }

        // GET: api/vehicles/statistics
        [HttpGet("statistics")]
        public async Task<IActionResult> GetStatistics()
        {
            var vehicles = await _repo.GetAllAsync();
            var vehicleList = vehicles.ToList();

            var stats = new VehicleStatistics
            {
                TotalVehicles = vehicleList.Count,
                ActiveVehicles = vehicleList.Count(v => v.Status == 1),
                IdleVehicles = vehicleList.Count(v => v.Status == 0),
                MaintenanceVehicles = vehicleList.Count(v => v.Status == 2),
                OfflineVehicles = vehicleList.Count(v => v.Status == 3),
                AverageFuelLevel = vehicleList.Any() ? vehicleList.Average(v => v.FuelLevel) : 0,
                AverageMileage = vehicleList.Any() ? vehicleList.Average(v => v.CurrentMileage) : 0,
                LowFuelCount = vehicleList.Count(v => v.FuelLevel < 25),
                MaintenanceDueCount = vehicleList.Count(v => v.NextMaintenanceDate.HasValue && v.NextMaintenanceDate.Value <= DateTime.UtcNow.AddDays(7))
            };

            return Ok(stats);
        }

        // GET: api/vehicles/fuel
        [HttpGet("fuel")]
        public async Task<IActionResult> GetFuelData([FromQuery] string? status)
        {
            var vehicles = await _repo.GetAllAsync();
            
            var fuelData = vehicles.Select(v => new FuelData
            {
                VehicleId = v.Id,
                VehicleIdentifier = $"{v.Make} {v.Model} ({v.LicensePlate})",
                Make = v.Make,
                Model = v.Model,
                FuelLevel = v.FuelLevel,
                FuelType = v.FuelType,
                CurrentDriver = v.CurrentDriver,
                Status = GetStatusString(v.Status)
            });

            if (!string.IsNullOrEmpty(status))
            {
                fuelData = fuelData.Where(f => f.Status.Equals(status, StringComparison.OrdinalIgnoreCase));
            }

            return Ok(fuelData);
        }

        // GET: api/vehicles/low-fuel
        [HttpGet("low-fuel")]
        public async Task<IActionResult> GetLowFuelVehicles([FromQuery] double threshold = 25.0)
        {
            var vehicles = await _repo.GetLowFuelVehiclesAsync(threshold);
            var vehicleDtos = vehicles.Select(v => MapToDto(v));
            return Ok(vehicleDtos);
        }

        // Helper method to map Vehicle to VehicleDto
        private VehicleDto MapToDto(Vehicle vehicle)
        {
            return new VehicleDto
            {
                Id = vehicle.Id,
                Make = vehicle.Make,
                Model = vehicle.Model,
                Year = vehicle.Year,
                LicensePlate = vehicle.LicensePlate,
                Color = vehicle.Color,
                FuelType = vehicle.FuelType,
                CurrentMileage = vehicle.CurrentMileage,
                FuelLevel = vehicle.FuelLevel,
                CurrentLocation = vehicle.CurrentLocation,
                CurrentDriver = vehicle.CurrentDriver,
                Status = vehicle.Status,
                LastMaintenanceDate = vehicle.LastMaintenanceDate,
                NextMaintenanceDate = vehicle.NextMaintenanceDate,
                CreatedAt = vehicle.CreatedAt,
                UpdatedAt = vehicle.UpdatedAt
            };
        }

        // Helper method to convert status int to string
        private string GetStatusString(int status)
        {
            return status switch
            {
                0 => "idle",
                1 => "active",
                2 => "maintenance",
                3 => "offline",
                _ => "unknown"
            };
        }
    }
}
