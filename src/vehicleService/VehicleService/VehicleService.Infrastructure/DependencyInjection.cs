using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using VehicleService.Application.Interfaces;
using VehicleService.Infrastructure.Data;
using VehicleService.Infrastructure.Repositories;

namespace VehicleService.Infrastructure
{
    public static class DependencyInjection
    {
        public static IServiceCollection AddInfrastructure(this IServiceCollection services, IConfiguration configuration)
        {
            var connectionString = configuration.GetConnectionString("DefaultConnection");

            services.AddDbContext<VehicleDbContext>(options =>
                options.UseNpgsql(connectionString));


            services.AddScoped<IVehicleRepository, VehicleRepository>();

            return services;
        }
    }
}
