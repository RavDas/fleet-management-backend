# Multi-stage Dockerfile for VehicleService.Api
# Builds and publishes the ASP.NET Core 9.0 app located at VehicleService/VehicleService.Api

# ----------------
# Build stage
# ----------------
FROM mcr.microsoft.com/dotnet/sdk:9.0 AS build
WORKDIR /src

# copy csproj files to leverage Docker cache for nuget restore
COPY VehicleService/VehicleService.Domain/VehicleService.Domain.csproj VehicleService/VehicleService.Domain/
COPY VehicleService/VehicleService.Infrastructure/VehicleService.Infrastructure.csproj VehicleService/VehicleService.Infrastructure/
COPY VehicleService/VehicleService.Application/VehicleService.Application.csproj VehicleService/VehicleService.Application/
COPY VehicleService/VehicleService.Api/VehicleService.Api.csproj VehicleService/VehicleService.Api/

RUN dotnet restore VehicleService/VehicleService.Api/VehicleService.Api.csproj

# copy everything else and publish
COPY VehicleService/ VehicleService/
WORKDIR /src/VehicleService/VehicleService.Api
RUN dotnet publish -c Release -o /app/publish

# ----------------
# Runtime stage
# ----------------
FROM mcr.microsoft.com/dotnet/aspnet:9.0 AS runtime
WORKDIR /app

# install curl used by the HEALTHCHECK (small overhead)
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

COPY --from=build /app/publish .

# Service listens on 8080 by project configuration
ENV ASPNETCORE_URLS=http://+:8080
ENV ASPNETCORE_ENVIRONMENT=Production

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:8080/health || exit 1

ENTRYPOINT ["dotnet", "VehicleService.Api.dll"]
