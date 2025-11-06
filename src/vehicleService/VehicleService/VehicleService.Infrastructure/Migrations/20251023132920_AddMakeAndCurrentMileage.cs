using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace VehicleService.Infrastructure.Migrations
{
    /// <inheritdoc />
    public partial class AddMakeAndCurrentMileage : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropColumn(
                name: "Manufacturer",
                table: "Vehicles");

            migrationBuilder.RenameColumn(
                name: "VehicleCode",
                table: "Vehicles",
                newName: "Make");

            migrationBuilder.RenameColumn(
                name: "Mileage",
                table: "Vehicles",
                newName: "CurrentMileage");

            migrationBuilder.AlterColumn<string>(
                name: "CurrentLocation",
                table: "Vehicles",
                type: "text",
                nullable: true,
                oldClrType: typeof(string),
                oldType: "text");

            migrationBuilder.AlterColumn<string>(
                name: "CurrentDriver",
                table: "Vehicles",
                type: "text",
                nullable: true,
                oldClrType: typeof(string),
                oldType: "text");
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.RenameColumn(
                name: "Make",
                table: "Vehicles",
                newName: "VehicleCode");

            migrationBuilder.RenameColumn(
                name: "CurrentMileage",
                table: "Vehicles",
                newName: "Mileage");

            migrationBuilder.AlterColumn<string>(
                name: "CurrentLocation",
                table: "Vehicles",
                type: "text",
                nullable: false,
                defaultValue: "",
                oldClrType: typeof(string),
                oldType: "text",
                oldNullable: true);

            migrationBuilder.AlterColumn<string>(
                name: "CurrentDriver",
                table: "Vehicles",
                type: "text",
                nullable: false,
                defaultValue: "",
                oldClrType: typeof(string),
                oldType: "text",
                oldNullable: true);

            migrationBuilder.AddColumn<string>(
                name: "Manufacturer",
                table: "Vehicles",
                type: "text",
                nullable: false,
                defaultValue: "");
        }
    }
}
