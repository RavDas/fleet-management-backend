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
                CreatedAt = DateTime.UtcNow,
                UpdatedAt = DateTime.UtcNow
            };

            await _repo.AddAsync(vehicle);
            await _repo.SaveChangesAsync();

            return CreatedAtAction(nameof(GetVehicleById), new { id = vehicle.Id }, vehicle);
        }

        [HttpGet("{id}")]
        public async Task<IActionResult> GetVehicleById(Guid id)
        {
            var vehicle = await _repo.GetByIdAsync(id);
            if (vehicle == null)
                return NotFound();
            return Ok(vehicle);
        }

        [HttpGet]
        public async Task<IActionResult> GetAll()
        {
            var vehicles = await _repo.GetAllAsync();
            return Ok(vehicles);
        }
    }
}
