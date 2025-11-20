using Microsoft.EntityFrameworkCore;
using VehicleService.Application.Interfaces;
using VehicleService.Domain.Entities;
using VehicleService.Infrastructure.Data;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace VehicleService.Infrastructure.Repositories
{
    public class VehicleRepository : IVehicleRepository
    {
        private readonly VehicleDbContext _context;
        public VehicleRepository(VehicleDbContext context)
        {
            _context = context;
        }

        public async Task<IEnumerable<Vehicle>> GetAllAsync()
            => await _context.Vehicles.ToListAsync();

        public async Task<Vehicle?> GetByIdAsync(Guid id)
            => await _context.Vehicles.FindAsync(id);

        public async Task<IEnumerable<Vehicle>> GetByStatusAsync(int status)
            => await _context.Vehicles.Where(v => v.Status == status).ToListAsync();

        public async Task<IEnumerable<Vehicle>> GetLowFuelVehiclesAsync(double threshold)
            => await _context.Vehicles.Where(v => v.FuelLevel < threshold).ToListAsync();

        public async Task AddAsync(Vehicle vehicle)
            => await _context.Vehicles.AddAsync(vehicle);

        public async Task UpdateAsync(Vehicle vehicle)
        {
            _context.Vehicles.Update(vehicle);
        }

        public async Task DeleteAsync(Vehicle vehicle)
        {
            _context.Vehicles.Remove(vehicle);
        }

        public async Task SaveChangesAsync()
            => await _context.SaveChangesAsync();
    }
}
