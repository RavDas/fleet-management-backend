using Microsoft.AspNetCore.Mvc;
using VehicleService.Application.Interfaces;
using VehicleService.Application.DTOs;

namespace VehicleService.Api.Controllers
{
    [ApiController]
    [Route("api/vehicles/batch")]
    public class VehicleBatchController : ControllerBase
    {
        private readonly IVehicleRepository _repo;

        public VehicleBatchController(IVehicleRepository repo)
        {
            _repo = repo;
        }

        // POST: api/vehicles/batch/update-status
        [HttpPost("update-status")]
        public async Task<IActionResult> BatchUpdateStatus([FromBody] BatchUpdateStatusRequest request)
        {
            if (request.VehicleIds == null || !request.VehicleIds.Any())
                return BadRequest("Vehicle IDs are required");

            var updatedVehicles = new List<VehicleDto>();
            var failedUpdates = new List<string>();

            foreach (var vehicleId in request.VehicleIds)
            {
                var vehicle = await _repo.GetByIdAsync(vehicleId);
                if (vehicle == null)
                {
                    failedUpdates.Add(vehicleId.ToString());
                    continue;
                }

                int oldStatus = vehicle.Status;
                vehicle.Status = request.NewStatus;
                vehicle.UpdatedAt = DateTime.UtcNow;

                await _repo.UpdateAsync(vehicle);

                // Log status change
                await _repo.LogStatusChangeAsync(
                    vehicle.Id, 
                    oldStatus, 
                    request.NewStatus,
                    request.Reason ?? "Batch status update",
                    request.ChangedBy ?? "System"
                );

                updatedVehicles.Add(new VehicleDto
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
                });
            }

            await _repo.SaveChangesAsync();

            return Ok(new
            {
                message = $"Updated {updatedVehicles.Count} vehicles",
                successCount = updatedVehicles.Count,
                failedCount = failedUpdates.Count,
                updatedVehicles = updatedVehicles,
                failedIds = failedUpdates
            });
        }

        // POST: api/vehicles/batch/update-fuel
        [HttpPost("update-fuel")]
        public async Task<IActionResult> BatchUpdateFuel([FromBody] BatchUpdateFuelRequest request)
        {
            if (request.VehicleIds == null || !request.VehicleIds.Any())
                return BadRequest("Vehicle IDs are required");

            var updatedVehicles = new List<VehicleDto>();
            var failedUpdates = new List<string>();

            foreach (var vehicleId in request.VehicleIds)
            {
                var vehicle = await _repo.GetByIdAsync(vehicleId);
                if (vehicle == null)
                {
                    failedUpdates.Add(vehicleId.ToString());
                    continue;
                }

                vehicle.FuelLevel = request.NewFuelLevel;
                vehicle.UpdatedAt = DateTime.UtcNow;

                await _repo.UpdateAsync(vehicle);

                updatedVehicles.Add(new VehicleDto
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
                });
            }

            await _repo.SaveChangesAsync();

            return Ok(new
            {
                message = $"Updated fuel level for {updatedVehicles.Count} vehicles",
                successCount = updatedVehicles.Count,
                failedCount = failedUpdates.Count,
                updatedVehicles = updatedVehicles,
                failedIds = failedUpdates
            });
        }

        // POST: api/vehicles/batch/schedule-maintenance
        [HttpPost("schedule-maintenance")]
        public async Task<IActionResult> BatchScheduleMaintenance([FromBody] BatchScheduleMaintenanceRequest request)
        {
            if (request.VehicleIds == null || !request.VehicleIds.Any())
                return BadRequest("Vehicle IDs are required");

            var updatedVehicles = new List<VehicleDto>();
            var failedUpdates = new List<string>();

            foreach (var vehicleId in request.VehicleIds)
            {
                var vehicle = await _repo.GetByIdAsync(vehicleId);
                if (vehicle == null)
                {
                    failedUpdates.Add(vehicleId.ToString());
                    continue;
                }

                vehicle.NextMaintenanceDate = request.MaintenanceDate;
                vehicle.UpdatedAt = DateTime.UtcNow;

                // Optionally set to maintenance status
                if (request.SetToMaintenanceStatus)
                {
                    int oldStatus = vehicle.Status;
                    vehicle.Status = 2; // maintenance
                    
                    await _repo.LogStatusChangeAsync(
                        vehicle.Id,
                        oldStatus,
                        2,
                        "Scheduled for maintenance",
                        request.ScheduledBy ?? "System"
                    );
                }

                await _repo.UpdateAsync(vehicle);

                updatedVehicles.Add(new VehicleDto
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
                });
            }

            await _repo.SaveChangesAsync();

            return Ok(new
            {
                message = $"Scheduled maintenance for {updatedVehicles.Count} vehicles",
                successCount = updatedVehicles.Count,
                failedCount = failedUpdates.Count,
                updatedVehicles = updatedVehicles,
                failedIds = failedUpdates
            });
        }

        // DELETE: api/vehicles/batch/delete
        [HttpPost("delete")]
        public async Task<IActionResult> BatchDelete([FromBody] BatchDeleteRequest request)
        {
            if (request.VehicleIds == null || !request.VehicleIds.Any())
                return BadRequest("Vehicle IDs are required");

            var deletedIds = new List<Guid>();
            var failedDeletes = new List<string>();

            foreach (var vehicleId in request.VehicleIds)
            {
                var vehicle = await _repo.GetByIdAsync(vehicleId);
                if (vehicle == null)
                {
                    failedDeletes.Add(vehicleId.ToString());
                    continue;
                }

                await _repo.DeleteAsync(vehicle);
                deletedIds.Add(vehicleId);
            }

            await _repo.SaveChangesAsync();

            return Ok(new
            {
                message = $"Deleted {deletedIds.Count} vehicles",
                successCount = deletedIds.Count,
                failedCount = failedDeletes.Count,
                deletedIds = deletedIds,
                failedIds = failedDeletes
            });
        }
    }

    // Batch request DTOs
    public class BatchUpdateStatusRequest
    {
        public List<Guid> VehicleIds { get; set; } = new List<Guid>();
        public int NewStatus { get; set; }
        public string? Reason { get; set; }
        public string? ChangedBy { get; set; }
    }

    public class BatchUpdateFuelRequest
    {
        public List<Guid> VehicleIds { get; set; } = new List<Guid>();
        public double NewFuelLevel { get; set; }
    }

    public class BatchScheduleMaintenanceRequest
    {
        public List<Guid> VehicleIds { get; set; } = new List<Guid>();
        public DateTime MaintenanceDate { get; set; }
        public bool SetToMaintenanceStatus { get; set; } = false;
        public string? ScheduledBy { get; set; }
    }

    public class BatchDeleteRequest
    {
        public List<Guid> VehicleIds { get; set; } = new List<Guid>();
    }
}

