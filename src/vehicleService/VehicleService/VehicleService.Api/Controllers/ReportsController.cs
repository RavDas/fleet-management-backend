using Microsoft.AspNetCore.Mvc;
using VehicleService.Application.Interfaces;
using VehicleService.Application.DTOs;

namespace VehicleService.Api.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class ReportsController : ControllerBase
    {
        private readonly IVehicleRepository _repo;

        public ReportsController(IVehicleRepository repo)
        {
            _repo = repo;
        }

        // GET: api/reports/fleet-performance
        [HttpGet("fleet-performance")]
        public async Task<IActionResult> GetFleetPerformance([FromQuery] string? period = "month")
        {
            var vehicles = await _repo.GetAllAsync();
            var vehicleList = vehicles.ToList();

            var report = new
            {
                reportType = "Fleet Performance Report",
                period = period,
                generatedAt = DateTime.UtcNow,
                summary = new
                {
                    totalVehicles = vehicleList.Count,
                    activeVehicles = vehicleList.Count(v => v.Status == 1),
                    utilizationRate = vehicleList.Count > 0 
                        ? (double)vehicleList.Count(v => v.Status == 1) / vehicleList.Count * 100 
                        : 0,
                    averageMileage = vehicleList.Any() ? vehicleList.Average(v => v.CurrentMileage) : 0,
                    totalMileage = vehicleList.Sum(v => v.CurrentMileage)
                },
                vehicles = vehicleList.Select(v => new
                {
                    id = v.Id,
                    make = v.Make,
                    model = v.Model,
                    licensePlate = v.LicensePlate,
                    status = GetStatusString(v.Status),
                    mileage = v.CurrentMileage,
                    fuelLevel = v.FuelLevel,
                    lastMaintenance = v.LastMaintenanceDate
                })
            };

            return Ok(report);
        }

        // GET: api/reports/fuel-consumption
        [HttpGet("fuel-consumption")]
        public async Task<IActionResult> GetFuelConsumption([FromQuery] string? period = "month")
        {
            var vehicles = await _repo.GetAllAsync();
            var vehicleList = vehicles.ToList();

            var report = new
            {
                reportType = "Fuel Consumption Analysis",
                period = period,
                generatedAt = DateTime.UtcNow,
                summary = new
                {
                    averageFuelLevel = vehicleList.Any() ? vehicleList.Average(v => v.FuelLevel) : 0,
                    lowFuelVehicles = vehicleList.Count(v => v.FuelLevel < 25),
                    criticalFuelVehicles = vehicleList.Count(v => v.FuelLevel < 15),
                    fuelTypeDistribution = vehicleList.GroupBy(v => v.FuelType)
                        .Select(g => new { fuelType = g.Key, count = g.Count() })
                        .ToList()
                },
                vehicles = vehicleList.Select(v => new
                {
                    id = v.Id,
                    make = v.Make,
                    model = v.Model,
                    licensePlate = v.LicensePlate,
                    fuelLevel = v.FuelLevel,
                    fuelType = v.FuelType,
                    currentDriver = v.CurrentDriver,
                    status = GetStatusString(v.Status)
                })
            };

            return Ok(report);
        }

        // GET: api/reports/maintenance-summary
        [HttpGet("maintenance-summary")]
        public async Task<IActionResult> GetMaintenanceSummary([FromQuery] string? period = "month")
        {
            var vehicles = await _repo.GetAllAsync();
            var vehicleList = vehicles.ToList();

            var now = DateTime.UtcNow;
            var maintenanceDue = vehicleList
                .Where(v => v.NextMaintenanceDate.HasValue && v.NextMaintenanceDate.Value <= now.AddDays(7))
                .ToList();

            var overdue = vehicleList
                .Where(v => v.NextMaintenanceDate.HasValue && v.NextMaintenanceDate.Value < now)
                .ToList();

            var report = new
            {
                reportType = "Maintenance Summary Report",
                period = period,
                generatedAt = DateTime.UtcNow,
                summary = new
                {
                    totalVehicles = vehicleList.Count,
                    inMaintenance = vehicleList.Count(v => v.Status == 2),
                    maintenanceDueSoon = maintenanceDue.Count,
                    overdueCount = overdue.Count,
                    nextWeekScheduled = maintenanceDue.Count
                },
                upcomingMaintenance = maintenanceDue.Select(v => new
                {
                    vehicleId = v.Id,
                    make = v.Make,
                    model = v.Model,
                    licensePlate = v.LicensePlate,
                    dueDate = v.NextMaintenanceDate,
                    lastMaintenance = v.LastMaintenanceDate,
                    currentMileage = v.CurrentMileage,
                    priority = v.NextMaintenanceDate.HasValue && v.NextMaintenanceDate.Value < now 
                        ? "overdue" 
                        : "due-soon"
                }),
                vehiclesInService = vehicleList.Where(v => v.Status == 2).Select(v => new
                {
                    vehicleId = v.Id,
                    make = v.Make,
                    model = v.Model,
                    licensePlate = v.LicensePlate,
                    currentMileage = v.CurrentMileage
                })
            };

            return Ok(report);
        }

        // GET: api/reports/summary
        [HttpGet("summary")]
        public async Task<IActionResult> GetSummaryReport()
        {
            var vehicles = await _repo.GetAllAsync();
            var vehicleList = vehicles.ToList();

            var report = new
            {
                reportType = "Fleet Summary Report",
                generatedAt = DateTime.UtcNow,
                fleetOverview = new
                {
                    totalVehicles = vehicleList.Count,
                    activeVehicles = vehicleList.Count(v => v.Status == 1),
                    idleVehicles = vehicleList.Count(v => v.Status == 0),
                    maintenanceVehicles = vehicleList.Count(v => v.Status == 2),
                    offlineVehicles = vehicleList.Count(v => v.Status == 3)
                },
                fuelStatus = new
                {
                    averageFuelLevel = vehicleList.Any() ? vehicleList.Average(v => v.FuelLevel) : 0,
                    lowFuelCount = vehicleList.Count(v => v.FuelLevel < 25),
                    criticalFuelCount = vehicleList.Count(v => v.FuelLevel < 15)
                },
                maintenance = new
                {
                    inService = vehicleList.Count(v => v.Status == 2),
                    dueSoon = vehicleList.Count(v => v.NextMaintenanceDate.HasValue && 
                        v.NextMaintenanceDate.Value <= DateTime.UtcNow.AddDays(7) &&
                        v.NextMaintenanceDate.Value >= DateTime.UtcNow)
                },
                mileageStats = new
                {
                    totalMileage = vehicleList.Sum(v => v.CurrentMileage),
                    averageMileage = vehicleList.Any() ? vehicleList.Average(v => v.CurrentMileage) : 0,
                    highestMileage = vehicleList.Any() ? vehicleList.Max(v => v.CurrentMileage) : 0,
                    lowestMileage = vehicleList.Any() ? vehicleList.Min(v => v.CurrentMileage) : 0
                }
            };

            return Ok(report);
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

