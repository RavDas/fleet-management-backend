using VehicleService.Domain.Entities;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace VehicleService.Application.Interfaces
{
    public interface IVehicleRepository
    {
        Task<IEnumerable<Vehicle>> GetAllAsync();
        Task<Vehicle?> GetByIdAsync(Guid id);
        Task<IEnumerable<Vehicle>> GetByStatusAsync(int status);
        Task<IEnumerable<Vehicle>> GetLowFuelVehiclesAsync(double threshold);
        Task AddAsync(Vehicle vehicle);
        Task UpdateAsync(Vehicle vehicle);
        Task DeleteAsync(Vehicle vehicle);
        Task SaveChangesAsync();
    }
}
