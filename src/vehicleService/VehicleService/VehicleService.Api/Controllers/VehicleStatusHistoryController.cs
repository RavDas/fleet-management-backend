using Microsoft.AspNetCore.Mvc;
using VehicleService.Application.Interfaces;
using VehicleService.Application.DTOs;

namespace VehicleService.Api.Controllers
{
    [ApiController]
    [Route("api/vehicles/{vehicleId}/[controller]")]
    public class StatusHistoryController : ControllerBase
    {
        private readonly IVehicleRepository _vehicleRepo;

        public StatusHistoryController(IVehicleRepository vehicleRepo)
        {
            _vehicleRepo = vehicleRepo;
        }

        // GET: api/vehicles/{vehicleId}/statushistory
        [HttpGet]
        public async Task<IActionResult> GetVehicleStatusHistory(Guid vehicleId)
        {
            var vehicle = await _vehicleRepo.GetByIdAsync(vehicleId);
            if (vehicle == null)
                return NotFound(new { message = $"Vehicle with ID {vehicleId} not found" });

            var history = await _vehicleRepo.GetStatusHistoryAsync(vehicleId);
            var historyDtos = history.Select(h => new VehicleStatusHistoryDto
            {
                Id = h.Id,
                VehicleId = h.VehicleId,
                Status = GetStatusString((int)h.Status),
                ChangedBy = h.ChangedBy,
                Description = h.Description,
                ChangedAt = h.ChangedAt
            });

            return Ok(historyDtos);
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
    }
}

