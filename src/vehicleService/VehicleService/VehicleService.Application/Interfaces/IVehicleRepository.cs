using VehicleService.Domain.Entities;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace VehicleService.Application.Interfaces
{
    public interface IVehicleRepository
    {
        Task<IEnumerable<Vehicle>> GetAllAsync();
        Task<Vehicle?> GetByIdAsync(Guid id);
        Task AddAsync(Vehicle vehicle);
        Task SaveChangesAsync();
    }
}
