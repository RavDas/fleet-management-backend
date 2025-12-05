using Microsoft.EntityFrameworkCore;
using System.Collections.Generic;
using System.Reflection.Emit;
using VehicleService.Domain.Entities;

namespace VehicleService.Infrastructure.Data
{
    public class VehicleDbContext : DbContext
    {
        public VehicleDbContext(DbContextOptions<VehicleDbContext> options)
            : base(options)
        {
        }

        public DbSet<Vehicle> Vehicles => Set<Vehicle>();
        public DbSet<VehicleStatusHistory> VehicleStatusHistories => Set<VehicleStatusHistory>();
        public DbSet<GeneratedReport> GeneratedReports => Set<GeneratedReport>();

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            base.OnModelCreating(modelBuilder);

            // Example: Fluent configuration
            modelBuilder.Entity<Vehicle>()
                .HasMany(v => v.StatusHistory)
                .WithOne()
                .HasForeignKey(h => h.VehicleId)
                .OnDelete(DeleteBehavior.Cascade);
        }
    }
}
