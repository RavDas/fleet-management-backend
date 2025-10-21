using Microsoft.EntityFrameworkCore;
using VehicleService.Domain.Entities;
using VehicleService.Infrastructure.Data;

namespace VehicleService.Infrastructure.Repositories
{
    public class VehicleRepository
    {
        private readonly VehicleDbContext _context;
        public VehicleRepository(VehicleDbContext context)
        {
            _context = context;
        }

        public async Task<List<Vehicle>> GetAllAsync()
        {
            return await _context.Vehicles
                .Include(v => v.MaintenanceRecords)
                .Include(v => v.StatusHistory)
                .ToListAsync();
        }

        public async Task AddAsync(Vehicle vehicle)
        {
            _context.Vehicles.Add(vehicle);
            await _context.SaveChangesAsync();
        }
    }
}
