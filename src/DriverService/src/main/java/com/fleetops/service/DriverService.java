package com.fleetops.service;

import com.fleetops.dto.Driver;

import java.util.List;

public interface DriverService {
    boolean addDriver(Driver driver);
    Driver getDriver(Long id);
    List<Driver> getDriverList();
    Driver updateDriver(Driver driver);
    boolean deleteDriver(Long id);
}
