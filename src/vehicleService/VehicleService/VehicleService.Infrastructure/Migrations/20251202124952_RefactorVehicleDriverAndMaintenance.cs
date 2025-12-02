using System;
using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace VehicleService.Infrastructure.Migrations
{
    /// <inheritdoc />
    public partial class RefactorVehicleDriverAndMaintenance : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropTable(
                name: "MaintenanceRecords");

            migrationBuilder.DropColumn(
                name: "CurrentDriver",
                table: "Vehicles");

            migrationBuilder.AddColumn<Guid>(
                name: "CurrentDriverId",
                table: "Vehicles",
                type: "uuid",
                nullable: true);
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropColumn(
                name: "CurrentDriverId",
                table: "Vehicles");

            migrationBuilder.AddColumn<string>(
                name: "CurrentDriver",
                table: "Vehicles",
                type: "text",
                nullable: true);

            migrationBuilder.CreateTable(
                name: "MaintenanceRecords",
                columns: table => new
                {
                    Id = table.Column<Guid>(type: "uuid", nullable: false),
                    Cost = table.Column<double>(type: "double precision", nullable: false),
                    CreatedAt = table.Column<DateTime>(type: "timestamp with time zone", nullable: false),
                    Description = table.Column<string>(type: "text", nullable: false),
                    PerformedBy = table.Column<string>(type: "text", nullable: false),
                    ServiceCenter = table.Column<string>(type: "text", nullable: false),
                    ServiceDate = table.Column<DateTime>(type: "timestamp with time zone", nullable: false),
                    ServiceType = table.Column<string>(type: "text", nullable: false),
                    VehicleId = table.Column<Guid>(type: "uuid", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_MaintenanceRecords", x => x.Id);
                    table.ForeignKey(
                        name: "FK_MaintenanceRecords_Vehicles_VehicleId",
                        column: x => x.VehicleId,
                        principalTable: "Vehicles",
                        principalColumn: "Id",
                        onDelete: ReferentialAction.Cascade);
                });

            migrationBuilder.CreateIndex(
                name: "IX_MaintenanceRecords_VehicleId",
                table: "MaintenanceRecords",
                column: "VehicleId");
        }
    }
}
