# ===============================
# Build Stage
# ===============================
FROM mcr.microsoft.com/dotnet/sdk:9.0 AS build
WORKDIR /src

# Copy only project files first (for caching restore)
COPY VehicleService/VehicleService.Domain/VehicleService.Domain.csproj VehicleService/VehicleService.Domain/
COPY VehicleService/VehicleService.Infrastructure/VehicleService.Infrastructure.csproj VehicleService/VehicleService.Infrastructure/
COPY VehicleService/VehicleService.Application/VehicleService.Application.csproj VehicleService/VehicleService.Application/
COPY VehicleService/VehicleService.Api/VehicleService.Api.csproj VehicleService/VehicleService.Api/

# Restore dependencies
RUN dotnet restore VehicleService/VehicleService.Api/VehicleService.Api.csproj

# Copy the rest of the source
COPY . .

# Build and publish
WORKDIR /src/VehicleService/VehicleService.Api
RUN dotnet publish -c Release -o /app/publish

# ===============================
# Runtime Stage
# ===============================
FROM mcr.microsoft.com/dotnet/aspnet:9.0 AS final
WORKDIR /app
COPY --from=build /app/publish .

EXPOSE 8080
EXPOSE 8081

ENV ASPNETCORE_URLS=http://+:8080
ENV ASPNETCORE_ENVIRONMENT=Development

ENTRYPOINT ["dotnet", "VehicleService.Api.dll"]
