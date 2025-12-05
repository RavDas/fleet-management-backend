using Microsoft.AspNetCore.Mvc;
using VehicleService.Application.Interfaces;
using VehicleService.Infrastructure.Data;
using VehicleService.Domain.Entities;
using Microsoft.EntityFrameworkCore;
using System.Text.Json;

namespace VehicleService.Api.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class ReportsController : ControllerBase
    {
        private readonly IVehicleRepository _repo;
        private readonly VehicleDbContext _context;

        public ReportsController(IVehicleRepository repo, VehicleDbContext context)
        {
            _repo = repo;
            _context = context;
        }

        // POST: api/reports/generate/{reportType}
        [HttpPost("generate/{reportType}")]
        public async Task<IActionResult> GenerateReport(string reportType, [FromQuery] string? period = "month")
        {
            object reportData = null;
            string reportName = "";

            switch (reportType.ToLower())
            {
                case "fleet-performance":
                    reportData = await GenerateFleetPerformanceData(period);
                    reportName = "Fleet Performance Report";
                    break;
                case "fuel-consumption":
                    reportData = await GenerateFuelConsumptionData(period);
                    reportName = "Fuel Consumption Analysis";
                    break;
                case "maintenance-summary":
                    reportData = await GenerateMaintenanceSummaryData(period);
                    reportName = "Maintenance Summary Report";
                    break;
                case "summary":
                    reportData = await GenerateSummaryData();
                    reportName = "Fleet Summary Report";
                    break;
                default:
                    return BadRequest("Invalid report type");
            }

            var jsonContent = JsonSerializer.Serialize(reportData);
            var fileSize = System.Text.Encoding.UTF8.GetByteCount(jsonContent);
            var sizeString = FormatFileSize(fileSize);

            var generatedReport = new GeneratedReport
            {
                ReportName = $"{reportName} - {DateTime.UtcNow:yyyy-MM-dd HH:mm}",
                ReportType = reportType,
                GeneratedDate = DateTime.UtcNow,
                FileSize = sizeString,
                Format = "JSON",
                Data = jsonContent
            };

            _context.GeneratedReports.Add(generatedReport);
            await _context.SaveChangesAsync();

            return Ok(generatedReport);
        }

        // GET: api/reports/recent
        [HttpGet("recent")]
        public async Task<IActionResult> GetRecentReports()
        {
            var reports = await _context.GeneratedReports
                .OrderByDescending(r => r.GeneratedDate)
                .Take(10)
                .Select(r => new 
                { 
                    r.Id, 
                    r.ReportName, 
                    r.ReportType, 
                    r.GeneratedDate, 
                    r.FileSize, 
                    r.Format 
                }) // Don't return Data here to save bandwidth
                .ToListAsync();

            return Ok(reports);
        }

        // GET: api/reports/{id}/download
        [HttpGet("{id}/download")]
        public async Task<IActionResult> DownloadReport(int id)
        {
            var report = await _context.GeneratedReports.FindAsync(id);
            if (report == null)
                return NotFound();

            var bytes = System.Text.Encoding.UTF8.GetBytes(report.Data);
            return File(bytes, "application/json", $"{report.ReportType}_{report.GeneratedDate:yyyyMMddHHmm}.json");
        }

        // Existing GET methods (kept for backward compatibility but reusing logic)
        [HttpGet("fleet-performance")]
        public async Task<IActionResult> GetFleetPerformance([FromQuery] string? period = "month")
        {
            return Ok(await GenerateFleetPerformanceData(period));
        }

        [HttpGet("fuel-consumption")]
        public async Task<IActionResult> GetFuelConsumption([FromQuery] string? period = "month")
        {
            return Ok(await GenerateFuelConsumptionData(period));
        }

        [HttpGet("maintenance-summary")]
        public async Task<IActionResult> GetMaintenanceSummary([FromQuery] string? period = "month")
        {
            return Ok(await GenerateMaintenanceSummaryData(period));
        }

        [HttpGet("summary")]
        public async Task<IActionResult> GetSummaryReport()
        {
            return Ok(await GenerateSummaryData());
        }

        // Private Generation Logic
        private async Task<object> GenerateFleetPerformanceData(string? period)
        {
            var vehicles = await _repo.GetAllAsync();
            var vehicleList = vehicles.ToList();

            return new
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
        }

        private async Task<object> GenerateFuelConsumptionData(string? period)
        {
             var vehicles = await _repo.GetAllAsync();
            var vehicleList = vehicles.ToList();

            return new
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
                    currentDriver = v.CurrentDriverId,
                    status = GetStatusString(v.Status)
                })
            };
        }

        private async Task<object> GenerateMaintenanceSummaryData(string? period)
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

            return new
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
        }

        private async Task<object> GenerateSummaryData()
        {
            var vehicles = await _repo.GetAllAsync();
            var vehicleList = vehicles.ToList();

            return new
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
        }

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
        
        private string FormatFileSize(long bytes)
        {
            string[] sizes = { "B", "KB", "MB", "GB" };
            int order = 0;
            double len = bytes;
            while (len >= 1024 && order < sizes.Length - 1)
            {
                order++;
                len = len / 1024;
            }
            return $"{len:0.##} {sizes[order]}";
        }
    }
}
